---
description: Il ciclo di Korvaal — Rogue Trader (Warhammer 40.000). Pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|personaggi|copertina|epub|sito|stato|fascicolo] [volume]"
---

# Il ciclo di Korvaal

Collana **Il ciclo di Korvaal** — Rogue Trader (Warhammer 40.000). Cartella: `roguetrader/ciclo-korvaal/`.
Voce: **polifonia**: una voce solista in prima persona per racconto, note in personaggio, tono agrodolce «ogni vittoria si paga».
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
   - `roguetrader/ciclo-korvaal/CLAUDE.md`
   - `roguetrader/ciclo-korvaal/assets/PROMPT_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `roguetrader/ciclo-korvaal/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . korvaal
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py roguetrader/ciclo-korvaal <volume>
   cd roguetrader/ciclo-korvaal && bash build_epub.sh <volume>
   ```

Per la fase **`personaggi`** (anagrafe, evoluzione, ritratti) segui il comando dedicato
`/personaggi korvaal …` e la reference `references/fase-personaggi.md`.

## Da non dimenticare, qui

- Confezione: falsa collana **FANTAFLOTTA**, tascabile Urania 1982.
- I volumi sono tematici ma la storia è una sola: il filo cronologico si legge dalla
  **Timeline** di `assets/canone_serie.md`, ed è quello che il sito usa per prev/next.
- Il ciclo è già stato riscritto end-to-end dai log con la **regola dura delle morti**:
  prima di toccare un racconto, leggi che cosa è già stato deciso nel canone.
- L'omnibus ha l'EPUB ma **non** la pagina web.

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
