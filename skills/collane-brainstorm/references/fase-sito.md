# Fase `sito` — portare un volume finito online

## La cosa da sapere prima di tutte

**Il dominio si aggiorna via FTP, a mano, dall'utente.** Non è GitHub Pages. Il lavoro di una
sessione arriva fino ai **file pronti in locale**; il caricamento lo fa l'utente.

Quindi: **una build non è una pubblicazione**, e un file corretto nel repository può restare
sbagliato per chi apre il sito. Dirlo sempre, alla fine: che cosa va caricato.

## Dove vanno le cose

```
sito/libri/<prefisso><slug>.epub     l'EPUB pubblicato      (korvaal-origini.epub, hu-il-panfilo.epub)
sito/libri/<prefisso><slug>.jpg      la copertina full-size
sito/leggi/<collana>/                le pagine di lettura, generate
sito/index.html                      la home: sezione #libri
```

I prefissi e gli slug non coincidono sempre col nome della cartella sorgente: `5-teste` diventa
`le-cinque-teste`, `ronan-di-kimmeria` diventa `apoc-ronan`. La mappa sta in `scripts/collane.json`
(campo `alias`) e, in forma autorevole, nel registro `COLLANE` in cima a `sito/build_leggi.py`.

## I passi

1. **Copia** `epub/<vol>.epub` e la copertina in `sito/libri/` con il nome pubblicato.
2. **Rigenera** le pagine di lettura:
   ```bash
   python3 sito/build_leggi.py <collana>     # una collana
   python3 sito/build_leggi.py               # tutte + llms.txt
   ```
   Il sito **non contiene testo originale**: lo rigenera dalle stesse fonti degli EPUB. Non
   ricopiare mai un racconto dentro `sito/`.
3. **Guarda gli avvisi** di `build_leggi.py`: quando dice che un racconto non è in Timeline (o
   viceversa) sta segnalando un buco nel canone, non un rumore.
4. **Home**: la card del libro nella sezione `#libri`, con «Leggi online» come link primario e
   l'EPUB retrocesso. I **pesi non si scrivono a mano**: si rileggono dal disco a ogni
   rigenerazione. L'ordine dei libri è **cronologico della storia**, non di pubblicazione.
5. **Sinossi senza spoiler**: sono ganci, non rivelazioni. Chi legge può essere un giocatore.
6. **Verifica prima di dire «fatto»**:
   - HTML ben formato, **una sola `h1`**, nessun salto di livello, nessuna ancora morta, JSON-LD che
     si parsifica, link locali che risolvono;
   - le pagine in un browser, in **entrambi i temi** e a **larghezza di telefono**;
   - dopo che l'utente ha caricato: le URL della sitemap rispondono, il lettore è servito, e le
     pagine che non devono esistere danno **404**.
7. **Dire all'utente che cosa caricare**: l'elenco dei file nuovi o cambiati.

## Vincoli che non si rompono

- **Il lettore è uno solo**: `leggi/lettore.css` + `leggi/lettore.js` + `lettore.py`. Li usano sia i
  libri sia i fascicoli dell'impaginatore. Se tocchi il lettore, rigenera **e confronta**: i libri
  devono restare identici byte per byte quando il cambiamento non li riguardava.
- **Una sola entità del club** nel JSON-LD, richiamata per `@id` dalle altre pagine. Mai ricopiarne
  i dati.
- `title` ≤ 75 caratteri, `description` ≤ 165, canonical su ogni pagina, `og:url` uguale al
  canonical, nessun duplicato di title o description, sitemap allineata alle pagine vere.
- **Contrasti**: `--primary` è il rosso dei **fondi**; per il testo rosso c'è `--accento`. Se
  aggiungi testo colorato, misura.

## Non va online

- gli `-interno.html` e i loro PDF (p.es. il Grimorio completo);
- le pagine degli omnibus;
- qualunque cosa riassuma o riproduca il contenuto dei manuali degli editori.

In caso di dubbio su un documento nuovo: **se non ha un `--url`, non è pubblicabile. Chiedi.**
