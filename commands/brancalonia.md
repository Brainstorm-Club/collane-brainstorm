---
description: Regno di Taglia (Brancalonia (Acheron Games)) — pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|copertina|epub|sito|stato|fascicolo] [volume]"
---

# Regno di Taglia

Collana **Regno di Taglia** — Brancalonia (Acheron Games). Cartella: `brancalonia/`.
Voce: narratore unico: **Nanoc Orabrabli**, picaresco alla Pratchett.
Schema: capitoli — un libro è un racconto solo, in `libri/<nome>/` (epigrafe + `NN_*.md`), senza manifest.

**Richiesta:** $ARGUMENTS
(se è vuota, chiedi quale fase serve dopo aver mostrato lo stato)

## Come procedere

1. Usa la skill **`collane-brainstorm`**: leggine `SKILL.md`, poi **solo** la reference della fase
   richiesta (`references/fase-<fase>.md`). La prima volta in una sessione, anche
   `references/regole-ferme.md`.
2. Leggi il contesto della collana, che ha l'ultima parola su voce, tono, confezione e stato:
   - `brancalonia/CLAUDE.md`
   - `brancalonia/assets/prompt_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `brancalonia/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . brancalonia
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py brancalonia <libro> --capitoli
   cd brancalonia && bash build_epub.sh <libro>
   ```

## Da non dimenticare, qui

- Le copertine si chiamano `copertine/prompt-libro-<nome>.md` → `<nome>.png`.
- Sul sito gli slug sono per esteso (`5-teste` → `le-cinque-teste`) e alcuni EPUB hanno nome
  diverso dalla cartella (`le_cinque_teste.epub`): la mappa è in `scripts/collane.json`.
- La **pagina dell'autore** cambia a ogni libro (innesto nuovo su `assets/autore.md`).
- In `brancalonia/avventure/` ci sono i **fascicoli giocabili**: è un lavoro diverso,
  fase `fascicolo`, con i suoi quattro principi.

## Sempre

- **Niente EPUB senza copertina**: prompt → l'utente carica l'immagine → build.
- **Se muore nel log, muore nel racconto.**
- **Co-design socratico**: prima le domande, poi l'outline da approvare, poi la prosa.
- **Tre revisori dopo ogni modifica** (Redattore → Bozze → Stile).
- **Il sito si carica via FTP a mano**: una build non è una pubblicazione.
- Quello che resta fuori diventa una **issue**, non una riga in chat.
