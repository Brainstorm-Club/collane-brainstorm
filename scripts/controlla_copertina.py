#!/usr/bin/env python3
"""Controlla la copertina di un volume prima del build EPUB.

    python3 controlla_copertina.py <cartella-progetto> <volume>

Verifica, nell'ordine in cui il lavoro le richiede:
  1. esiste il prompt copertina (prompt-copertina-<vol>.md o prompt-libro-<vol>.md);
  2. esiste il file immagine (.jpg preferito, .png accettato);
  3. formato, proporzioni (2:3), risoluzione e peso;
  4. il peso previsto dell'EPUB con quella copertina (tetto 3 MB).

Non apre l'immagine: dice solo quel che si misura. Il giudizio su che cosa
c'è *dentro* (coerenza col prompt, col canone, testo leggibile, dita storte)
lo dà chi legge, guardando il file con lo strumento di lettura immagini.

Uscita: 0 tutto a posto · 1 avvisi · 2 manca qualcosa di obbligatorio.
"""
import os
import struct
import sys

MIN_LARGHEZZA = 1200          # sotto, la cover sgrana sugli e-reader retina
RAPPORTO_ATTESO = 2 / 3       # 2:3 verticale, standard della collana
TOLLERANZA_RAPPORTO = 0.04
PESO_MAX_COVER = 3.0 * 1024 * 1024   # oltre, l'EPUB sfonda i 3 MB da solo


def dimensioni(path):
    """(larghezza, altezza, formato) leggendo l'intestazione del file."""
    with open(path, "rb") as f:
        testa = f.read(32)
        if testa[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", testa[16:24])
            return w, h, "PNG"
        if testa[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                if not marker:
                    break
                if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h, "JPEG"
                lung = struct.unpack(">H", f.read(2))[0]
                f.seek(lung - 2, os.SEEK_CUR)
    return None, None, "sconosciuto"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    radice, vol = sys.argv[1].rstrip("/"), sys.argv[2]
    cop = os.path.join(radice, "copertine")
    errori, avvisi, ok = [], [], []

    if not os.path.isdir(cop):
        print(f"ERRORE: manca {cop}/")
        return 2

    # 1. prompt copertina — viene prima dell'immagine, sempre
    prompt = [p for p in (f"prompt-copertina-{vol}.md", f"prompt-libro-{vol}.md")
              if os.path.isfile(os.path.join(cop, p))]
    immagine_c_e = any(os.path.isfile(os.path.join(cop, f"{vol}{e}"))
                       for e in (".jpg", ".jpeg", ".png"))
    if prompt:
        ok.append(f"prompt copertina: copertine/{prompt[0]}")
    elif immagine_c_e:
        # in qualche collana il prompt porta il nome del racconto, non del volume
        avvisi.append(f"nessun prompt-copertina-{vol}.md accanto all'immagine: "
                      "controlla se è intitolato al racconto, altrimenti la copertina "
                      "non è riproducibile")
    else:
        errori.append(f"manca il prompt copertina (copertine/prompt-copertina-{vol}.md): "
                      "va scritto PRIMA che l'utente generi l'immagine")

    # 2. immagine
    immagini = [os.path.join(cop, f"{vol}{e}") for e in (".jpg", ".jpeg", ".png")
                if os.path.isfile(os.path.join(cop, f"{vol}{e}"))]
    if not immagini:
        errori.append(f"manca la copertina (copertine/{vol}.jpg o .png): "
                      "NIENTE EPUB SENZA COPERTINA — fermati e aspetta che la carichi l'utente")
        stampa(ok, avvisi, errori)
        return 2

    scelta = immagini[0]                       # .jpg vince sul .png, come il build
    if len(immagini) > 1:
        ok.append("presenti sia .jpg sia .png: il build usa il .jpg (più leggero)")

    peso = os.path.getsize(scelta)
    w, h, fmt = dimensioni(scelta)
    ok.append(f"copertina: {os.path.relpath(scelta, radice)} ({fmt}, {peso/1024/1024:.2f} MB)")

    if not w:
        avvisi.append("non riesco a leggere le dimensioni: formato inatteso?")
    else:
        ok.append(f"dimensioni: {w}×{h} px")
        if h <= w:
            errori.append(f"la copertina è orizzontale o quadrata ({w}×{h}): la collana vuole 2:3 verticale")
        else:
            rapporto = w / h
            if abs(rapporto - RAPPORTO_ATTESO) > TOLLERANZA_RAPPORTO:
                avvisi.append(f"proporzioni {rapporto:.3f} invece di 0.667 (2:3): "
                              "sugli e-reader comparirà con le bande")
        if w < MIN_LARGHEZZA:
            avvisi.append(f"larghezza {w} px sotto i {MIN_LARGHEZZA}: sgrana sugli schermi densi")

    if fmt == "PNG" and peso > 1.5 * 1024 * 1024:
        avvisi.append("PNG pesante: ricomprimilo in JPEG q95 "
                      f"(`sips -s format jpeg -s formatOptions 95 copertine/{vol}.png "
                      f"--out copertine/{vol}.jpg`) per tenere l'EPUB sotto i 3 MB")
    if peso > PESO_MAX_COVER:
        errori.append(f"copertina da {peso/1024/1024:.2f} MB: da sola sfonda il tetto di 3 MB dell'EPUB")

    # 3. il peso che avrà l'EPUB
    epub = os.path.join(radice, "epub", f"{vol}.epub")
    if os.path.isfile(epub):
        p = os.path.getsize(epub)
        voce = f"EPUB attuale: {p/1024/1024:.2f} MB"
        (avvisi if p > 3 * 1024 * 1024 else ok).append(
            voce + (" — oltre i 3 MB" if p > 3 * 1024 * 1024 else ""))

    stampa(ok, avvisi, errori)
    return 2 if errori else (1 if avvisi else 0)


def stampa(ok, avvisi, errori):
    for v in ok:
        print(f"  ok   {v}")
    for v in avvisi:
        print(f"  !    {v}")
    for v in errori:
        print(f"  ERR  {v}")
    if not errori and not avvisi:
        print("\nCopertina a posto. Resta da guardarla: apri il file e confrontalo col prompt.")
    elif not errori:
        print("\nNiente di bloccante. Guarda comunque il file prima del build.")
    else:
        print("\nNon costruire l'EPUB finché gli ERR non sono risolti.")


if __name__ == "__main__":
    sys.exit(main())
