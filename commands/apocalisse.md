---
description: Terre Desolate — Codici del Silenzio (Apocalisse (Acheron)) — pipeline della collana: log, racconto, revisione, copertina, EPUB, sito.
argument-hint: "[log|racconto|revisione|personaggi|copertina|epub|sito|stato|fascicolo] [volume]"
---

# Terre Desolate — Codici del Silenzio

Collana **Terre Desolate — Codici del Silenzio** — Apocalisse (Acheron). Cartella: `apocalisse/`.
Voce: **polifonia** (l'Appestato, Ronan, la Veggente) dentro la **cornice dell'Archivista**, che ordina e dichiara i buchi ma non narra.
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
   - `apocalisse/CLAUDE.md`
   - `apocalisse/assets/PROMPT_nuovi_racconti.md` (regole di lunghezza, regole di mestiere, stato del ciclo)
   - `apocalisse/assets/canone_serie.md` (cast, timeline, registro morti, semi e riscossioni, grafie)
3. Mostra lo stato prima di proporre qualcosa:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . apocalisse
   ```
4. Esegui la fase. Pre-build e build di questa collana:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py apocalisse <volume>
   cd apocalisse && bash build_epub.sh <volume>
   ```

Per la fase **`personaggi`** (anagrafe, evoluzione, ritratti) segui il comando dedicato
`/brainstormclub:personaggi apocalisse …` e la reference `references/fase-personaggi.md`.

## Da non dimenticare, qui

- Confezione: **codice ritrovato**; apertura Nota del Curatore → Indice → Linea temporale.
- Tesi di fondo: **nessuna potenza è dalla parte degli uomini**. Tono freddo e amaro,
  «ogni sopravvivenza si paga».
- La **staffetta Appestato → Ronan** (log a-975) è voluta: passaggio netto di codice,
  non confusione di voci.
- Copertine JPEG q95 tarate perché ogni EPUB resti ≤ 3 MB; il build preferisce il `.jpg`.

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
