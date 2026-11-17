# Il patto — chi pensa, chi verifica, chi firma

Questa skill fa scrivere prosa a un modello linguistico. Il rischio non è che scriva male: è che
scriva **abbastanza bene da essere firmata senza essere stata pensata**. Il patto serve a impedirlo.

È la traduzione operativa del **Triangolo del Pensare-Con** (*Pensare con LLM — the right way*,
cap. 2): tre posture da presidiare insieme, non in sequenza, più una soglia firmata in anticipo che
decide dove grava la pressione.

| vertice | chi | domanda | se cede |
|---|---|---|---|
| **Intento** | l'autore, prima del prompt | che cosa cerco, e che cosa ne farò? | «vediamo cosa esce»: ci si ritrova a difendere un racconto che non si è scelto |
| **Avversario** | la verifica costruita **prima** di leggere l'output | che cosa potrebbe non funzionare, e come lo scopro? | «suona bene»: il testo convince per ragioni che non c'entrano con la sua qualità |
| **Editore** | l'autore, con nome e cognome | posso rispondere di questo testo? | «lo mando in build»: il libro è formalmente nostro e sostanzialmente di nessuno |

**La decisione resta dell'autore.** Il modello è materia di lavoro: propone, completa, contraddice
se glielo si chiede. Non decide la voce, non decide il canone, non firma.

---

## 1. Intento — una riga, all'apertura

Ogni comando comincia così, prima di qualunque lettura di file o proposta:

> **Intento:** voglio *[esplorare · chiudere · verificare · correggere]* **[oggetto]**
> per **[volume / destinazione]**; l'output sarà **[bozza da riscrivere · testo definitivo · referto]**.
> **Riuscito se:** *[criterio osservabile]*.

Se l'utente l'ha già detto, riformulalo in quella riga e fattelo confermare. Se non l'ha detto,
proponi la riga e chiedi. **Non partire con «vediamo cosa esce».**

Due distinzioni che cambiano tutto il resto della sessione:

- **esplorare ≠ chiudere.** Leggere un log per vedere che cosa c'è è esplorazione; scrivere il
  capitolo 4 è chiusura. Mescolarle produce sessioni lunghe che non portano da nessuna parte.
- **bozza ≠ definitivo.** Una bozza si riscrive a mano; un definitivo si firma. Se l'utente dice
  «definitivo», la soglia sale (vedi §4).

A metà di una sessione lunga, rileggi la riga. *Respice finem*: se la conversazione ha deviato,
dillo invece di seguirla.

## 2. Avversario — la verifica si costruisce prima

Prima della stesura, non dopo. Una volta letto, un testo plausibile ha già convinto.

**Prima di scrivere**, la bibbia del racconto contiene una sezione **«Verifiche»**:
- le **ancore di fatto** che il testo deve rispettare (eventi cardine del log, chi muore e come);
- le **ancore di canone** che rischiano di più in questo racconto (grafie, stato dei personaggi);
- l'**orizzonte di conoscenza** della voce: che cosa il narratore *non* può sapere;
- la **soglia di rinuncia** del racconto (§4).

**Dopo aver scritto**, la verifica ha tre livelli e nessuno dei tre basta da solo:
1. **gli script** — misurano quello che si misura (note, manifest, copertina, apparato);
2. **le tre passate** — redattore, correttore, revisore di stile: referti, non verdetti;
3. **la lettura dell'autore** — l'unica che conta come firma (§3).

**Il limite da dire ad alta voce.** Gli agenti di revisione sono lo stesso tipo di modello che ha
scritto il testo. Il contesto separato attenua l'indulgenza, non la elimina. Per questo:
- i referti si leggono come **materiale per l'Editore**, non come un'assoluzione: «tre passate
  pulite» non significa «testo buono»;
- il revisore di stile chiude con un **mirror-busting**: argomenta il contrario della scelta
  principale di voce o di tono, così l'autore vede l'alternativa che non ha scelto;
- se tre passate non trovano **niente** in un testo nuovo, è un segnale da guardare, non da
  festeggiare.

## 3. Editore — la firma sul testo

La firma non è formale: è la disponibilità a rispondere del libro davanti a chi lo legge — e chi
legge può essere uno dei giocatori di quel tavolo.

**Il cancello.** Prima del prompt di copertina, l'autore legge il testo **per intero** e lo firma
nel `meta.yaml` del volume (o del libro):

```yaml
firmato: "Nome Cognome, 2026-11-17"
```

`controlla_volume.py` **blocca il build** se il campo manca, come lo blocca se manca la copertina.
Il modello **non scrive mai** questo campo da sé, neanche su richiesta generica di «sistemare il
meta»: lo scrive l'autore, o lo detta lui parola per parola.

Le firme di finzione — Nanoc Orabrabli, Ozymandias il Grande, l'Analista, l'Archivista — sono
confezione. **Non sostituiscono la firma reale**: la coprono, e proprio per questo serve.

Tre pratiche che rendono la firma vera:
- **riscrivere a mano almeno un passaggio** del racconto: se nulla è stato riscritto, il testo è
  tuo nel file, non nella testa;
- saper rispondere a **«che cosa avrei scritto senza il modello?»**;
- quando un volume esce, chiedersi **che cosa si è imparato** sulla collana, non quante pagine si
  sono prodotte.

## 4. La soglia — dove grava la pressione

Il Triangolo non è equilatero. La pressione si decide **per classe di output**, in base a quanto
costa l'errore — e si decide **prima**, non quando il risultato è già sul tavolo.

| classe di output | costo dell'errore | baricentro | in pratica |
|---|---|---|---|
| prompt di copertina | basso: si rigenera | **Intento** — delega disciplinata | iterare liberamente; la verifica è guardare l'immagine |
| ritratto di un personaggio | basso: si rigenera | **Intento** | ma il soggetto viene solo dall'aspetto con le fonti, e non dev'essere scaduto |
| scheda di un personaggio | alto: è canone di dettaglio, ci si appoggiano i racconti futuri | **Editore** | ogni tratto con la fonte; scritta dopo il via dell'autore |
| referto di lettura dei log | alto: tutto ciò che segue ci si appoggia | **Avversario** | niente invenzioni, `[il log tace]`, citazioni brevi a supporto |
| bozza di capitolo | medio: si riscrive | **Intento** | esplorare varianti, ma con la riga d'intento in vista |
| racconto definitivo | alto: pubblico, letto dai giocatori | **Avversario + Editore** | pensare-con pieno: verifiche in bibbia, tre passate, firma |
| `canone_serie.md` | altissimo: si propaga a tutta la collana | **Editore** | ogni cambio di stato lo approva l'autore, riga per riga |
| fascicolo pubblicabile, sito | altissimo: online, diritti degli editori | **Editore** | `--url` solo se deciso; l'FTP lo fa l'autore |

**Soglie di rinuncia** — scritte prima, applicate senza rinegoziare a fine serata:
- **un morto che ricompare vivo** → il capitolo si butta e si riscrive dall'outline, non si
  rattoppa con una frase;
- **bloccanti del redattore in due revisioni di fila** → si torna all'outline: il problema è a
  monte della prosa;
- **una voce che non regge per due capitoli** → si rimette in discussione la scelta della voce, non
  si lima lo stile;
- **un racconto che dopo tre blocchi non ha ancora il suo baricentro** → ci si ferma e si torna al
  co-design;
- **un fascicolo con un difetto intercambiabile** → si butta la stesura (`fase-fascicolo.md`).

Se in un ciclo intero **non si è mai buttato niente**, l'Avversario è collassato: riapri il patto.

## 5. Il patto delle quattro decisioni, per queste collane

Vale per tutte e sei. Una collana può stringerlo nel suo `CLAUDE.md`, non allargarlo.

**Cosa si delega al modello** — come materia prima, mai come decisione:
lettura e referto dei log · proposte di racconto · proposte di schede dei personaggi e soggetti dei ritratti · outline da discutere · stesura a blocchi ·
le tre passate di revisione · prompt di copertina · build, controlli, rigenerazione del sito.

**Cosa non si delega mai:**
la scelta del racconto e della voce · le decisioni di canone e lo stato dei personaggi · come si
sanano le discrepanze · che cosa resta in un capitolo e che cosa si taglia · la firma sul testo ·
che cosa va online · il caricamento FTP.

**Come si verifica:** §2 — verifiche scritte in bibbia prima della stesura, script, tre passate con
mirror-busting, lettura integrale dell'autore.

**Chi firma:** l'autore, con nome e cognome nel `meta.yaml`. Non «il club», non il narratore di
finzione.

**Con quale soglia ci si ferma:** §4.

**Il patto si riapre** a ogni arco concluso, o prima se scatta una soglia. È un patto, non una
policy: regge perché si rinegozia.

---

## La domanda da tenere a portata di mano

> **Quale vertice sto presidiando adesso?**

Se il modello non sa rispondere — perché sta scrivendo senza una riga d'intento, verificando senza
verifiche scritte prima, o andando verso il build senza firma — si ferma e lo dice.
