#!/usr/bin/env bash
#
# Build EPUB di un VOLUME della collana «{{COLLANA}}» ({{GIOCO}}).
# Da lanciare dalla RADICE del progetto (la cartella {{CARTELLA}}/):
#
#     bash build_epub.sh <volume>
#     bash build_epub.sh --all          # ricostruisce tutti i volumi (salta volumi/_*)
#
# Un RACCONTO vive UNA volta sola in racconti/; i VOLUMI lo compongono via manifest.
# Lo stesso racconto puo' stare in piu' volumi senza essere duplicato.
#
# Struttura attesa (radice = cartella corrente):
#   racconti/<nome>.md            i singoli racconti                                     [fonte unica]
#   volumi/<vol>/meta.yaml        title/subtitle/author/lang/date/description (+ firmato) [obbligatorio]
#   volumi/<vol>/front.md         {{APERTURA}}                                            [opzionale]
#   volumi/<vol>/timeline.md      linea temporale                                        [opzionale]
#   volumi/<vol>/manifest.txt     righe "<nome-racconto>  <prefisso-note>", in ordine    [obbligatorio]
#   copertine/<vol>.jpg|.png      copertina a piena pagina                               [OBBLIGATORIA]
#   assets/colophon.md            colofone condiviso, in coda a ogni volume              [obbligatorio]
#   assets/epub.css               stile EPUB                                             [opzionale]
#   -> output: epub/<vol>.epub
#
# Prima del build: python3 <plugin>/scripts/controlla_volume.py . <vol>  (firma, note, apparato)
# Generato da nuova_collana.py del plugin brainstormclub.
set -euo pipefail

ROOT="$(pwd)"

build_one () {
  local VOL="$1"
  local VDIR="$ROOT/volumi/$VOL"
  [ -d "$VDIR" ]                 || { echo "ERRORE: manca la cartella $VDIR"; return 1; }
  [ -f "$VDIR/meta.yaml" ]       || { echo "ERRORE: manca $VDIR/meta.yaml"; return 1; }
  [ -f "$VDIR/manifest.txt" ]    || { echo "ERRORE: manca $VDIR/manifest.txt"; return 1; }
  [ -f "$ROOT/assets/colophon.md" ] || { echo "ERRORE: manca assets/colophon.md"; return 1; }

  local SRC; SRC="$(mktemp)"
  cat "$VDIR/meta.yaml" > "$SRC"; printf '\n' >> "$SRC"
  # front (nota dell'Analista + indice) e timeline, se presenti
  [ -f "$VDIR/front.md" ]    && { cat "$VDIR/front.md";    printf '\n\n'; } >> "$SRC"
  [ -f "$VDIR/timeline.md" ] && { cat "$VDIR/timeline.md"; printf '\n\n'; } >> "$SRC"

  # racconti dal manifest, con prefisso-note applicato (via python, per robustezza)
  python3 - "$ROOT" "$VDIR/manifest.txt" >> "$SRC" <<'PY'
import re, sys
root, manifest = sys.argv[1], sys.argv[2]
blocks = []
for raw in open(manifest, encoding="utf-8"):
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()
    name = parts[0]
    pref = parts[1] if len(parts) > 1 else ""
    path = f"{root}/racconti/{name}.md"
    try:
        t = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        sys.stderr.write(f"ERRORE: manca racconti/{name}.md\n"); sys.exit(3)
    if pref:
        t = re.sub(r'\[\^([0-9A-Za-z]+)\]', lambda m: f'[^{pref}{m.group(1)}]', t)
    blocks.append(t.strip())
print("\n\n\n".join(blocks))
PY
  printf '\n\n' >> "$SRC"

  # colofone condiviso in coda (Brainstorm Club)
  cat "$ROOT/assets/colophon.md" >> "$SRC"; printf '\n' >> "$SRC"

  mkdir -p "$ROOT/epub"
  local OUT="$ROOT/epub/$VOL.epub"
  # copertina: preferisci <vol>.jpg (piu' leggera), poi <vol>.png
  local COVER=""
  if   [ -f "$ROOT/copertine/$VOL.jpg" ]; then COVER="--epub-cover-image=$ROOT/copertine/$VOL.jpg"
  elif [ -f "$ROOT/copertine/$VOL.png" ]; then COVER="--epub-cover-image=$ROOT/copertine/$VOL.png"
  else
    # regola della collana: NIENTE EPUB SENZA COPERTINA
    echo "ERRORE: manca copertine/$VOL.jpg|.png — prima il prompt copertina, poi l'immagine, poi il build"
    rm -f "$SRC"; return 1
  fi
  local CSS="";   [ -f "$ROOT/assets/epub.css" ]    && CSS="--css=$ROOT/assets/epub.css"

  pandoc "$SRC" -o "$OUT" $COVER $CSS \
    --toc --toc-depth=2 \
    --split-level=1 \
    --from markdown+smart+footnotes

  # check: note orfane + cover + voci indice  (fatto sul sorgente combinato e sull'EPUB)
  python3 - "$SRC" "$OUT" <<'PY'
import sys, re, zipfile
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
refs = set(re.findall(r'\[\^([0-9A-Za-z]+)\]:', t))
uses = set(re.findall(r'\[\^([0-9A-Za-z]+)\](?!:)', t))
orphan = uses - refs
z = zipfile.ZipFile(out)
opf = z.read([n for n in z.namelist() if n.endswith('.opf')][0]).decode()
nav = z.read('EPUB/nav.xhtml').decode() if 'EPUB/nav.xhtml' in z.namelist() else ''
voci = len(re.findall(r'<a[^>]*>', nav))
cover = 'ok' if 'cover-image' in opf else 'MANCA (metti copertine/<vol>.png)'
note = 'ok' if not orphan else f'ORFANE: {sorted(orphan)}'
print(f"  cover: {cover} | voci indice: {voci} | note: {note}")
if orphan:
    sys.exit(4)
PY
  rm -f "$SRC"
  echo "Creato: $OUT"
}

if [ "${1:-}" = "--all" ]; then
  for d in "$ROOT"/volumi/*/; do
    vol="$(basename "$d")"
    case "$vol" in _*) echo "== salto $vol (template) =="; continue;; esac
    echo "== $vol =="
    build_one "$vol"
  done
else
  VOL="${1:?Uso: bash build_epub.sh <vol> | --all   (es. omnibus)}"
  build_one "$VOL"
fi
