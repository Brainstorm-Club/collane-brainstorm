# Fase `copertina` — il prompt, l'attesa, il controllo

**La copertina è parte della confezione quanto il testo.** Ed è la classe di output con il
baricentro più leggero (`patto.md` §4): si rigenera, quindi si itera liberamente — la verifica è
guardare l'immagine. Un EPUB senza copertina non si costruisce
(la regola 1), e la copertina non si improvvisa: prima si scrive il prompt, poi l'immagine la genera
e la carica **l'utente**.

## 1. Il prompt

Si scrive quando il racconto (o il volume) è **completo, revisionato e firmato** dall'autore
(`firmato:` nel `meta.yaml`, vedi `patto.md` §3) — se la firma manca, fermati e chiedila. Va in
`copertine/prompt-copertina-<vol>.md` — in Brancalonia `copertine/prompt-libro-<nome>.md`.

Il file non è solo il prompt: è il **documento di continuità della collana**. Struttura che
funziona, ricavata dai prompt esistenti:

1. **Titolo** — di che volume si tratta e che numero porta nella collana.
2. **Output atteso** — il percorso esatto del file e il comando di build che seguirà.
3. **Continuità di serie + regole apprese** — che cosa resta *identico parola per parola* rispetto
   agli altri volumi (il contenitore: cartelletta, fascia, palette, luce, grano, tipografia) e che
   cosa cambia (il soggetto al centro). Qui si annotano anche le correzioni dei tentativi andati
   male: valgono più del prompt stesso.
4. **Il prompt vero** in un blocco ```text``` da copiare **tutto intero**, in inglese, con la coda
   per il generatore usato (p.es. `--ar 2:3 --style raw`).
5. **Note di coerenza (canone)** — perché c'è quello che c'è: chi sono le facce, che cos'è
   l'oggetto, quale accento di colore ricorre su tutta la collana.

Regole di scrittura del prompt:

- **2:3 verticale**, sempre.
- **Il contenitore è la copertina**: la cartelletta/il libro/il codice riempie il fotogramma, bordo
  a bordo. Niente scrivania, niente sfondo, niente oggetti esterni — è l'errore che si ripete.
- **Una palette con un accento solo**, dichiarato e ricorrente su tutta la collana.
- **Lista «Avoid:» esplicita** in coda: stili sbagliati, loghi reali, nomi leggibili di persone
  reali, watermark, lens flare, colori che non appartengono alla collana.
- **Niente esergo firmato da un personaggio che nel volume non compare.**
- Coerenza con la finta collana: Urania '82 per Korvaal, fanzine anni '90 per dnd-jr, dossier
  riservato per Heroes, codice ritrovato per Apocalisse, atti proibiti per Dark Heresy, paperback
  1982 per Brancalonia.

## 2. L'attesa

Scritto il prompt: **fermati e dillo**. L'immagine la genera l'utente e la carica in
`copertine/<vol>.png` (o `.jpg`). Non costruire l'EPUB, non "preparare intanto": è la regola che
l'utente ha chiesto esplicitamente di rispettare, e gli script dei progetti falliscono apposta.

## 3. Il controllo, quando l'immagine arriva

Due controlli, e servono tutti e due.

**Quello che si misura** — `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_copertina.py <progetto> <volume>`:
formato, proporzioni 2:3, risoluzione (≥ 1200 px di larghezza), peso, e il tetto di **3 MB**
dell'EPUB. Un PNG grosso si ricomprime in JPEG q95: il build preferisce il `.jpg` quando c'è.

```bash
sips -s format jpeg -s formatOptions 95 copertine/<vol>.png --out copertine/<vol>.jpg
```

**Quello che si guarda** — apri davvero il file e confrontalo col prompt:

- il contenitore riempie il fotogramma? c'è una scrivania o uno sfondo che non doveva esserci?
- il testo in copertina è leggibile e **scritto giusto**? (i generatori sbagliano le parole, e il
  titolo sbagliato è l'errore che si vede per primo)
- l'accento di colore della collana c'è ed è l'unico?
- le facce, gli oggetti, i mezzi corrispondono a quello che dice il canone del volume?
- è coerente con le copertine già fatte della stessa collana? mettile a confronto, non a memoria.

Se qualcosa non va, **non aggiustare il file**: aggiorna il prompt con la correzione appresa (punto
3 della struttura) e chiedi un nuovo tentativo.

## 4. La sinossi

Insieme alla copertina, il volume vuole la sua **sinossi** come campo `description:` in
`meta.yaml`: una o due frasi nella voce della collana, dal contenuto reale del libro, **senza
spoiler** — chi legge può essere un giocatore. Il sito la usa per l'overlay sulla copertina e per il
JSON-LD. Un volume buildato solo in `epub/` vuole comunque il suo `meta.yaml` con la `description`.
