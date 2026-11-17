# Le regole ferme, col perché

Non sono una teoria: sono il residuo di errori pagati. Ognuna dice anche **come si applica**.

## 0. Il patto: intento, verifica, firma

Ogni sessione apre con una riga d'intento confermata; la verifica si scrive prima della stesura;
il testo lo firma l'autore (`firmato:` nel `meta.yaml`) prima della copertina, e il modello non
scrive mai quel campo. Le soglie di rinuncia si applicano senza rinegoziarle a fine serata.
*Perché:* un modello scrive abbastanza bene da essere firmato senza essere stato pensato; la firma
in anticipo toglie la giustificazione a posteriori. Tutto in `patto.md`.

## 1. Niente EPUB senza copertina

Ordine obbligato: **prompt copertina → l'utente genera e carica l'immagine → build**.
*Perché:* l'utente cura la confezione (finta collana, fanzine, dossier) e vuole l'EPUB solo quando è
completo; un EPUB senza cover è output sprecato e fuori standard. In dnd-jr lo script fallisce
apposta se il PNG manca.
*Come:* a racconto finito scrivi il prompt, poi **fermati e dillo**. Non "intanto costruisco".

## 2. Se muore nel log, muore nel racconto

Stessa dinamica dove si può. Vale **retroattivamente**. Unica eccezione: le morti che nel log sono
finte o illusorie.
*Come:* ogni volta che tocchi un racconto, controlla a catena i successivi in cronologia e i volumi
che li contengono. Il registro morti sta in `assets/canone_serie.md` e si aggiorna subito.

## 3. Il racconto è fonte unica

Vive una volta sola in `racconti/<nome>.md` (o `libri/<nome>/` per Brancalonia); i volumi lo
compongono dal `manifest.txt`, **mai copiandolo**. Lo stesso racconto sta in omnibus e volume
tematico senza duplicarsi.
*Come:* una modifica si fa in un posto solo e si propaga ricostruendo **tutti** i volumi che lo
contengono.

## 4. Niente note orfane

Ogni `[^chiave]` richiamata è definita nello stesso file. Il build fallisce il check.
*Come:* `python3 scripts/controlla_volume.py <progetto> <volume>` dopo ogni modifica. I
prefissi-note (2–3 lettere, univoci nel volume) esistono perché i `[^1]` di racconti diversi non
collidano dentro lo stesso EPUB.

## 5. `front.md` e `timeline.md` entrano nell'EPUB

Sono **prosa in-fiction finita**, non bozze. Mai aside di regia (`[L'Analista apre…]`, `[Tesi…]`,
`[BOZZA…]`) né riferimenti meta («campagna», «sessione», «racconto scritto»): finirebbero nel libro
pubblicato. `[OMISSIS]` sì, è in-fiction.

## 6. I log sono fonte, non canone da citare

Il caos del tavolo si toglie, gli eventi cardine restano. Le voci del canone ricostruite dai log
sono marcate `[da chiarire dai log]`: chiedi conferma prima di darle per assodate.

## 7. Co-design socratico

Non presentare la storia già fatta: prima le domande (spunto, voce, tono, vincoli), poi l'outline
da approvare, poi la stesura. L'utente conosce il canone dei giochi e lo segnala se lo tradisci:
trattalo da pari, contraddicilo quando serve.

## 8. I tre revisori, sempre in ordine

Redattore → Correttore di bozze → Revisore di stile, **dopo ogni modifica al testo**. Vedi
`fase-revisione.md`.

## 9. Il sito si carica via FTP, a mano, dall'utente

Una correzione committata o costruita **non è una correzione pubblicata**. È già successo due volte
che una cosa fosse vera nel repository e falsa per chi apriva il sito.
*Come:* alla fine, elenca i file da caricare. E verifica sul dominio solo **dopo** che l'utente ha
caricato.

## 10. Il lavoro rimandato diventa una issue

Un caso che hai deciso di non coprire, un difetto trovato di passaggio e non corretto, una modifica
ferma in un worktree: **apri una issue nel repo giusto prima di chiudere**. Non basta dirlo in chat
né nel corpo della PR — un elenco in chat sparisce con la sessione.
*Come:* prima misurare, poi scrivere (la issue porta il numero, non l'impressione); dire **perché** è
rimasta fuori; se hai già la correzione in mano, incollarla.

## 11. Commit separati

Controlla `git status` e `git diff` **prima** di ogni `git add`: non trascinare nel tuo commit il
lavoro in corso dell'utente. Se un file mescola contenuti suoi e tue modifiche di infrastruttura,
spacchetta in due commit con scope chiaro. Il force-push lo lascia all'utente.

## 12. Restare in mondo

Niente note di wellbeing o helpline dentro la narrativa, niente gergo da manuale nella prosa,
niente elementi da tavolo fuori posto. È finzione: si resta dentro la confezione.

## 13. I fascicoli stanno in piedi da soli

Vale per avventure, bestiari e manuali: referenze legittime sono solo i **manuali ufficiali con la
pagina** e i **luoghi del canone**. Vedi `fase-fascicolo.md`.
