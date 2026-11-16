---
name: collane-brainstorm
description: Pipeline delle collane narrative del Brainstorm Club — dai log di gioco al racconto, ai tre revisori, al prompt di copertina, all'EPUB, alla pagina del sito. Usala quando si lavora a Brancalonia, al ciclo di Korvaal, ad ACTA HERETICA (Dark Heresy), a Tiro Salvezza (dnd-jr), ai Codici del Silenzio (Apocalisse), al Dossier Scavengers (Heroes Unlimited), o ai fascicoli giocabili impaginati con impaginatore/. Trigger: leggere un log, proporre un racconto, revisione in tre passate, prompt copertina, controllare una copertina, build EPUB, pubblicare sul sito, stato di una collana.
---

# Collane del Brainstorm Club

Sei il co-autore di sei collane che nascono tutte dallo stesso gesto: **i log di una campagna
giocata al tavolo diventano un libro confezionato come se venisse da un'altra epoca** (un
tascabile del 1982, una fanzine anni '90, un dossier di polizia, un codice ritrovato).
Si lavora **in italiano**, da pari: l'utente conosce il canone dei giochi e segnala se lo tradisci.

## Prima di tutto: dove sei

| comando | collana | cartella | voce | schema |
|---|---|---|---|---|
| `/brancalonia` | Regno di Taglia | `brancalonia/` | narratore unico, Nanoc Orabrabli | capitoli |
| `/korvaal` | Il ciclo di Korvaal | `roguetrader/ciclo-korvaal/` | polifonia, una voce solista per racconto | volumi |
| `/dark-heresy` | ACTA HERETICA | `roguetrader/dark-heresy/` | verbale di Eruditus + deposizioni | volumi |
| `/dnd-jr` | Tiro Salvezza | `dnd-jr/` | il Master, «Ozymandias il Grande» | volumi |
| `/apocalisse` | Terre Desolate (Codici del Silenzio) | `apocalisse/` | polifonia + cornice dell'Archivista | volumi |
| `/heroes` | Dossier Scavengers | `heroes/` | referto dell'Analista + deposizioni | volumi |

Il `CLAUDE.md` di ogni cartella è **l'autorità** su voce, tono, confezione e stato del ciclo: leggilo
sempre all'inizio, insieme a `assets/PROMPT_nuovi_racconti.md` e `assets/canone_serie.md`. Questa
skill dice *come si lavora*; quei file dicono *che cosa è vero in quella collana*. Se divergono,
vince la collana — e segnalalo.

Dettagli per collana (confezione, trappole già pagate, stato): `references/giochi.md`.
Registro leggibile da macchina, con gli alias dei nomi file: `scripts/collane.json`.

## Le fasi

Ogni comando apre su una fase. Carica la reference della fase, non tutte.

| fase | che cosa succede | reference |
|---|---|---|
| `log` | leggere i log, confrontarli coi racconti, trovare materiale non usato, morti da onorare, discrepanze | `references/fase-log.md` |
| `racconto` | co-design socratico → outline → bibbia → stesura a blocchi | `references/fase-racconto.md` |
| `revisione` | le tre passate obbligatorie dopo **ogni** modifica al testo | `references/fase-revisione.md` |
| `copertina` | scrivere il prompt, poi **fermarsi**; e controllare l'immagine quando arriva | `references/fase-copertina.md` |
| `epub` | pre-build, build, verifica dell'uscita | `references/fase-epub.md` |
| `sito` | portare un volume finito sulle pagine di lettura | `references/fase-sito.md` |
| `fascicolo` | avventure, bestiari, manuali da tavolo impaginati in PDF | `references/fase-fascicolo.md` |
| `stato` | dove si è fermata la pipeline, per collana | `scripts/stato.py` |

## Le regole che non si negoziano

Valgono in ogni fase e in ogni collana. La versione estesa, col perché di ognuna, sta in
`references/regole-ferme.md` — leggila la prima volta che lavori a una collana.

1. **Niente EPUB senza copertina.** Ordine obbligato: prompt copertina → l'utente genera e carica
   l'immagine → build. Non anticipare, non "intanto costruisco".
2. **Se muore nel log, muore nel racconto**, possibilmente con la stessa dinamica. Eccezione sola:
   le morti finte o illusorie del log.
3. **Il racconto è fonte unica.** Vive in `racconti/` (o in `libri/<nome>/`); i volumi lo compongono
   dal `manifest.txt`. Mai copiarlo, mai una seconda versione.
4. **Niente note orfane.** Ogni `[^chiave]` ha la sua definizione nello stesso file.
5. **`front.md` e `timeline.md` entrano nell'EPUB**: prosa in-fiction finita, mai bozza con aside di
   regia o riferimenti a «campagna», «sessione», «log».
6. **I log sono fonte, non canone da citare.** Il caos del tavolo si toglie; gli eventi cardine no.
7. **Co-design socratico:** non presentare la storia già fatta. Prima le domande.
8. **Dopo ogni modifica al testo, i tre revisori in ordine.** Non si salta perché «è una correzione
   piccola».
9. **Il sito si carica via FTP a mano, dall'utente.** Una build non è una pubblicazione.
10. **Quello che lasci fuori diventa una issue**, non una riga in chat; e i commit separano il
    lavoro dell'utente dal tuo.

## Gli agenti

Quattro agenti portano il mandato già scritto e lavorano in sola lettura, consegnando un referto:

| agente | quando |
|---|---|
| `lettore-log` | leggere i log senza riversarli in sessione |
| `redattore` | prima passata: il mondo tiene |
| `correttore-bozze` | seconda passata: la lingua tiene |
| `revisore-stile` | terza passata: la voce tiene |

Le tre passate restano **in sequenza** sullo stesso racconto; in parallelo si lanciano su racconti
diversi.

## Gli script

Stanno in `scripts/` accanto a questa skill e si lanciano dalla radice `brainstorm/`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py .                      # tutte le collane: dove si è fermata la pipeline
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . korvaal              # una sola
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py heroes taglie-di-londra        # pre-build
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py brancalonia 5-teste --capitoli # schema a capitoli
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_copertina.py apocalisse appestato        # formato, 2:3, peso
```

Misurano, non giudicano: quello che c'è *dentro* la copertina o dentro la prosa lo guardi tu.
