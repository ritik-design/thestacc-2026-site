---
term: "Redirection 301"
slug: "301-redirect"
definition: "Une redirection 301 envoie définitivement les utilisateurs et les moteurs de recherche d'une URL vers une autre. Découvrez quand utiliser les redirections 301, comment les implémenter et leur impact sur le SEO."
category: "SEO"
difficulty: "Intermediate"
keyword: "qu'est-ce qu'une redirection 301"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## Qu'est-ce qu'une redirection 301 ?

Une redirection 301 est un code de statut HTTP qui transfère de façon permanente une URL vers une autre. Elle indique aux navigateurs et aux moteurs de recherche que l'adresse d'origine a définitivement bougé.

Lorsque Googlebot ou un visiteur rencontre un code 301, il est automatiquement envoyé vers la nouvelle URL. Pas de page cassée. Pas d'impasse. Le « 301 » désigne le code de réponse HTTP spécifique. C'est la façon qu'a le web de dire « cette page a été définitivement déplacée vers un nouvel emplacement ». Il existe une [redirection 302](/glossary/302-redirect) pour les déplacements temporaires, mais c'est la 301 qui compte pour le [SEO](/glossary/seo).

Voici pourquoi c'est crucial : les recherches de Moz montrent que les redirections 301 transmettent environ 95 à 99 % du [link equity](/glossary/link-equity) vers l'URL de destination. Cela signifie que le pouvoir de classement acquis par votre ancienne URL grâce aux [backlinks](/glossary/backlinks) ne disparaît pas. Il est transféré vers la nouvelle page. Une mauvaise gestion des 301 revient à jeter des années d'autorité accumulée.

## Pourquoi une redirection 301 est-elle importante ?

Chaque fois qu'une URL change sans redirection appropriée, quelque chose se casse. Classements, trafic, expérience utilisateur. Choisissez deux parmi les trois.

- **Préserve les classements de recherche.** Sans 301, Google traite la nouvelle URL comme une toute nouvelle page sans aucune autorité. Vos classements disparaissent du jour au lendemain.
- **Transfère le link equity.** Ces [backlinks](/glossary/backlinks) que vous avez gagnés ? Un 301 transfère leur valeur vers la nouvelle URL. Sans lui, ce link juice s'évapore.
- **Prévient les erreurs 404.** Les utilisateurs qui ont mis l'ancienne URL en favori ou qui cliquent sur un lien externe accèdent à une page qui fonctionne plutôt qu'à une [erreur 404](/glossary/404-error). Meilleure expérience, [taux de rebond](/glossary/bounce-rate) plus faible.
- **Consolide le contenu dupliqué.** Plusieurs URL servant le même contenu diluent votre autorité. Les 301 les fusionnent en une seule page solide.

Si vous avez déjà déplacé un site web, changé une structure d'URL ou fusionné deux pages, vous aviez besoin de redirections 301. Les ignorer est l'une des erreurs de [SEO technique](/glossary/technical-seo) les plus courantes et les plus coûteuses.

## Comment fonctionne une redirection 301

Le processus se déroule en millisecondes, mais voici ce qui se passe réellement sous le capot.

### Le cycle de requête HTTP

Un utilisateur ou un robot d'exploration demande l'ancienne URL. Le serveur répond avec le code de statut HTTP 301 et un en-tête « Location » pointant vers la nouvelle URL. Le navigateur demande alors automatiquement la nouvelle URL. L'utilisateur voit la page finale. Il peut même ne pas remarquer que la redirection a eu lieu.

### Comment Google traite les 301

Lorsque [Googlebot](/glossary/crawling) rencontre un 301, il fait trois choses : il suit la redirection vers la nouvelle URL, transfère la majorité des signaux de classement de l'ancienne page vers la nouvelle page, et finalement retire l'ancienne URL de son index. Ce processus peut prendre des jours ou des semaines selon la fréquence à laquelle Google explore votre site.

### Implémentation au niveau serveur vs au niveau page

Les redirections 301 sont configurées au niveau du serveur. Pas dans votre HTML. Les méthodes les plus courantes :

- **Apache (.htaccess) :** `Redirect 301 /ancienne-page https://exemple.com/nouvelle-page`
- **Nginx :** `rewrite ^/ancienne-page$ /nouvelle-page permanent;`
- **Plugins WordPress :** Yoast, Redirection ou Rank Math gèrent cela via le tableau de bord
- **Cloudflare :** Règles de page ou Redirections en masse pour les changements au niveau du domaine

Les redirections meta refresh au niveau page existent, mais elles sont plus lentes et ne transmettent pas le link equity aussi fiablement. Utilisez toujours des 301 au niveau serveur.

## Types de redirections

Comprendre les différences prévient des erreurs coûteuses :

- **301 (Permanent).** La page a définitivement bougé. Transfère ~95-99 % du link equity. À utiliser pour les changements d'URL, les migrations de domaine et la consolidation de contenu.
- **[302 (Temporaire)](/glossary/302-redirect).** La page a temporairement bougé. Google peut ou non transférer le link equity. À utiliser pour les tests A/B, les pages de maintenance ou le contenu saisonnier.
- **307 (Temporaire, HTTP/1.1).** Identique au 302, mais préserve strictement la méthode de requête (POST reste POST). Uniquement pour des cas d'usage techniques.
- **308 (Permanent, HTTP/1.1).** Identique au 301 avec préservation stricte de la méthode. Rarement utilisé dans des contextes SEO.
- **Meta refresh.** Redirection basée sur le HTML. Lente, faible valeur SEO. À éviter.

En cas de doute, utilisez un 301. C'est le choix sûr pour les changements d'URL permanents.

## Exemples de redirections 301

**Exemple 1 : Un commerce local qui refond son site web**
Un cabinet d'avocats refond son site web et modifie la structure d'URL de `/services/avocat-prejudice-corporel` vers `/domaines-pratique/prejudice-corporel`. Sans 301, l'ancienne page — qui se classait en 3e position pour « avocat préjudice corporel [ville] » — renverrait une erreur 404. Avec la redirection, la nouvelle URL hérite de la position de classement et les 47 [backlinks](/glossary/backlinks) pointant vers l'ancienne page continuent de fonctionner.

**Exemple 2 : Fusion de deux articles de blog en une page plus solide**
Une société de plomberie a deux articles légers : « Comment réparer un robinet qui fuit » et « Guide de réparation de robinet qui fuit ». Aucun ne se classe bien. Ils les fusionnent en un guide détaillé sur l'URL la plus solide et font un 301 sur la plus faible. Les signaux d'[autorité de domaine](/glossary/domain-authority) combinés font passer la page fusionnée de la position 12 à la position 4 en 6 semaines.

**Exemple 3 : Migration de domaine mal gérée**
Un site e-commerce migre d'anciendomaine.com vers nouveaudomaine.com mais ne redirige que la page d'accueil. Les 2 400 pages de produits et les 180 articles de blog renvoient tous des erreurs 404. Le [trafic organique](/glossary/organic-traffic) chute de 78 % en 2 semaines. Chaque URL avait besoin d'une redirection 301 individuelle. Cette erreur prend des mois à corriger, si elle est détectée rapidement.

## Redirection 301 vs URL canonique

Les deux traitent le contenu dupliqué, mais fonctionnent différemment.

| | Redirection 301 | [URL canonique](/glossary/canonical-url) |
|---|---|---|
| **Ce qu'elle fait** | Envoie les utilisateurs et les robots vers une nouvelle URL | Indique à Google quelle URL est la version « maître » |
| **Expérience utilisateur** | L'utilisateur voit la nouvelle page (redirection automatique) | L'utilisateur peut toujours accéder à la page d'origine |
| **Quand l'utiliser** | L'ancienne page ne doit plus exister | Les deux pages doivent rester accessibles |
| **Link equity** | Transfère ~95-99 % | Consolide les signaux vers la canonique |
| **Exemple** | Ancienne URL de blog déplacée vers la nouvelle structure | Page produit accessible via 3 URL différentes |

Utilisez les 301 lorsque l'ancienne page est définitivement supprimée. Utilisez les canonicals lorsque les deux pages doivent exister mais que vous souhaitez que Google en privilégie une.

## Bonnes pratiques des redirections 301

- **Mappez chaque ancienne URL vers une nouvelle URL pertinente.** Ne redirigez pas tout vers la page d'accueil. Redirigez chaque ancienne page vers son équivalent le plus proche. Google traite les redirections massives vers la page d'accueil comme des soft 404s.
- **Implémentez des redirections 1 pour 1 lors des migrations de site.** Avant de lancer un nouveau site, explorez l'ancien, exportez chaque URL et créez une carte de redirections. Manquez cette étape et vous regarderez le [trafic organique](/glossary/organic-traffic) s'effondrer.
- **Évitez les chaînes de redirections.** A > B > C > D ralentit l'utilisateur, gaspille le [budget d'exploration](/glossary/crawl-budget) et peut perdre du link equity à chaque saut. Chaque redirection doit pointer directement vers la destination finale.
- **Surveillez avec Google Search Console.** Vérifiez le rapport de couverture pour les erreurs d'exploration après l'implémentation des redirections. [Google Search Console](/glossary/google-search-console) affiche les pages renvoyant des erreurs 404 pour que vous puissiez détecter rapidement les redirections manquantes.
- **Auditez les redirections chaque trimestre.** Les anciennes redirections pointant vers des pages qui n'existent plus créent des chaînes. Les services comme theStacc intègrent des structures d'URL appropriées dans chaque article publié, mais si vous migrez ou réorganisez votre contenu, planifiez des audits réguliers de redirections pour maintenir la propreté.

## Questions fréquemment posées

### Les redirections 301 nuisent-elles au SEO ?

Pas lorsqu'elles sont correctement utilisées. Un 301 correctement implémenté transfère la quasi-totalité du link equity vers la nouvelle URL. John Mueller de Google a confirmé que les 301 n'entraînent pas de perte de classement. Le risque vient d'une implémentation incorrecte : chaînes de redirections, redirections massives vers la page d'accueil, ou pages entièrement manquantes.

### Combien de temps faut-il conserver une redirection 301 ?

Indéfiniment, ou au moins un an. Google a besoin de temps pour réexplorer l'ancienne URL, traiter la redirection et mettre à jour son index. Supprimer un 301 trop tôt signifie que les liens externes vers l'ancienne URL rencontreront à nouveau des erreurs 404.

### Un trop grand nombre de redirections 301 peut-il ralentir un site ?

Les redirections individuelles ajoutent quelques millisecondes. Mais les chaînes de redirections (page A > B > C) multiplient ce délai. Maintenez les redirections sur un seul saut maximum. Un site avec des milliers de 301 propres fonctionne bien. Ce sont les chaînes et les boucles qui causent des problèmes.

### Quelle est la différence entre un 301 et un 302 ?

Un [301 est permanent](/glossary/301-redirect) ; un [302 est temporaire](/glossary/302-redirect). Utilisez 301 lorsque l'ancienne URL est définitivement supprimée. Utilisez 302 lorsque la page d'origine reviendra (contenu saisonnier, maintenance temporaire). Google transfère le link equity plus fiablement via les 301.

---

Vous voulez une architecture de site conçue pour le SEO dès le départ ? theStacc publie 30 articles optimisés pour le SEO sur votre site chaque mois avec des structures d'URL propres et un maillage interne approprié. Automatiquement. [Commencer pour 1 $ →](https://app.thestacc.com)

## Sources

- [Google Search Central : Redirections et Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz : Guide de redirection](https://moz.com/learn/seo/redirection)
- [Ahrefs : Redirections 301 pour le SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal : Redirections 301 vs 302](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Aide Google Search Console : Corriger les erreurs d'exploration](https://support.google.com/webmasters/answer/7440203)
