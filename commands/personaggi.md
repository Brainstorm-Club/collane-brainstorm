---
description: Anagrafe dei personaggi di una collana — chi compare dove, come cambia libro dopo libro, stato e morte, e il prompt per il ritratto.
argument-hint: "<collana> [censisci|aggiorna|verifica|ritratto|stato] [personaggio]"
---

# Anagrafe dei personaggi

**Richiesta:** $ARGUMENTS

Collane: `brancalonia` · `korvaal` · `dark-heresy` · `dnd-jr` · `apocalisse` · `heroes`.
Le schede stanno in `<progetto>/assets/personaggi/`, una per personaggio, nell'ordine della storia.

## Come procedere

0. **Intento in una riga**, confermato prima di tutto. Quale dei quattro lavori?
   - **censisci** — costruire l'anagrafe di una collana (o di un gruppo di personaggi) da zero;
   - **aggiorna** — allineare le schede dopo un racconto nuovo o un cambio di canone;
   - **verifica** — controllare un racconto contro le schede esistenti;
   - **ritratto** — preparare il prompt per l'immagine di un personaggio, in un momento preciso
     della storia.

   Se manca la collana o il lavoro, chiedi.
1. Leggi la skill **`collane-brainstorm`**: `SKILL.md`, poi `references/fase-personaggi.md`. La prima
   volta in sessione anche `references/patto.md`.
2. Leggi `<progetto>/CLAUDE.md` e `<progetto>/assets/canone_serie.md`: il canone resta l'autorità su
   stato e grafie.
3. Mostra dove sta l'anagrafe:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> ordine
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . <collana> stato
   ```
4. Esegui il lavoro:
   - **censisci / aggiorna** — per i personaggi senza scheda:
     `personaggi.py . <collana> nuovo "Nome" "alias1, alias2"` crea lo scheletro con le righe
     d'Evoluzione già al loro posto. Poi i `?` si riempiono leggendo: su più personaggi, delega
     all'agente **`anagrafe`** (uno per personaggio o per piccolo gruppo, in parallelo). Mostra
     all'utente le proposte, e scrivi le schede **solo dopo il suo via**.
   - **verifica** — agente `anagrafe` sul racconto indicato, contro le schede: solo le differenze.
   - **ritratto** — se manca `assets/personaggi/_stile.md`, proponilo ricavandolo dal prompt di
     copertina della collana (stesso stile, stessa palette, stesso *Avoid*) con il segnaposto
     `{SOGGETTO}`. Poi:
     `personaggi.py . <collana> prompt <scheda>`. Se è scaduto, aggiorna prima il soggetto.
     L'immagine la genera l'utente.
5. Rigenera l'indice: `personaggi.py . <collana> indice`.
6. Chiudi con `stato`, e riporta quello che resta aperto.

## Sempre

- **Ogni tratto ha la sua fonte** `file:riga`. Dove il testo tace: `[il testo tace]`.
- **L'ordine è quello della storia**, non di pubblicazione: i prequel vengono prima.
- **Se muore, muore**: dopo `morto_in` ogni apparizione è ricordo, flashback, cadavere — o errore.
- **Il canone è l'autorità**: se una scheda lo contraddice, segnala la divergenza, non sistemarla da
  una parte sola.
- **Niente dati del tavolo**: niente giocatori, niente statistiche.
