# Fase `fascicolo` — avventure, bestiari, manuali da tavolo

Altra cosa dai racconti. Qui non si narra una campagna giocata: si scrive **materiale giocabile**
che un tavolo qualunque deve poter usare. Vive in `brancalonia/avventure/<nome>/` (e in cartelle
analoghe per gli altri giochi) e si impagina in PDF con `impaginatore/`.

## Le due regole di struttura

1. **Ogni cartella si porta i propri asset**: markdown, `build.sh`, `copertina.jpg` e il suo
   `copertina.md` (il prompt), le illustrazioni con `illustrazioni.md`, `valutazione.md`. Niente
   cartelle trasversali: quella strada è già stata aperta e chiusa.
2. **Il generatore resta fuori**: l'impaginazione sta in `impaginatore/` ed è condivisa fra i
   giochi. Non duplicarla, non metterci dentro roba di un gioco solo.

## I quattro principi di scrittura

### 1. Il fascicolo sta in piedi da solo

Chi ha in mano **solo questo fascicolo più i manuali ufficiali** deve poterlo giocare. Un bestiario
o un manuale di oggetti dev'essere per giunta **estraneo alle avventure che ne usano il materiale**.

Sono errori — tutti già commessi:
- prima persona plurale che racconta una nostra serata;
- rimandi ad altri nostri documenti («vedi il bestiario»);
- nostri luoghi o PNG inventati dati per noti fuori dal documento che li ha creati;
- un tratto che rimanda a un dato che sta altrove («il nome della sirena» — quale sirena?);
- confronti che legano tutto a una regione;
- ganci che consegnano la trama di un'altra avventura;
- eserghi di copertina firmati da personaggi che nel fascicolo non compaiono;
- un colofone che accredita luoghi non più citati, o che tace quelli usati.

Referenze legittime: **solo i manuali ufficiali con la pagina** e i **luoghi del canone**.

### 2. Ogni difetto discende dalla sua virtù

Il difetto di un oggetto, il limite di un PNG, il costo di una scena non sono punizioni
appiccicate: sono la stessa cosa vista da dietro. Gli stivali fanno atterrare in piedi, e quindi
fanno atterrare *in posa*. **Criterio per buttare una stesura:** se il difetto si potesse scambiare
con quello di un altro pezzo, è scritto male.

### 3. Il prezzo si paga in società, non in punti ferita

Reputazione, opzioni, dignità: i danni si curano. Le vittorie costano, e il conto arriva dopo.

### 4. Non chiudere mai una porta per fare una predica

I giocatori sono canaglie e non è detto che siano gentili. La gentilezza è la strada **gratis** e
più corta, **mai l'unica**: ogni nodo vuole almeno due chiavi, e la via storta si paga con risorse
concrete (tempo, danni, Malefatte, PNG che chiudono le porte, oggetti rotti per sempre). Nelle note
al Condottiero non dare per scontata la reazione emotiva del tavolo: il Condottiero **alza il
prezzo, non chiude la porta**, e non commenta i sentimenti dei giocatori.

In revisione: elenca i nodi bloccanti e verifica che ognuno abbia la sua via da canaglia **col
prezzo scritto**. Compreso il caso «la risorsa chiave non arriva»: serve un piano B.

## Impaginare

```bash
impaginatore/impagina.sh documento.md --titolo "Titolo" --tema brancalonia [--tipo avventura] [--web]
```

Produce `<nome>.pdf` (copertina carbone, da schermo) e `<nome>-stampa.pdf` (copertina bianca); con
`--web` anche la pagina autocontenuta che usa **lo stesso lettore dei libri del sito**.
Temi disponibili: `brancalonia`, `apocalisse`, `dnd`. `--tipo avventura` aggiunge riquadri del
narratore, testo da leggere, dialoghi, statblock, mappe, e il salto pagina a ogni `h1`.

## Pubblicabile o interno: lo decide `--url`

| il documento dichiara… | uscita | che cos'è |
|---|---|---|
| `--url https://…` | `<nome>-web.html` | **pubblicabile**: canonical, Open Graph, `index, follow` |
| niente `--url` | `<nome>-interno.html` | **copia di servizio del club**: `noindex`, avviso in testa, non va online |

Serve a rendere impossibile un equivoco già successo: il *Grimorio di Bassa Lega* completo riassume
58 incantesimi dei manuali dell'editore e **al club resta, online non va**; pubblicabile è solo la
variante `-regole`. In caso di dubbio su un documento nuovo: se non ha un `--url`, **chiedi**.

Sul sito i fascicoli stanno in `sito/avventure/<slug>-web.html` + i PDF + `-cover.jpg`, e
mantengono gli URL di sempre: sono indicizzati, non si spostano. I teaser `.mp4` **non** sono
incorporati: vanno caricati via FTP accanto alla pagina, o il riquadro resta vuoto.
