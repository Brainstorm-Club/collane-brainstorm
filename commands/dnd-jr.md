---
description: Tiro Salvezza — D&D 5ª ed. nel Vecchio Mondo di Warhammer, tavolo under 16. Pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|personaggi|copertina|epub|sito|stato|fascicolo] [volume]"
---

# Tiro Salvezza

Collana **Tiro Salvezza** — D&D 5ª ed. nel Vecchio Mondo di Warhammer (tavolo under 16). Cartella: `dnd-jr/`.
Voce: **narratore unico**: il Master, **Ozymandias il Grande** — ironico e affettuoso; le note sono la sua **rubrica**.
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
   - `dnd-jr/CLAUDE.md`
   - `dnd-jr/assets/PROMPT_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `dnd-jr/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . dnd-jr
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py dnd-jr <volume>
   cd dnd-jr && bash build_epub.sh <volume>
   ```

Per la fase **`personaggi`** (anagrafe, evoluzione, ritratti) segui il comando dedicato
`/personaggi dnd-jr …` e la reference `references/fase-personaggi.md`.

## Da non dimenticare, qui

- Confezione: **fanzine di GdR dei primi anni '90**; apertura Editoriale → Sommario → Linea temporale.
- Tono comico-epico **con retrogusto**: si ride, ma i morti e le maledizioni sono veri.
- `build_epub.sh` **fallisce apposta** se manca `copertine/<vol>.png`.
- Pagina dell'autore per volume: innesto nuovo su `assets/autore.md`.

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
