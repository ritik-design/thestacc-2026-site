---
term: "Schema Markup"
slug: "schema-markup"
definition: "Le Schema Markup est un code standardisé (généralement JSON-LD) ajouté à vos pages pour que les moteurs comprennent votre contenu et affichent des résultats enrichis."
category: "SEO"
difficulty: "Intermediate"
keyword: "qu'est-ce que schema markup"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "rich-results"
  - "serp"
  - "technical-seo"
  - "json-ld"
  - "e-e-a-t"
---

## Qu'est-ce que le Schema Markup ?

**Le Schema Markup est un vocabulaire de données structurées que vous ajoutez à votre HTML pour indiquer aux moteurs de recherche ce que représente exactement votre contenu : un produit, une recette, un événement, une entreprise, une FAQ.**

Sans schema, Google doit deviner de quoi parle votre page. Avec schema, vous lui tendez un schéma annoté. Le balisage suit le standard Schema.org, maintenu conjointement par Google, Microsoft, Yahoo et Yandex.

Une étude de Milestone Research a montré que les pages avec schema markup se positionnent en moyenne 4 places plus haut que celles qui n'en ont pas. Pas parce que schema est un facteur de classement direct – Google a dit que ce n'était pas le cas. Mais les [résultats enrichis](/glossary/rich-results) générés par schema font grimper le taux de clics de façon spectaculaire, et un meilleur CTR finit par influencer les classements dans la durée.

## Pourquoi les données structurées comptent-elles ?

La plupart des sites n'utilisent toujours pas schema. Une opportunité pour qui veut bien y consacrer 30 minutes.

- **Résultats enrichis dans la recherche**. Étoiles d'avis, FAQ déroulantes, fourchettes de prix et dates d'événements apparaissent directement dans la [SERP](/glossary/serp). Ces éléments visuels peuvent augmenter le CTR de 20 à 30 %.
- **Meilleure visibilité IA**. Les AI Overviews de Google et les autres expériences pilotées par l'IA tirent leur contenu des données structurées. Schema rend votre contenu plus facile à citer pour les machines.
- **Présence locale renforcée** – le [schema LocalBusiness](/glossary/localbusiness-schema) transmet horaires, adresse et avis directement aux Knowledge Panels de Google et au [local pack](/glossary/local-pack).
- **Prêt pour la recherche vocale**. Quand quelqu'un pose une question à un assistant vocal, les données structurées aident votre réponse à remonter. FAQ et How-To schema sont particulièrement précieux ici.

Si vous investissez dans du contenu [SEO](/glossary/seo) sans ajouter schema, vous laissez de la visibilité sur la table.

## Comment fonctionne le Schema Markup

Schema se loge dans le HTML de votre page. Les robots le lisent, le valident et s'en servent pour générer des résultats de recherche enrichis.

### Le format du code

Trois formats existent : JSON-LD, Microdata et RDFa. Google recommande JSON-LD. C'est un bloc de script que vous déposez dans la section `<head>`. Il ne se mélange pas à votre HTML visible, ce qui le rend plus simple à gérer et moins susceptible de casser votre mise en page.

### Le processus de validation

Une fois schema ajouté, le rapport Résultats enrichis de la Google Search Console indique si votre balisage est valide. Les erreurs – champs requis manquants, types incorrects – empêchent l'apparition des résultats enrichis. L'outil Rich Results Test de Google permet de vérifier des URLs individuelles avant un déploiement à l'échelle du site.

### Comment Google le restitue

Googlebot explore votre page, analyse le JSON-LD et le confronte aux types de schema connus. Si tout est conforme et que la page respecte les directives qualité, le listing enrichi apparaît dans la recherche en quelques jours à quelques semaines. Tout schema valide ne déclenche pas un résultat enrichi. Google tranche en fonction du contexte de la requête et de la qualité de la page.

## Types de Schema Markup

Schema.org liste plus de 800 types. Mais pour la plupart des entreprises, une poignée couvre 90 % des cas :

- **Article schema**. Indique à Google qu'il s'agit d'un article de blog ou d'actualité. Aide pour Google Discover et les carrousels d'actualités.
- **FAQ schema**. Ajoute des paires question-réponse repliables directement dans votre listing. Fort impact pour les requêtes informationnelles.
- **LocalBusiness schema**. Transmet le nom, l'adresse, les horaires et les avis à Google. Indispensable pour le [SEO local](/glossary/local-seo).
- **Product schema**. Affiche prix, disponibilité et notes dans la recherche. Critique pour l'eCommerce.
- **How-To schema**. Montre des instructions étape par étape avec images dans les résultats. Très efficace pour le contenu tutoriel.
- **Review/Rating schema**. Les étoiles jaunes que vous voyez dans les résultats. Augmentent nettement le CTR.

Le bon schema dépend du type de page. La page de service d'un plombier a besoin de LocalBusiness. Un article de blog a besoin d'Article et éventuellement de FAQ.

## Exemples de Schema Markup

**Exemple 1 : Cabinet dentaire avec FAQ schema**
Une dentiste à Lyon ajoute du FAQ schema à sa page de service « Blanchiment dentaire » avec 5 questions fréquentes des patients. Son listing dans la recherche affiche désormais des Q&A repliables, occupant 3 fois plus d'espace visuel que ses concurrents. Les clics vers cette page bondissent de 35 % en 2 mois.

**Exemple 2 : Société de climatisation avec LocalBusiness schema**
Une entreprise de chauffage et climatisation ajoute du LocalBusiness schema avec zone d'intervention, horaires et note agrégée (4,8 étoiles sur plus de 200 avis). Google affiche les étoiles directement dans les résultats organiques – pas seulement dans le map pack. La société constate une hausse nette des appels depuis la recherche organique.

**Exemple 3 : Blog SaaS avec Article schema**
Un éditeur de logiciels B2B publie chaque semaine des guides how-to. Après l'ajout d'Article schema avec informations sur l'auteur et dates de publication, ses articles apparaissent dans Google Discover. Le trafic Discover ajoute à lui seul 15 % aux visites organiques mensuelles.

## Schema Markup vs. Rich Snippets

On utilise ces termes de manière interchangeable. À tort.

| | Schema Markup | Rich Snippets / Résultats enrichis |
|---|---|---|
| **Ce que c'est** | Du code que vous ajoutez à vos pages | Des listings améliorés affichés par Google |
| **Qui le contrôle** | Vous (le webmaster) | Google (décide de les afficher ou non) |
| **Garanti ?** | Vous pouvez toujours ajouter le balisage | Google peut afficher les résultats enrichis ou non |
| **Objectif** | Communiquer le sens de la page aux robots | Améliorer l'apparence visuelle dans les [SERP](/glossary/serp) |
| **Exemple** | Script JSON-LD dans votre HTML | Étoiles d'avis sous votre listing |

Le schema markup est l'entrée. Les résultats enrichis sont la sortie (possible). Ajouter du balisage ne garantit pas un listing amélioré. Mais sans cela, vous n'en aurez jamais.

## Bonnes pratiques pour le Schema Markup

- **Commencer par l'essentiel**. N'essayez pas d'ajouter tous les types de schema d'un coup. Vous êtes un commerce local ? Démarrez par LocalBusiness et FAQ. Vous étofferez ensuite.
- **Utiliser JSON-LD, pas Microdata**. Google le préfère. Plus simple à implémenter, plus facile à déboguer, et il ne pollue pas votre HTML.
- **Valider chaque page**. Faites passer tout nouveau schema dans le Rich Results Test de Google avant publication. Un seul champ manquant peut invalider tout le bloc.
- **Garder le schema exact**. Si vos horaires changent, mettez le schema à jour. Des données structurées erronées enfreignent les directives de Google et peuvent vous faire perdre vos résultats enrichis.
- **Associer schema et contenu de qualité**. Schema sur des pages pauvres ne génère pas de résultats enrichis. Des services comme theStacc publient 30 articles optimisés SEO par mois. Chacun est une occasion d'ajouter Article et FAQ schema qui méritent vraiment des rich results.

## Questions fréquentes

### Le schema markup est-il un facteur de classement ?

Google dit que schema n'est pas un facteur de classement direct. Mais les pages avec schema obtiennent des [résultats enrichis](/glossary/rich-results), qui boostent le CTR. Un meilleur CTR envoie des signaux d'engagement positifs, qui peuvent améliorer les classements de manière indirecte.

### Comment ajouter schema à mon site web ?

La méthode la plus simple est JSON-LD : un bloc script dans la section `<head>` de votre page. Des plugins WordPress comme Yoast et RankMath le génèrent automatiquement. Pour des sites sur mesure, utilisez le Structured Data Markup Helper de Google.

### Schema fonctionne-t-il pour les petites entreprises ?

Absolument. Les commerces locaux voient souvent l'impact le plus important parce que LocalBusiness et FAQ schema sont sous-utilisés par les petits concurrents. Ajouter un schema basique à un site local de 10 pages prend moins d'une heure.

### Combien de temps avant de voir des résultats enrichis ?

Après l'ajout d'un schema valide, Google le traite généralement en quelques jours à 2 semaines. Suivez le statut dans le rapport Résultats enrichis de la Google Search Console.

---

Vous voulez du contenu SEO optimisé et publié sans lever le petit doigt ? theStacc publie 30 articles sur votre site chaque mois. Automatiquement. [Démarrer pour $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central : Comprendre le fonctionnement des données structurées](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
- [Milestone Research : Impact du Schema Markup sur les classements](https://www.milestoneinternet.com/thought-leadership/research/schema-markup-drives-results)
- [Moz : Le guide débutant des données structurées](https://moz.com/blog/beginners-guide-to-structured-data)
