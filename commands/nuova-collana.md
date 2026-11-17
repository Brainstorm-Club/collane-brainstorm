---
description: Crea una collana nuova — dal gioco alla voce, alla confezione, allo stile delle copertine — con lo scheletro di cartelle, istruzioni e build pronto.
argument-hint: "[gioco o idea della collana]"
---

# Nuova collana

**Richiesta:** $ARGUMENTS

0. **Intento in una riga**, confermato: «voglio *progettare* una collana nuova da **[gioco / campagna]**;
   l'output sarà lo **scheletro della collana**; riuscito se: voce, confezione, tono e stile di
   copertina sono decisi dall'autore e la cartella costruisce».
1. Leggi la skill **`collane-brainstorm`**: `SKILL.md`, `references/fase-nuova-collana.md` (le
   domande e la scheda), `references/patto.md` e `references/giochi.md` (le sei collane esistenti
   sono i modelli da cui partire, e da cui distinguersi).
2. **Co-design socratico**, nell'ordine della reference: gioco e log → modello di voce → chi
   racconta → note → confezione → tono e tesi → apertura dei volumi → stile di copertina e ritratti →
   nome, chiave, slug del sito. **Una domanda per volta** quando la risposta cambia le successive;
   proponi sempre un'opzione motivata, guardando la collana più vicina. Le decisioni sono dell'autore.
3. Scrivi la **scheda** (JSON, campi nella reference) nella scratchpad della sessione e mostrala
   all'autore. Solo dopo il suo via:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nuova_collana.py . <scheda.json> --prova
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nuova_collana.py . <scheda.json>
   ```
   Lo script non sovrascrive mai e registra la collana in `collane.local.json` della radice.
4. **Rifinisci** a mano, con l'autore, ciò che il modello lascia generico: il canone del gioco in
   `assets/canone_serie.md`, il colofone, `assets/epub.css` per la confezione, il prompt di copertina
   del primo volume quando ci sarà.
5. Verifica: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . <chiave>`.
6. Chiudi dicendo il passo successivo: i log in `<cartella>/log/`, poi
   `/brainstormclub:collana <chiave> log`. Se la collana andrà sul sito, ricorda che la voce in
   `COLLANE` di `sito/build_leggi.py` va aggiunta a mano quando c'è il primo volume.

## Sempre

- La collana nuova **si distingue** dalle sei esistenti: dillo, se una scelta la rende una copia.
- Niente decisioni al posto dell'autore su voce, tono, confezione: sono la collana.
- Niente dati personali dei giocatori nei file della collana.
