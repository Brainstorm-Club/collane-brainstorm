# collane-brainstorm

**Manuale online:** <https://brainstorm-club.github.io/collane-brainstorm/>

Plugin per Claude Code che impacchetta il modo in cui al **Brainstorm Club** si trasformano i log
di una campagna in un libro confezionato: **log → racconto → tre revisori → firma dell'autore →
copertina → EPUB → sito**. Un comando per ogni campagna, più gli script che fanno i controlli che prima si facevano a
occhio (e che ogni tanto saltavano).

## Il patto: chi pensa, chi verifica, chi firma

Il plugin fa scrivere prosa a un modello. Il rischio non è che scriva male: è che scriva
abbastanza bene da essere firmata senza essere stata pensata. Per questo è costruito sul
**Triangolo del Pensare-Con** (*Pensare con LLM — the right way*, cap. 2):

| vertice | che cosa chiede | come lo fa rispettare il plugin |
|---|---|---|
| **Intento** | sapere che cosa si cerca prima del primo prompt | ogni comando apre con una riga d'intento da confermare: esplorare o chiudere, bozza o definitivo, criterio di riuscita |
| **Avversario** | costruire la verifica prima di leggere l'output | «Verifiche» scritte nella bibbia prima della stesura; script che misurano; tre passate che consegnano referti, non assoluzioni; il revisore di stile argomenta il contrario; soglie di rinuncia |
| **Editore** | la firma resta dell'autore | `firmato: "Nome Cognome, data"` nel `meta.yaml`, che il modello non scrive mai: senza, `controlla_volume.py` blocca il build |

La pressione non è uguale per tutto — un prompt di copertina si delega, un racconto definitivo si
pensa insieme, il canone e il sito sono dell'autore — e le soglie di rinuncia sono scritte prima.
Tutto in [`references/patto.md`](skills/collane-brainstorm/references/patto.md).

> **I volumi costruiti prima del patto non hanno `firmato:`.** Al prossimo rebuild l'autore li
> rilegge e li firma; `stato.py` li segnala come «non firmato» intanto.

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
| `/personaggi` | una a scelta | l'anagrafe dei personaggi: evoluzione nei libri e ritratti |

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
| `personaggi` | l'anagrafe della collana: chi compare dove, come cambia, stato e morte, prompt del ritratto (comando `/personaggi`) |
| `copertina` | scrive il prompt, poi **si ferma**; e controlla l'immagine quando arriva |
| `epub` | pre-build (firma compresa), build, verifica dell'uscita |
| `sito` | porta un volume finito sulle pagine di lettura (il caricamento FTP resta a mano) |
| `fascicolo` | avventure, bestiari e manuali da tavolo, impaginati in PDF |

## Che cosa c'è dentro

```
plugin-collane/
├── commands/          un comando per collana + /collane + /personaggi
├── skills/collane-brainstorm/
│   ├── SKILL.md       il registro delle collane, le fasi, le regole ferme
│   └── references/    una reference per fase (personaggi compresa) + patto.md + giochi.md + regole-ferme.md
├── agents/            lettore-log · redattore · correttore-bozze · revisore-stile · anagrafe
├── docs/index.html  come è fatto questo plugin, e come se ne costruisce uno
└── scripts/
    ├── collane.json            registro delle collane (percorsi, slug, alias dei nomi file)
    ├── stato.py                panoramica della pipeline
    ├── controlla_volume.py     pre-build: firma, note orfane, manifest, prefissi, meta, spie di bozza
    ├── controlla_copertina.py  formato, 2:3, risoluzione, peso, tetto di 3 MB dell'EPUB
    └── personaggi.py           anagrafe: ordine della storia, apparizioni, morti, ritratti scaduti, indice, prompt
```

Gli script si lanciano dalla radice `brainstorm/` e non modificano niente — tranne `personaggi.py nuovo` (crea uno scheletro, mai sopra una scheda esistente) e `personaggi.py indice` (rigenera `INDICE.md`):

```bash
python3 scripts/stato.py .
python3 scripts/stato.py . korvaal
python3 scripts/controlla_volume.py heroes taglie-di-londra
python3 scripts/controlla_volume.py brancalonia 5-teste --capitoli
python3 scripts/controlla_copertina.py apocalisse appestato
python3 scripts/personaggi.py . heroes stato
python3 scripts/personaggi.py . heroes nuovo "Darko"
python3 scripts/personaggi.py . heroes prompt darko
```

## Gli agenti

Cinque mestieri delegabili, tutti in sola lettura, che tornano come referto invece che come testo
riscritto:

| agente | quando |
|---|---|
| `anagrafe` | proporre o verificare le schede dei personaggi: aspetto con le fonti, evoluzione nell'ordine della storia, soggetto del ritratto |
| `lettore-log` | leggere i log senza riversarli in sessione: eventi cardine, registro morti, materiale mai usato, discrepanze |
| `redattore` | prima passata: coerenza, semine, orizzonte di conoscenza, canone, morti onorate |
| `correttore-bozze` | seconda passata: lingua, false friend, grafie canoniche, note orfane (lancia lo script) |
| `revisore-stile` | terza passata: tenuta della voce, tono, note, tagli |

Sullo stesso racconto vanno **in sequenza**; in parallelo si lanciano su racconti diversi.

## L'anagrafe dei personaggi

`/personaggi <collana>` tiene una scheda per personaggio in `<progetto>/assets/personaggi/`:
chi è, com'è fatto (ogni tratto con la sua fonte `file:riga`), e una tabella d'evoluzione con una
riga per ogni racconto in cui compare, **nell'ordine della storia** — i prequel vengono prima, e la
cicatrice presa nel quinto libro non c'è nel primo.

`personaggi.py stato` confronta le schede con i testi: trova i racconti in cui un personaggio
compare ma la scheda non ne parla, i morti che ricompaiono dopo `morto_in`, i personaggi assenti
dal canone, e i **ritratti scaduti** — quando l'aspetto è cambiato dopo il racconto per cui il
prompt era stato scritto.

Il ritratto funziona come le copertine: `_stile.md` è il contenitore comune della collana (stile,
luce, *Avoid*, con il segnaposto `{SOGGETTO}`), la scheda porta solo il soggetto.
`personaggi.py prompt <scheda>` li compone. L'immagine la genera l'utente.

## Il manuale

[`docs/index.html`](docs/index.html) — come è fatto questo plugin e che cosa se ne impara per
costruirne uno: i cinque pezzi, i tre livelli di contesto, i cancelli del flusso, il Triangolo del
Pensare-Con dentro la pipeline, la divisione fra
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
Il [manuale](docs/index.html) spiega perché è fatto così.

## Che cosa dà per scontato

- la radice `brainstorm/` con dentro le cartelle delle campagne, `sito/` e `impaginatore/`;
- `pandoc` ≥ 3.1 per i build EPUB, `python3`, e per i fascicoli `node` + Microsoft Edge;
- il `CLAUDE.md` di ogni campagna, che resta **l'autorità** su voce, tono e confezione: la skill
  dice come si lavora, quei file dicono che cosa è vero in quella collana.

## Le regole che il plugin difende

1. Niente copertina senza la firma dell'autore, niente EPUB senza copertina.
2. Se un personaggio muore nel log, muore nel racconto.
3. Il racconto è fonte unica: i volumi lo compongono, non lo copiano.
4. Niente note orfane.
5. `front.md` e `timeline.md` entrano nell'EPUB: prosa finita, mai bozza.
6. Il sito si carica via FTP a mano: una build non è una pubblicazione.
7. Quello che resta fuori diventa una issue, non una riga in chat.

La versione lunga, col perché di ognuna, sta in
`skills/collane-brainstorm/references/regole-ferme.md`.
