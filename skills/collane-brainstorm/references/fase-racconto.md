# Fase `racconto` — dal log alla prosa

Undici passi, nell'ordine. I primi tre si fanno **con l'utente**, non per l'utente, e il nono lo
fa **solo** l'utente. Prima di cominciare: la riga d'intento (`patto.md` §1) — esplorare o chiudere?
bozza o definitivo?

## 1. Co-design socratico

Non presentare la storia già fatta. Fai le domande che servono a deciderla:

- da quale log (o quale pezzo di log) si parte, e quanto copre;
- **chi racconta** (vedi sotto): è la decisione che detta tutto il resto;
- dove sta il baricentro del tono, dentro i limiti della collana (agrodolce, comico-con-retrogusto,
  50/50 beffa-brutalità, referto freddo);
- quali vincoli di canone e quali discrepanze vanno sanate qui;
- dove va a finire: quale volume, prima o dopo quale racconto nella cronologia.

Una domanda per volta quando la risposta cambia le successive. Se hai un'opinione, dilla: l'utente
tratta da pari, non vuole un questionario.

## 2. La voce

| collana | come funziona |
|---|---|
| Brancalonia | **una sola** per tutta la collana: Nanoc Orabrabli |
| dnd-jr | **una sola**: il Master, Ozymandias il Grande; le note sono la «rubrica del Master» |
| Korvaal | **una per racconto**, prima persona, scelta fra i testimoni; le note sono in personaggio |
| Apocalisse | **una per codice**, prima persona; la cornice dell'Archivista ordina ma non narra |
| Dark Heresy | cornice **unica e ricorrente** (verbale di Eruditus, terza persona) + deposizioni in blockquote |
| Heroes | cornice dell'Analista (referto) + 1–3 deposizioni in blockquote |

La voce si sceglie **prima dell'outline**: detta ritmo, note, e soprattutto **che cosa chi racconta
può sapere**. Non mescolare voci dentro lo stesso racconto — salvo le staffette volute, che si
gestiscono come passaggio netto, dichiarato.

## 3. Outline e punti critici

Capitolo per capitolo, con i punti critici dichiarati (dove la coerenza rischia, dove il tono
rischia, dove il log è contraddittorio). **Da approvare prima di scrivere.**

## 4. Bibbia del racconto

`racconti/<nome>.bibbia.md` (o `libri/<nome>/bibbia_narrativa.md`): voce, baricentro,
semi e riscossioni, vincoli di canone, morti da onorare — e una sezione **«Verifiche»** scritta
**prima** della stesura: le ancore di fatto e di canone che il testo deve rispettare, l'orizzonte di
conoscenza della voce, la soglia di rinuncia di questo racconto. È il vertice Avversario del patto
(`patto.md` §2): la verifica costruita dopo cerca solo conferme. È il file che permette a un'altra sessione
di riprendere il lavoro senza rileggere tutto.

## 5. Stesura a blocchi

Il testo in `racconti/<nome>.md`: capitoli come `##`, stacchi di scena `---`, note a piè di pagina
`[^chiave]` definite **nello stesso file**. Per Brancalonia: capitoli numerati
`libri/<nome>/NN_nome.md`.

Si scrive a blocchi e si mostra a blocchi. Un racconto intero riversato tutto insieme non si può
correggere — e non si può firmare.

Le soglie di rinuncia valgono durante la stesura: se dopo tre blocchi il racconto non ha ancora il
suo baricentro, ci si ferma e si torna al co-design (`patto.md` §4).

## 6. Lunghezza

Ogni racconto **≥ 25 pagine**; se copre **più di 1,2 avventure**, il target sale a **50**.
Calibrazione: ~275 parole a pagina (25 pp ≈ 6.900 parole, 50 pp ≈ 13.500).

**Ma la densità batte il target.** Nel Dossier Scavengers lo stile-dossier è compressivo e gonfiare
sarebbe un errore: il numero è un ordine di grandezza, non una quota da riempire.

## 7. Le tre passate

Dopo **ogni** modifica al testo, nell'ordine: Redattore → Correttore di bozze → Revisore di stile.
Vedi `fase-revisione.md`.

## 8. Il canone si aggiorna subito

Quando il racconto cambia lo stato di qualcuno o qualcosa (morti, mutilazioni, epiteti, navi perse,
patti, catture, oggetti), **aggiorna `assets/canone_serie.md`** e verifica a catena i racconti
**cronologicamente successivi** e i volumi che li contengono.

## 8b. L'anagrafe dei personaggi

Le schede dei personaggi che compaiono nel racconto vanno allineate prima della firma
(`/brainstormclub:personaggi <collana> aggiorna`): `personaggi.py stato` dice quali righe mancano e se un morto
ricompare. È un controllo di coerenza in più, e tiene i ritratti aggiornati.

## 9. La firma dell'autore

Prima della confezione, l'autore **legge il racconto per intero** e lo fa suo: riscrive a mano
almeno un passaggio, sa dire che cosa avrebbe scritto senza il modello, risponde delle scelte.
Poi scrive `firmato: "Nome Cognome, AAAA-MM-GG"` nel `meta.yaml` del volume.

**Quel campo non lo scrivi tu**, nemmeno se ti chiedono di «sistemare il meta». Senza firma
`controlla_volume.py` blocca il build. È il vertice Editore (`patto.md` §3).

## 10. Confezione

Poi si passa al prompt copertina (`fase-copertina.md`) e **ci si ferma**.

## 11. Volumi

Aggiungi il racconto ai `manifest.txt` pertinenti con un **prefisso-note** univoco nel volume
(2–3 lettere), aggiorna `front.md` (indice) e `timeline.md`, e solo allora builda.

## Errori che abbiamo già pagato

- note di wellbeing o helpline dentro la narrativa: è finzione, si resta in mondo;
- gergo da manuale del gioco nella prosa;
- elementi da tavolo (iniziativa, tiri, punti) fuori posto;
- neologismi forzati, false friend, *lost in translation* dall'inglese del manuale;
- un morto che torna vivo perché il racconto successivo non è stato ricontrollato.
