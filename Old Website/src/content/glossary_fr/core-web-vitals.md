---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "Les Core Web Vitals sont les trois métriques Google qui mesurent l'expérience page : LCP, INP et CLS. Apprenez ce qu'elles mesurent et comment les améliorer."
category: "SEO"
difficulty: "Intermediate"
keyword: "qu'est-ce que core web vitals"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## Qu'est-ce que les Core Web Vitals ?

Les Core Web Vitals sont un ensemble de trois métriques précises que Google utilise pour mesurer la rapidité, la réactivité et la stabilité visuelle perçues d'une page web par les vrais utilisateurs.

Google les a introduites en 2020 et en a fait un signal de classement officiel en 2021. Elles s'inscrivent dans la conversation plus large sur la [vitesse de page](/glossary/page-speed), mais avec plus de précision. Plutôt qu'un unique « score de vitesse », les Core Web Vitals décomposent l'expérience utilisateur en trois composants mesurables. Chargement, interactivité et stabilité visuelle.

D'après les données de Google, les pages qui respectent les trois seuils enregistrent 24 % d'abandons en moins. Ce n'est pas une amélioration UX mineure. C'est un lien direct vers plus de conversions et un meilleur [trafic organique](/glossary/organic-traffic).

## Pourquoi les Core Web Vitals comptent-ils ?

Ignorer les Core Web Vitals ne fera pas s'effondrer vos classements du jour au lendemain. Mais, à conditions égales, Google privilégiera les pages qui passent ces seuils par rapport à celles qui échouent.

- **Facteur de classement depuis 2021**. Google a confirmé les Core Web Vitals comme partie intégrante de ses signaux page experience, ce qui influence directement votre place dans les [résultats de recherche](/glossary/serp)
- **24 % d'abandons en moins**. Les pages qui passent les trois seuils retiennent les utilisateurs nettement plus longtemps (Google, 2021)
- **Impact mobile-first**. Avec l'[indexation mobile-first](/glossary/mobile-first-indexing) par défaut, ce sont les pages mobiles lentes qui trinquent le plus
- **Corrélation avec les revenus publicitaires**. Les éditeurs ayant amélioré leurs scores CWV ont vu jusqu'à 15 % de revenus publicitaires en plus grâce à des sessions plus longues

Si vous gérez une PME ou une activité locale, c'est important parce que vos concurrents n'optimisent probablement pas non plus pour les CWV. Obtenir un score qui passe quand eux échouent est un avantage réel.

## Comment fonctionnent les Core Web Vitals

Google collecte les données Core Web Vitals depuis de vrais utilisateurs de Chrome via le Chrome User Experience Report (CrUX). Vos scores viennent donc de visiteurs réels. Pas d'une simulation en laboratoire.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) mesure le temps que met le plus grand élément visible de votre page à se charger. Pensez : l'image hero, un gros bloc de texte ou la vignette d'une vidéo. Google veut ce score sous les 2,5 secondes. Au-delà de 4 secondes, c'est jugé « médiocre ».

La solution est généralement directe : compresser les images, utiliser un [CDN](/glossary/content-delivery-network-cdn), différer les ressources hors écran et améliorer le temps de réponse serveur.

### Interaction to Next Paint (INP)

INP a remplacé First Input Delay (FID) en mars 2024. Il mesure la vitesse à laquelle votre page répond aux interactions utilisateur. Clics, taps et pressions de touches. Sur l'ensemble de la visite, pas seulement la première interaction.

Un bon INP est sous les 200 millisecondes. Si votre page se fige une demi-seconde quand on clique sur un bouton, c'est un échec. Le JavaScript lourd est généralement le coupable.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) mesure la stabilité visuelle. Vous avez déjà essayé d'appuyer sur un bouton qui s'est déplacé parce qu'une pub ou une image a chargé en retard ? C'est un layout shift.

Google veut un CLS sous 0,1. Les causes les plus fréquentes : images sans dimensions définies, publicités injectées au-dessus du contenu, et polices web qui changent de taille pendant le chargement.

## Types d'évaluations Core Web Vitals

Les données Core Web Vitals existent en deux versions, et elles racontent souvent des histoires différentes :

- **Données de terrain (RUM)**. Real User Metrics collectées auprès de visiteurs réels via CrUX. C'est ce que Google utilise pour ses décisions de classement. Visibles dans la [Google Search Console](/glossary/google-search-console) et PageSpeed Insights.
- **Données de laboratoire**. Tests de performance simulés avec des outils comme Lighthouse, WebPageTest et Chrome DevTools. Utiles pour le débogage, mais pas utilisées directement pour le classement.
- **Niveau origine vs. niveau URL**. Google évalue les CWV à la fois au niveau du domaine entier et de la page individuelle. Si votre site passe globalement mais qu'une landing page clé échoue, cette page peut quand même être impactée.
- **Mobile vs. desktop**. Les scores sont mesurés séparément pour mobile et desktop. La plupart des sites font moins bien en mobile, qui est la version privilégiée par Google.

Pour les audits [SEO technique](/glossary/technical-seo), commencez toujours par les données de terrain. Les données de laboratoire aident à identifier le problème, mais les données de terrain disent si le problème pénalise vraiment les visiteurs réels.

## Exemples de Core Web Vitals

**Exemple 1 : la page d'accueil lente d'un plombier**
Un plombier local à Lyon a une page d'accueil avec un LCP de 4,8 secondes à cause d'une image hero non compressée (3,2 Mo). Après conversion en WebP et redimensionnement aux bonnes dimensions, le LCP descend à 1,9 seconde. Le taux de rebond chute de 18 % le mois suivant.

**Exemple 2 : une boutique e-commerce avec du layout shift**
Une boutique Shopify d'accessoires pour animaux affiche un CLS de 0,34 parce que les images produit chargent sans attributs width/height. Ajouter des dimensions explicites à chaque balise image fait passer le CLS à 0,04. Fini les clics accidentels sur « Ajouter au panier » d'acheteurs agacés.

**Exemple 3 : un blog plombé par le JavaScript**
Le blog d'une agence marketing utilise 14 scripts tiers. Analytics, widgets de chat, embeds sociaux, trackers publicitaires. L'INP est à 480 ms. Après audit et suppression de 6 scripts inutilisés, l'INP tombe à 160 ms. Les pages créées et publiées via theStacc partent déjà avec un code propre et optimisé. Pas de scripts surchargés.

## Core Web Vitals vs. vitesse de page

On utilise les deux indifféremment. À tort.

| | Core Web Vitals | Vitesse de page |
|---|---|---|
| **Ce qui est mesuré** | 3 métriques UX précises (LCP, INP, CLS) | Temps de chargement global et score de performance |
| **Source des données** | Données utilisateurs réelles (CrUX) | Simulations en labo (Lighthouse) |
| **Signal de classement Google** | Oui, directement | Indirectement (via les CWV) |
| **Périmètre** | Centré sur l'expérience perçue | Parapluie plus large de la performance |
| **Métrique exemple** | LCP : 2,1 s | Score PageSpeed : 74/100 |

La [vitesse de page](/glossary/page-speed) est le concept large. Les Core Web Vitals sont les métriques précises que Google utilise réellement.

## Bonnes pratiques Core Web Vitals

- **Compressez et dimensionnez correctement toutes les images**. Utilisez les formats WebP ou AVIF, et fixez toujours les attributs width et height explicites pour empêcher le layout shift
- **Limitez les scripts tiers**. Chaque script externe (widgets de chat, analytics, trackers) alourdit l'INP. Auditez sans pitié et supprimez ce dont vous n'avez pas besoin.
- **Servez les ressources statiques via un CDN**. Diffuser images et CSS depuis des serveurs edge proches de vos visiteurs réduit drastiquement le LCP
- **Différez le JavaScript non critique**. Chargez d'abord le contenu above-the-fold, puis laissez les scripts secondaires arriver une fois la page interactive
- **Surveillez les données de terrain chaque mois dans Google Search Console**. Les scores labo fluctuent, mais les données de terrain montrent si les vrais visiteurs ont une bonne expérience. Des services comme theStacc publient automatiquement du contenu qui suit les bonnes pratiques HTML, ce qui réduit les problèmes CWV dès le départ.

## Questions fréquentes

### Les Core Web Vitals sont-ils un facteur de classement ?

Google a confirmé les Core Web Vitals comme signal de classement en juin 2021. Ils font partie du système page experience. L'impact est réel mais secondaire face à la pertinence du contenu et aux [backlinks](/glossary/backlinks). Plutôt départage que décision.

### Qu'est-ce qui a remplacé First Input Delay ?

Interaction to Next Paint (INP) a officiellement remplacé FID comme Core Web Vital en mars 2024. INP mesure la réactivité sur l'ensemble des interactions d'une visite, pas seulement le premier clic.

### Comment vérifier mes Core Web Vitals ?

Utilisez le rapport Core Web Vitals de Google Search Console pour les données de terrain. PageSpeed Insights vous donne données de terrain et de laboratoire pour n'importe quelle URL. Chrome DevTools et Lighthouse conviennent pour les tests locaux pendant le développement.

### Qu'est-ce qu'un bon score LCP ?

Google considère un LCP inférieur à 2,5 secondes comme « bon », entre 2,5 et 4 secondes comme « à améliorer », et au-delà de 4 secondes comme « médiocre ». La plupart des sites galèrent avec le LCP à cause d'images non optimisées et de réponses serveur lentes.

---

Vous voulez un contenu qui charge vite et se classe bien sans gérer la technique ? theStacc publie 30 articles optimisés SEO sur votre site chaque mois. Automatiquement. [Démarrer pour $1 →](https://app.thestacc.com)

## Sources

- [Google : Web Vitals](https://web.dev/vitals/)
- [Google Search Central : Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev : Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs : Core Web Vitals et SEO](https://ahrefs.com/blog/core-web-vitals/)
