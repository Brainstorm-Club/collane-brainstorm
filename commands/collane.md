---
description: Stato di tutte le collane del Brainstorm Club e scelta della prossima mossa.
argument-hint: "[collana] (brancalonia|korvaal|dark-heresy|dnd-jr|apocalisse|heroes)"
---

# Collane del Brainstorm Club

**Richiesta:** $ARGUMENTS

1. Mostra dove si è fermata la pipeline:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . $ARGUMENTS
   ```
   (senza argomento: tutte e sei)
2. Leggi la skill **`collane-brainstorm`** (`SKILL.md` + `references/giochi.md`) per sapere che cosa
   significa ogni stato e quale fase viene dopo.
3. Riporta per ogni collana **una riga**: dove sta e qual è la mossa successiva. Poi proponi,
   motivandola, **una** cosa da fare adesso — non un elenco di tutto il possibile.

I comandi per lavorare davvero sono uno per collana:
`/brancalonia` · `/korvaal` · `/dark-heresy` · `/dnd-jr` · `/apocalisse` · `/heroes`,
ognuno con una fase: `log`, `racconto`, `revisione`, `copertina`, `epub`, `sito`, `fascicolo`, `stato`.
Per i personaggi di una collana: `/personaggi <collana>`.

Ricorda: il sito si carica **via FTP a mano, dall'utente**. Una build non è una pubblicazione.
