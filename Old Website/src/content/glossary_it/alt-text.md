---
term: "Alt text (testo alternativo)"
slug: "alt-text"
definition: "L'alt text (testo alternativo) descrive le immagini per motori di ricerca e screen reader. Scopri come scrivere alt text efficaci, esempi e perché sono importanti per il SEO."
category: "SEO"
difficulty: "Beginner"
keyword: "alt text"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## Cosa è l'alt text?

L'alt text (testo alternativo) è un attributo HTML che fornisce una descrizione scritta di un'immagine. Usato dagli screen reader per utenti con disabilità visiva e dai motori di ricerca per capire cosa mostra un'immagine.

Probabilmente l'hai visto nel codice: `<img src="foto.jpg" alt="descrizione qui">`. Quella descrizione è l'alt text. Serve due audience simultaneamente. Per le persone che non possono vedere l'immagine. Sia che usino uno screen reader, abbiano una connessione lenta o l'immagine non si carichi. L'alt text dice loro cosa c'è. Per Google, è uno dei segnali primari usati per indicizzare e posizionare le immagini in Google Immagini.

L'analisi di accessibilità 2024 di WebAIM ha trovato che il 54,5 % delle immagini sul web manca di alt text. Più della metà. Questo è sia un fallimento di [accessibilità](/glossary/accessibility-content) sia un'opportunità SEO che aspetta lì per chiunque sia disposto a riempire un campo di testo.

## Perché l'alt text è importante?

L'alt text sta all'intersezione di accessibilità, [SEO](/glossary/seo) ed esperienza utente. Ignoralo, e perdi su tutti e tre i fronti.

- **Conformità di accessibilità**. Le linee guida ADA e WCAG 2.1 richiedono alt text su immagini significative. Le cause per accessibilità web sono aumentate del 300 %+ dal 2018. Non è opzionale.
- **Traffico dalla ricerca per immagini**. Google Immagini genera [traffico organico](/glossary/organic-traffic) significativo. Senza alt text, Google non può indicizzare correttamente le tue immagini, e perdi quel traffico interamente.
- **Segnali di [SEO On-Page](/glossary/on-page-seo)**. L'alt text dà a Google contesto aggiuntivo sul contenuto della tua pagina. Un articolo sulla ristrutturazione della cucina con immagini correttamente descritte rinforza la rilevanza tematica della pagina.
- **Fallback quando le immagini si rompono**. Se un'immagine non si carica (connessione lenta, URL rotta, client email che bloccano immagini), l'alt text appare al suo posto. Gli utenti capiscono ancora cosa doveva essere lì.

Ogni immagine sul tuo sito dovrebbe avere alt text. Le immagini decorative (bordi, spaziatori) ricevono un attributo alt vuoto (`alt=""`). Tutto il resto riceve una descrizione.

## Come funziona l'alt text

Scrivere alt text è semplice in concetto. Farlo bene richiede di capire cosa diversi sistemi ne hanno bisogno.

### Come lo usano gli screen reader

Quando uno screen reader incontra un'immagine, legge l'alt text ad alta voce. Se l'alt text dice "foto stock di riunione di lavoro", è quello che l'utente sente. Inutile. Se dice "5 membri del team che esaminano un report di marketing intorno a un tavolo da conferenza", l'utente capisce il contesto. Scrivi per la persona che ascolta, non per un motore di ricerca.

### Come lo usa Google

Googlebot non può "vedere" le immagini come fanno gli umani. Si affida ad alt text, testo circostante, nomi di file e dati strutturati per capire il contenuto dell'immagine. La documentazione stessa di Google afferma che l'alt text è "estremamente utile" per il ranking di Google Immagini. È uno dei segnali di [SEO immagine](/glossary/image-seo) più forti che puoi controllare.

### L'implementazione HTML

L'alt text vive nell'attributo `alt` del tag `<img>`:

`<img src="reception-studio-dentistico.jpg" alt="Reception moderna di studio dentistico con personale che accoglie un paziente">`

La maggior parte delle piattaforme CMS (WordPress, Webflow, Ghost) ha campi alt text dedicati nelle interfacce di upload immagini. Non devi modificare l'HTML direttamente.

### Cosa succede senza alt text

Se un'immagine non ha alcun attributo alt, gli screen reader potrebbero leggere il nome del file invece. Qualcosa come "IMG_4392.jpg." Inutile. Se l'attributo alt è presente ma vuoto (`alt=""`), gli screen reader saltano l'immagine completamente, che è comportamento corretto per le immagini decorative ma sbagliato per quelle significative.

## Tipi di alt text

Non ogni immagine ha bisogno dello stesso trattamento:

- **Alt text informativo**. Descrive cosa mostra l'immagine e perché è importante. Usato per foto, illustrazioni, grafici e elementi grafici che trasmettono informazione. "Grafico a barre che mostra un aumento del 40 % nel traffico organico da gennaio a giugno 2025."
- **Alt text funzionale**. Descrive cosa fa un'immagine cliccabile. Usato per pulsanti, icone e immagini linkate. "Pulsante di ricerca" o "Scarica report PDF."
- **Alt text decorativo (vuoto)**. Usato per immagini puramente decorative che non aggiungono informazioni. Imposta `alt=""` così gli screen reader le saltano. Pattern di sfondo, linee di divisione e icone decorative cadono qui.
- **Alt text complesso**. Usato per grafici, diagrammi e infografiche che contengono dati densi. L'alt text fornisce un riassunto, e una descrizione più lunga va in un attributo `longdesc` o testo vicino.

Azzeccare il tipo conta. Sovra-descrivere immagini decorative ingombra l'esperienza dello screen reader. Sotto-descrivere immagini informative perde sia valore di accessibilità che SEO.

## Esempi di alt text

**Esempio 1: La pagina menu di un ristorante**
Alt text cattivo: "cibo" o "foto del piatto" o nessun alt text. Alt text buono: "Salmone alla griglia con verdure arrosto e salsa al burro e limone servito su un piatto bianco." La versione descrittiva aiuta Google a posizionare l'immagine per ricerche di "salmone alla griglia" e aiuta utenti con disabilità visiva a capire l'elemento del menu.

**Esempio 2: Un annuncio immobiliare**
Cattivo: "esterno della casa." Buono: "Casa coloniale a due piani con facciata in mattoni rossi, colonne bianche e giardino curato in Via Principale 123." Una vittoria di [SEO locale](/glossary/local-seo). La descrizione dettagliata include caratteristiche della proprietà che corrispondono a ciò che gli acquirenti di case cercano in Google Immagini.

**Esempio 3: Una pagina prodotto e-commerce**
Cattivo: "immagine prodotto 1." Buono: "Scarpa da corsa Nike Air Max 90 in bianco e grigio, vista laterale." Questo alt text include marca, nome del prodotto, colore e angolazione. Esattamente ciò di cui Google ha bisogno per mostrarla nei risultati Shopping e di ricerca immagini. Usare contenuto blog pubblicato da theStacc insieme a immagini prodotto correttamente ottimizzate crea una solida base di [SEO On-Page](/glossary/on-page-seo).

## Alt text vs. testo titolo

Questi vengono confusi costantemente, ma servono a scopi completamente diversi.

| | Alt text | Testo titolo |
|---|---|---|
| **Scopo** | Descrive l'immagine per accessibilità e SEO | Fornisce info supplementari al passaggio del mouse |
| **Richiesto** | Sì (conformità WCAG) | No |
| **Impatto SEO** | Forte (segnale primario di ranking immagine) | Minimo |
| **Screen reader** | Letto ad alta voce automaticamente | A volte letto, dipende dalle impostazioni |
| **Visibilità** | Mostrato quando l'immagine non si carica | Mostrato come tooltip al passaggio del mouse |

L'alt text è obbligatorio. Il testo titolo è opzionale e principalmente cosmetico. Concentra il tuo sforzo sull'alt text.

## Best practice per l'alt text

- **Sii specifico e conciso**. Descrivi cosa c'è nell'immagine in 125 caratteri o meno. Gli screen reader possono tagliare descrizioni più lunghe. "Golden retriever che prende un frisbee in un parco" batte "cane" ogni volta.
- **Includi parole chiave naturalmente, non forzatamente**. Se l'immagine è su una pagina di [keyword research](/glossary/keyword-research) e l'immagine mostra uno strumento di analisi parole chiave, menzionalo. Ma non riempire: "keyword research strumento parole chiave migliore keyword research SEO parole chiave" è spam.
- **Non iniziare con "immagine di" o "foto di"**. Gli screen reader già annunciano che è un'immagine. Iniziare con "immagine di" è ridondante. Salta direttamente alla descrizione.
- **Descrivi la funzione per immagini cliccabili**. Se un'immagine è un link o pulsante, l'alt text dovrebbe descrivere l'azione, non l'immagine. Un'icona di lente che attiva la ricerca dovrebbe avere `alt="Cerca"`. Non `alt="lente d'ingrandimento"`.
- **Automatizza dove possibile**. Quando si pubblica in scala, mantenere alt text coerenti diventa difficile. theStacc include alt text ottimizzati in ogni articolo che pubblica, quindi le immagini sono accessibili e pronte per il SEO dal giorno uno.

## Domande frequenti

### Quanto dovrebbe essere lungo l'alt text?

Mantieni sotto i 125 caratteri. La maggior parte degli screen reader taglia l'alt text a quella lunghezza. Per immagini complesse come infografiche, fornisci un breve riassunto in alt text e aggiungi una descrizione più lunga nel contenuto della pagina circostante.

### L'alt text influenza i ranking di Google?

Sì. L'alt text è un fattore di ranking confermato per Google Immagini e fornisce contesto di supporto per i ranking di ricerca web. La documentazione di Search Central di Google raccomanda esplicitamente di scrivere alt text descrittivo per il [SEO On-Page](/glossary/on-page-seo).

### Ogni immagine dovrebbe avere alt text?

Ogni immagine significativa ha bisogno di alt text. Le immagini decorative (spaziatori, pattern di sfondo, abbellimenti visivi) dovrebbero avere attributi alt vuoti (`alt=""`) così gli screen reader le saltano. La domanda chiave: questa immagine trasmette informazione? Se sì, descrivila.

### L'alt text può essere troppo lungo?

Sì. Alt text eccessivamente lungo è frustrante per gli utenti di screen reader e può sembrare [keyword stuffing](/glossary/keyword-stuffing) per Google. Mantieni le descrizioni focalizzate. Se un'immagine ha bisogno di un paragrafo di spiegazione, mettilo nel testo del corpo vicino all'immagine. Non nell'attributo alt.

---

Vuoi ogni post di blog pubblicato con alt text appropriato, [tag intestazione](/glossary/heading-tags) e SEO on-page integrato? theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. Automaticamente. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: Best practice SEO immagini](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM: Guida al testo alternativo](https://webaim.org/techniques/alttext/)
- [WebAIM: The WebAIM Million (Report annuale di accessibilità)](https://webaim.org/projects/million/)
- [W3C: Requisiti immagine WCAG 2.1](https://www.w3.org/WAI/tutorials/images/)
- [Moz: Guida al SEO immagine](https://moz.com/learn/seo/image-seo)
