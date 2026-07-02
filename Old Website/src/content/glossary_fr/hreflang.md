---
term: "hreflang"
slug: "hreflang"
definition: "hreflang est un attribut HTML qui indique aux moteurs de recherche quelle version linguistique ou régionale d'une page servir à chaque utilisateur, évitant le contenu dupliqué."
category: "SEO"
difficulty: "Advanced"
keyword: "balise hreflang"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## Qu'est-ce que hreflang ?

hreflang est un attribut HTML (`rel="alternate" hreflang="x"`) qui signale à Google et aux autres moteurs quelle langue et quel pays cible une version donnée d'une page.

Si votre site dispose de pages en plusieurs langues ou de variantes régionales — français pour la France et français pour le Canada, par exemple —, la balise hreflang empêche Google de les considérer comme du [contenu dupliqué](/glossary/duplicate-content). Sans elle, Google choisit une version et la diffuse partout. Rarement la bonne pour chaque audience.

Une étude d'Ahrefs montre que seuls 19 % des sites multilingues implémentent hreflang correctement. Les 81 % restants accumulent des erreurs : balises de retour manquantes, URL cassées, codes mal saisis. C'est l'un des éléments de SEO technique les plus mal configurés.

## Pourquoi hreflang est-il important ?

Une balise hreflang bien posée détermine si la bonne audience voit la bonne page.

- **Diffusion linguistique correcte**. Un visiteur lyonnais voit la version française, un visiteur québécois voit la version canadienne — sans redirection manuelle ni script côté navigateur
- **Protection contre le filtrage des doublons**. Google comprend que vos pages `/fr/` et `/de/` ne sont pas des copies mais des traductions intentionnelles
- **Meilleure expérience utilisateur**. Atterrir sur une page dans sa langue maternelle réduit le taux de rebond et augmente la conversion
- **Tarifs et catalogues régionaux**. Les sites e-commerce qui pratiquent des prix, devises ou produits différents par pays ont besoin de hreflang pour servir la bonne version à chaque marché

Toute entreprise active dans plusieurs pays ou plusieurs langues a besoin de hreflang. Sans exception.

## Comment fonctionne hreflang

### Les méthodes d'implémentation

Trois voies existent pour implémenter hreflang : balises `<link>` dans le `<head>` HTML, en-têtes HTTP (pour les PDF et les fichiers non HTML) ou via votre [sitemap XML](/glossary/xml-sitemap). Google recommande de choisir une seule méthode et de s'y tenir. L'approche sitemap est la plus pratique pour les grands sites comportant des centaines de variantes linguistiques.

### La règle du retour bidirectionnel

Chaque annotation hreflang doit être réciproque. Si la page A dit « mon équivalent espagnol est la page B », alors la page B doit dire « mon équivalent français est la page A ». Les balises de retour manquantes sont l'erreur d'implémentation numéro un. Sans elles, Google ignore tout simplement les annotations.

### La balise x-default

La valeur `x-default` indique à Google quelle version afficher quand aucune correspondance précise de langue ou de région n'est trouvée. Votre solution de repli. Généralement la version anglaise ou celle de votre marché principal. Sans `x-default`, Google devine — et ne devine pas toujours juste.

## Exemples de hreflang

**Exemple 1 : une boutique en ligne avec des versions France et Belgique**
Un détaillant lyonnais exploite `example.com/fr-fr/chaussures` (prix en euros, TVA française) et `example.com/fr-be/chaussures` (prix en euros, TVA belge, frais de port différents). Sans hreflang, Google pourrait montrer la version française à un internaute belge. Avec une balise hreflang correcte, chaque audience voit les bons prix et la bonne logistique. L'[URL canonique](/glossary/canonical-url) reste indépendante pour chaque version.

**Exemple 2 : un éditeur SaaS avec des pages traduites**
Un outil de gestion de projet propose sa page d'accueil en 8 langues. L'équipe implémente hreflang via le sitemap XML, chaque langue pointant vers toutes les autres. Les internautes germanophones atterrissent sur `/de/`, les hispanophones sur `/es/`, et tous les autres tombent sur la version anglaise marquée `x-default`.

Vous voulez publier du contenu international sans vous battre avec le câblage hreflang ? theStacc publie 30 articles optimisés pour le SEO sur votre site chaque mois. Automatiquement. [Démarrer pour 1 $ →](https://app.thestacc.com)

## Questions fréquemment posées

### hreflang influence-t-il le classement ?

hreflang n'améliore pas directement le classement. Il dicte simplement quelle version apparaît dans chaque marché. Mais servir la bonne langue à la bonne audience améliore les signaux d'engagement — taux de rebond plus bas, [temps de séjour](/glossary/dwell-time) plus long — qui peuvent influencer le ranking au fil du temps.

### Peut-on utiliser hreflang pour la même langue dans plusieurs pays ?

Oui. C'est précisément l'un de ses meilleurs usages. Anglais des États-Unis (`en-us`), anglais du Royaume-Uni (`en-gb`) et anglais d'Australie (`en-au`) peuvent cohabiter avec des annotations distinctes. Google s'appuie sur le code pays, pas seulement sur la langue, pour choisir la version à servir.

### Que se passe-t-il en cas d'implémentation incorrecte ?

Google ignore complètement les annotations et décide seul quelle version afficher. Pas de pénalité. Juste une perte de contrôle sur la page qui apparaît dans chaque marché. Le rapport Ciblage international de la Google Search Console identifie les erreurs hreflang en détail.

---

Vous voulez gagner en visibilité à l'international sans recruter une équipe SEO dans chaque pays ? theStacc publie 30 articles optimisés pour le SEO sur votre site chaque mois. Automatiquement. [Démarrer pour 1 $ →](https://app.thestacc.com)

## Sources

- [Google Search Central : implémentation de hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs : guide des balises hreflang](https://ahrefs.com/blog/hreflang-tags/)
- [Moz : le guide ultime de hreflang](https://moz.com/learn/seo/hreflang-tag)
