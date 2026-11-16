# collane-brainstorm

Plugin per Claude Code che impacchetta il modo in cui al **Brainstorm Club** si trasformano i log
di una campagna in un libro confezionato: **log → racconto → tre revisori → copertina → EPUB →
sito**. Un comando per ogni campagna, più gli script che fanno i controlli che prima si facevano a
occhio (e che ogni tanto saltavano).

## I comandi

| comando | collana | gioco |
|---|---|---|
| `/collane` | tutte | panoramica e prossima mossa |
| `/brancalonia` | Regno di Taglia | Brancalonia (Acheron Games) |
| `/korvaal` | Il ciclo di Korvaal | Rogue Trader (W40K) |
| `/dark-heresy` | ACTA HERETICA | Dark Heresy (Settore Calixis) |
| `/dnd-jr` | Tiro Salvezza | D&D 5e nel Vecchio Mondo di Warhammer |
| `/apocalisse` | Terre Desolate | Apocalisse (Acheron) |
| `/heroes` | Dossier Scavengers | Heroes Unlimited (Palladium) |

Ogni comando prende una **fase**:

```
/korvaal stato
/heroes log
/apocalisse racconto
/dnd-jr revisione
/brancalonia copertina
/dark-heresy epub miniera
/korvaal sito origini
/brancalonia fascicolo
```

| fase | che cosa fa |
|---|---|
| `stato` | dove si è fermata la pipeline, volume per volume |
| `log` | legge i log: eventi cardine, registro morti, materiale non usato, discrepanze |
| `racconto` | co-design socratico → outline → bibbia → stesura a blocchi |
| `revisione` | le tre passate: Redattore → Correttore di bozze → Revisore di stile |
| `copertina` | scrive il prompt, poi **si ferma**; e controlla l'immagine quando arriva |
| `epub` | pre-build, build, verifica dell'uscita |
| `sito` | porta un volume finito sulle pagine di lettura (il caricamento FTP resta a mano) |
| `fascicolo` | avventure, bestiari e manuali da tavolo, impaginati in PDF |

## Che cosa c'è dentro

```
plugin-collane/
├── commands/          un comando per collana + /collane
├── skills/collane-brainstorm/
│   ├── SKILL.md       il registro delle collane, le fasi, le regole ferme
│   └── references/    una reference per fase + giochi.md + regole-ferme.md
├── agents/            lettore-log · redattore · correttore-bozze · revisore-stile
├── docs/manuale.html  come è fatto questo plugin, e come se ne costruisce uno
└── scripts/
    ├── collane.json            registro delle collane (percorsi, slug, alias dei nomi file)
    ├── stato.py                panoramica della pipeline
    ├── controlla_volume.py     pre-build: note orfane, manifest, prefissi, meta, spie di bozza
    └── controlla_copertina.py  formato, 2:3, risoluzione, peso, tetto di 3 MB dell'EPUB
```

Gli script si lanciano dalla radice `brainstorm/` e non modificano niente:

```bash
python3 scripts/stato.py .
python3 scripts/stato.py . korvaal
python3 scripts/controlla_volume.py heroes taglie-di-londra
python3 scripts/controlla_volume.py brancalonia 5-teste --capitoli
python3 scripts/controlla_copertina.py apocalisse appestato
```

## Gli agenti

Quattro mestieri delegabili, tutti in sola lettura, che tornano come referto invece che come testo
riscritto:

| agente | quando |
|---|---|
| `lettore-log` | leggere i log senza riversarli in sessione: eventi cardine, registro morti, materiale mai usato, discrepanze |
| `redattore` | prima passata: coerenza, semine, orizzonte di conoscenza, canone, morti onorate |
| `correttore-bozze` | seconda passata: lingua, false friend, grafie canoniche, note orfane (lancia lo script) |
| `revisore-stile` | terza passata: tenuta della voce, tono, note, tagli |

Sullo stesso racconto vanno **in sequenza**; in parallelo si lanciano su racconti diversi.

## Il manuale

[`docs/manuale.html`](docs/manuale.html) — come è fatto questo plugin e che cosa se ne impara per
costruirne uno: i cinque pezzi, i tre livelli di contesto, i cancelli del flusso, la divisione fra
quel che misura uno script e quel che giudica il modello, gli agenti come mandati. Con i diagrammi.
Si apre in un browser, non serve altro.

## Installare

Dal repository GitHub:

```bash
claude plugin marketplace add Brainstorm-Club/collane-brainstorm
```

```bash
claude plugin install collane-brainstorm@brainstorm-club
```

Da una copia locale (si aggiorna da sola quando modifichi i file):

```bash
claude plugin marketplace add ./collane-brainstorm
```

In alternativa, senza plugin: copiare `skills/collane-brainstorm/` in `~/.claude/skills/`,
`agents/*.md` in `~/.claude/agents/` e `commands/*.md` in `~/.claude/commands/`. In quel caso
`${CLAUDE_PLUGIN_ROOT}` non è definito e i percorsi degli script vanno scritti per esteso.

## Usarlo fuori dal Brainstorm Club

Il plugin è scritto per le sei collane del club, ma la struttura è riusabile: le collane stanno
tutte in `scripts/collane.json` e nella tabella di `SKILL.md`. Per adattarlo a un altro tavolo si
riscrive il registro, `references/giochi.md` e i comandi; gli script, le fasi e gli agenti restano.
Il [manuale](docs/manuale.html) spiega perché è fatto così.

## Che cosa dà per scontato

- la radice `brainstorm/` con dentro le cartelle delle campagne, `sito/` e `impaginatore/`;
- `pandoc` ≥ 3.1 per i build EPUB, `python3`, e per i fascicoli `node` + Microsoft Edge;
- il `CLAUDE.md` di ogni campagna, che resta **l'autorità** su voce, tono e confezione: la skill
  dice come si lavora, quei file dicono che cosa è vero in quella collana.

## Le regole che il plugin difende

1. Niente EPUB senza copertina (prompt → l'utente carica l'immagine → build).
2. Se un personaggio muore nel log, muore nel racconto.
3. Il racconto è fonte unica: i volumi lo compongono, non lo copiano.
4. Niente note orfane.
5. `front.md` e `timeline.md` entrano nell'EPUB: prosa finita, mai bozza.
6. Il sito si carica via FTP a mano: una build non è una pubblicazione.
7. Quello che resta fuori diventa una issue, non una riga in chat.

La versione lunga, col perché di ognuna, sta in
`skills/collane-brainstorm/references/regole-ferme.md`.
