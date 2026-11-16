---
description: ACTA HERETICA (Dark Heresy — Settore Calixis (Warhammer 40.000)) — pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|copertina|epub|sito|stato|fascicolo] [volume]"
---

# ACTA HERETICA

Collana **ACTA HERETICA** — Dark Heresy — Settore Calixis (Warhammer 40.000). Cartella: `roguetrader/dark-heresy/`.
Voce: **cornice unica**: il verbale del sapiente **Eruditus** in terza persona + **deposizioni** degli accoliti in blockquote; grimdark investigativo, da referto.
Schema: volumi — `racconti/<nome>.md` composti da `volumi/<vol>/manifest.txt`.

**Richiesta:** $ARGUMENTS
(se è vuota, chiedi quale fase serve dopo aver mostrato lo stato)

## Come procedere

1. Usa la skill **`collane-brainstorm`**: leggine `SKILL.md`, poi **solo** la reference della fase
   richiesta (`references/fase-<fase>.md`). La prima volta in una sessione, anche
   `references/regole-ferme.md`.
2. Leggi il contesto della collana, che ha l'ultima parola su voce, tono, confezione e stato:
   - `roguetrader/dark-heresy/CLAUDE.md`
   - `roguetrader/dark-heresy/assets/PROMPT_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `roguetrader/dark-heresy/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . dark-heresy
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py roguetrader/dark-heresy <volume>
   cd roguetrader/dark-heresy && bash build_epub.sh <volume>
   ```

## Da non dimenticare, qui

- Confezione: **dossier proibito dell'Ordo**.
- Arco **Haarlock** e **specchio in 13 frammenti**: posizionare ogni nuovo racconto nell'arco
  prima dell'outline. Grafie canoniche in `assets/canone_serie.md`.
- Qui i prompt di copertina portano il nome del **racconto**, non del volume: non concludere
  che manchino perché non si chiamano `prompt-copertina-<vol>.md`.

## Sempre

- **Niente EPUB senza copertina**: prompt → l'utente carica l'immagine → build.
- **Se muore nel log, muore nel racconto.**
- **Co-design socratico**: prima le domande, poi l'outline da approvare, poi la prosa.
- **Tre revisori dopo ogni modifica** (Redattore → Bozze → Stile).
- **Il sito si carica via FTP a mano**: una build non è una pubblicazione.
- Quello che resta fuori diventa una **issue**, non una riga in chat.
