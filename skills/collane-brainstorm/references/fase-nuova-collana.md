# Fase `nuova-collana` — progettare una collana da zero

Una collana non è una cartella: è **una voce, una confezione e un tono** applicati a una campagna.
Lo scheletro lo crea lo script in un secondo; il lavoro vero è decidere quelle tre cose prima, con
l'autore, in modo che ogni racconto futuro abbia un metro.

## Le sei collane come modelli

Prima delle domande, tieni davanti la tabella di `giochi.md`: ogni collana nuova si costruisce **per
somiglianza e per differenza** con una di quelle. Dillo apertamente: «è come Dark Heresy, ma la
cornice è un diario invece di un verbale».

| modello di voce | collane | quando sceglierlo |
|---|---|---|
| **narratore-unico** | Brancalonia, dnd-jr | il tavolo ha un narratore naturale (il Master, un bardo); comico o picaresco; le note sono una rubrica |
| **polifonia** | Korvaal, Apocalisse | personaggi forti, ciascuno con un mondo interiore; tono tragico; ogni racconto cambia testimone |
| **cornice-deposizioni** | Dark Heresy, Heroes | il gruppo è corale; c'è un'istituzione che indaga o archivia; il comico o l'orrore nascono dallo scarto fra referto e fatti |

## Le domande, nell'ordine

Una per volta quando la risposta cambia le successive. Proponi sempre un'opzione motivata.

1. **Gioco e log.** Che gioco, che editore, quanti log ci sono già, che campagna è (one-shot,
   campagna lunga, gruppo a rotazione)?
2. **Modello di voce.** Uno dei tre qui sopra.
3. **Chi racconta, esattamente.** Il nome e la postura del narratore (o della cornice), che cosa può
   sapere, che cosa non sa. È la decisione che detta tutte le altre.
4. **Le note a piè di pagina.** In personaggio, rubrica, glosse dell'archivista, timbri d'ufficio?
5. **La confezione.** Il finto oggetto editoriale da un'altra epoca o da dentro il mondo: tascabile,
   fanzine, dossier, codice, diario sequestrato, bollettino parrocchiale… Deve essere **riconoscibile
   in copertina**.
6. **Tono e tesi.** Il tono con il suo baricentro (es. «50/50 beffa e brutalità») e la tesi in una
   riga: quello che ogni racconto, alla fine, deve far sentire.
7. **Apertura dei volumi.** La tripletta che apre ogni volume nella confezione (es. «Nota
   dell'Inquisitore → Indice → Cronologia»).
8. **Stile delle copertine e dei ritratti.** Il **contenitore** comune (supporto, palette con *un*
   accento, luce, grana, tipografia, lista *Avoid*) in inglese, per il generatore d'immagini. Per i
   ritratti dei personaggi lo stesso contenitore, con il segnaposto `{SOGGETTO}`.
9. **Nomi.** Titolo della collana, chiave (minuscole e trattini), cartella, byline dei volumi, slug
   e prefisso per il sito.
10. **Lunghezza.** 25 pagine per racconto è il default del club; una confezione compressiva (dossier)
    può dichiarare che la densità batte il target.

## La scheda

Quando le risposte ci sono, scrivi la scheda JSON nella scratchpad della sessione e **mostrala**:

```json
{
  "chiave": "notti-roma",
  "progetto": "vampiri",
  "collana": "Le notti di Roma",
  "gioco": "Vampiri: la Masquerade",
  "editore": "Renegade Game Studios",
  "editore_url": "",
  "modello_voce": "polifonia",
  "voce": "Ogni racconto è il diario di un Fratello diverso, scritto per non dimenticare chi era.",
  "note": "Glosse in personaggio, a margine del diario.",
  "confezione": "diari sequestrati dalla Seconda Inquisizione",
  "apertura": "Nota dell'Inquisitore → Indice → Cronologia delle notti",
  "tono": "gotico freddo, con la pietà che arriva sempre tardi",
  "tesi": "la Bestia vince sempre: è solo questione di notti",
  "firma_narrativa": "a cura dell'Inquisitore",
  "stile_copertina": "a leather-bound diary on an evidence table, wax seal, one crimson accent",
  "stile_ritratto": "Faded sepia daguerreotype pinned in an evidence ledger: {SOGGETTO}. Avoid: colour photography, visible fangs, gore.",
  "slug_sito": "notti-di-roma",
  "prefisso_sito": "roma-",
  "pagine": 25,
  "occhiello": "Una riga di presentazione per il sito."
}
```

Obbligatori: tutti tranne `editore`, `editore_url`, `pagine`, `occhiello`, `stile_copertina`.

## Lo scheletro

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nuova_collana.py . scheda.json --prova
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nuova_collana.py . scheda.json
```

Crea, nella cartella indicata: `CLAUDE.md` della collana, il brief `PROMPT_nuovi_racconti.md`, il
canone vuoto, il colofone, `epub.css`, `_stile.md` dei ritratti, il modello di volume
(`volumi/_TEMPLATE/`), `log/COPERTURA.txt` e `build_epub.sh`, che **si rifiuta di costruire senza
copertina**. Registra la collana in `collane.local.json` della radice: gli script lo leggono insieme
al registro del plugin, che resta generico.

Lo script non sovrascrive mai. Se la cartella esiste e non è vuota, si ferma.

## Dopo lo scheletro

- **Il canone del gioco** in `canone_serie.md` (ambientazione, istituzioni, nomi): lo scheletro lo
  lascia vuoto apposta, va scritto con l'autore.
- **Il colofone**: il modello è quello del club; adattalo alla collana.
- **`epub.css`**: la confezione si vede anche nell'impaginazione (intestazioni, timbri, rubriche).
- **I volumi**: un volume nuovo si crea copiando `volumi/_TEMPLATE/`; ricordati di aggiungerlo a
  `ordine_volumi` in `collane.local.json`, perché anagrafe e sentinella del sito seguono quell'ordine.
- **Il sito**: la collana entra nelle pagine di lettura solo quando c'è il primo volume, con una voce
  nel registro `COLLANE` di `sito/build_leggi.py`.
- Poi si lavora come per le altre: `/brainstormclub:collana <chiave> <fase>`.
