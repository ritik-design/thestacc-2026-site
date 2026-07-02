---
term: "Crawl budget (budget d'exploration)"
slug: "crawl-budget"
definition: "Le crawl budget est le nombre de pages qu'un bot de moteur de recherche explorera sur votre site dans un délai donné. Bien le gérer garantit que vos pages les plus importantes sont priorisées."
category: "SEO"
difficulty: "Intermediate"
keyword: "crawl budget"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "site-architecture"
  - "xml-sitemap"
---

## Qu'est-ce que le crawl budget ?

Le crawl budget est le nombre total d'URL que Googlebot ira chercher sur votre site pendant une période donnée, déterminé par une combinaison de limite de taux d'exploration et de demande d'exploration.

Google ne donne pas une attention illimitée à chaque site. Googlebot alloue des ressources basées sur la taille, la santé et l'importance perçue de votre site. Pour la plupart des petits à moyens sites (moins de 10 000 pages), le crawl budget n'est pas une préoccupation. Mais pour les plus grands sites. Boutiques e-commerce, éditeurs, annuaires. Cela peut être la différence entre du nouveau contenu indexé en heures ou en semaines.

Gary Illyes de Google a déclaré que le crawl budget « n'est pas quelque chose dont la plupart des sites doivent s'inquiéter », mais a aussi confirmé que le gaspiller sur des URL de faible valeur peut retarder l'[indexation](/glossary/indexing) de pages importantes.

## Pourquoi le crawl budget est-il important ?

Si Googlebot ne peut pas atteindre vos pages clés, elles ne peuvent pas se classer. Point.

- **Indexation plus rapide**. Une utilisation efficace du crawl budget signifie que le nouveau contenu est découvert et indexé plus tôt
- **Pages priorisées**. Quand Googlebot gaspille du budget sur du [contenu dupliqué](/glossary/duplicate-content), pages 404 ou URL de paramètre, vos pages money peuvent ne pas être explorées du tout pendant ce cycle
- **Signal de santé du site**. Un site facile à explorer signale la qualité aux systèmes de Google, tandis que les pièges d'exploration et erreurs font le contraire
- **Mise à l'échelle du contenu**. Les sites publiant 30+ pages par mois ont besoin que Googlebot suive le rythme du nouveau contenu, rendant l'efficacité d'exploration critique

Tout site avec plus de quelques milliers de pages devrait gérer activement le crawl budget.

## Comment fonctionne le crawl budget

### Limite de taux d'exploration

Google définit une vitesse maximale d'exploration pour éviter de surcharger votre serveur. Si votre serveur répond lentement ou retourne des erreurs, Googlebot se retire. Un hébergement rapide et fiable augmente directement votre limite de taux d'exploration.

### Demande d'exploration

Même si Googlebot *pouvait* explorer plus, il ne le fera que s'il a une raison. Les pages populaires avec beaucoup de [backlinks](/glossary/backlinks) sont ré-explorées fréquemment. Les pages obsolètes et de faible autorité peuvent passer des mois entre les visites. Mettre à jour le contenu et gagner des liens augmente la demande d'exploration pour des URL spécifiques.

### Gaspilleurs courants de crawl budget

Navigation à facettes, IDs de session dans URL, défilement infini sans pagination appropriée, [liens cassés](/glossary/broken-link) retournant des [erreurs 404](/glossary/404-error) et contenu dupliqué à travers les variations de paramètres consomment tous du crawl budget. Utilisez [robots.txt](/glossary/robots-txt) et les [balises noindex](/glossary/noindex) pour empêcher Googlebot de gaspiller du temps sur ces pages.

## Exemples de crawl budget

**Exemple 1 : Un site e-commerce avec des URL de filtre**
Le site d'un magasin de meubles génère 50 000 URL uniques à partir de combinaisons de filtres (couleur, taille, matériau, prix). Seulement 3 000 sont des pages produit réelles. Sans bloquer les URL de filtre via robots.txt, Googlebot dépense 94 % de son crawl budget sur des pages qui ne devraient pas être indexées.

**Exemple 2 : Un blog riche en contenu**
Une entreprise publie 30 articles par mois via theStacc. Avec une [architecture de site](/glossary/site-architecture) propre et un sitemap XML, Googlebot découvre et indexe les nouveaux articles en 48 heures. Un concurrent publiant le même volume sur un site mal structuré attend 2-3 semaines pour l'indexation.

### Outils et ressources

| Outil | Objectif | Prix |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Données de performance de recherche | Gratuit |
| **Ahrefs** | Backlinks, mots-clés, audit de site | À partir de 99 $/mois |
| **Semrush** | Plateforme SEO tout-en-un | À partir de 130 $/mois |
| **Screaming Frog** | Analyse d'exploration technique | Gratuit (500 URL) |
| **theStacc** | Publication automatisée de contenu SEO | À partir de 99 $/mois |

## Questions fréquentes

### Comment vérifier mon crawl budget ?

Le rapport Statistiques d'exploration de Google Search Console montre combien de pages Googlebot explore par jour, le temps de réponse moyen et les tendances de demandes d'exploration. Vérifiez sous Paramètres > Statistiques d'exploration. Cherchez des motifs. Une chute soudaine du taux d'exploration signale souvent des problèmes de serveur.

### Le crawl budget affecte-t-il les petits sites ?

Pour les sites de moins de 1 000 pages, le crawl budget importe rarement. Googlebot peut facilement gérer les petits sites en une seule session d'exploration. Commencez à y prêter attention quand vous dépassez 10 000 URL indexables ou remarquez une indexation lente du nouveau contenu.

### Comment améliorer le crawl budget ?

Supprimez ou noindexez les pages de faible valeur, corrigez les erreurs d'exploration, améliorez les temps de réponse du serveur, soumettez un [sitemap XML](/glossary/xml-sitemap) à jour et construisez des liens internes vers les pages importantes. Facilitez la tâche à Googlebot pour trouver et accéder rapidement à votre meilleur contenu.

---

Vous publiez du contenu régulièrement ? Assurez-vous que Google puisse suivre. theStacc publie 30 articles optimisés SEO sur votre site chaque mois. Automatiquement. [Démarrez pour $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central : Gestion du crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central Blog : Ce que signifie le crawl budget](https://developers.google.com/search/blog/2017/01/what-crawl-budget-means-for-googlebot)
- [Ahrefs : Crawl budget et SEO](https://ahrefs.com/blog/crawl-budget/)
- [Moz : Crawl budget expliqué](https://moz.com/blog/crawl-budget)
