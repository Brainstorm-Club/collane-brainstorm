---
description: Dossier Scavengers — Heroes Unlimited (Palladium), Londra dopo l'«evento zero». Pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|personaggi|copertina|epub|sito|stato|fascicolo] [volume]"
---

# Dossier Scavengers

Collana **Dossier Scavengers** — Heroes Unlimited (Palladium) — Londra dopo l'«evento zero». Cartella: `heroes/`.
Voce: **cornice + deposizioni**: il referto freddo dell'**Analista** e le deposizioni parziali dei soggetti; nero-comico **di scarto**, 50/50 beffa ↔ brutalità.
Schema: volumi — `racconti/<nome>.md` composti da `volumi/<vol>/manifest.txt`.

**Richiesta:** $ARGUMENTS
(se è vuota, chiedi quale fase serve dopo aver mostrato lo stato)

## Come procedere

0. **Intento in una riga, prima di tutto.** Riformula la richiesta così e fattela confermare:
   > voglio *[esplorare · chiudere · verificare · correggere]* **[oggetto]** per **[volume]**;
   > l'output sarà **[bozza · definitivo · referto]**; riuscito se *[criterio osservabile]*.

   Se la richiesta è troppo vaga per scriverla, chiedi — non partire da «vediamo cosa esce».
1. Usa la skill **`collane-brainstorm`**: leggine `SKILL.md`, poi **solo** la reference della fase
   richiesta (`references/fase-<fase>.md`). La prima volta in una sessione, anche
   `references/patto.md` (chi pensa, chi verifica, chi firma) e `references/regole-ferme.md`.
2. Leggi il contesto della collana, che ha l'ultima parola su voce, tono, confezione e stato:
   - `heroes/CLAUDE.md`
   - `heroes/assets/PROMPT_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `heroes/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . heroes
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py heroes <volume>
   cd heroes && bash build_epub.sh <volume>
   ```

Per la fase **`personaggi`** (anagrafe, evoluzione, ritratti) segui il comando dedicato
`/personaggi heroes …` e la reference `references/fase-personaggi.md`.

## Da non dimenticare, qui

- Confezione: **fascicolo riservato** dei Cavalieri della Corona, con `[OMISSIS]`.
- **Ironia portante:** il fascicolo è troppo pulito perché **Darko** è la talpa che lo cura.
- Antieroi: non redimerli e non moralizzare — **contabilizzare**.
- **Densità sopra il target**: lo stile-dossier comprime, non gonfiare per arrivare a 50 pagine.
- ⚠ `front.md` e `timeline.md` entrano nell'EPUB: prosa finita, mai bozza con aside di regia.

## Sempre

- **Niente copertina senza firma, niente EPUB senza copertina**: l'autore legge e scrive
  `firmato:` nel `meta.yaml` → prompt → l'utente carica l'immagine → build. Il campo `firmato:`
  non lo scrivi mai tu.
- **I referti dei revisori sono materiale per l'autore**, non un'assoluzione.
- **Se muore nel log, muore nel racconto.**
- **Co-design socratico**: prima le domande, poi l'outline da approvare, poi la prosa.
- **Tre revisori dopo ogni modifica** (Redattore → Bozze → Stile).
- **Il sito si carica via FTP a mano**: una build non è una pubblicazione.
- Quello che resta fuori diventa una **issue**, non una riga in chat.
