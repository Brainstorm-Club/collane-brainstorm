# Fase `revisione` — le tre passate

Si fanno **dopo ogni modifica al testo**, in quest'ordine, e sono tre mestieri diversi: non
accorparle in una lettura sola, perché una lettura sola vede una cosa sola.

## 1. Redattore — tiene insieme il mondo

- **Coerenza scenica**: chi è dove, chi è entrato, chi non può essere in quella stanza.
- **Semine e riscossioni**: ogni seme piantato si riscuote o si dichiara aperto nella bibbia; ogni
  riscossione ha il suo seme.
- **Orizzonte di conoscenza**: il narratore non sa quello che sa il tavolo.
- **Geografia e sequenza**: distanze, tempi, ordine degli eventi.
- **Effetti a catena**: quello che cambia qui cambia nei racconti successivi.
- **Coerenza di serie**: contro `assets/canone_serie.md` — cast, timeline, registro morti, grafie
  canoniche, stato di navi/bande/domini.
- **Regola delle morti**: chi muore nel log muore qui, con la stessa dinamica.

## 2. Correttore di bozze — tiene insieme la lingua

Refusi, accordi, tempi verbali, punteggiatura dei dialoghi; **false friend** e *lost in
translation* dall'inglese dei manuali; **niente neologismi forzati**; grafie canoniche dei nomi;
note a piè di pagina: ogni `[^chiave]` richiamata è definita nello stesso file e viceversa.

Controllo meccanico disponibile:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_volume.py <progetto> <volume>` (note orfane, note mai richiamate,
prefissi che collidono).

## 3. Revisore di stile — tiene insieme la voce

Qui cambia per collana, ed è la passata che non si può automatizzare:

| collana | che cosa si misura |
|---|---|
| Brancalonia | ritmo alla Pratchett, resa delle note, dosaggio delle battute, picaresco che non diventa farsa |
| dnd-jr | voce del Master: ironia affettuosa, aside di regia, note-rubrica in mondo, «si ride ma il conto è vero» |
| Korvaal | tenuta della voce solista scelta, freddezza contabile, note in personaggio, «ogni vittoria si paga» |
| Apocalisse | voce del testimone, note in personaggio, sottotesto dantesco/apocalittico, «ogni sopravvivenza si paga» |
| Dark Heresy | referto freddo del verbale contro il calore delle deposizioni; l'orrore è la macchina imperiale |
| Heroes | 50/50 beffa-brutalità, comico **di scarto** (lingua del fascicolo contro fatti osceni), understatement finale |

## Che cosa consegna una revisione

Non «ho revisionato». Un elenco di **interventi fatti** e di **cose trovate e non corrette** con il
perché. Le seconde, se restano aperte, diventano una issue — non una riga in chat che sparisce con
la sessione.

## Delegare ai tre agenti

Il plugin porta un agente per passata: **`redattore`**, **`correttore-bozze`**, **`revisore-stile`**.
Hanno il mandato già scritto e strumenti di sola lettura (il correttore può lanciare lo script di
controllo), così non riscrivono il testo per conto loro.

L'ordine resta quello: il redattore prima, perché un refuso dentro una scena che va tagliata è
lavoro buttato; lo stile per ultimo, perché giudica il testo definitivo. **Non lanciarli in
parallelo sullo stesso racconto**: leggerebbero versioni diverse.

In parallelo si lanciano su **racconti diversi** — uno per racconto, o per coppia di documenti —
dando a ciascuno l'elenco esplicito di che cosa è violazione e che cosa no. Il consolidamento dei
referti lo fai tu: si leggono, non si inoltrano.

## Quando il testo è lungo

Si possono mandare **revisori in parallelo**, uno per racconto o per coppia di documenti, dando a
ciascuno l'elenco esplicito di che cosa è violazione e che cosa no. È il modo che ha funzionato sui
fascicoli autonomi. Il consolidamento però lo fai tu: i referti si leggono, non si inoltrano.
