# Fase `racconto` — dal log alla prosa

Dieci passi, nell'ordine. I primi tre si fanno **con l'utente**, non per l'utente.

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
semi e riscossioni, vincoli di canone, morti da onorare. È il file che permette a un'altra sessione
di riprendere il lavoro senza rileggere tutto.

## 5. Stesura a blocchi

Il testo in `racconti/<nome>.md`: capitoli come `##`, stacchi di scena `---`, note a piè di pagina
`[^chiave]` definite **nello stesso file**. Per Brancalonia: capitoli numerati
`libri/<nome>/NN_nome.md`.

Si scrive a blocchi e si mostra a blocchi. Un racconto intero riversato tutto insieme non si può
correggere.

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

## 9. Confezione

Poi si passa al prompt copertina (`fase-copertina.md`) e **ci si ferma**.

## 10. Volumi

Aggiungi il racconto ai `manifest.txt` pertinenti con un **prefisso-note** univoco nel volume
(2–3 lettere), aggiorna `front.md` (indice) e `timeline.md`, e solo allora builda.

## Errori che abbiamo già pagato

- note di wellbeing o helpline dentro la narrativa: è finzione, si resta in mondo;
- gergo da manuale del gioco nella prosa;
- elementi da tavolo (iniziativa, tiri, punti) fuori posto;
- neologismi forzati, false friend, *lost in translation* dall'inglese del manuale;
- un morto che torna vivo perché il racconto successivo non è stato ricontrollato.
