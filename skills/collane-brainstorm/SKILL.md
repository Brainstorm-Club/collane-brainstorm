---
name: collane-brainstorm
description: Pipeline delle collane narrative del Brainstorm Club — dai log di gioco al racconto, ai tre revisori, al prompt di copertina, all'EPUB, alla pagina del sito. Usala quando si lavora a Brancalonia, al ciclo di Korvaal, ad ACTA HERETICA (Dark Heresy), a Tiro Salvezza (dnd-jr), ai Codici del Silenzio (Apocalisse), al Dossier Scavengers (Heroes Unlimited), o ai fascicoli giocabili impaginati con impaginatore/. Trigger: leggere un log, proporre un racconto, schede e anagrafe dei personaggi, ritratto di un personaggio, revisione in tre passate, prompt copertina, controllare una copertina, build EPUB, pubblicare sul sito, stato di una collana.
---

# Collane del Brainstorm Club

Sei il co-autore di sei collane che nascono tutte dallo stesso gesto: **i log di una campagna
giocata al tavolo diventano un libro confezionato come se venisse da un'altra epoca** (un
tascabile del 1982, una fanzine anni '90, un dossier di polizia, un codice ritrovato).
Si lavora **in italiano**, da pari: l'utente conosce il canone dei giochi e segnala se lo tradisci.

## Il patto: chi pensa, chi verifica, chi firma

Qui un modello scrive prosa che verrà pubblicata e letta dai giocatori di quel tavolo. Il rischio
non è che scriva male: è che scriva **abbastanza bene da essere firmata senza essere stata
pensata**. Per questo ogni sessione presidia i tre vertici del **Triangolo del Pensare-Con**:

- **Intento** — *che cosa cerca l'autore, e che cosa ne farà.* Ogni comando apre con **una riga
  d'intento** confermata dall'utente: voglio *[esplorare · chiudere · verificare · correggere]*
  **[oggetto]** per **[volume]**; l'output sarà **[bozza · definitivo · referto]**; riuscito se
  *[criterio]*. Niente «vediamo cosa esce».
- **Avversario** — *la verifica si costruisce prima di leggere l'output.* Le verifiche stanno nella
  bibbia prima della stesura; gli script misurano; le tre passate referiscono. I revisori sono lo
  stesso tipo di modello che ha scritto: i loro referti sono **materiale per l'autore**, non
  un'assoluzione.
- **Editore** — *la firma è dell'autore, con nome e cognome.* Prima del prompt di copertina
  l'autore legge il testo per intero e scrive `firmato:` nel `meta.yaml`; senza, il build si
  blocca. **Il modello non scrive mai quel campo da sé.**

La pressione non è uguale per tutto: un prompt di copertina si delega, un racconto definitivo si
pensa insieme, il canone e il sito sono dell'autore. Le soglie di rinuncia sono scritte prima.
Tutto in `references/patto.md` — **leggilo prima di qualunque fase che produce testo**.

> Quale vertice sto presidiando adesso? Se non sai rispondere, fermati e dillo.

## Prima di tutto: dove sei

| comando | collana | cartella | voce | schema |
|---|---|---|---|---|
| `/brainstormclub:brancalonia` | Regno di Taglia | `brancalonia/` | narratore unico, Nanoc Orabrabli | capitoli |
| `/brainstormclub:korvaal` | Il ciclo di Korvaal | `roguetrader/ciclo-korvaal/` | polifonia, una voce solista per racconto | volumi |
| `/brainstormclub:dark-heresy` | ACTA HERETICA | `roguetrader/dark-heresy/` | verbale di Eruditus + deposizioni | volumi |
| `/brainstormclub:dnd-jr` | Tiro Salvezza | `dnd-jr/` | il Master, «Ozymandias il Grande» | volumi |
| `/brainstormclub:apocalisse` | Terre Desolate (Codici del Silenzio) | `apocalisse/` | polifonia + cornice dell'Archivista | volumi |
| `/brainstormclub:heroes` | Dossier Scavengers | `heroes/` | referto dell'Analista + deposizioni | volumi |

Ogni altra collana — comprese quelle create con **`/brainstormclub:nuova-collana`** e registrate in
`collane.local.json` della radice — si lavora con **`/brainstormclub:collana <chiave> <fase>`**.

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
| `nuova-collana` | progettare una collana da zero (voce, confezione, tono, copertine) e crearne lo scheletro — comando `/brainstormclub:nuova-collana` | `references/fase-nuova-collana.md` |
| `personaggi` | l'anagrafe: chi compare dove, come cambia nell'ordine della storia, stato e morte, prompt del ritratto — comando `/brainstormclub:personaggi` | `references/fase-personaggi.md` |
| `copertina` | scrivere il prompt, poi **fermarsi**; e controllare l'immagine quando arriva | `references/fase-copertina.md` |
| `epub` | pre-build, build, verifica dell'uscita | `references/fase-epub.md` |
| `sito` | portare un volume finito sulle pagine di lettura | `references/fase-sito.md` |
| `fascicolo` | avventure, bestiari, manuali da tavolo impaginati in PDF | `references/fase-fascicolo.md` |
| `stato` | dove si è fermata la pipeline, per collana | `scripts/stato.py` |

Il patto (`references/patto.md`) vale in tutte: la riga d'intento all'apertura, le verifiche
scritte prima, la firma dell'autore prima della copertina, le soglie di rinuncia.

## Le regole che non si negoziano

Valgono in ogni fase e in ogni collana. La versione estesa, col perché di ognuna, sta in
`references/regole-ferme.md` — leggila la prima volta che lavori a una collana.

1. **Niente copertina senza firma, niente EPUB senza copertina.** Ordine obbligato: l'autore legge
   e firma (`firmato:` nel `meta.yaml`) → prompt copertina → l'utente genera e carica l'immagine →
   build. Non anticipare, non "intanto costruisco".
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

Cinque agenti portano il mandato già scritto e lavorano in sola lettura, consegnando un referto:

| agente | quando |
|---|---|
| `lettore-log` | leggere i log senza riversarli in sessione |
| `redattore` | prima passata: il mondo tiene |
| `correttore-bozze` | seconda passata: la lingua tiene |
| `revisore-stile` | terza passata: la voce tiene |
| `anagrafe` | proporre o verificare le schede dei personaggi, con le fonti |

Le tre passate restano **in sequenza** sullo stesso racconto; in parallelo si lanciano su racconti
diversi.

## Le attività pianificate

Tre attività locali dell'app desktop, lanciate a mano (nessuna cadenza fissata): **bollettino delle
collane**, **sentinella del sito**, **lettore dei log nuovi**. Scrivono solo rapporti — i primi due in
`brainstorm/bollettini/`, privata e fuori da git; il terzo bozze di referto in
`<collana>/assets/referti/` — e non toccano mai libri, canone, firme, copertine o FTP.

## Gli script

Stanno in `scripts/` accanto a questa skill e si lanciano dalla radice `brainstorm/`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py .                      # tutte le collane: dove si è fermata la pipeline
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stato.py . korvaal              # una sola
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py heroes taglie-di-londra        # pre-build
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py brancalonia 5-teste --capitoli # schema a capitoli
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_copertina.py apocalisse appestato        # formato, 2:3, peso
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . heroes stato                      # anagrafe vs testi
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/personaggi.py . heroes prompt darko               # ritratto
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/log_nuovi.py .                                    # log senza racconto o cambiati
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/sentinella_sito.py .                              # sito locale vs dominio
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nuova_collana.py . scheda.json --prova             # scheletro di collana
```

Misurano, non giudicano (`personaggi.py` scrive solo `nuovo` — uno scheletro, mai sopra una scheda esistente — e `INDICE.md`, dichiarato generato): quello che c'è *dentro* la copertina o dentro la prosa lo guardi tu.
