---
title: "Dofollow vs nofollow: differenze, strategie ed esempi pratici"
description: "Guida completa su dofollow vs nofollow: come funzionano, quando usarli, come bilanciare il profilo di link e gli errori da evitare. Aggiornato giugno 2026."
slug: "dofollow-vs-nofollow"
keyword: "dofollow vs nofollow"
author: "Siddharth Gangal"
date: "2026-06-08"
category: "SEO Tips"
image: "/blogs-preview-images/dofollow-vs-nofollow.webp"
---

Ogni link su internet rientra in una di due categorie. I link dofollow passano autorità di ranking. I link nofollow dicono a Google di non contare il link come un voto.

Capire la differenza tra dofollow e nofollow determina come costruisci backlink, strutturi i link interni e fai audit del tuo profilo. Se sbagli, perdi mesi a inseguire link che non muovono le classifiche. O peggio, attivi una penalità di Google con un profilo di link innaturale.

L'89,4% di tutti i backlink tra i primi 110.000 siti web sono dofollow. Il restante 10,6% è nofollow. Ma un profilo di link sano ha bisogno di entrambi i tipi. Google si aspetta un mix naturale.

Abbiamo pubblicato oltre 3.500 articoli SEO in più di 70 settori. La strategia di link è parte di ogni campagna. Questa guida copre tutto quello che devi sapere sui link dofollow e nofollow, incluso l'aggiornamento del 2019 che ha cambiato il modo in cui funziona nofollow.

Ecco cosa imparerai:

- La differenza esatta tra link dofollow e nofollow
- Come Google ha trasformato nofollow da direttiva a "hint" nel 2019
- Quando usare `rel="nofollow"`, `rel="sponsored"` e `rel="ugc"`
- Come controllare lo stato di un link in pochi secondi
- Il rapporto ideale tra dofollow e nofollow per un profilo naturale
- Errori comuni che attivano le penalità di Google

![Confronto tra link dofollow e nofollow e impatto sulla SEO](/images/blog/dofollow-vs-nofollow-comparison.webp)

---

## Cosa sono i link Dofollow?

Un link dofollow è un link HTML standard che passa link equity (anche chiamato "link juice" o PageRank) da una pagina all'altra. Non esiste un attributo `rel="dofollow"` in HTML. "Dofollow" è uno shorthand dell'industria per indicare un link a cui non è applicato l'attributo nofollow.

Ecco come appare un link dofollow in HTML:

```html
<a href="https://example.com">Anchor Text</a>
```

Nessun attributo speciale necessario. Ogni link è dofollow di default.

Quando Google scansiona un link dofollow, succedono 3 cose:

1. Google segue il link verso la pagina di destinazione
2. Google passa una porzione dell'autorità della pagina sorgente alla destinazione
3. Google usa il link come segnale di ranking per la pagina di destinazione

I link dofollow sono il fondamento dell'originale algoritmo PageRank di Google. Più link dofollow puntano a una pagina da fonti autorevoli, più quella pagina tende a posizionarsi. [Siti con profili di backlink forti](https://ahrefs.com/blog/backlink-growth-study/) ricevono il 67% di traffico organico in più rispetto a siti con profili deboli.

Per questo il link building rimane una delle parti più importanti (e più difficili) della SEO. Il 41% dei marketer dice che costruire [backlink](/glossary/backlinks) di qualità è il compito SEO più difficile.

---

## Cosa sono i link Nofollow?

Un link nofollow include l'attributo `rel="nofollow"`. Questo attributo dice ai motori di ricerca: "Non usate questo link come segnale di ranking."

Ecco come appare un link nofollow in HTML:

```html
<a href="https://example.com" rel="nofollow">Anchor Text</a>
```

Google ha introdotto l'attributo nofollow nel 2005 per combattere lo spam nei commenti. Gli spammer inondavano commenti e forum con link per aumentare i ranking. Nofollow ha dato ai proprietari di siti un modo per linkare senza passare autorità.

### Dove compaiono naturalmente i link Nofollow

La maggior parte dei link su internet è nofollow di default su queste piattaforme:

- **Social media:** link da Facebook, X (Twitter), LinkedIn, Instagram, Pinterest e TikTok
- **Forum e community:** Reddit, Quora, Stack Overflow e la maggior parte dei forum
- **Commenti ai blog:** WordPress e la maggior parte dei CMS mettono automaticamente nofollow ai link nei commenti
- **Wikipedia:** tutti i link esterni sono nofollow
- **Comunicati stampa:** la maggior parte delle distribuzioni di comunicati stampa usa nofollow
- **Directory generate dagli utenti:** Yelp, Google Business Profile e piattaforme di recensioni

I link nofollow non aumentano direttamente i ranking. Ma servono ad altri scopi. Portano traffico referral, costruiscono brand awareness e segnalano a Google che il tuo sito ha una diversità di link naturale.

---

## Dofollow vs Nofollow: differenze chiave

La differenza si riduce a una domanda: il link passa autorità di ranking?

| Caratteristica | Dofollow | Nofollow |
|---|---|---|
| Passa link equity | Sì | No (ma Google può sovrascrivere) |
| Attributo HTML | Nessuno (comportamento di default) | `rel="nofollow"` |
| Impatto SEO diretto | Sì. Migliora i ranking | Nessun impatto diretto |
| Traffico referral | Sì | Sì |
| Crawling di Google | Sempre seguito e scansionato | Può essere o non essere scansionato |
| Visibilità del brand | Sì | Sì |
| Necessità in un profilo naturale | 60-80% dei link totali | 20-40% dei link totali |
| Rischio di over-optimization | Alto se 100% dofollow | Basso |

Il dettaglio critico che la maggior parte delle guide ignora: dal 2019, Google tratta nofollow come un "hint", non una direttiva. Google può scegliere di seguire e contare un link nofollow se i suoi algoritmi determinano che il link è rilevante e affidabile. Ne parliamo meglio nella prossima sezione.

> I link dofollow costruiscono autorità di ranking. I link nofollow costruiscono un profilo naturale. Servono entrambi.

---

## L'aggiornamento Google del 2019: Nofollow diventa un hint

Il 10 settembre 2019, Google ha pubblicato un post intitolato ["Evolving nofollow"](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) che ha cambiato il modo in cui funzionano i link nofollow. Questo aggiornamento è lo sviluppo più importante nell'attribuzione dei link in oltre un decennio. Molte guide SEO lo spiegano ancora male.

### Cosa è cambiato

**Prima del 2019:** Nofollow era una direttiva. Google la rispettava in modo assoluto. Un link nofollow passava zero autorità, zero segnali di crawl e zero beneficio di ranking. Punto.

**Dopo il 2019:** Nofollow è diventato un hint. Google si riserva il diritto di considerare i link nofollow come segnali di ranking se i suoi algoritmi li trovano rilevanti. Google può anche scoprire e indicizzare nuove pagine attraverso link nofollow.

### Tre nuovi attributi per i link

Google ha introdotto 2 nuovi attributi insieme a nofollow:

| Attributo | Caso d'uso | Esempio |
|---|---|---|
| `rel="sponsored"` | Link a pagamento, pubblicità, sponsorizzazioni | Link affiliati, placement pagati, banner |
| `rel="ugc"` | Contenuto generato dagli utenti | Commenti, post nei forum, submission di community |
| `rel="nofollow"` | Segnale generico di "non approvo" | Qualsiasi link per cui non vuoi garantire |

Puoi combinare gli attributi: `rel="nofollow sponsored"` o `rel="nofollow ugc"`. Google raccomanda di usare l'attributo più specifico disponibile.

![Evoluzione del nofollow da direttiva a hint con i nuovi attributi sponsored e ugc](/images/blog/google-nofollow-hint-evolution.webp)

### Cosa significa nella pratica

**Per chi fa link building:** i link nofollow da siti autorevoli (Wikipedia, grandi pubblicazioni, Reddit) possono ora avere un certo valore di ranking. Non dovresti ignorarli.

**Per i proprietari di siti:** usa `rel="sponsored"` sui link a pagamento. Usa `rel="ugc"` sui link inseriti dagli utenti. Usa `rel="nofollow"` sui link che non ti fidi o non approvi. I link nofollow esistenti non devono essere modificati.

**Per chi fa audit SEO:** un [audit di backlink](/blog/backlink-audit-guide) dovrebbe ora analizzare separatamente i link nofollow da domini ad alta autorità. Questi possono contribuire ai ranking anche senza passare link equity tradizionale.

Il 78,8% dei professionisti SEO crede ora che i link nofollow influenzino i ranking in qualche misura. Il modello "hint" significa che il trattamento di Google verso nofollow non è più binario.

---

> **Smetti di scrivere. Inizia a posizionarti.** Stacc pubblica 30 articoli SEO al mese per 99 dollari. Ogni articolo costruisce la tua [domain authority](/blog/domain-authority-guide) con link interni ed esterni.
> [Inizia da 1 dollaro →](/pricing/)

---

## Quando usare ogni tipo di link

Sapere quando applicare dofollow o nofollow previene penalità e massimizza il valore dei link.

### Quando usare Dofollow (default)

Lascia i link dofollow quando approvi genuinamente la destinazione:

- **Link editoriali nei tuoi contenuti:** link a fonti, riferimenti e risorse che consigli
- **Link interni:** tutti i [link interni](/blog/internal-linking-blog-posts/) dovrebbero essere dofollow (con rare eccezioni)
- **Link nella bio degli autori di guest post:** pratica standard per guest contribution legittime
- **Link nelle pagine risorse:** liste curate di tool, guide o riferimenti di cui ti fidi
- **Link a partner e fornitori:** quando il rapporto è genuino, non a pagamento

### Quando usare Nofollow

Applica `rel="nofollow"` quando non vuoi garantire la destinazione:

- **Contenuto non affidabile:** link a siti che non hai verificato personalmente
- **Sezioni commenti:** qualsiasi link inviato dagli utenti (la maggior parte dei CMS gestisce questo automaticamente)
- **Link a login o signup:** Google non ha bisogno di scansionare queste pagine

### Quando usare rel="sponsored"

Applica `rel="sponsored"` su qualsiasi link che comporta uno scambio di denaro:

- **Link affiliati:** raccomandazioni di prodotti con parametri di tracking
- **Placement pagati:** contenuti sponsorizzati, advertorial, directory a pagamento
- **Link nei banner:** pubblicità display che portano a siti esterni
- **Partnership con influencer:** link a recensioni di prodotti con compensazione

Google ha dichiarato esplicitamente che non taggare i link a pagamento con `rel="sponsored"` o `rel="nofollow"` può comportare una penalità manuale. Questo vale sia per il sito che linka che per quello linkato.

### Quando usare rel="ugc"

Applica `rel="ugc"` sui link creati dai tuoi utenti:

- **Commenti ai blog:** commenti inviati dagli utenti con link
- **Post nei forum:** contenuto generato dalla community
- **Recensioni utente:** recensioni di prodotti o servizi inviate dai clienti
- **Contenuti in stile wiki:** pagine modificabili dai membri della community

### Albero decisionale rapido

| Scenario | Attributo da usare |
|---|---|
| L'hai scritto tu e approvi la destinazione | Dofollow (nessun attributo) |
| Inviato da un utente | `rel="ugc"` |
| C'è stato uno scambio di denaro | `rel="sponsored"` |
| Non ti fidi della destinazione | `rel="nofollow"` |
| Link interno nel tuo sito | Dofollow (nessun attributo) |
| Link affiliato con tracking | `rel="sponsored"` |

---

## Come controllare se un link è Dofollow o Nofollow

Puoi controllare lo stato di un link in 3 modi. Dall'ispezione manuale agli strumenti di audit in bulk.

### Metodo 1: Ispeziona elemento (manuale)

Fai clic destro su qualsiasi link nel browser e seleziona "Ispeziona" o "Ispeziona elemento". Guarda il tag `<a>` nell'HTML.

**Esempio dofollow:**
```html
<a href="https://example.com">Testo del link</a>
```
Nessun attributo `rel="nofollow"` presente. Il link è dofollow.

**Esempio nofollow:**
```html
<a href="https://example.com" rel="nofollow">Testo del link</a>
```
L'attributo `rel="nofollow"` dice a Google di non passare autorità.

Questo metodo funziona per controllare link singoli. Non scala per auditare un intero sito.

### Metodo 2: Estensioni browser (controllo rapido)

Installa un'estensione browser che evidenzia automaticamente i tipi di link:

- **NoFollow** (Chrome): evidenzia i link nofollow con un bordo rosso tratteggiato
- **SEOquake** (Chrome/Firefox): mostra lo stato di follow in un overlay
- **MozBar** (Chrome): mostra gli attributi dei link insieme alle metriche DA/PA

Queste estensioni funzionano su qualsiasi pagina web. Sono utili per analisi rapide dei competitor e controlli spot sui tuoi contenuti.

### Metodo 3: Tool di crawling (audit in bulk)

Per un audit completo del sito, usa un tool di crawling per analizzare ogni link:

- **Screaming Frog:** scansiona l'intero sito ed esporta tutti i link con i loro attributi
- **Ahrefs Site Audit:** identifica il tuo rapporto dofollow/nofollow su tutte le pagine
- **Semrush Backlink Audit:** analizza il tuo profilo di link in entrata per stato di follow

Un [audit SEO](/blog/how-to-do-seo-audit) completo dovrebbe includere un'analisi degli attributi dei link. Questo rivela se il tuo profilo appare naturale o over-ottimizzato.

---

## Costruire un profilo di link naturale

Google si aspetta un mix naturale di link dofollow e nofollow. Un profilo con il 100% di link dofollow segnala manipolazione. Un profilo con troppi link nofollow suggerisce bassa autorità.

### Il rapporto ideale

| Tipo di profilo | Dofollow % | Nofollow % | Livello di rischio |
|---|---|---|---|
| Naturale / Sano | 60-80% | 20-40% | Basso |
| Leggermente aggressivo | 80-90% | 10-20% | Medio |
| Over-ottimizzato | 90-100% | 0-10% | Alto |
| Deficit di autorità | Sotto il 50% | Sopra il 50% | Medio |

La media tra i primi 110.000 siti web è dell'89,4% dofollow e del 10,6% nofollow. Ma questa media è distorta verso l'alto perché i grandi siti autorevoli attraggono naturalmente più link editoriali dofollow.

![Rapporti naturali nel profilo di link con percentuali dofollow vs nofollow e livelli di rischio](/images/blog/dofollow-nofollow-link-profile-ratio.webp)

Per piccole e medie imprese, un rapporto 70/30 è un obiettivo sano. Raggiungilo costruendo link dofollow di qualità attraverso contenuti e outreach, accumulando naturalmente link nofollow da social media, forum e directory.

### Come costruire link Dofollow

I migliori link dofollow vengono da menzioni editoriali. Qualcuno legge i tuoi contenuti, li trova utili e ti linka senza essere pagato. Ecco strategie che generano link editoriali dofollow:

- **Pubblica ricerche o dati originali.** Gli studi sui dati attraggono citazioni. Giornalisti e blogger linkano a statistiche originali.
- **Crea guide ad alta utilità.** Guide passo passo che risolvono problemi reali guadagnano link da pagine risorse.
- **Costruisci tool gratuiti.** Un tool gratuito utile guadagna link naturali da chi lo consiglia. Dai un'occhiata ai nostri [tool SEO](/tools/seo-audit/) per esempi.
- **Guest posting su siti rilevanti.** Scrivi per siti del tuo settore. Includi un link dofollow naturale nel corpo del testo (non solo nella bio).
- **Ripara link rotti.** Trova link in uscita rotti su siti autorevoli e offri i tuoi contenuti come sostituto. Si chiama [broken link building](/blog/fix-broken-links/).
- **Ottieni menzioni stampa.** Rispondi alle richieste dei giornalisti su piattaforme come HARO, Connectively o Qwoted.

### Come guadagnare link Nofollow in modo naturale

I link nofollow si accumulano attraverso l'attività commerciale normale:

- Condividi i tuoi contenuti sui social media (tutti i link social sono nofollow)
- Partecipa a discussioni rilevanti su Reddit e Quora
- Mantieni le schede aziendali su directory e piattaforme di recensioni
- Incoraggia recensioni dei clienti che linkano al tuo sito
- Commenta su blog di settore con contributi genuini (non spam)

---

> **Il tuo team SEO. 99 dollari al mese.** 30 articoli ottimizzati, pubblicati automaticamente. Ogni articolo guadagna backlink e costruisce [topical authority](/blog/build-topical-authority/) nel tempo.
> [Inizia da 1 dollaro →](/pricing/)

---

## Errori comuni su Dofollow vs Nofollow

Questi errori costano posizionamenti e a volte attivano penalità. Evitali tutti.

**Errore 1: mettere nofollow ai tuoi link interni.**
I link interni dovrebbero quasi sempre essere dofollow. Aggiungere nofollow ai link interni blocca il flusso di PageRank all'interno del tuo sito. Si chiama "PageRank sculpting", e [Google ha confermato nel 2009](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) che non funziona. Il PageRank che sarebbe passato attraverso un link interno nofollow scompare. Non si ridistribuisce agli altri link.

**Errore 2: costruire link 100% dofollow.**
Un profilo tutto dofollow sembra artificiale. Gli algoritmi di Google rilevano pattern innaturali. Un profilo sano include link nofollow da piattaforme social, directory e contenuti generati dagli utenti. Punta a un rapporto 70/30 tra dofollow e nofollow.

**Errore 3: non taggare i link a pagamento come sponsored.**
Google richiede `rel="sponsored"` o `rel="nofollow"` su qualsiasi link che comporti pagamento. Non taggare i link a pagamento può comportare una penalità manuale contro entrambi i siti. Include link affiliati, post sponsorizzati e placement a pagamento nelle directory.

**Errore 4: ignorare i link nofollow nell'analisi dei backlink.**
Dopo l'aggiornamento del 2019, i link nofollow da domini ad alta autorità possono avere valore di ranking. Un [audit di backlink](/blog/backlink-audit-guide) completo dovrebbe analizzare entrambi i tipi di link. Dismissare tutti i link nofollow significa perdere potenziali segnali di ranking.

**Errore 5: ossessionarsi sugli attributi dei singoli link.**
Un link dofollow da un sito spam di bassa autorità fa più male che bene. Un link nofollow dal New York Times porta migliaia di visitatori referral. Qualità e rilevanza contano più dello stato di follow. Concentrati su guadagnare link da fonti rilevanti e autorevoli, indipendentemente dalla loro politica nofollow.

**Errore 6: usare nofollow sui link editoriali in uscita.**
Alcuni proprietari di siti mettono nofollow a ogni link in uscita per "conservare" PageRank. Questo è inutile e potenzialmente dannoso. Google si aspetta link in uscita naturali. Mettere nofollow a ogni link esterno fa sembrare i tuoi contenuti sospetti. Linka a fonti autorevoli con dofollow. Non danneggia i tuoi ranking.

---

## Dofollow vs Nofollow e link interni

I link interni meritano un'attenzione speciale. Funzionano in modo diverso dai backlink esterni.

Ogni [link interno](/blog/internal-linking-blog-posts/) sul tuo sito dovrebbe essere dofollow. I link interni distribuiscono il PageRank tra le tue pagine. Aiutano Google a scoprire e indicizzare nuovi contenuti. Segnalano quali pagine consideri più importanti.

L'unica eccezione: pagine di login, carrelli, o altre pagine che non vuoi Google prioritizzi. Ma anche queste raramente hanno bisogno di nofollow. Google gestisce la maggior parte di queste attraverso `robots.txt` e tag `noindex`.

Una struttura di link interni forte moltiplica il valore di ogni backlink dofollow che il tuo sito guadagna. Quando un link dofollow esterno punta alla tua homepage, i link interni distribuiscono quell'autorità ai tuoi post, pagine prodotto e pagine di servizio.

Usa l'[ottimizzazione dell'anchor text](/blog/anchor-text-optimization/) per i link interni. L'anchor text descrittivo dice a Google di cosa tratta la pagina di destinazione. Evita frasi generiche come "clicca qui" o "leggi di più".

---

## La distinzione tra Nofollow e Noindex

I principianti spesso confondono nofollow e noindex. Servono a scopi completamente diversi.

| Attributo | Cosa fa | Ambito |
|---|---|---|
| `rel="nofollow"` | Dice a Google di non passare autorità attraverso un link specifico | A livello di link |
| `<meta name="robots" content="noindex">` | Dice a Google di non includere una pagina nei risultati di ricerca | A livello di pagina |

Un link nofollow permette comunque a Google di vedere e potenzialmente scansionare la pagina di destinazione. Influenza solo se l'autorità passa attraverso quel link specifico.

Un tag noindex nasconde un'intera pagina dai risultati di ricerca. La pagina esiste ancora e si carica per i visitatori. Ma Google la rimuove dall'indice.

Questi due attributi risolvono problemi diversi. Usa nofollow quando non vuoi che un link passi autorità. Usa noindex quando non vuoi che una pagina appaia nei risultati di ricerca. Possono essere usati insieme sulla stessa pagina per il massimo controllo.

Per saperne di più su come Google gestisce le direttive di indicizzazione, vedi la nostra [checklist di SEO tecnica](/blog/technical-seo-checklist/).

---

> **Oltre 3.500 blog pubblicati. 92% di SEO score medio.** Scopri cosa Stacc può fare per la tua strategia di link building. Pubblichiamo contenuti che guadagnano backlink.
> [Inizia da 1 dollaro →](/pricing/)

---

## FAQ

**Qual è la differenza tra link dofollow e nofollow?**

Un link dofollow passa autorità di ranking (PageRank) da una pagina all'altra. Un link nofollow include `rel="nofollow"` e dice a Google di non contarlo come segnale di ranking. I link dofollow migliorano direttamente la SEO. I link nofollow portano traffico e visibilità del brand senza impatto diretto sui ranking.

**I link nofollow aiutano la SEO?**

I link nofollow non passano direttamente autorità di ranking. Ma contribuiscono a un profilo di link naturale, portano traffico referral e costruiscono brand awareness. Dall'aggiornamento Google del 2019, nofollow è un "hint" piuttosto che una direttiva. Google può scegliere di contare alcuni link nofollow come segnali di ranking. Il 78,8% dei professionisti SEO crede che i link nofollow influenzino ancora i ranking.

**Qual è il rapporto ideale tra link dofollow e nofollow?**

Un profilo di link sano contiene tra il 60 e l'80% di link dofollow e tra il 20 e il 40% di link nofollow. La media tra i siti top è dell'89,4% dofollow. Per piccole e medie imprese, un rapporto 70/30 segnala un profilo naturale e organico. Un profilo 100% dofollow sembra artificiale e rischia di attivare penalità Google.

**I link dai social media sono dofollow o nofollow?**

Tutte le principali piattaforme social usano link nofollow. Include Facebook, X (Twitter), LinkedIn, Instagram, Pinterest e TikTok. I link social non passano autorità di ranking diretta. Ma portano traffico referral e contribuiscono alla percentuale di link nofollow.

**Qual è la differenza tra nofollow e noindex?**

Nofollow è un attributo a livello di link che impedisce il passaggio di autorità attraverso un link specifico. Noindex è una direttiva a livello di pagina che impedisce a un'intera pagina di apparire nei risultati di ricerca. Risolvono problemi diversi. Usa nofollow sui link che non approvi. Usa noindex sulle pagine che non vuoi indicizzare.

**Dovrei mettere nofollow a tutti i link in uscita?**

No. Mettere nofollow a ogni link in uscita è inutile e sembra innaturale. Linka a fonti autorevoli con dofollow quando approvi genuinamente i contenuti. Google si aspetta link in uscita naturali. Usa nofollow solo su link di cui non ti fidi, link a pagamento o contenuti generati dagli utenti.

**Cosa sono rel="sponsored" e rel="ugc"?**

Google ha introdotto questi attributi nel settembre 2019 insieme al cambio di nofollow in "hint". Usa `rel="sponsored"` su qualsiasi link che comporti scambio di denaro (link affiliati, placement pagati, sponsorizzazioni). Usa `rel="ugc"` sui contenuti generati dagli utenti (commenti, post nei forum, recensioni). Entrambi dicono a Google di non passare autorità di ranking attraverso il link.

---

I link dofollow e nofollow servono a scopi diversi. Entrambi sono essenziali per una strategia SEO sana. Costruisci link dofollow per l'autorità di ranking. Guadagna link nofollow per traffico, diversità e segnali naturali. Monitora il tuo rapporto, tagga correttamente i link a pagamento e ricorda che Google tratta nofollow come un hint, non come un comando.

Se vuoi scalare i contenuti che attraggono link editoriali di qualità, prova theStacc. Pubblichiamo articoli SEO ottimizzati che costruiscono autorità nel tempo, senza che tu debba gestire un team di copywriter. [Inizia da 1 dollaro →](/pricing/)
