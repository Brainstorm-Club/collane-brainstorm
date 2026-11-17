# Fase `epub` — pre-build, build, verifica

Serve `pandoc` ≥ 3.1. Si lancia **dalla radice del progetto**, non dalla radice del repo.

## 1. Pre-build

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py heroes taglie-di-londra
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py brancalonia 5-teste --capitoli
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_copertina.py heroes taglie-di-londra
```

Controlla: manifest completo, prefissi-note univoci, **note orfane**, note definite e mai
richiamate, `meta.yaml` con `title`, `description` e **`firmato:`** (la firma dell'autore: se
manca, non si builda e non la scrivi tu), copertina presente, e le spie di bozza in
`front.md` / `timeline.md`.

**Gli avvisi su front/timeline vanno letti uno per uno.** Quei due file **entrano nell'EPUB**: un
`[BOZZA…]`, un aside di regia `[L'Analista apre…]`, la parola «campagna» o «sessione» finiscono nel
libro pubblicato. Tenere solo quello che è in-fiction, `[OMISSIS]` compreso.

Il controllo è volutamente sospettoso e qualche avviso è legittimo: in *Tiro Salvezza* il Master
parla davvero del suo tavolo e della sua campagna, ed è in voce. Decidi tu caso per caso — quello
che non si può fare è non guardare.

## 2. Build

```bash
cd heroes
bash build_epub.sh taglie-di-londra
bash build_epub.sh --all        # tutti i volumi; salta volumi/_*
```

Lo script compone `meta.yaml` + `front.md` + `timeline.md` + i racconti del `manifest.txt` (con i
prefissi-note applicati) + `assets/colophon.md`, usa `copertine/<vol>.jpg|.png` come cover e
`assets/epub.css`, e scrive `epub/<vol>.epub`.

Brancalonia ha lo schema a capitoli: `bash build_epub.sh <nome>` prende
`libri/<nome>/meta.yaml` + `epigrafe.md` + i `NN_*.md`.

## 3. Verifica dell'uscita

Lo script stampa già il suo check (cover presente, voci d'indice, note orfane). Oltre a quello:

- **peso**: tetto **3 MB** per EPUB. Se sfonda, è quasi sempre la copertina: JPEG q95.
- **indice**: le voci ci sono tutte e nell'ordine di lettura del manifest?
- **apertura**: ogni volume si apre con la sua tripletta di confezione (nota del curatore →
  indice → linea temporale) e si chiude col colofone del club, aggiunto in automatico.
- **ricostruire a catena**: un racconto toccato va ricostruito in **tutti** i volumi che lo
  contengono, omnibus compreso. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py .` segnala gli EPUB più vecchi delle loro
  fonti.

## 4. Che cosa non si fa

- **Niente DOCX, niente PDF**: le collane sono EPUB + Markdown. I PDF sono dei fascicoli da tavolo,
  che è un'altra cosa (`fase-fascicolo.md`).
- **Niente build prima della copertina, e niente copertina prima della firma.**
- **Volumi già pubblicati prima del patto** non hanno `firmato:`: al prossimo rebuild l'autore li
  rilegge e li firma. Non aggiungere il campo in blocco per far passare il controllo.
- **Niente copia del racconto dentro il volume**: il manifest lo referenzia, sempre.

## Casi già visti

- **Volume con un racconto solo**: sul sito non si spezza in pagine (sarebbe uno stub più un URL
  doppio). Nell'EPUB non cambia niente.
- **Omnibus**: si costruisce ad **arco concluso**. Korvaal lo tiene come EPUB ma non gli dà una
  pagina web, perché ripeterebbe per intero i racconti degli altri volumi.
- **Prefissi che collidono**: due racconti con lo stesso prefisso mescolano le note senza che il
  build se ne accorga. Il pre-build sì.
