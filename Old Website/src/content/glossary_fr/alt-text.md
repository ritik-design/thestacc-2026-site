---
term: "Texte alternatif (alt text)"
slug: "alt-text"
definition: "Le texte alternatif (alt text) décrit les images pour les moteurs de recherche et les lecteurs d'écran. Apprenez à rédiger un texte alternatif efficace, des exemples et pourquoi il importe pour le SEO."
category: "SEO"
difficulty: "Beginner"
keyword: "texte alternatif"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## Qu'est-ce que le texte alternatif ?

Le texte alternatif (alt text) est un attribut HTML qui fournit une description écrite d'une image. Utilisé par les lecteurs d'écran pour les utilisateurs malvoyants et par les moteurs de recherche pour comprendre ce qu'une image montre.

Vous l'avez probablement vu dans le code : `<img src="photo.jpg" alt="description ici">`. Cette description est le texte alternatif. Il sert deux audiences simultanément. Pour les personnes qui ne peuvent pas voir l'image. Qu'elles utilisent un lecteur d'écran, aient une connexion lente ou que l'image ne charge pas. Le texte alt leur dit ce qui est là. Pour Google, c'est l'un des principaux signaux utilisés pour indexer et classer les images dans Google Images.

L'analyse d'accessibilité 2024 de WebAIM a trouvé que 54,5 % des images sur le web n'ont pas de texte alternatif. Plus de la moitié. C'est à la fois un échec d'[accessibilité](/glossary/accessibility-content) et une opportunité SEO juste là pour quiconque est prêt à remplir un champ texte.

## Pourquoi le texte alternatif est-il important ?

Le texte alt est à l'intersection de l'accessibilité, du [SEO](/glossary/seo) et de l'expérience utilisateur. Ignorez-le et vous perdez sur les trois fronts.

- **Conformité d'accessibilité**. Les lignes directrices ADA et WCAG 2.1 exigent du texte alt sur les images significatives. Les poursuites pour accessibilité web ont augmenté de plus de 300 % depuis 2018. Ce n'est pas optionnel.
- **Trafic de recherche d'images**. Google Images génère un [trafic organique](/glossary/organic-traffic) significatif. Sans texte alt, Google ne peut pas indexer correctement vos images, et vous manquez ce trafic entièrement.
- **Signaux de [SEO On-Page](/glossary/on-page-seo)**. Le texte alt donne à Google un contexte supplémentaire sur le contenu de votre page. Un article sur la rénovation de cuisine avec des images correctement décrites renforce la pertinence thématique de la page.
- **Solution de repli quand les images cassent**. Si une image ne charge pas (connexion lente, URL cassée, clients e-mail bloquant les images), le texte alt apparaît à sa place. Les utilisateurs comprennent encore ce qui était censé être là.

Chaque image de votre site devrait avoir du texte alt. Les images décoratives (bordures, espaceurs) reçoivent un attribut alt vide (`alt=""`). Tout le reste reçoit une description.

## Comment fonctionne le texte alternatif

Écrire du texte alt est simple en concept. Bien le faire requiert de comprendre ce que différents systèmes en ont besoin.

### Comment les lecteurs d'écran l'utilisent

Quand un lecteur d'écran rencontre une image, il lit le texte alt à voix haute. Si le texte alt dit « photo de stock de réunion d'affaires », c'est ce que l'utilisateur entend. Inutile. S'il dit « 5 membres d'équipe examinant un rapport marketing autour d'une table de conférence », l'utilisateur comprend le contexte. Écrivez pour la personne qui écoute, pas pour un moteur de recherche.

### Comment Google l'utilise

Googlebot ne peut pas « voir » les images comme les humains. Il s'appuie sur le texte alt, le texte environnant, les noms de fichiers et les données structurées pour comprendre le contenu d'image. La propre documentation de Google indique que le texte alt est « extrêmement utile » pour le classement Google Images. C'est l'un des signaux de [SEO d'image](/glossary/image-seo) les plus forts que vous pouvez contrôler.

### L'implémentation HTML

Le texte alt vit dans l'attribut `alt` de la balise `<img>` :

`<img src="reception-cabinet-dentaire.jpg" alt="Réception moderne de cabinet dentaire avec personnel d'accueil saluant un patient">`

La plupart des plateformes CMS (WordPress, Webflow, Ghost) ont des champs de texte alt dédiés dans leurs interfaces de téléchargement d'images. Vous n'avez pas besoin d'éditer le HTML directement.

### Que se passe-t-il sans texte alt

Si une image n'a pas du tout d'attribut alt, les lecteurs d'écran peuvent lire le nom de fichier à la place. Quelque chose comme « IMG_4392.jpg ». Inutile. Si l'attribut alt est présent mais vide (`alt=""`), les lecteurs d'écran sautent l'image entièrement, ce qui est un comportement correct pour les images décoratives mais incorrect pour celles significatives.

## Types de texte alt

Toutes les images n'ont pas besoin du même traitement :

- **Texte alt informatif**. Décrit ce que l'image montre et pourquoi cela compte. Utilisé pour photos, illustrations, graphiques et éléments graphiques qui transmettent de l'information. « Graphique à barres montrant une augmentation de 40 % du trafic organique de janvier à juin 2025. »
- **Texte alt fonctionnel**. Décrit ce qu'une image cliquable fait. Utilisé pour boutons, icônes et images liées. « Bouton de recherche » ou « Télécharger le rapport PDF. »
- **Texte alt décoratif (vide)**. Utilisé pour images purement décoratives qui n'ajoutent aucune information. Définissez `alt=""` pour que les lecteurs d'écran les sautent. Les motifs d'arrière-plan, lignes de division et icônes décoratives entrent ici.
- **Texte alt complexe**. Utilisé pour graphiques, courbes et infographies contenant des données denses. Le texte alt fournit un résumé, et une description plus longue va dans un attribut `longdesc` ou texte à proximité.

Bien choisir le type compte. Sur-décrire les images décoratives encombre l'expérience du lecteur d'écran. Sous-décrire les images informatives perd à la fois la valeur d'accessibilité et SEO.

## Exemples de texte alt

**Exemple 1 : La page menu d'un restaurant**
Mauvais texte alt : « nourriture » ou « photo de plat » ou aucun texte alt. Bon texte alt : « Saumon grillé avec légumes rôtis et sauce au beurre citronné servi sur une assiette blanche. » La version descriptive aide Google à classer l'image pour les recherches « saumon grillé » et aide les utilisateurs malvoyants à comprendre le plat du menu.

**Exemple 2 : Une annonce immobilière**
Mauvais : « extérieur de maison ». Bon : « Maison coloniale à deux étages avec façade en briques rouges, colonnes blanches et jardin paysager au 123 rue Principale. » Une victoire de [SEO local](/glossary/local-seo). La description détaillée inclut des caractéristiques de propriété qui correspondent à ce que les acheteurs cherchent dans Google Images.

**Exemple 3 : Une page produit e-commerce**
Mauvais : « image produit 1 ». Bon : « Chaussure de running Nike Air Max 90 en blanc et gris, vue de côté. » Ce texte alt inclut la marque, le nom du produit, la couleur et l'angle. Exactement ce dont Google a besoin pour la faire apparaître dans Shopping et les résultats de recherche d'images. Utiliser le contenu blog publié par theStacc avec des images produit correctement optimisées crée une base solide de [SEO On-Page](/glossary/on-page-seo).

## Texte alt vs. texte de titre

Ces deux sont confondus constamment, mais servent à des objectifs complètement différents.

| | Texte alt | Texte de titre |
|---|---|---|
| **Objectif** | Décrit l'image pour accessibilité et SEO | Fournit info supplémentaire au survol |
| **Requis** | Oui (conformité WCAG) | Non |
| **Impact SEO** | Fort (signal principal de classement d'image) | Minimal |
| **Lecteur d'écran** | Lu à voix haute automatiquement | Parfois lu, dépend des paramètres |
| **Visibilité** | Affiché quand l'image ne charge pas | Affiché en infobulle au survol de souris |

Le texte alt est obligatoire. Le texte de titre est optionnel et principalement cosmétique. Concentrez votre effort sur le texte alt.

## Bonnes pratiques pour le texte alt

- **Soyez spécifique et concis**. Décrivez ce qu'il y a dans l'image en 125 caractères ou moins. Les lecteurs d'écran peuvent couper les descriptions plus longues. « Golden retriever attrapant un frisbee dans un parc » bat « chien » à chaque fois.
- **Incluez des mots-clés naturellement, pas de force**. Si l'image est sur une page sur la [recherche de mots-clés](/glossary/keyword-research) et que l'image montre un outil d'analyse de mots-clés, mentionnez-le. Mais ne bourrez pas : « recherche mots-clés outil mots-clés meilleure recherche SEO mots-clés » est du spam.
- **Ne commencez pas par « image de » ou « photo de »**. Les lecteurs d'écran annoncent déjà que c'est une image. Commencer par « image de » est redondant. Sautez direct à la description.
- **Décrivez la fonction pour les images cliquables**. Si une image est un lien ou bouton, le texte alt devrait décrire l'action, pas l'image. Une icône loupe qui déclenche la recherche devrait avoir `alt="Rechercher"`. Pas `alt="loupe"`.
- **Automatisez quand possible**. Lors de la publication à grande échelle, maintenir un texte alt cohérent devient difficile. theStacc inclut un texte alt optimisé dans chaque article publié, donc les images sont accessibles et prêtes pour le SEO dès le premier jour.

## Questions fréquentes

### Quelle longueur devrait avoir le texte alt ?

Restez sous 125 caractères. La plupart des lecteurs d'écran coupent le texte alt autour de cette longueur. Pour des images complexes comme des infographies, fournissez un bref résumé en alt et ajoutez une description plus longue dans le contenu environnant de la page.

### Le texte alt affecte-t-il les classements Google ?

Oui. Le texte alt est un facteur de classement confirmé pour Google Images et fournit un contexte de soutien pour les classements de recherche web. La documentation Search Central de Google recommande explicitement d'écrire du texte alt descriptif pour le [SEO On-Page](/glossary/on-page-seo).

### Chaque image doit-elle avoir du texte alt ?

Chaque image significative a besoin de texte alt. Les images décoratives (espaceurs, motifs d'arrière-plan, fioritures visuelles) devraient avoir des attributs alt vides (`alt=""`) pour que les lecteurs d'écran les sautent. La question clé : cette image transmet-elle de l'information ? Si oui, décrivez-la.

### Le texte alt peut-il être trop long ?

Oui. Un texte alt excessivement long est frustrant pour les utilisateurs de lecteurs d'écran et peut ressembler à du [keyword stuffing](/glossary/keyword-stuffing) pour Google. Gardez les descriptions concentrées. Si une image a besoin d'un paragraphe d'explication, mettez-le dans le texte du corps près de l'image. Pas dans l'attribut alt.

---

Vous voulez chaque article de blog publié avec un texte alt approprié, des [balises de titre](/glossary/heading-tags) et un SEO on-page intégré ? theStacc publie 30 articles optimisés SEO sur votre site chaque mois. Automatiquement. [Démarrez pour $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central : Bonnes pratiques de SEO d'image](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM : Guide du texte alternatif](https://webaim.org/techniques/alttext/)
- [WebAIM : Le WebAIM Million (Rapport annuel d'accessibilité)](https://webaim.org/projects/million/)
- [W3C : Exigences d'image WCAG 2.1](https://www.w3.org/WAI/tutorials/images/)
- [Moz : Guide du SEO d'image](https://moz.com/learn/seo/image-seo)
