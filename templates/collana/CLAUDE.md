# {{COLLANA}} ({{GIOCO}}) — istruzioni di progetto

{{OCCHIELLO}}

Racconti ricavati dai log di gioco di una campagna di **{{GIOCO}}**{{EDITORE_FRASE}}, confezionati come
**{{CONFEZIONE}}**. Si lavora in **italiano**. Trattami da pari su game design e mestiere: conosco il
canone del gioco e di serie e lo segnalo se lo tradisci.

## Voce

**Modello:** {{MODELLO_VOCE}}.
{{VOCE}}

**Note a piè di pagina:** {{NOTE}}

**Tono:** {{TONO}}
**Tesi di fondo:** {{TESI}}

## Contesto da caricare sempre

@assets/PROMPT_nuovi_racconti.md
@assets/canone_serie.md

## Struttura del progetto

Un **racconto** vive **una volta sola** in `racconti/`; i **volumi** lo compongono via `manifest.txt`.

```
{{CARTELLA}}/
├── assets/       PROMPT_nuovi_racconti.md · canone_serie.md · colophon.md · epub.css · personaggi/
├── copertine/    <vol>.jpg|.png · prompt-copertina-<vol>.md
├── epub/         <vol>.epub (output del build)
├── log/          log di gioco — fonte, non canone · COPERTURA.txt
├── racconti/     <nome>.md + <nome>.bibbia.md
├── volumi/       _TEMPLATE/ (modello, il build lo salta) · <vol>/ meta.yaml front.md timeline.md manifest.txt
└── build_epub.sh
```

## Workflow

Segue il plugin **brainstormclub** (`/brainstormclub:collana {{CHIAVE}} <fase>`): riga d'intento →
lettura dei log → co-design socratico → outline approvato → bibbia con «Verifiche» → stesura a
blocchi → tre revisori (Redattore → Correttore di bozze → Revisore di stile) → anagrafe dei
personaggi → **firma dell'autore** (`firmato:` nel meta.yaml) → prompt copertina → l'autore carica
l'immagine → build → sito.

## Regole ferme

- **Solo EPUB + Markdown.**
- **Niente EPUB senza copertina, niente copertina senza firma.**
- **Se muore nel log, muore nel racconto.**
- **Racconto = fonte unica.** **Niente note orfane.**
- **Confezione:** ogni volume si apre con **{{APERTURA}}** e si chiude col colofone
  (`assets/colophon.md`, aggiunto dal build). `front.md` e `timeline.md` entrano nell'EPUB: prosa
  in-fiction finita, mai bozza.
- Niente elementi da tavolo fuori posto e niente note di wellbeing dentro la narrativa.
- Quando un racconto cambia lo stato di qualcuno, **aggiorna `assets/canone_serie.md`**.

## Lunghezza

Ogni racconto **≥ {{PAGINE}} pagine**; se copre **> 1,2 avventure** il target raddoppia. ~275 parole
a pagina. La densità batte il target.

## Build

```bash
bash build_epub.sh <volume>
bash build_epub.sh --all
```

## Stato

Collana appena creata: nessun log, nessun racconto. Primo passo: mettere i log in `log/` e lanciare
`/brainstormclub:collana {{CHIAVE}} log`.
