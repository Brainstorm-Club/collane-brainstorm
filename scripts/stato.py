#!/usr/bin/env python3
"""Panoramica di una collana (o di tutte): a che punto è la pipeline.

    python3 stato.py <radice-brainstorm> [collana]

Per ogni volume dice dove si è fermato il lavoro — prompt copertina, copertina,
EPUB, pubblicazione sul sito — e se l'EPUB è più vecchio delle sue fonti (cioè
va ricostruito). I log senza racconto sono materiale non ancora usato.

Non modifica niente. Legge collane.json, che sta accanto a questo script.
"""
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))


def mtime(p):
    try:
        return os.path.getmtime(p)
    except OSError:
        return 0


def elenca(d, suffissi=None, cartelle=False):
    if not os.path.isdir(d):
        return []
    v = []
    for n in sorted(os.listdir(d)):
        if n.startswith(".") or n.startswith("_"):
            continue
        p = os.path.join(d, n)
        if cartelle and os.path.isdir(p):
            v.append(n)
        elif not cartelle and os.path.isfile(p) and (not suffissi or n.endswith(suffissi)):
            v.append(n)
    return v


def stato_collana(radice, chiave, c):
    prog = os.path.join(radice, c["progetto"])
    print(f"\n━━ {chiave}  ·  {c['collana']}  ({c['progetto']})")
    if not os.path.isdir(prog):
        print("   cartella assente")
        return

    log = elenca(os.path.join(prog, "log"), (".md", ".txt"))
    capitoli = c["schema"] == "capitoli"
    unita = elenca(os.path.join(prog, "libri" if capitoli else "volumi"), cartelle=True)
    racconti = [] if capitoli else [f[:-3] for f in elenca(os.path.join(prog, "racconti"), (".md",))
                                    if not f.endswith(".bibbia.md")]
    print(f"   log: {len(log)}" + (f"   racconti: {len(racconti)}" if racconti else "") +
          f"   {'libri' if capitoli else 'volumi'}: {len(unita)}")

    usati = set()
    for v in unita:
        vdir = os.path.join(prog, "libri" if capitoli else "volumi", v)
        fonti = []
        if capitoli:
            fonti = [os.path.join(vdir, f) for f in elenca(vdir, (".md",))]
        else:
            man = os.path.join(vdir, "manifest.txt")
            if os.path.isfile(man):
                for riga in open(man, encoding="utf-8"):
                    riga = riga.strip()
                    if riga and not riga.startswith("#"):
                        nome = riga.split()[0]
                        usati.add(nome)
                        fonti.append(os.path.join(prog, "racconti", f"{nome}.md"))
            fonti += [os.path.join(vdir, f) for f in ("front.md", "timeline.md", "meta.yaml")]

        prompt = any(os.path.isfile(os.path.join(prog, "copertine", n))
                     for n in (f"prompt-copertina-{v}.md", f"prompt-libro-{v}.md"))
        cover = next((e for e in (".jpg", ".jpeg", ".png")
                      if os.path.isfile(os.path.join(prog, "copertine", f"{v}{e}"))), None)
        alias = c.get("alias", {}).get(v, {})
        nome_epub = alias.get("epub", v)
        slug_sito = alias.get("sito", v) if "sito" in alias else v
        epub = os.path.join(prog, "epub", f"{nome_epub}.epub")
        t_epub = mtime(epub)
        vecchio = t_epub and any(mtime(f) > t_epub for f in fonti if f)

        if slug_sito is None:
            pubblicato, t_pub = None, None     # volume che sul sito non va
        else:
            pubblicato = os.path.join(radice, "sito", "libri",
                                      f"{c['prefisso_sito']}{slug_sito}.epub")
            t_pub = mtime(pubblicato)

        if not cover and not prompt:
            passo = "da scrivere il prompt copertina"
        elif not cover:
            passo = "in attesa della copertina dall'utente"
        elif not t_epub:
            passo = "pronto per il build"
        elif vecchio:
            passo = "EPUB più vecchio delle fonti → ricostruire"
        elif t_pub is None:
            passo = "costruito · sul sito non va" + (f" ({alias['nota']})" if alias.get("nota") else "")
        elif not t_pub:
            passo = "da pubblicare sul sito"
        elif t_pub < t_epub:
            passo = "sito disallineato → ricopiare l'EPUB e rigenerare"
        else:
            passo = "allineato"

        peso = f" {os.path.getsize(epub)/1024/1024:.1f} MB" if t_epub else ""
        print(f"   · {v:<28} {passo}{peso}")

    orfani = [r for r in racconti if r not in usati]
    if orfani:
        print(f"   racconti fuori da ogni manifest: {', '.join(orfani)}")
    if log:
        print(f"   log in {c['log']}: {len(log)} file "
              f"({', '.join(log[:6])}{'…' if len(log) > 6 else ''})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    radice = sys.argv[1].rstrip("/")
    filtro = sys.argv[2] if len(sys.argv) > 2 else None
    reg = json.load(open(os.path.join(QUI, "collane.json"), encoding="utf-8"))
    collane = reg["collane"]
    if filtro:
        if filtro not in collane:
            print(f"collana sconosciuta: {filtro} (ho {', '.join(collane)})")
            return 2
        collane = {filtro: collane[filtro]}
    for chiave, c in collane.items():
        stato_collana(radice, chiave, c)
    print("\nRicorda: il sito si carica via FTP a mano. Una build non è una pubblicazione.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
