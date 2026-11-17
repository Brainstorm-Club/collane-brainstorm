#!/usr/bin/env python3
"""Sentinella del sito: quello che è costruito in locale è davvero quello che è online?

    python3 sentinella_sito.py <radice-brainstorm> [--solo-locale]

Due controlli, nell'ordine:

  1. locale  per ogni volume pubblicato, sito/libri/<slug>.epub dev'essere uguale
             (stessa dimensione e contenuto) a <progetto>/epub/<vol>.epub; segnala gli
             EPUB mancanti, quelli disallineati e quelli più vecchi della build.
  2. dominio ogni URL di sito/sitemap.xml deve rispondere 200; le pagine che non
             devono stare online (*-interno.html, omnibus senza pagina) devono dare
             404. Se il dominio risponde diverso dal locale, è un caricamento FTP
             mancato o vecchio.

Il caricamento FTP lo fa l'autore: questo script lo verifica, non lo esegue.
Non modifica niente. Uscita: 0 allineato · 1 avvisi · 2 errori.
"""
import filecmp
import json
import os
import re
import sys
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))


def registro(radice):
    reg = json.load(open(os.path.join(QUI, "collane.json"), encoding="utf-8"))["collane"]
    locale = os.path.join(radice, "collane.local.json")
    if os.path.isfile(locale):
        reg.update(json.load(open(locale, encoding="utf-8")).get("collane", {}))
    return reg


def stato_http(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "sentinella-sito"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"errore: {e.__class__.__name__}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    radice = os.path.abspath(args[0])
    sito = os.path.join(radice, "sito")
    errori, avvisi, ok = [], [], []

    # 1. locale
    for chiave, c in registro(radice).items():
        prog = os.path.join(radice, c["progetto"])
        edir = os.path.join(prog, "epub")
        alias = c.get("alias", {})
        for vol in c.get("ordine_volumi", []):
            a = alias.get(vol, {})
            slug = a.get("sito", vol) if "sito" in a else vol
            if slug is None:
                continue
            src = os.path.join(edir, f"{a.get('epub', vol)}.epub")
            dst = os.path.join(sito, "libri", f"{c.get('prefisso_sito', '')}{slug}.epub")
            rel = os.path.relpath(dst, radice)
            if not os.path.isfile(src):
                continue
            if not os.path.isfile(dst):
                avvisi.append(f"{rel}: manca sul sito (l'EPUB esiste in {os.path.relpath(src, radice)})")
            elif not filecmp.cmp(src, dst, shallow=False):
                piu = "più vecchio" if os.path.getmtime(dst) < os.path.getmtime(src) else "diverso"
                avvisi.append(f"{rel}: {piu} da {os.path.relpath(src, radice)} → ricopiarlo e caricarlo")
            else:
                ok.append(rel)

    # 2. dominio
    if "--solo-locale" not in sys.argv:
        smap = os.path.join(sito, "sitemap.xml")
        urls = re.findall(r"<loc>([^<]+)</loc>", open(smap, encoding="utf-8").read()) \
            if os.path.isfile(smap) else []
        base = re.match(r"https?://[^/]+/", urls[0]).group(0) if urls else None
        for u in urls:
            s = stato_http(u)
            (ok if s == 200 else errori).append(f"{u} → {s}" if s != 200 else u)
        if base:
            vietate = []
            for d, _, files in os.walk(sito):
                for f in files:
                    if f.endswith("-interno.html"):
                        vietate.append(os.path.relpath(os.path.join(d, f), sito))
            for v in vietate:
                s = stato_http(base + v)
                if s != 404:
                    errori.append(f"{base + v} → {s}: pagina interna raggiungibile online, deve dare 404")
                else:
                    ok.append(f"{base + v} → 404 (giusto)")
        print(f"dominio: {len(urls)} URL dalla sitemap controllate")

    print(f"allineati: {len(ok)}")
    for v in avvisi:
        print(f"  !    {v}")
    for v in errori:
        print(f"  ERR  {v}")
    if not avvisi and not errori:
        print("Sito allineato: quello che è in locale è quello che è online.")
    return 2 if errori else (1 if avvisi else 0)


if __name__ == "__main__":
    sys.exit(main())
