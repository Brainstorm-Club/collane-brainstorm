---
description: Lavora su una collana qualunque, comprese quelle create in locale con /brainstormclub:nuova-collana — stessa pipeline dei comandi dedicati.
argument-hint: "<collana> [log|racconto|revisione|personaggi|copertina|epub|sito|stato] [volume]"
---

# Collana

**Richiesta:** $ARGUMENTS

Il primo argomento è la **chiave** della collana: una delle sei del club (`brancalonia`, `korvaal`,
`dark-heresy`, `dnd-jr`, `apocalisse`, `heroes`) o una creata in locale e registrata in
`collane.local.json` della radice. Se manca, mostra lo stato di tutte e chiedi.

0. **Intento in una riga**, confermato prima di tutto: voglio *[esplorare · chiudere · verificare ·
   correggere]* **[oggetto]** per **[volume]**; l'output sarà **[bozza · definitivo · referto]**;
   riuscito se *[criterio]*.
1. Trova la collana nel registro (`${CLAUDE_PLUGIN_ROOT}/scripts/collane.json` più
   `collane.local.json`): cartella, voce, confezione.
2. Leggi la skill **`collane-brainstorm`**: `SKILL.md`, poi solo la reference della fase; la prima
   volta anche `references/patto.md` e `references/regole-ferme.md`.
3. Leggi `<cartella>/CLAUDE.md`, il brief e `assets/canone_serie.md`: hanno l'ultima parola.
4. Stato: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . <collana>` e
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/log_nuovi.py . <collana>`.
5. Esegui la fase. Pre-build: `controlla_volume.py <cartella> <volume>`; build: `bash build_epub.sh <volume>`
   dalla cartella della collana.

## Sempre

- Niente copertina senza firma, niente EPUB senza copertina; `firmato:` lo scrive solo l'autore.
- Se muore nel log, muore nel racconto. Co-design prima della prosa. Tre revisori dopo ogni modifica.
- Il sito si carica via FTP a mano. Quello che resta fuori diventa una issue.
