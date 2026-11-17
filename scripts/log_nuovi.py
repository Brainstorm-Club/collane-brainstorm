#!/usr/bin/env python3
"""Quali log di gioco non sono ancora diventati racconto, o sono cambiati dopo.

    python3 log_nuovi.py <radice-brainstorm> [collana] [--json]

Per ogni log in <progetto>/log/ dice:
  · scoperto   nessuna bibbia lo cita come fonte → materiale non ancora usato
  · cambiato   git lo segnala modificato o non tracciato → il racconto che lo
               cita potrebbe non rispecchiarlo più
  · referto    se esiste già un referto di lettura in assets/referti/ che lo cita

Un log «coperto» è citato come `log/06.md`, `06.md`, `log 06` o `a-975` in una bibbia
(racconti/*.bibbia.md, libri/*/bibbia_narrativa.md) o, per le collane senza bibbie,
nel CLAUDE.md, nel canone o nel brief della collana. Chi non cita i log per nome li
dichiara in log/COPERTURA.txt: una riga per log, `<file>  <racconto|escluso>  [nota]`.

Non modifica niente. Uscita: 0 nessun log da guardare · 1 c'è qualcosa.
"""
import glob
import json
import os
import re
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))


def registro(radice):
    reg = json.load(open(os.path.join(QUI, "collane.json"), encoding="utf-8"))["collane"]
    locale = os.path.join(radice, "collane.local.json")
    if os.path.isfile(locale):
        reg.update(json.load(open(locale, encoding="utf-8")).get("collane", {}))
    return reg


def git_cambiati(radice):
    try:
        out = subprocess.run(["git", "-C", radice, "status", "--porcelain", "--untracked-files=all"],
                             capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return set()
    return {os.path.normpath(os.path.join(radice, riga[3:].strip().strip('"')))
            for riga in out.splitlines() if len(riga) > 3}


def citato(testo, nome):
    stem = nome.rsplit(".", 1)[0]
    pat = (rf"(?<![\w-]){re.escape(nome)}(?![\w])|log[/\s]+{re.escape(stem)}(?![\w])"
           rf"|(?<![\w-]){re.escape(stem)}(?![\w.-])" if not stem.isdigit()
           else rf"(?<![\w-]){re.escape(nome)}(?![\w])|log[/\s]+{re.escape(stem)}(?![\w])")
    return re.search(pat, testo, re.I) is not None


def analizza(radice, chiave, c, cambiati_git):
    prog = os.path.join(radice, c["progetto"])
    ldir = os.path.join(prog, "log")
    if not os.path.isdir(ldir):
        return []
    bibbie = glob.glob(os.path.join(prog, "racconti", "*.bibbia.md")) + \
        glob.glob(os.path.join(prog, "libri", "*", "bibbia_narrativa.md"))
    bt = [(b, open(b, encoding="utf-8").read(), os.path.getmtime(b)) for b in bibbie]
    # dove le collane senza bibbie dichiarano la copertura: canone, brief, istruzioni
    altre = [os.path.join(prog, x) for x in ("CLAUDE.md", "assets/canone_serie.md",
             "assets/PROMPT_nuovi_racconti.md", "assets/prompt_nuovi_racconti.md")]
    at = " ".join(open(x, encoding="utf-8").read() for x in altre if os.path.isfile(x))
    referti = [(r, open(r, encoding="utf-8").read())
               for r in glob.glob(os.path.join(prog, "assets", "referti", "*.md"))]
    # dichiarazione esplicita, per chi non cita i log per nome:
    # log/COPERTURA.txt, una riga per log: "<file>  <racconto o «escluso»>  [nota]"
    dichiarati = {}
    cop = os.path.join(ldir, "COPERTURA.txt")
    if os.path.isfile(cop):
        for riga in open(cop, encoding="utf-8"):
            parti = riga.split()
            if parti and not parti[0].startswith("#"):
                dichiarati[parti[0]] = parti[1] if len(parti) > 1 else "coperto"
    out = []
    for f in sorted(os.listdir(ldir)):
        p = os.path.join(ldir, f)
        if f.startswith(".") or not os.path.isfile(p) or not f.endswith((".md", ".txt")):
            continue
        if f.lower().startswith("readme") or f == "COPERTURA.txt":
            continue
        cit = [(b, t) for b, t, m in bt if citato(t, f)]
        stato = []
        if not cit and not citato(at, f) and f not in dichiarati:
            stato.append("scoperto")
        if os.path.normpath(p) in cambiati_git:
            stato.append("cambiato (git)")
        if not stato:
            continue
        ref = [os.path.relpath(r, prog) for r, t in referti if citato(t, f)]
        out.append({"collana": chiave, "log": os.path.relpath(p, radice),
                    "parole": len(open(p, encoding="utf-8", errors="ignore").read().split()),
                    "stato": stato, "referti": ref,
                    "racconti": [os.path.basename(b).replace(".bibbia.md", "") for b, _ in cit]})
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    radice = os.path.abspath(args[0])
    reg = registro(radice)
    if len(args) > 1:
        reg = {args[1]: reg[args[1]]}
    cambiati = git_cambiati(radice)
    tutti = [x for k, c in reg.items() for x in analizza(radice, k, c, cambiati)]
    if "--json" in sys.argv:
        print(json.dumps(tutti, ensure_ascii=False, indent=2))
    else:
        if not tutti:
            print("Nessun log da guardare: tutti coperti e invariati.")
        for x in tutti:
            ref = f" · referto: {', '.join(x['referti'])}" if x["referti"] else " · nessun referto"
            rac = f" · racconti: {', '.join(x['racconti'])}" if x["racconti"] else ""
            print(f"  {x['log']:<34} {x['parole']:>6} parole  {' + '.join(x['stato'])}{rac}{ref}")
    return 1 if tutti else 0


if __name__ == "__main__":
    sys.exit(main())
