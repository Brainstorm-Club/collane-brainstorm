#!/usr/bin/env python3
"""Anagrafe dei personaggi di una collana: chi compare dove, come cambia, e il suo ritratto.

    python3 personaggi.py <radice-brainstorm> <collana> ordine
    python3 personaggi.py <radice-brainstorm> <collana> stato
    python3 personaggi.py <radice-brainstorm> <collana> nuovo "Nome" ["alias1, alias2"]
    python3 personaggi.py <radice-brainstorm> <collana> indice
    python3 personaggi.py <radice-brainstorm> <collana> prompt <scheda>

Le schede vivono nella collana, in `<progetto>/assets/personaggi/<scheda>.md`; lo stile comune dei
ritratti in `assets/personaggi/_stile.md`. Formato in references/fase-personaggi.md.

  ordine   i racconti (o i libri) nell'ordine cronologico della storia — quello su cui si misura
           tutto il resto
  stato    per ogni scheda: dove il nome compare davvero nei testi, quali racconti mancano
           nell'«Evoluzione», se un morto ricompare dopo la morte, se il prompt del ritratto è più
           vecchio dell'ultimo cambio d'aspetto, se il personaggio è nel canone di serie.
           Non modifica niente.
  nuovo    crea lo scheletro di una scheda, con una riga di «Evoluzione» già pronta per ogni
           racconto in cui il nome compare. Non sovrascrive mai una scheda esistente.
  indice   rigenera assets/personaggi/INDICE.md dalle schede (è l'unico file che lo script scrive
           da sé, ed è dichiarato generato)
  prompt   compone il prompt del ritratto: il contenitore di _stile.md con il soggetto della
           scheda al posto di {SOGGETTO}. Avvisa se il soggetto è scaduto.

Uscita: 0 pulito · 1 avvisi · 2 errori.
"""
import json
import os
import re
import sys
import unicodedata

QUI = os.path.dirname(os.path.abspath(__file__))
VUOTO = {"", "—", "-", "–", "=", "id.", "invariato", "?"}
BORDO = r"(?<![\wÀ-ÿ])"
FINE = r"(?![\wÀ-ÿ])"


# ---------------------------------------------------------------- collana e ordine

def carica_collana(radice, chiave):
    reg = json.load(open(os.path.join(QUI, "collane.json"), encoding="utf-8"))["collane"]
    if chiave not in reg:
        sys.exit(f"collana sconosciuta: {chiave} (ho {', '.join(reg)})")
    c = reg[chiave]
    return c, os.path.join(radice, c["progetto"])


def leggi_manifest(path):
    if not os.path.isfile(path):
        return []
    out = []
    for riga in open(path, encoding="utf-8"):
        riga = riga.strip()
        if riga and not riga.startswith("#"):
            out.append(riga.split()[0])
    return out


def ordine_unita(c, prog):
    """Le unità narrative in ordine cronologico: racconti (schema volumi) o libri (capitoli)."""
    if c["schema"] == "capitoli":
        return [v for v in c.get("ordine_volumi", [])
                if os.path.isdir(os.path.join(prog, "libri", v))]
    visti, ordine = set(), []
    for vol in c.get("ordine_volumi", []):
        for r in leggi_manifest(os.path.join(prog, "volumi", vol, "manifest.txt")):
            if r not in visti:
                visti.add(r)
                ordine.append(r)
    # racconti che non stanno in nessun volume dell'ordine: in coda, dichiarati
    rdir = os.path.join(prog, "racconti")
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            if f.endswith(".md") and not f.endswith(".bibbia.md") and f != "README.md":
                if f[:-3] not in visti:
                    ordine.append(f[:-3] + " *")
    return ordine


def testo_unita(c, prog, unita):
    """[(file relativo, testo)] di un'unità."""
    nome = unita.rstrip(" *")
    if c["schema"] == "capitoli":
        d = os.path.join(prog, "libri", nome)
        files = sorted(f for f in os.listdir(d)
                       if re.match(r"^\d\d_.*\.md$", f) or f == "epigrafe.md")
        return [(os.path.join("libri", nome, f), open(os.path.join(d, f), encoding="utf-8").read())
                for f in files]
    p = os.path.join(prog, "racconti", f"{nome}.md")
    return [(os.path.join("racconti", f"{nome}.md"), open(p, encoding="utf-8").read())]


# ---------------------------------------------------------------- schede

def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def leggi_scheda(path):
    t = open(path, encoding="utf-8").read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if m:
        for riga in m.group(1).splitlines():
            if ":" in riga:
                k, v = riga.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    evol = []
    sez = re.search(r"^## Evoluzione\s*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if sez:
        for riga in sez.group(1).splitlines():
            celle = [x.strip() for x in riga.strip().strip("|").split("|")]
            if len(celle) >= 3 and riga.strip().startswith("|") and not set(celle[0]) <= set("-: ") \
                    and celle[0].lower() != "racconto":
                evol.append({"unita": celle[0].strip("`* "), "stato": celle[1], "aspetto": celle[2]})
    soggetto = None
    sp = re.search(r"^## Prompt immagine\s*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if sp:
        b = re.search(r"```text\n(.*?)\n```", sp.group(1), re.S)
        if b and b.group(1).strip() and "{" not in b.group(1)[:3]:
            soggetto = b.group(1).strip()
    return {"meta": meta, "evoluzione": evol, "soggetto": soggetto, "testo": t}


def nomi_di(meta):
    nomi = [meta.get("nome", "")] + [a.strip() for a in meta.get("alias", "").split(",")]
    return [n for n in nomi if len(n) >= 2]


def schede(prog):
    d = os.path.join(prog, "assets", "personaggi")
    if not os.path.isdir(d):
        return d, {}
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".md") and not f.startswith("_") and f != "INDICE.md":
            out[f[:-3]] = leggi_scheda(os.path.join(d, f))
    return d, out


def apparizioni(c, prog, ordine, nomi):
    """{unità: (conteggio, 'file:riga' della prima occorrenza)}"""
    rx = re.compile(BORDO + "(" + "|".join(re.escape(n) for n in nomi) + ")" + FINE)
    out = {}
    for u in ordine:
        tot, prima = 0, None
        for rel, testo in testo_unita(c, prog, u):
            for n_riga, riga in enumerate(testo.splitlines(), 1):
                k = len(rx.findall(riga))
                if k:
                    tot += k
                    prima = prima or f"{rel}:{n_riga}"
        if tot:
            out[u.rstrip(" *")] = (tot, prima)
    return out


# ---------------------------------------------------------------- comandi

def cmd_ordine(c, prog):
    for i, u in enumerate(ordine_unita(c, prog), 1):
        print(f"{i:>3}. {u}")
    print("\n* = racconto fuori dai volumi dell'ordine: messo in coda, la sua posizione è incerta.")
    return 0


def cmd_stato(c, prog):
    ordine = [u.rstrip(" *") for u in ordine_unita(c, prog)]
    pos = {u: i for i, u in enumerate(ordine)}
    d, tutte = schede(prog)
    errori, avvisi = [], []
    if not tutte:
        print(f"Nessuna scheda in {os.path.relpath(d, prog)}/. Si comincia con `nuovo`.")
        return 1
    canone = os.path.join(prog, "assets", "canone_serie.md")
    canone_t = open(canone, encoding="utf-8").read() if os.path.isfile(canone) else ""
    stile = os.path.join(d, "_stile.md")
    if not os.path.isfile(stile):
        avvisi.append("manca assets/personaggi/_stile.md: i ritratti non hanno un contenitore comune")
    elif "{SOGGETTO}" not in open(stile, encoding="utf-8").read():
        errori.append("_stile.md non contiene il segnaposto {SOGGETTO}")

    for nome_f, s in tutte.items():
        m = s["meta"]
        tag = f"{nome_f}"
        if not m.get("nome"):
            errori.append(f"{tag}: frontmatter senza nome:")
            continue
        nomi = nomi_di(m)
        app = apparizioni(c, prog, ordine, nomi)
        righe = {r["unita"]: r for r in s["evoluzione"]}

        da_fare = [r["unita"] for r in s["evoluzione"]
                   if "?" in (r["stato"], r["aspetto"])]
        if da_fare:
            avvisi.append(f"{tag}: {len(da_fare)} righe d'Evoluzione ancora con «?» "
                          f"({', '.join(da_fare[:4])}{'…' if len(da_fare) > 4 else ''})")
        for u in righe:
            if u not in pos:
                errori.append(f"{tag}: riga d'Evoluzione per «{u}», che non è un racconto della collana")
        for u, (k, dove) in app.items():
            if u not in righe:
                avvisi.append(f"{tag}: compare in «{u}» ({k} menzioni, da {dove}) ma l'Evoluzione non ne parla")
        for u in righe:
            if u in pos and u not in app:
                avvisi.append(f"{tag}: riga per «{u}» ma il nome non compare nel testo (manca un alias?)")

        morto = m.get("morto_in", "")
        if morto:
            if morto not in pos:
                errori.append(f"{tag}: morto_in «{morto}» non è un racconto della collana")
            else:
                for u, (k, dove) in app.items():
                    if pos.get(u, -1) > pos[morto]:
                        avvisi.append(f"{tag}: MORTO in «{morto}» ma compare in «{u}» ({k} menzioni, "
                                      f"da {dove}) — ricordo o errore? Regola delle morti")
        if m.get("stato", "").lower().startswith("mort") and not morto:
            avvisi.append(f"{tag}: stato morto ma senza morto_in:")

        # ritratto
        cambi = [r["unita"] for r in s["evoluzione"]
                 if r["aspetto"].strip() not in VUOTO and r["unita"] in pos]
        ultimo = max(cambi, key=lambda u: pos[u]) if cambi else None
        valido = m.get("prompt_aggiornato_a", "")
        if not s["soggetto"]:
            avvisi.append(f"{tag}: nessun soggetto per il ritratto (## Prompt immagine)")
        elif valido and valido not in pos:
            errori.append(f"{tag}: prompt_aggiornato_a «{valido}» non è un racconto della collana")
        elif ultimo and (not valido or pos[ultimo] > pos[valido]):
            avvisi.append(f"{tag}: ritratto SCADUTO — l'aspetto cambia in «{ultimo}», il prompt è "
                          f"fermo a «{valido or '?'}»")

        if canone_t and not any(re.search(BORDO + re.escape(n) + FINE, canone_t) for n in nomi):
            avvisi.append(f"{tag}: non compare in canone_serie.md — il canone resta l'autorità sullo stato")

        prima = min(app, key=lambda u: pos[u]) if app else "—"
        ultima = max(app, key=lambda u: pos[u]) if app else "—"
        print(f"  {m['nome']:<26} {m.get('stato', '?'):<10} {len(app):>2} racconti  "
              f"({prima} → {ultima})")

    print()
    for v in avvisi:
        print(f"  !    {v}")
    for v in errori:
        print(f"  ERR  {v}")
    if not avvisi and not errori:
        print("Anagrafe allineata ai testi.")
    return 2 if errori else (1 if avvisi else 0)


SCHELETRO = """---
nome: {nome}
alias: {alias}
ruolo:
stato: vivo
prima_apparizione: {prima}
morto_in:
prompt_aggiornato_a:
---

# {nome}

## Chi è

<!-- due-quattro righe, in mondo. Niente nomi di giocatori, niente statistiche di gioco. -->

## Aspetto canonico

<!-- una riga per tratto, OGNUNA con la fonte. Solo quello che il testo dice. Dove tace: [il testo tace].
- tratto — `racconti/x.md:123` -->

## Evoluzione

| racconto | stato | aspetto | fatti | fonte |
|---|---|---|---|---|
{righe}

## Prompt immagine

<!-- il SOGGETTO del ritratto, in inglese, solo dall'Aspetto canonico valido a prompt_aggiornato_a.
Il contenitore (stile, luce, inquadratura, negativo) sta in _stile.md, uguale per tutti. -->

```text
```
"""


def cmd_nuovo(c, prog, nome, alias):
    d, _ = schede(prog)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, slug(nome) + ".md")
    if os.path.exists(path):
        print(f"ERRORE: {os.path.relpath(path, prog)} esiste già. Non sovrascrivo.")
        return 2
    ordine = [u.rstrip(" *") for u in ordine_unita(c, prog)]
    nomi = [nome] + [a.strip() for a in alias.split(",") if a.strip()]
    app = apparizioni(c, prog, ordine, nomi)
    righe = "\n".join(f"| {u} | ? | ? | ? | `{dove}` |" for u, (k, dove) in app.items()) \
        or "| | | | | |"
    open(path, "w", encoding="utf-8").write(SCHELETRO.format(
        nome=nome, alias=", ".join(nomi[1:]), prima=next(iter(app), ""), righe=righe))
    print(f"creata {os.path.relpath(path, prog)} — compare in {len(app)} racconti:")
    for u, (k, dove) in app.items():
        print(f"   {u:<34} {k:>3} menzioni  (prima: {dove})")
    print("\nI ? si riempiono LEGGENDO i testi, non deducendo: ogni tratto con la sua fonte.")
    return 0


def cmd_indice(c, prog):
    ordine = [u.rstrip(" *") for u in ordine_unita(c, prog)]
    pos = {u: i for i, u in enumerate(ordine)}
    d, tutte = schede(prog)
    if not tutte:
        print("Nessuna scheda: niente indice.")
        return 1
    righe = []
    for nome_f, s in tutte.items():
        m = s["meta"]
        app = apparizioni(c, prog, ordine, nomi_di(m)) if m.get("nome") else {}
        prima = min(app, key=lambda u: pos[u]) if app else "—"
        ultima = max(app, key=lambda u: pos[u]) if app else "—"
        ritratto = ("a " + m["prompt_aggiornato_a"]) if s["soggetto"] and m.get("prompt_aggiornato_a") \
            else ("sì" if s["soggetto"] else "—")
        stato = m.get("stato", "?") + (f" († {m['morto_in']})" if m.get("morto_in") else "")
        righe.append((pos.get(prima, 999), f"| [{m.get('nome', nome_f)}]({nome_f}.md) | "
                      f"{m.get('ruolo', '')} | {stato} | {prima} | {ultima} | {len(app)} | {ritratto} |"))
    righe.sort()
    out = ["<!-- generato da personaggi.py indice: non modificare a mano, modifica le schede -->",
           "", f"# Personaggi — {c['collana']}", "",
           "In ordine di prima apparizione nella cronologia della storia. Le apparizioni sono "
           "contate sui testi, non dichiarate.", "",
           "| personaggio | ruolo | stato | prima | ultima | racconti | ritratto |",
           "|---|---|---|---|---|---|---|"] + [r for _, r in righe]
    path = os.path.join(d, "INDICE.md")
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"scritto {os.path.relpath(path, prog)} ({len(righe)} personaggi)")
    return 0


def cmd_prompt(c, prog, chi):
    d, tutte = schede(prog)
    chi = chi[:-3] if chi.endswith(".md") else chi
    if chi not in tutte:
        print(f"ERRORE: nessuna scheda «{chi}» (ho: {', '.join(tutte) or 'nessuna'})")
        return 2
    s = tutte[chi]
    stile = os.path.join(d, "_stile.md")
    if not os.path.isfile(stile):
        print("ERRORE: manca assets/personaggi/_stile.md (il contenitore comune dei ritratti)")
        return 2
    st = open(stile, encoding="utf-8").read()
    blocco = re.search(r"```text\n(.*?)\n```", st, re.S)
    if not blocco or "{SOGGETTO}" not in blocco.group(1):
        print("ERRORE: _stile.md deve avere un blocco ```text``` con {SOGGETTO}")
        return 2
    if not s["soggetto"]:
        print(f"ERRORE: la scheda {chi} non ha ancora il soggetto (## Prompt immagine)")
        return 2
    # scadenza
    ordine = [u.rstrip(" *") for u in ordine_unita(c, prog)]
    pos = {u: i for i, u in enumerate(ordine)}
    cambi = [r["unita"] for r in s["evoluzione"] if r["aspetto"].strip() not in VUOTO and r["unita"] in pos]
    valido = s["meta"].get("prompt_aggiornato_a", "")
    ultimo = max(cambi, key=lambda u: pos[u]) if cambi else None
    print(f"# Ritratto — {s['meta'].get('nome')}  (aspetto valido a: {valido or '?'})\n")
    print(blocco.group(1).replace("{SOGGETTO}", s["soggetto"]))
    if ultimo and valido in pos and pos[ultimo] > pos[valido]:
        print(f"\n! SCADUTO: l'aspetto cambia in «{ultimo}». Aggiorna il soggetto prima di generare.")
        return 1
    return 0


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        print(__doc__)
        return 2
    radice, chiave, cmd = a[0].rstrip("/"), a[1], a[2]
    c, prog = carica_collana(radice, chiave)
    if cmd == "ordine":
        return cmd_ordine(c, prog)
    if cmd == "stato":
        return cmd_stato(c, prog)
    if cmd == "indice":
        return cmd_indice(c, prog)
    if cmd == "nuovo" and len(a) >= 4:
        return cmd_nuovo(c, prog, a[3], a[4] if len(a) > 4 else "")
    if cmd == "prompt" and len(a) >= 4:
        return cmd_prompt(c, prog, a[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
