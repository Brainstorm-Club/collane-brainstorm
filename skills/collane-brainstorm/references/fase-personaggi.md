# Fase `personaggi` — l'anagrafe della collana

Una collana dura anni e attraversa più libri. Un personaggio cambia: si prende una cicatrice in un
libro, perde un occhio in un altro, muore nel quinto. E i prequel lo rimettono in scena **prima**
di quei cambiamenti. Ricordarselo a memoria è impossibile; ricostruirlo ogni volta rileggendo i
libri è lento e porta a errori.

L'anagrafe serve a questo: **una scheda per personaggio, che segue la cronologia della storia** e
dice com'è fatto e in che stato si trova in ogni racconto, con la fonte di ogni affermazione. Dalla
scheda nasce il **ritratto**: un prompt per generare un'immagine coerente con il personaggio *in
quel momento* della storia e con lo stile della collana.

## Dove sta

```
<progetto>/assets/personaggi/
├── _stile.md        il contenitore comune dei ritratti (uguale per tutti, come per le copertine)
├── INDICE.md        generato da personaggi.py indice — non si modifica a mano
├── darko.md         una scheda per personaggio
└── mau-kamekona.md
```

Sta nella collana, non nel plugin: è materiale di quella collana, come il canone.

**Rapporto col canone.** `assets/canone_serie.md` resta **l'autorità** su chi è vivo, chi è morto,
come si scrive un nome. L'anagrafe è il dettaglio che il canone non può portare: l'aspetto,
racconto per racconto, con le fonti. Se divergono, ha ragione il canone — e la divergenza va
segnalata, non sistemata in silenzio da una parte sola.

## La scheda

```markdown
---
nome: Truciolo
alias: Truci
ruolo: il più giovane della cricca
stato: vivo
prima_apparizione: rosaspina
morto_in:
prompt_aggiornato_a: grigione
---

# Truciolo

## Chi è
Due-quattro righe, in mondo.

## Aspetto canonico
- magro, mani sempre sporche di trucioli — `libri/rosaspina/01_il_compare_contento.md:17`
- cicatrice sulla guancia sinistra (da *Le cinque teste* in poi) — `libri/5-teste/15_la_testa_giusta.md:42`
- età: [il testo tace]

## Evoluzione
| racconto | stato | aspetto | fatti | fonte |
|---|---|---|---|---|
| rosaspina | vivo | — | entra nella cricca | `libri/rosaspina/01_…md:17` |
| 5-teste | vivo | cicatrice sulla guancia sinistra | ferito da … | `libri/5-teste/15_…md:42` |

## Prompt immagine
Valido a: grigione

```text
a skinny young carpenter's apprentice, wood shavings on his sleeves, a fresh scar on his left cheek
```
```

Regole della scheda:

- **Ogni tratto ha la sua fonte** (`file:riga`). Se il testo tace, si scrive `[il testo tace]`:
  non si inventa un colore d'occhi per riempire un prompt.
- **«Evoluzione» ha una riga per ogni racconto in cui il personaggio compare**, nell'ordine della
  storia. La colonna «aspetto» si compila **solo quando l'aspetto cambia**; altrimenti `—`.
- **`morto_in`** è il racconto in cui muore. Da lì in poi ogni sua apparizione è un ricordo, un
  flashback, un cadavere — o un errore. Vale la regola delle morti.
- **Niente dati del tavolo**: niente nomi dei giocatori, niente statistiche, niente livelli. È una
  scheda in mondo.
- **Le fonti sono i testi pubblicati**, non i log. Il log serve a sapere *che cosa è successo*; la
  scheda registra *che cosa i libri hanno detto*. Se il log e il libro divergono sull'aspetto di un
  personaggio, è una discrepanza da segnalare (`fase-log.md`), non da sanare nella scheda.

## Il ritratto

Funziona come le copertine: un **contenitore** comune a tutta la collana e un **soggetto** che
cambia da personaggio a personaggio.

`_stile.md` contiene il contenitore: un blocco ```text``` in inglese con lo stile della collana,
la luce, l'inquadratura, la lista *Avoid*, e il segnaposto **`{SOGGETTO}`**. Si ricava dal prompt
di copertina della collana, così i ritratti sembrano dello stesso libro:

| collana | ritratto coerente con la confezione |
|---|---|
| Brancalonia | illustrazione da paperback italiano 1982 |
| Korvaal | illustrazione da tascabile Urania 1982, FANTAFLOTTA |
| Dark Heresy | foto segnaletica o incisione da atti dell'Ordo |
| dnd-jr | disegno a china da fanzine anni '90 |
| Apocalisse | miniatura o xilografia da codice ritrovato |
| Heroes | foto di sorveglianza in bianco e nero, graffettata al fascicolo |

La scheda contiene solo il **soggetto**: chi è e com'è fatto, in inglese, ricavato **solo**
dall'«Aspetto canonico» valido al racconto indicato in `prompt_aggiornato_a`.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> prompt <scheda>
```

compone i due pezzi e avvisa se il ritratto è **scaduto**, cioè se l'aspetto è cambiato in un
racconto successivo a quello per cui il soggetto era stato scritto.

**Ritratti per un momento preciso.** In una collana con prequel lo stesso personaggio può servire
in due momenti diversi (Truciolo prima e dopo la cicatrice). Si scrive il soggetto per il momento
che serve, si aggiorna `prompt_aggiornato_a`, e la variante precedente — se serve tenerla — va in
un blocco a parte con il suo «Valido a:». Lo script controlla solo il primo blocco.

## Come si lavora

1. **Intento** (`patto.md` §1): *censire* una collana da zero, *aggiornare* l'anagrafe dopo un
   racconto nuovo, *verificare* un racconto contro le schede, o *preparare un ritratto*? Sono
   quattro lavori diversi.
2. **Stato:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> ordine
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> stato
   ```
   `stato` dice dove il nome compare **davvero** nei testi, quali racconti mancano nelle schede, se
   un morto ricompare, se un ritratto è scaduto, se il personaggio manca dal canone.
3. **Scheletro** per un personaggio nuovo:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> nuovo "Nome" "alias1, alias2"
   ```
   Crea la scheda con una riga di «Evoluzione» per ogni racconto in cui il nome compare, e i `?` da
   compilare. Non sovrascrive mai.
4. **Lettura**: i `?` si riempiono **leggendo i passaggi**, non deducendo. Su una collana intera
   conviene delegare all'agente **`anagrafe`**, uno per personaggio o per gruppo: torna una
   proposta di scheda con le fonti, non la scrive.
5. **L'autore approva**: l'anagrafe è canone di dettaglio, quindi il baricentro è sull'**Editore**
   (`patto.md` §4). Le schede le scrive il modello solo dopo che l'autore ha visto la proposta.
6. **Indice:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> indice
   ```
7. **Ritratto**: `prompt <scheda>`, poi lo genera l'utente. Come per la copertina, l'immagine non
   la fa il modello e non si salva al posto dell'utente.

## Quando aggiornare

- **dopo ogni racconto nuovo**, prima della firma: le schede dei personaggi che compaiono vanno
  allineate, ed è un buon controllo di coerenza in più per il redattore;
- **quando cambia il canone**: una morte, una mutilazione, un nome sanato;
- **prima di generare un ritratto**, sempre: `stato` dice se è scaduto.

## Che cosa `stato` non può vedere

Lo script cerca i nomi e gli alias **come parole intere**, con le maiuscole. Non vede un
personaggio chiamato solo «la navigatrice» o «il vecchio», e può contare un nome comune che
coincide con una parola («Lord»). Per questo gli alias si scelgono con cura, e il censimento dei
personaggi **senza nome** lo fa la lettura, non lo script.
