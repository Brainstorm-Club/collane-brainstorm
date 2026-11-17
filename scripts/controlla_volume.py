#!/usr/bin/env python3
"""Controllo pre-build di un volume (o di un libro, schema «capitoli»).

    python3 controlla_volume.py <cartella-progetto> <volume> [--capitoli]

Fa prima del build i controlli che altrimenti si scoprono dopo, o peggio
dentro l'EPUB pubblicato:

  · manifest       ogni racconto elencato esiste davvero in racconti/
  · prefissi-note  univoci nel volume (se collidono, le note si mescolano)
  · note orfane    ogni [^chiave] ha la sua definizione nello stesso file
  · note mai usate definizioni senza richiamo (restano in fondo al capitolo)
  · meta.yaml      title e description (la sinossi è parte della confezione)
  · firma          `firmato:` nel meta.yaml: l'autore ha letto il testo per intero
                   e ne risponde. Senza firma non si builda (vedi references/patto.md)
  · front/timeline sono prosa in-fiction finita, non bozza con aside di regia:
                   front.md e timeline.md ENTRANO nell'EPUB
  · copertina      presente (il controllo completo è controlla_copertina.py)

Uscita: 0 pulito · 1 avvisi · 2 errori bloccanti.
"""
import os
import re
import sys

# aside di regia e riferimenti meta che non devono finire in un libro pubblicato
SPIE_BOZZA = [
    (r"\[BOZZA", "marcatore di bozza"),
    (r"\[TODO", "marcatore di lavoro"),
    (r"\[DA ", "appunto di lavorazione"),
    (r"\[Tesi\b", "aside di regia"),
    (r"\[L['’][A-Z]", "aside di regia («[L'Analista apre…]»)"),
    (r"\bcampagna\b", "riferimento meta al tavolo di gioco"),
    (r"\bsession[ei]\b", "riferimento meta al tavolo di gioco"),
    (r"\bgiocator", "riferimento meta al tavolo di gioco"),
    (r"\blog\b", "riferimento meta ai log"),
    (r"\bracconto scritto\b", "riferimento meta"),
]
# in-fiction, legittimo: non segnalarlo
AMMESSI = [r"\[OMISSIS\]"]


def note(testo):
    richiami = set(re.findall(r"\[\^([^\]\s]+)\](?!:)", testo))
    definite = set(re.findall(r"^\[\^([^\]\s]+)\]:", testo, re.M))
    return richiami, definite


def controlla_testo(path, etichetta, errori, avvisi):
    testo = open(path, encoding="utf-8").read()
    richiami, definite = note(testo)
    for k in sorted(richiami - definite):
        errori.append(f"{etichetta}: nota orfana [^{k}] — richiamata e mai definita (il build fallisce)")
    for k in sorted(definite - richiami):
        avvisi.append(f"{etichetta}: nota [^{k}] definita e mai richiamata")
    return testo


def controlla_apparato(path, errori, avvisi):
    """front.md / timeline.md: entrano nell'EPUB, vanno letti come testo pubblicato."""
    testo = open(path, encoding="utf-8").read()
    for riga_n, riga in enumerate(testo.splitlines(), 1):
        pulita = riga
        for a in AMMESSI:
            pulita = re.sub(a, "", pulita)
        for spia, perche in SPIE_BOZZA:
            if re.search(spia, pulita, re.I):
                avvisi.append(f"{os.path.basename(path)}:{riga_n}: {perche} → «{riga.strip()[:70]}»")
                break


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    capitoli = "--capitoli" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    radice, vol = args[0].rstrip("/"), args[1]
    errori, avvisi, ok = [], [], []

    if capitoli:
        vdir = os.path.join(radice, "libri", vol)
        if not os.path.isdir(vdir):
            print(f"ERRORE: manca {vdir}/")
            return 2
        capitoli_md = sorted(f for f in os.listdir(vdir) if re.match(r"^\d\d_.*\.md$", f))
        if not capitoli_md:
            errori.append("nessun capitolo NN_*.md")
        for c in capitoli_md:
            controlla_testo(os.path.join(vdir, c), c, errori, avvisi)
        ok.append(f"{len(capitoli_md)} capitoli: {', '.join(capitoli_md)}")
        epigrafe = os.path.join(vdir, "epigrafe.md")
        ok.append("epigrafe.md presente" if os.path.isfile(epigrafe) else "epigrafe.md assente (facoltativa)")
    else:
        vdir = os.path.join(radice, "volumi", vol)
        if not os.path.isdir(vdir):
            print(f"ERRORE: manca {vdir}/")
            return 2
        manifest = os.path.join(vdir, "manifest.txt")
        if not os.path.isfile(manifest):
            print(f"ERRORE: manca {manifest}")
            return 2
        visti = {}
        n = 0
        for riga in open(manifest, encoding="utf-8"):
            riga = riga.strip()
            if not riga or riga.startswith("#"):
                continue
            pezzi = riga.split()
            nome, pref = pezzi[0], (pezzi[1] if len(pezzi) > 1 else "")
            n += 1
            rpath = os.path.join(radice, "racconti", f"{nome}.md")
            if not os.path.isfile(rpath):
                errori.append(f"manifest: racconti/{nome}.md non esiste")
                continue
            if not pref:
                avvisi.append(f"manifest: {nome} senza prefisso-note (collisioni [^1] se il volume ne ha più d'uno)")
            elif pref in visti:
                errori.append(f"manifest: prefisso-note «{pref}» usato sia da {visti[pref]} sia da {nome}")
            else:
                visti[pref] = nome
            controlla_testo(rpath, f"racconti/{nome}.md", errori, avvisi)
        ok.append(f"manifest: {n} racconti, tutti presenti" if not errori else f"manifest: {n} righe")

        for apparato in ("front.md", "timeline.md"):
            p = os.path.join(vdir, apparato)
            if os.path.isfile(p):
                controlla_apparato(p, errori, avvisi)
            else:
                avvisi.append(f"{apparato} assente: il volume si apre senza {'indice' if apparato == 'front.md' else 'linea temporale'}")

    # meta.yaml — vale per tutti e due gli schemi
    meta = os.path.join(vdir, "meta.yaml")
    if not os.path.isfile(meta):
        errori.append("manca meta.yaml")
    else:
        m = open(meta, encoding="utf-8").read()
        if not re.search(r"^title:", m, re.M):
            errori.append("meta.yaml senza title:")
        firma = re.search(r"^firmato:[ \t]*(.*)$", m, re.M)
        valore = firma.group(1).strip().strip("\"'").strip() if firma else ""
        if not valore:
            errori.append("meta.yaml senza firmato: — l'autore deve leggere il testo per intero e "
                          "firmarlo (firmato: \"Nome Cognome, AAAA-MM-GG\"). Il campo NON lo scrive "
                          "il modello. Vedi references/patto.md §3")
        else:
            ok.append(f"firmato: {valore}")
        if not re.search(r"^description:", m, re.M):
            avvisi.append("meta.yaml senza description: — la sinossi serve al sito (overlay copertina + JSON-LD)")
        else:
            ok.append("meta.yaml: title + description")

    # copertina
    cop = [e for e in (".jpg", ".jpeg", ".png")
           if os.path.isfile(os.path.join(radice, "copertine", f"{vol}{e}"))]
    if cop:
        ok.append(f"copertina presente ({vol}{cop[0]}) — per il controllo completo: controlla_copertina.py")
    else:
        errori.append(f"manca copertine/{vol}.jpg|.png — NIENTE EPUB SENZA COPERTINA")

    for v in ok:
        print(f"  ok   {v}")
    for v in avvisi:
        print(f"  !    {v}")
    for v in errori:
        print(f"  ERR  {v}")
    print()
    if errori:
        print("Non buildare: risolvi gli ERR.")
        return 2
    if avvisi:
        print("Buildabile. Gli avvisi su front/timeline vanno letti uno per uno: quel testo finisce nel libro.")
        return 1
    print("Pre-build pulito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
