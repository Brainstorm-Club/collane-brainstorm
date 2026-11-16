# Le sei collane

Scheda breve per orientarsi. **L'autorità resta il `CLAUDE.md` della cartella** e, per lo stato del
ciclo, `assets/PROMPT_nuovi_racconti.md` sez. [8] + `assets/canone_serie.md`: lì lo stato è vivo,
qui è una fotografia.

---

## Brancalonia — *Regno di Taglia* · `brancalonia/`

GDR **Brancalonia** (Acheron Games), la Banda degli Sganassoni a Penumbria.
Racconti picareschi firmati **Nanoc Orabrabli**, narratore unico. Tono alla Pratchett.
**Schema a capitoli**: un libro è un racconto solo, in `libri/<nome>/` (epigrafe + `NN_*.md`), senza
manifest; le note non si prefissano. Copertine: `copertine/prompt-libro-<nome>.md` → `<nome>.png`,
paperback italiano 1982.
**Pagina dell'autore per libro**: `assets/autore.md` è il template, l'innesto cambia ogni volta.
Sul sito gli slug sono per esteso (`5-teste` → `le-cinque-teste`): vedi gli alias in `collane.json`.
Accanto, in `avventure/`, i **fascicoli giocabili** — altra cosa: `fase-fascicolo.md`.

## Rogue Trader — *Il ciclo di Korvaal* · `roguetrader/ciclo-korvaal/`

GDR **Rogue Trader** (Warhammer 40.000), la cricca del mercante corsaro Korvaal.
**Polifonia**: ogni racconto ha una voce solista in prima persona (il comandante megalomane, il
siniscalco contabile, le ancelle, il magos, il medico, la capitana); le note sono in personaggio.
Tono freddo, tragico, agrodolce: «ogni vittoria si paga». Falsa collana **FANTAFLOTTA**, tascabile
Urania 1982.
Volumi tematici (`origini`, `cronache`, `jen-lo-xenocida`, `estarosa`, `omnibus`) su una storia
sola: sul sito il **filo cronologico** si ricava dalla Timeline di `canone_serie.md`.
Ciclo **riscritto end-to-end** dal materiale dei log (13 racconti, ~137.600 parole): la regola dura
delle morti nasce qui, e qui è già applicata a tutto. L'omnibus ha l'EPUB ma non la pagina web.

## Dark Heresy — *ACTA HERETICA* · `roguetrader/dark-heresy/`

GDR **Dark Heresy**, Settore Calixis: una cellula di accoliti dell'inquisitore Vivaldi.
**Cornice unica e ricorrente**: il verbale del sapiente **Eruditus** in terza persona, più
**deposizioni** degli accoliti in prima persona (blockquote). Grimdark investigativo, da referto:
l'orrore è la macchina imperiale prima del caos. Confezione: dossier proibito dell'Ordo.
Arco **Haarlock** e **specchio in 13 frammenti** in `canone_serie.md`, con le grafie canoniche.
Attenzione: qui i prompt di copertina portano il nome del **racconto**, non del volume.

## D&D 5e under 16 — *Tiro Salvezza* · `dnd-jr/`

**D&D 5ª ed.** nel **Vecchio Mondo di Warhammer** (l'Impero, Ulthuan, Nehekara, Sylvania), giocato
dai ragazzi del club. **Narratore unico**: il Master, **Ozymandias il Grande** — onnisciente,
ironico, affettuoso, già presente dentro i log. Le note sono la **rubrica del Master** (regolamento
tradotto in mondo, false etimologie, statistiche di tavolo).
Tono **comico-epico con retrogusto**: si ride del gioco avido e caotico del gruppo, ma i morti e le
maledizioni sono veri. Confezione: **fanzine di GdR dei primi anni '90**.
Qui `build_epub.sh` fallisce apposta se manca il PNG di copertina.

## Apocalisse — *Terre Desolate / Codici del Silenzio* · `apocalisse/`

GDR **Apocalisse** (Acheron): Italia/Europa ~20 anni dopo i sette sigilli.
**Polifonia** — l'Appestato che scrive per non dimenticare, Ronan di Kimmeria risorto, la Veggente
cieca — con una **cornice**: l'**Archivista**, che ordina e dichiara i buchi ma **non migliora** e
non narra. Note in personaggio. Tono freddo e amaro: «ogni sopravvivenza si paga». Tesi di fondo:
**nessuna potenza è dalla parte degli uomini**.
Confezione: **codice ritrovato**, apertura Nota del Curatore → Indice → Linea temporale.
C'è una **staffetta voluta** (Appestato → Ronan, log a-975): passaggio netto di codice, non
confusione di voci. Copertine JPEG q95 tarate perché ogni EPUB resti ≤ 3 MB.

## Heroes Unlimited — *Dossier Scavengers* · `heroes/`

**Heroes Unlimited** (Palladium), ambientazione del tavolo: Londra dopo l'**evento zero** del 2012,
le radiazioni Z, la droga **Connettore Z**. Gli Scavengers sono **antieroi mercenari** che cacciano
HERO per taglia.
**Cornice + deposizioni**: l'**Analista** di Scotland Yard scrive un referto freddo e burocratico,
i soggetti depongono in prima persona, parziali e auto-assolutori. Il nero-comico nasce dallo
**scarto** fra la lingua del fascicolo e l'osceno dei fatti — mai dalla battuta. Tono **50/50**
beffa ↔ brutalità. **Ironia portante:** il fascicolo è troppo pulito perché **Darko** è la talpa che
lo cura dall'interno.
Confezione: fascicolo riservato dei **Cavalieri della Corona**, con `[OMISSIS]`.
**Densità sopra il target**: lo stile-dossier è compressivo, non gonfiare per arrivare a 50 pagine.
Allegato `racconti/schede_dei_soggetti.md` (profili in-fiction degli otto soggetti).

---

## Dove si somigliano, dove no

| | voce | schema | confezione |
|---|---|---|---|
| Brancalonia | narratore unico | capitoli | paperback 1982 |
| dnd-jr | narratore unico | volumi | fanzine anni '90 |
| Korvaal | polifonia pura | volumi | Urania '82 |
| Apocalisse | polifonia + cornice | volumi | codice ritrovato |
| Dark Heresy | cornice + deposizioni | volumi | atti dell'Ordo |
| Heroes | cornice + deposizioni | volumi | fascicolo di polizia |

Quando una collana tace su qualcosa, guarda la collana più vicina in questa tabella — ma **dillo**,
non importarlo di nascosto.
