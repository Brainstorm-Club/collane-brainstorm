#!/usr/bin/env python3
"""Crea lo scheletro di una collana nuova a partire da una scheda di progetto.

    python3 nuova_collana.py <radice-brainstorm> <scheda.json> [--prova]

La scheda la si compila nel co-design (references/fase-nuova-collana.md): gioco, voce,
confezione, tono, stile della copertina, slug del sito. Lo script:

  1. controlla che la scheda abbia tutti i campi e che chiave e cartella siano libere;
  2. copia i modelli di templates/collana/ nella cartella nuova, sostituendo i segnaposto;
  3. registra la collana in <radice>/collane.local.json, il registro LOCALE che gli altri
     script leggono insieme a quello del plugin (il plugin resta generico e aggiornabile).

Non sovrascrive mai: se la cartella esiste e non è vuota, si ferma. Con --prova mostra cosa
farebbe senza scrivere niente. Uscita: 0 creata · 2 scheda incompleta o cartella occupata.
"""
import json
import os
import re
import shutil
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
MODELLI = os.path.join(QUI, "..", "templates", "collana")

MODELLI_VOCE = {
    "narratore-unico": "narratore unico per tutta la collana",
    "polifonia": "polifonia: una voce in prima persona diversa per ogni racconto",
    "cornice-deposizioni": "cornice unica in terza persona più deposizioni in prima persona (blockquote)",
}

OBBLIGATORI = {
    "chiave": "identificativo breve, minuscole e trattini (es. «vampiri-roma»)",
    "progetto": "cartella relativa alla radice (es. «vampiri» o «wod/roma»)",
    "collana": "titolo della collana (es. «Le notti di Roma»)",
    "gioco": "gioco di ruolo d'origine (es. «Vampiri: la Masquerade»)",
    "modello_voce": "uno fra: " + ", ".join(MODELLI_VOCE),
    "voce": "chi racconta e come (2-4 frasi)",
    "note": "che forma hanno le note a piè di pagina",
    "confezione": "il finto oggetto editoriale (es. «diario sequestrato dall'Inquisizione»)",
    "apertura": "la tripletta d'apertura dei volumi (es. «Nota del curatore → Indice → Linea temporale»)",
    "tono": "il tono e il suo baricentro",
    "tesi": "la tesi di fondo della collana in una riga",
    "firma_narrativa": "la byline dei volumi (es. «a cura dell'Archivista»)",
    "stile_ritratto": "contenitore dei ritratti in inglese, con {SOGGETTO} (coerente con le copertine)",
    "slug_sito": "slug della collana sul sito (es. «notti-di-roma»)",
    "prefisso_sito": "prefisso dei file sul sito (es. «roma-»)",
}
FACOLTATIVI = {"editore": "", "editore_url": "", "occhiello": "", "pagine": 25,
               "stile_copertina": ""}


def compila(testo, s):
    ed = f" ({s['editore']})" if s.get("editore") else ""
    valori = {
        "COLLANA": s["collana"], "GIOCO": s["gioco"], "CARTELLA": s["progetto"],
        "CHIAVE": s["chiave"], "EDITORE_FRASE": ed,
        "MODELLO_VOCE": MODELLI_VOCE[s["modello_voce"]].capitalize(),
        "VOCE": s["voce"], "NOTE": s["note"], "CONFEZIONE": s["confezione"],
        "APERTURA": s["apertura"], "APERTURA_1": s["apertura"].split("→")[0].strip(),
        "TONO": s["tono"], "TESI": s["tesi"], "FIRMA_NARRATIVA": s["firma_narrativa"],
        "STILE_RITRATTO": s["stile_ritratto"], "PAGINE": str(s.get("pagine", 25)),
        "OCCHIELLO": s.get("occhiello") or s["tesi"],
    }
    return re.sub(r"\{\{([A-Z_0-9]+)\}\}", lambda m: valori.get(m.group(1), m.group(0)), testo)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prova = "--prova" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    radice = os.path.abspath(args[0])
    s = json.load(open(args[1], encoding="utf-8"))
    s = {**FACOLTATIVI, **s}

    mancano = [f"  {k}: {v}" for k, v in OBBLIGATORI.items() if not str(s.get(k, "")).strip()]
    if mancano:
        print("Scheda incompleta. Mancano:\n" + "\n".join(mancano))
        return 2
    if s["modello_voce"] not in MODELLI_VOCE:
        print(f"modello_voce deve essere uno fra: {', '.join(MODELLI_VOCE)}")
        return 2
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s["chiave"]):
        print("chiave: solo minuscole, cifre e trattini")
        return 2
    if "{SOGGETTO}" not in s["stile_ritratto"]:
        print("stile_ritratto deve contenere il segnaposto {SOGGETTO}")
        return 2

    reg_plugin = json.load(open(os.path.join(QUI, "collane.json"), encoding="utf-8"))["collane"]
    locale_p = os.path.join(radice, "collane.local.json")
    locale = json.load(open(locale_p, encoding="utf-8")) if os.path.isfile(locale_p) else {"collane": {}}
    if s["chiave"] in reg_plugin or s["chiave"] in locale["collane"]:
        print(f"la chiave «{s['chiave']}» è già usata da un'altra collana")
        return 2
    dest = os.path.join(radice, s["progetto"])
    if os.path.isdir(dest) and os.listdir(dest):
        print(f"{dest} esiste e non è vuota: non sovrascrivo")
        return 2

    file_creati = []
    for d, _, files in os.walk(MODELLI):
        for f in files:
            src = os.path.join(d, f)
            rel = os.path.relpath(src, MODELLI)
            file_creati.append(rel)
            if prova:
                continue
            out = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            if f.endswith((".md", ".sh", ".yaml", ".txt")):
                open(out, "w", encoding="utf-8").write(compila(open(src, encoding="utf-8").read(), s))
            else:
                shutil.copyfile(src, out)
            if f.endswith(".sh"):
                os.chmod(out, 0o755)

    voce = {
        "progetto": s["progetto"], "collana": s["collana"], "slug_sito": s["slug_sito"],
        "prefisso_sito": s["prefisso_sito"], "schema": "volumi",
        "unita": "racconti/<nome>.md composti da volumi/<vol>/manifest.txt",
        "gioco": s["gioco"] + (f" ({s['editore']})" if s.get("editore") else ""),
        "voce": MODELLI_VOCE[s["modello_voce"]], "confezione": s["confezione"],
        "prompt_copertina": "copertine/prompt-copertina-<vol>.md",
        "copertina": "copertine/<vol>.jpg|.png", "build": "bash build_epub.sh <vol>",
        "log": "log/*", "brief": "assets/PROMPT_nuovi_racconti.md",
        "canone": "assets/canone_serie.md", "ordine_volumi": [],
        "stile_copertina": s.get("stile_copertina", ""),
    }
    if not prova:
        locale["collane"][s["chiave"]] = voce
        locale.setdefault("_nota", "Collane create in locale con nuova_collana.py: si sommano a "
                                   "quelle del plugin. ordine_volumi va aggiornato a ogni volume nuovo.")
        json.dump(locale, open(locale_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(("PROVA — niente scritto. " if prova else "") +
          f"Collana «{s['collana']}» → {os.path.relpath(dest, radice)}/ ({len(file_creati)} file)")
    for f in sorted(file_creati):
        print(f"   {f}")
    print(f"registro: {os.path.relpath(locale_p, radice)} ← «{s['chiave']}»")
    print(f"\nProssimo passo: i log in {s['progetto']}/log/, poi "
          f"/brainstormclub:collana {s['chiave']} log")
    return 0


if __name__ == "__main__":
    sys.exit(main())
