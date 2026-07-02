---
title: "Liens Dofollow vs Nofollow (2026) : stratégies, tactiques et exemples"
description: "Guide dofollow vs nofollow pour 2026 : stratégies, tactiques, exemples concrets et étapes d'implémentation pour obtenir des résultats plus rapidement."
slug: "dofollow-vs-nofollow"
keyword: "dofollow vs nofollow"
author: "Siddharth Gangal"
date: "2026-06-09"
category: "SEO Tips"
image: "/blogs-preview-images/dofollow-vs-nofollow.webp"
---

Chaque lien sur Internet appartient à l'une de ces deux catégories. Les liens dofollow transmettent une autorité de classement. Les liens nofollow indiquent à Google de ne pas considérer le lien comme un vote de confiance.

Comprendre la différence entre les liens dofollow et nofollow détermine la façon dont vous construisez des backlinks, structurez vos liens internes et auditez votre profil de liens. Si vous vous trompez, vous perdez des mois à poursuivre des liens qui ne font pas bouger les classements. Ou pire, vous déclenchez une pénalité Google en construisant un profil de liens artificiel.

89,4 % de tous les backlinks parmi les 110 000 meilleurs sites web sont des liens dofollow. Les 10,6 % restants sont des liens nofollow. Mais un profil de liens sain a besoin des deux types. Google s'attend à un mélange naturel.

Nous avons publié plus de 3 500 articles SEO dans plus de 70 secteurs. La stratégie de liens fait partie de chaque campagne. Ce guide couvre tout ce que vous devez savoir sur les liens dofollow et nofollow, y compris la mise à jour de 2019 de Google qui a changé la façon dont fonctionne le nofollow.

Voici ce que vous allez apprendre :

- La différence exacte entre les liens dofollow et nofollow
- Comment Google a transformé le nofollow d'une directive en "indice" en 2019
- Quand utiliser `rel="nofollow"`, `rel="sponsored"` et `rel="ugc"`
- Comment vérifier le statut d'un lien en quelques secondes
- Le ratio dofollow/nofollow idéal pour un profil naturel
- Les erreurs courantes qui déclenchent des pénalités Google

![Comparaison entre liens dofollow et nofollow et leur impact sur le SEO](/images/blog/dofollow-vs-nofollow-comparison.webp)

---

## Qu'est-ce qu'un lien Dofollow ?

Un lien dofollow est un lien HTML standard qui transmet du jus de lien (aussi appelé "link juice" ou PageRank) d'une page à une autre. Il n'existe pas d'attribut `rel="dofollow"` en HTML. "Dofollow" est un raccourci professionnel pour désigner un lien sans attribut nofollow.

Voici à quoi ressemble un lien dofollow en HTML :

```html
<a href="https://example.com">Texte d'ancrage</a>
```

Aucun attribut spécial n'est nécessaire. Tout lien est dofollow par défaut.

Lorsque Google explore un lien dofollow, 3 choses se produisent :

1. Google suit le lien vers la page de destination
2. Google transmet une partie de l'autorité de la page source à la destination
3. Google utilise le lien comme signal de classement pour la page de destination

Les liens dofollow sont le fondement de l'algorithme original PageRank de Google. Plus une page reçoit de liens dofollow provenant de sources faisant autorité, plus elle a tendance à bien se classer. [Les sites dotés de profils de backlinks solides](https://ahrefs.com/blog/backlink-growth-study/) reçoivent 67 % de trafic organique en plus que les sites aux profils faibles.

C'est pourquoi le netlinking reste l'une des parties les plus importantes (et les plus difficiles) du SEO. 41 % des marketeurs estiment que construire des [backlinks](/glossary_fr/backlinks) de qualité est la tâche SEO la plus ardue.

---

## Qu'est-ce qu'un lien Nofollow ?

Un lien nofollow inclut l'attribut `rel="nofollow"`. Cet attribut indique aux moteurs de recherche : "N'utilisez pas ce lien comme signal de classement."

Voici à quoi ressemble un lien nofollow en HTML :

```html
<a href="https://example.com" rel="nofollow">Texte d'ancrage</a>
```

Google a introduit l'attribut nofollow en 2005 pour lutter contre le spam dans les commentaires. Les spammeurs inondaient les commentaires de blogs et les forums de liens pour booster leurs classements. Le nofollow a donné aux propriétaires de sites un moyen de créer des liens sans transmettre d'autorité.

### Où les liens Nofollow apparaissent naturellement

La plupart des liens sur Internet sont nofollow par défaut sur ces plateformes :

- **Réseaux sociaux :** liens provenant de Facebook, X (Twitter), LinkedIn, Instagram, Pinterest et TikTok
- **Forums et communautés :** Reddit, Quora, Stack Overflow et la plupart des logiciels de forum
- **Commentaires de blog :** WordPress et la plupart des CMS ajoutent automatiquement le nofollow aux liens de commentaires
- **Wikipédia :** tous les liens externes sont en nofollow
- **Communiqués de presse :** la plupart des services de distribution de communiqués utilisent le nofollow
- **Annuaires générés par les utilisateurs :** Yelp, Google Business Profile et plateformes d'avis

Les liens nofollow ne boostent pas directement les classements. Mais ils servent d'autres objectifs. Ils génèrent du trafic de référence, renforcent la notoriété de la marque et signalent à Google que votre site dispose d'une diversité de liens naturelle.

---

## Dofollow vs Nofollow : les principales différences

La différence se résume à une seule question : le lien transmet-il une autorité de classement ?

| Caractéristique | Dofollow | Nofollow |
|---|---|---|
| Transmet du jus de lien | Oui | Non (mais Google peut outrepasser) |
| Attribut HTML | Aucun (comportement par défaut) | `rel="nofollow"` |
| Impact SEO direct | Oui. Améliore les classements | Aucun impact direct |
| Trafic de référence | Oui | Oui |
| Exploration Google | Toujours suivi et exploré | Peut ou non être exploré |
| Visibilité de la marque | Oui | Oui |
| Besoin pour un profil naturel | 60-80 % des liens totaux | 20-40 % des liens totaux |
| Risque de sur-optimisation | Élevé si 100 % dofollow | Faible |

Le détail critique que la plupart des guides passent sous silence : depuis 2019, Google traite le nofollow comme un "indice", et non comme une directive. Google peut choisir de suivre et de compter un lien nofollow si ses algorithmes estiment que le lien est pertinent et digne de confiance. Nous y reviendrons dans la section suivante.

> Les liens dofollow construisent l'autorité de classement. Les liens nofollow construisent un profil naturel. Vous avez besoin des deux.

---

## La mise à jour de 2019 de Google : le Nofollow est devenu un indice

Le 10 septembre 2019, Google a publié un article de blog intitulé ["Evolving nofollow"](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) qui a changé la façon dont fonctionnent les liens nofollow. Cette mise à jour est le développement le plus important en matière d'attribution de liens depuis plus d'une décennie. De nombreux guides SEO se trompent encore à ce sujet.

### Ce qui a changé

**Avant 2019 :** Le nofollow était une directive. Google lui obéissait absolument. Un lien nofollow ne transmettait aucune autorité, aucun signal d'exploration et aucun bénéfice de classement. Point final.

**Après 2019 :** Le nofollow est devenu un indice. Google se réserve le droit de considérer les liens nofollow comme des signaux de classement si ses algorithmes les jugent pertinents. Google peut également découvrir et indexer de nouvelles pages via des liens nofollow.

### Trois nouveaux attributs de lien

Google a introduit 2 nouveaux attributs aux côtés du nofollow :

| Attribut | Cas d'usage | Exemple |
|---|---|---|
| `rel="sponsored"` | Liens payants, publicités, parrainages | Liens d'affiliation, placements payants, liens de bannières publicitaires |
| `rel="ugc"` | Contenu généré par les utilisateurs | Commentaires de blog, messages de forum, soumissions communautaires |
| `rel="nofollow"` | Signal général "je n'approuve pas" | Tout lien pour lequel vous ne souhaitez pas vous porter garant |

Vous pouvez combiner les attributs : `rel="nofollow sponsored"` ou `rel="nofollow ugc"`. Google recommande d'utiliser l'attribut le plus spécifique possible.

![Évolution du nofollow Google de directive à indice avec les nouveaux attributs sponsored et ugc](/images/blog/google-nofollow-hint-evolution.webp)

### Ce que cela signifie en pratique

**Pour les créateurs de liens :** Les liens nofollow provenant de sites faisant autorité (Wikipédia, grandes publications, Reddit) peuvent désormais avoir une certaine valeur de classement. Vous ne devriez pas les ignorer.

**Pour les propriétaires de sites :** Utilisez `rel="sponsored"` sur les liens payants. Utilisez `rel="ugc"` sur les liens soumis par les utilisateurs. Utilisez `rel="nofollow"` sur tout lien en lequel vous n'avez pas confiance ou que vous n'approuvez pas. Les liens nofollow existants n'ont pas besoin d'être modifiés.

**Pour les auditeurs SEO :** Un [audit de backlinks](/blog_fr/backlink-audit-guide) devrait désormais analyser séparément les liens nofollow provenant de domaines à forte autorité. Ceux-ci peuvent contribuer aux classements même sans transmettre de jus de lien traditionnel.

78,8 % des professionnels du SEO estiment désormais que les liens nofollow affectent encore les classements dans une certaine mesure. Le modèle de "l'indice" signifie que le traitement du nofollow par Google n'est plus binaire.

---

> **Arrêtez d'écrire. Commencez à classer.** Stacc publie 30 articles SEO par mois pour 99 $. Chaque article renforce votre [autorité de domaine](/blog_fr/domain-authority-guide) grâce à des liens internes et externes.
> [Commencer pour 1 $ →](/pricing)

---

## Quand utiliser chaque type de lien

Savoir quand appliquer les attributs dofollow ou nofollow permet d'éviter les pénalités et de maximiser la valeur des liens.

### Quand utiliser le Dofollow (par défaut)

Laissez les liens en dofollow lorsque vous approuvez sincèrement la destination :

- **Liens éditoriaux dans votre propre contenu :** liens vers des sources, références et ressources que vous recommandez
- **Liens internes :** tous les [liens internes](/blog_fr/internal-linking-blog-posts) devraient être dofollow (avec de rares exceptions)
- **Liens de biographie d'auteur d'invité :** pratique standard pour les contributions d'invité légitimes
- **Liens de pages de ressources :** listes organisées d'outils, guides ou références en lesquels vous avez confiance
- **Liens de partenaires et fournisseurs :** lorsque la relation est authentique, et non payée

### Quand utiliser le Nofollow

Appliquez `rel="nofollow"` lorsque vous ne souhaitez pas vous porter garant de la destination :

- **Contenu non vérifié :** liens vers des sites que vous n'avez pas personnellement vérifiés
- **Sections de commentaires :** tout lien soumis par des utilisateurs (la plupart des CMS gèrent cela automatiquement)
- **Liens de connexion ou d'inscription :** Google n'a pas besoin d'explorer ces pages

### Quand utiliser rel="sponsored"

Appliquez `rel="sponsored"` sur tout lien impliquant un échange monétaire :

- **Liens d'affiliation :** recommandations de produits avec paramètres de suivi
- **Placements payants :** contenu sponsorisé, publicités rédactionnelles, inscriptions payantes dans des annuaires
- **Liens de bannières publicitaires :** publicités display liant vers des sites externes
- **Partenariats d'influence :** liens d'avis sur des produits avec compensation

Google a explicitement déclaré que ne pas marquer les liens payants avec `rel="sponsored"` ou `rel="nofollow"` peut entraîner une pénalité manuelle. Cela s'applique aux deux sites, celui qui fait le lien et celui qui est lié.

### Quand utiliser rel="ugc"

Appliquez `rel="ugc"` sur les liens créés par vos utilisateurs :

- **Commentaires de blog :** commentaires soumis par les utilisateurs contenant des liens
- **Messages de forum :** contenu généré par la communauté
- **Avis d'utilisateurs :** avis sur des produits ou services soumis par des clients
- **Contenu de type wiki :** pages modifiables par les membres de la communauté

### Arbre de décision rapide

| Scénario de lien | Attribut à utiliser |
|---|---|
| Vous l'avez écrit et approuvez la destination | Dofollow (aucun attribut) |
| Un utilisateur a soumis le lien | `rel="ugc"` |
| De l'argent a été échangé | `rel="sponsored"` |
| Vous ne faites pas confiance à la destination | `rel="nofollow"` |
| Lien interne au sein de votre propre site | Dofollow (aucun attribut) |
| Lien d'affiliation avec suivi | `rel="sponsored"` |

---

## Comment vérifier si un lien est Dofollow ou Nofollow

Vous pouvez vérifier le statut d'un lien de 3 manières. De l'inspection manuelle aux outils d'audit en masse.

### Méthode 1 : Inspecter l'élément (manuel)

Faites un clic droit sur n'importe quel lien dans votre navigateur et sélectionnez "Inspecter" ou "Inspecter l'élément". Regardez la balise `<a>` dans le HTML.

**Exemple dofollow :**
```html
<a href="https://example.com">Texte du lien</a>
```
Aucun attribut `rel="nofollow"` présent. Le lien est dofollow.

**Exemple nofollow :**
```html
<a href="https://example.com" rel="nofollow">Texte du lien</a>
```
L'attribut `rel="nofollow"` indique à Google de ne pas transmettre d'autorité.

Cette méthode fonctionne pour vérifier des liens individuels. Elle ne passe pas à l'échelle pour auditer un site entier.

### Méthode 2 : Extensions de navigateur (vérification rapide)

Installez une extension de navigateur qui met en évidence les types de liens automatiquement :

- **NoFollow** (Chrome) : met en évidence les liens nofollow avec une bordure rouge pointillée
- **SEOquake** (Chrome/Firefox) : affiche le statut de suivi dans une barre d'outils superposée
- **MozBar** (Chrome) : affiche les attributs des liens aux côtés des métriques DA/PA

Ces extensions fonctionnent sur n'importe quelle page web. Elles sont utiles pour une analyse rapide des concurrents et des vérifications ponctuelles de votre propre contenu.

### Méthode 3 : Outils d'exploration (audit en masse)

Pour un audit complet d'un site, utilisez un outil d'exploration pour analyser chaque lien :

- **Screaming Frog :** explore l'ensemble de votre site et exporte tous les liens avec leurs attributs
- **Ahrefs Site Audit :** identifie votre ratio dofollow/nofollow sur l'ensemble des pages
- **Semrush Backlink Audit :** analyse votre profil de liens entrants par statut de suivi

Un [audit SEO](/blog_fr/how-to-do-seo-audit) complet devrait inclure une analyse des attributs des liens. Cela révèle si votre profil semble naturel ou sur-optimisé.

---

## Construire un profil de liens naturel

Google s'attend à un mélange naturel de liens dofollow et nofollow. Un profil à 100 % dofollow signale une manipulation. Un profil avec trop de liens nofollow suggère une faible autorité.

### Le ratio idéal

| Type de profil | % Dofollow | % Nofollow | Niveau de risque |
|---|---|---|---|
| Naturel / Sain | 60-80 % | 20-40 % | Faible |
| Légèrement agressif | 80-90 % | 10-20 % | Moyen |
| Sur-optimisé | 90-100 % | 0-10 % | Élevé |
| Déficit d'autorité | Moins de 50 % | Plus de 50 % | Moyen |

La moyenne parmi les 110 000 meilleurs sites web est de 89,4 % dofollow et 10,6 % nofollow. Mais cette moyenne est biaisée vers le haut car les grands sites d'autorité attirent naturellement plus de liens éditoriaux dofollow.

![Ratios de profil de liens naturels montrant les pourcentages dofollow vs nofollow et les niveaux de risque](/images/blog/dofollow-nofollow-link-profile-ratio.webp)

Pour les petites et moyennes entreprises, une répartition 70/30 est un objectif sain. Atteignez ce ratio en construisant des liens dofollow de qualité grâce au contenu et au démarchage, tout en accumulant naturellement des liens nofollow via les réseaux sociaux, les forums et les annuaires.

### Comment construire des liens Dofollow

Les meilleurs liens dofollow proviennent de mentions éditoriales. Quelqu'un lit votre contenu, le trouve utile, et y fait un lien sans avoir été sollicité. Voici des stratégies qui génèrent des liens dofollow éditoriaux :

- **Publiez des études ou données originales.** Les études basées sur des données attirent les citations. Les journalistes et blogueurs font des liens vers des statistiques originales.
- **Créez des guides très utiles.** Les guides étape par étape qui résolvent de vrais problèmes gagnent des liens depuis des pages de ressources.
- **Développez des outils gratuits.** Un outil gratuit utile gagne des liens naturels de la part de quiconque le recommande. Consultez nos [outils SEO](/tools/seo-audit) pour des exemples.
- **Publiez des articles invités sur des sites pertinents.** Écrivez pour des sites de votre secteur. Incluez un lien dofollow naturel dans le corps de l'article (et pas seulement dans la biographie).
- **Réparez des liens cassés.** Trouvez des liens sortants cassés sur des sites d'autorité et proposez votre contenu comme remplacement. Cela s'appelle le [broken link building](/blog_fr/fix-broken-links).
- **Obtenez des mentions dans la presse.** Répondez aux demandes des journalistes sur des plateformes comme HARO, Connectively ou Qwoted.

### Comment gagner des liens Nofollow naturellement

Les liens nofollow s'accumulent via l'activité commerciale normale :

- Partagez votre contenu sur les réseaux sociaux (tous les liens sociaux sont nofollow)
- Participez à des discussions pertinentes sur Reddit et Quora
- Maintenez des fiches d'entreprise sur des annuaires et plateformes d'avis
- Encouragez les avis clients qui font un lien vers votre site
- Commentez sur des blogs de votre secteur avec des contributions authentiques (pas du spam)

---

> **Votre équipe SEO. 99 $ par mois.** 30 articles optimisés, publiés automatiquement. Chaque article gagne des backlinks et renforce votre [autorité thématique](/blog_fr/build-topical-authority) au fil du temps.
> [Commencer pour 1 $ →](/pricing)

---

## Erreurs courantes sur les liens Dofollow et Nofollow

Ces erreurs coûtent des classements et déclenchent parfois des pénalités. Évitez-les toutes.

**Erreur 1 : Mettre ses propres liens internes en nofollow.**
Les liens internes devraient presque toujours être dofollow. Ajouter du nofollow aux liens internes bloque la circulation du PageRank au sein de votre propre site. Cela s'appelle le "sculpting de PageRank", et [Google a confirmé en 2009](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) que cela ne fonctionne pas. Le PageRank qui aurait dû passer par un lien interne nofollow s'évapore. Il n'est pas redistribué aux autres liens.

**Erreur 2 : Construire 100 % de liens dofollow.**
Un profil entièrement dofollow semble artificiel. Les algorithmes de Google détectent les schémas non naturels. Un profil sain inclut des liens nofollow provenant de réseaux sociaux, d'annuaires et de contenu généré par les utilisateurs. Visez un ratio dofollow/nofollow de 70/30.

**Erreur 3 : Ne pas marquer les liens payants comme sponsorisés.**
Google exige `rel="sponsored"` ou `rel="nofollow"` sur tout lien impliquant un paiement. Ne pas marquer les liens payants peut entraîner une action manuelle contre les deux sites. Cela inclut les liens d'affiliation, les articles sponsorisés et les inscriptions payantes dans des annuaires.

**Erreur 4 : Ignorer les liens nofollow dans l'analyse des backlinks.**
Après la mise à jour de 2019, les liens nofollow provenant de domaines à forte autorité peuvent avoir une valeur de classement. Un [audit de backlinks](/blog_fr/backlink-audit-guide) complet devrait analyser les deux types de liens. Ignorer tous les liens nofollow, c'est manquer des signaux de classement potentiels.

**Erreur 5 : S'obséder sur les attributs de chaque lien individuel.**
Un lien dofollow provenant d'un site spam de faible autorité fait plus de mal que de bien. Un lien nofollow du New York Times génère des milliers de visiteurs de référence. La qualité et la pertinence comptent plus que le statut de suivi. Concentrez-vous sur l'obtention de liens provenant de sources pertinentes et faisant autorité, quel que soit leur politique nofollow.

**Erreur 6 : Utiliser le nofollow sur les liens éditoriaires sortants.**
Certains propriétaires de sites mettent tous les liens sortants en nofollow pour "conserver" leur PageRank. C'est inutile et potentiellement nuisible. Google s'attend à des liens sortants naturels. Mettre tous les liens externes en nofollow rend votre contenu suspect. Faites des liens dofollow vers des sources faisant autorité lorsque vous les approuvez sincèrement. Cela ne nuit pas à vos classements.

---

## Dofollow vs Nofollow et liens internes

Les liens internes méritent une attention particulière. Ils fonctionnent différemment des backlinks externes.

Chaque [lien interne](/blog_fr/internal-linking-blog-posts) de votre site devrait être dofollow. Les liens internes distribuent le PageRank entre vos pages. Ils aident Google à découvrir et indexer de nouveaux contenus. Ils signalent quelles pages vous considérez comme les plus importantes.

La seule exception : les pages de connexion, les paniers d'achat ou autres pages que vous ne souhaitez pas que Google priorise. Mais même celles-ci ont rarement besoin de nofollow. Google gère la plupart de ces cas via `robots.txt` et les balises `noindex`.

Une structure de liens internes solide multiplie la valeur de chaque backlink dofollow que votre site gagne. Lorsqu'un lien dofollow externe pointe vers votre page d'accueil, les liens internes distribuent cette autorité vers vos articles de blog, pages produits et pages de services.

Utilisez l'[optimisation du texte d'ancrage](/blog_fr/anchor-text-optimization) pour les liens internes. Un texte d'ancrage descriptif indique à Google le sujet de la page de destination. Évitez les expressions génériques comme "cliquez ici" ou "en savoir plus".

---

## La distinction entre Nofollow et Noindex

Les débutants confondent souvent nofollow et noindex. Ils servent des objectifs complètement différents.

| Attribut | Ce qu'il fait | Portée |
|---|---|---|
| `rel="nofollow"` | Indique à Google de ne pas transmettre d'autorité via un lien spécifique | Niveau du lien |
| `<meta name="robots" content="noindex">` | Indique à Google de ne pas inclure une page dans les résultats de recherche | Niveau de la page |

Un lien nofollow permet toujours à Google de voir et potentiellement d'explorer la page de destination. Cela affecte seulement le fait que l'autorité passe ou non via ce lien spécifique.

Une balise noindex masque une page entière des résultats de recherche. La page existe toujours et se charge pour les visiteurs. Mais Google la retire de l'index.

Ces deux attributs résolvent des problèmes différents. Utilisez nofollow lorsque vous ne souhaitez pas qu'un lien transmette de l'autorité. Utilisez noindex lorsque vous ne souhaitez pas qu'une page apparaisse dans les résultats de recherche. Ils peuvent être utilisés ensemble sur la même page pour un contrôle maximal.

Pour en savoir plus sur la façon dont Google gère les directives d'indexation, consultez notre [checklist de SEO technique](/blog_fr/technical-seo-checklist).

---

> **Plus de 3 500 blogs publiés. Score SEO moyen de 92 %.** Découvrez ce que Stacc peut faire pour votre stratégie de netlinking. Nous publions du contenu qui gagne des backlinks.
> [Commencer pour 1 $ →](/pricing)

---

## FAQ

**Quelle est la différence entre les liens dofollow et nofollow ?**

Un lien dofollow transmet une autorité de classement (PageRank) d'une page à une autre. Un lien nofollow inclut `rel="nofollow"` qui indique à Google de ne pas le compter comme un signal de classement. Le dofollow améliore directement le SEO. Le nofollow génère du trafic et de la visibilité de marque sans impact direct sur le classement.

**Les liens nofollow aident-ils le SEO ?**

Les liens nofollow ne transmettent pas directement d'autorité de classement. Mais ils contribuent à un profil de liens naturel, génèrent du trafic de référence et renforcent la notoriété de la marque. Depuis la mise à jour de 2019 de Google, le nofollow est un "indice" plutôt qu'une directive. Google peut choisir de compter certains liens nofollow comme des signaux de classement. 78,8 % des professionnels du SEO estiment que les liens nofollow affectent encore les classements.

**Quel est le ratio idéal entre liens dofollow et nofollow ?**

Un profil de liens sain contient 60 à 80 % de liens dofollow et 20 à 40 % de liens nofollow. La moyenne parmi les meilleurs sites web est de 89,4 % dofollow. Pour les petites et moyennes entreprises, une répartition 70/30 signale un profil naturel et organique. Un profil à 100 % dofollow semble artificiel et risque de déclencher des pénalités Google.

**Les liens des réseaux sociaux sont-ils dofollow ou nofollow ?**

Toutes les grandes plateformes de réseaux sociaux utilisent des liens nofollow. Cela inclut Facebook, X (Twitter), LinkedIn, Instagram, Pinterest et TikTok. Les liens des réseaux sociaux ne transmettent pas d'autorité de classement directe. Ils génèrent cependant du trafic de référence et contribuent à votre pourcentage de liens nofollow.

**Quelle est la différence entre nofollow et noindex ?**

Nofollow est un attribut au niveau du lien qui empêche l'autorité de passer via un lien spécifique. Noindex est une directive au niveau de la page qui empêche une page entière d'apparaître dans les résultats de recherche. Ils résolvent des problèmes différents. Utilisez nofollow sur les liens que vous n'approuvez pas. Utilisez noindex sur les pages que vous ne souhaitez pas indexer.

**Devrais-je mettre tous les liens sortants en nofollow ?**

Non. Mettre tous les liens sortants en nofollow est inutile et semble artificiel. Faites des liens dofollow vers des sources faisant autorité lorsque vous approuvez sincèrement le contenu. Google s'attend à des liens sortants naturels. Utilisez le nofollow uniquement sur les liens en lesquels vous n'avez pas confiance, les liens payants ou le contenu généré par les utilisateurs.

**Que sont rel="sponsored" et rel="ugc" ?**

Google a introduit ces attributs en septembre 2019 aux côtés du changement de statut du nofollow en "indice". Utilisez `rel="sponsored"` sur tout lien impliquant un échange monétaire (liens d'affiliation, placements payants, parrainages). Utilisez `rel="ugc"` sur le contenu généré par les utilisateurs (commentaires, messages de forum, avis). Les deux indiquent à Google de ne pas transmettre d'autorité de classement via le lien.

---

Les liens dofollow et nofollow servent des objectifs différents. Les deux sont essentiels pour une stratégie SEO saine. Construisez des liens dofollow pour l'autorité de classement. Gagnez des liens nofollow pour le trafic, la diversité et les signaux naturels. Surveillez votre ratio, marquez correctement les liens payants, et rappelez-vous que Google traite le nofollow comme un indice, et non comme un ordre.
