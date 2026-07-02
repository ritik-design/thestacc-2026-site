---
title: "Comment configurer des redirections 301 (étape par étape)"
description: "Apprenez à configurer des redirections 301 pour le SEO. Couvre WordPress, .htaccess, Nginx, Shopify et Cloudflare. Avec les étapes de test. Mis à jour mars 2026."
slug: "301-redirects-guide"
keyword: "redirections 301"
author: "Siddharth Gangal"
date: "2026-04-26"
category: "SEO Tips"
image: "/blogs-preview-images/301-redirects-guide.webp"
---

Vous avez changé une URL. Peut-être que vous avez migré vers un nouveau domaine. Peut-être que vous avez consolidé 3 pages en 1. Maintenant les visiteurs tombent sur une erreur 404, et Google fait chuter vos classements du jour au lendemain.

Chaque URL cassée fait fuir le link equity que vous avez mis des mois à accumuler. Les utilisateurs repartent. Google signale votre site comme mal entretenu. Une seule migration sans redirections 301 peut effacer 40 % ou plus de votre trafic organique en une semaine.

Ce guide vous accompagne en 7 étapes pour configurer correctement des redirections 301. Vous apprendrez le processus exact pour WordPress, Apache `.htaccess`, Nginx, Shopify et Cloudflare. Sans approximations. Sans liens cassés. Sans perte de classement.

Nous publions plus de 3 500 articles sur plus de 70 secteurs d'activité. Les changements d'URL, les consolidations de pages et les migrations de domaines font partie de notre quotidien. Les étapes ci-dessous sont exactement celles que nous appliquons pour nos propres sites et ceux de nos clients.

Voici ce que vous allez apprendre :

- Comment trouver chaque URL nécessitant une redirection
- Comment faire correspondre les anciennes URL à leurs nouvelles destinations correctes
- Comment implémenter des redirections 301 sur 5 plateformes différentes
- Comment corriger les chaînes et les boucles de redirections avant qu'elles ne pénalisent votre vitesse
- Comment tester les redirections avant et après la mise en ligne
- Comment surveiller l'état des redirections dans Google Search Console

---

## Vue d'ensemble

- **Temps requis :** 10 à 30 minutes (selon le nombre de redirections)
- **Difficulté :** Débutant à Intermédiaire
- **Ce dont vous avez besoin :** Accès à votre CMS, panneau d'hébergement ou fichiers de configuration serveur

---

## Qu'est-ce qu'une redirection 301 ?

Un code de statut `301` indique aux navigateurs et aux moteurs de recherche qu'une page a été définitivement déplacée vers une nouvelle URL. Le navigateur envoie automatiquement les visiteurs vers la nouvelle adresse. Google transfère le link equity de l'ancienne URL vers la nouvelle.

Avant 2016, les redirections 301 entraînaient une perte de PageRank d'environ 15 % par saut. Ce n'est plus le cas aujourd'hui. [Google a confirmé que les redirections 30x ne diluent plus le PageRank](https://searchengineland.com/google-no-pagerank-dilution-using-301-302-30x-redirects-anymore-254608). Aujourd'hui, un `301` correctement configuré transfère 90 à 99 % du link equity selon Moz.

Cela fait des redirections 301 l'outil le plus important pour préserver votre SEO lors de tout changement d'URL. Si vous les ignorez, vous repartez de zéro.

---

## Étape 1 : Identifier les URL qui nécessitent des redirections

Vous ne pouvez pas rediriger ce que vous n'avez pas trouvé. La première étape consiste à dresser une liste complète des URL qui renvoient des erreurs ou qui ont changé.

Commencez par **Google Search Console**. Accédez au rapport Pages et filtrez par « Non trouvé (404) ». Cela affiche chaque URL que Google a tenté d'explorer sans succès. Exportez la liste complète.

Ensuite, consultez **Google Analytics** (GA4). Examinez le rapport Pages de destination pour les pages qui ont soudainement perdu du trafic. Une chute brutale après un changement d'URL est un signal fort qu'une redirection est manquante.

Lancez une **exploration de site** avec un outil comme Screaming Frog, Sitebulb ou Ahrefs Site Audit. Ces outils détectent les liens internes cassés, les pages orphelines et les réponses 404 que Google Search Console pourrait manquer. Un [audit SEO](/blog/how-to-do-seo-audit) complet fera remonter ces problèmes rapidement.

Trois scénarios courants qui nécessitent des redirections 301 :

1. **Changement de slug d'URL.** Vous avez renommé `/blog/ancien-article` en `/blog/nouvel-article`
2. **Migration de domaine.** Vous avez déménagé de `anciensite.com` vers `nouveausite.com`
3. **Consolidation de pages.** Vous avez fusionné 3 pages légères en 1 page plus solide pour [corriger le contenu léger](/blog/fix-thin-content)

### Quand utiliser 301 vs 404 vs 410 vs Canonical

Toutes les URL mortes ne nécessitent pas forcément une redirection. Utilisez ce cadre de décision.

| Scénario | Action | Pourquoi |
|---|---|---|
| Page déplacée vers une nouvelle URL | Redirection `301` | Préserve le link equity et l'expérience utilisateur |
| Page supprimée, pas de remplacement | `410` Gone | Indique à Google de désindexer plus vite qu'un `404` |
| Page supprimée, susceptible de revenir | `404` Not Found | Réponse standard pour les pages temporairement manquantes |
| Contenu dupliqué, les deux pages restent en ligne | Balise `canonical` | Consolide les signaux sans supprimer la page |
| Ancien domaine vers nouveau domaine | Redirection `301` (au niveau du domaine) | Transfère tout le link equity vers le nouveau domaine |

![Quand utiliser les redirections 301 vs 404 vs 410 vs canonical](/images/blog/301-redirect-decision-framework.webp)

**Pourquoi cette étape est importante :** Les redirections manquantes sont invisibles. Les utilisateurs voient une 404 et repartent. Google voit une URL morte et la retire de l'index. Vous perdez des classements sans aucun avertissement dans votre tableau de bord analytique.

**Conseil pro :** Exportez votre sitemap XML complet avant d'effectuer tout changement d'URL. Comparez-le avec l'exploration post-modification pour détecter chaque écart.

---

## Étape 2 : Cartographier les anciennes URL vers leurs nouvelles destinations

Une redirection ne vaut que ce que vaut sa destination. Envoyer toutes les anciennes URL vers la page d'accueil est une erreur courante. Google traite les redirections vers la page d'accueil depuis des pages profondes comme des [soft 404s](https://developers.google.com/search/docs/crawling-indexing/301-redirects). Vous perdez le link equity quand même.

Créez une feuille de calcul avec 4 colonnes :

| Ancienne URL | Nouvelle URL | Type de redirection | Notes |
|---|---|---|---|
| `/blog/ancien-guide-seo` | `/blog/guide-seo-on-page` | 301 | Contenu fusionné |
| `/services/web-design` | `/services/design` | 301 | Slug raccourci |
| `/blog/article-obsolete` | , | 410 | Pas de remplacement |

Respectez ces règles de cartographie :

- **Pointez toujours vers la page la plus pertinente.** Faites correspondre le sujet et l'intention, pas seulement la catégorie.
- **Pour les migrations de domaine, reproduisez la structure d'URL.** Si `/a-propos` existait sur l'ancien domaine, redirigez-le vers `/a-propos` sur le nouveau domaine.
- **Regroupez les redirections par type.** Les changements d'URL en masse (comme la suppression de `/blog/` des chemins) peuvent utiliser des règles basées sur des patterns plutôt que des entrées individuelles.
- **Signalez les pages avec un grand nombre de backlinks.** Utilisez Ahrefs ou le rapport Liens de Google Search Console pour identifier vos pages les plus liées. Ce sont les priorités absolues pour une cartographie précise.

Un [audit de contenu](/blog/how-to-content-audit) vous aide à identifier quelles pages consolider et lesquelles abandonner. Effectuez-le avant de commencer la cartographie.

**Pourquoi cette étape est importante :** Les mauvaises correspondances envoient les utilisateurs et le link equity vers des pages non pertinentes. Google remarque le décalage et peut ignorer complètement la redirection. Une mauvaise correspondance peut défaire des mois d'[autorité thématique](/blog/build-topical-authority) construite autour d'un cluster de mots-clés.

---

## Étape 3 : Configurer les redirections 301 sur votre plateforme

L'implémentation dépend de votre stack technique. Vous trouverez ci-dessous les instructions exactes pour 5 plateformes.

### WordPress (méthode par plugin)

L'option la plus rapide pour les sites WordPress. Trois plugins gèrent bien les redirections :

- **Redirection** (gratuit). Le plugin de redirection le plus populaire. Prend en charge les regex, enregistre les 404 et importe des fichiers CSV.
- **Rank Math** (gratuit/pro). Gestionnaire de redirections intégré dans Rank Math > Redirections.
- **Yoast SEO Premium**. Suggère automatiquement des redirections lorsque vous modifiez un slug.

Pour ajouter une redirection dans **Redirection** :

1. Allez dans Outils > Redirection
2. Saisissez l'URL source (ancien chemin)
3. Saisissez l'URL cible (nouveau chemin)
4. Sélectionnez « 301 Moved Permanently »
5. Cliquez sur « Ajouter une redirection »

Pour les redirections en masse, utilisez la fonction d'importation CSV. Format : `URL source, URL cible, 301`.

### Apache (.htaccess)

Si vous utilisez Apache, ajoutez des règles de redirection à votre fichier `.htaccess` à la racine du site.

Redirection unique :

```
Redirect 301 /ancienne-page https://exemple.com/nouvelle-page
```

Redirection basée sur un pattern avec `mod_rewrite` :

```
RewriteEngine On
RewriteRule ^ancien-repertoire/(.*)$ /nouveau-repertoire/$1 [R=301,L]
```

Redirection au niveau du domaine (site complet) :

```
RewriteEngine On
RewriteCond %{HTTP_HOST} ^anciensite\.com$ [NC]
RewriteRule ^(.*)$ https://nouveausite.com/$1 [R=301,L]
```

Sauvegardez toujours votre fichier `.htaccess` avant de le modifier. Une erreur de syntaxe ici fait tomber l'ensemble du site.

### Nginx

Nginx utilise le bloc `server` dans votre fichier de configuration (généralement `/etc/nginx/sites-available/`).

Redirection unique :

```
location = /ancienne-page {
    return 301 https://exemple.com/nouvelle-page;
}
```

Redirection basée sur un pattern :

```
location /ancien-repertoire/ {
    rewrite ^/ancien-repertoire/(.*)$ /nouveau-repertoire/$1 permanent;
}
```

Après modification, testez la configuration avec `nginx -t` et rechargez avec `systemctl reload nginx`.

### Shopify

Shopify dispose d'un outil de redirection intégré. Aucun plugin nécessaire.

1. Allez dans **Paramètres > Navigation > Redirections d'URL**
2. Cliquez sur « Ajouter une redirection d'URL »
3. Saisissez l'ancien chemin et le nouveau chemin
4. Enregistrez

Pour les redirections en masse, cliquez sur « Importer » et téléchargez un CSV avec 2 colonnes : `Rediriger depuis` et `Rediriger vers`.

Limitation de Shopify : vous ne pouvez pas rediriger vers des domaines externes depuis cet outil. Pour les migrations de domaine hors de Shopify, vous avez besoin de redirections au niveau DNS.

### Cloudflare (au niveau du CDN)

Les redirections Cloudflare s'effectuent au niveau du CDN. C'est l'option la plus rapide car la redirection se déclenche avant même que la requête n'atteigne votre serveur.

1. Allez dans **Règles > Règles de redirection**
2. Créez une nouvelle règle
3. Définissez la condition de correspondance (nom d'hôte, chemin URI ou caractère générique)
4. Définissez l'action sur « Redirection dynamique » ou « Redirection statique »
5. Choisissez `301` comme code de statut
6. Déployez

Cloudflare prend en charge les patterns avec caractères génériques, ce qui en fait l'idéal pour les migrations de domaine en masse.

### Comparaison des plateformes

| Plateforme | Difficulté | Support en masse | Vitesse | Idéal pour |
|---|---|---|---|---|
| Plugin WordPress | Facile | Import CSV | Standard | Sites de blog et de contenu |
| `.htaccess` | Moyen | Patterns regex | Standard | Hébergement mutualisé Apache |
| Nginx | Moyen | Règles de réécriture | Rapide | VPS et serveurs dédiés |
| Shopify | Facile | Import CSV | Standard | Boutiques e-commerce |
| Cloudflare | Facile | Règles génériques | Le plus rapide | Tout site utilisant Cloudflare |

![Configuration de la redirection 301 sur WordPress, Apache, Nginx, Shopify et Cloudflare](/images/blog/301-redirect-platforms.webp)

**Pourquoi cette étape est importante :** Une syntaxe incorrecte casse l'ensemble du site. Un fichier `.htaccess` mal configuré renvoie une erreur 500. Une mauvaise règle Nginx crée une boucle de redirection. Testez en environnement de staging si possible.

---

## Étape 4 : Gérer les chaînes et les boucles de redirections

Une chaîne de redirections se produit quand l'URL A redirige vers l'URL B, qui redirige vers l'URL C. Au lieu d'un seul saut, le navigateur en effectue 2 ou plus. Chaque saut ajoute 50 à 100 millisecondes de latence.

Une boucle de redirections se produit quand l'URL A redirige vers l'URL B, et que l'URL B redirige vers l'URL A. Le navigateur se retrouve dans une boucle infinie et affiche finalement une page d'erreur.

Google explore au maximum 5 sauts dans une chaîne de redirections. Au-delà, Google cesse de suivre. La page de destination n'est jamais explorée ni indexée.

### Comment détecter les chaînes et les boucles

Lancez une exploration avec Screaming Frog ou Ahrefs. Filtrez par chaînes de redirections (3xx > 3xx). Vous pouvez également utiliser le [vérificateur de redirections gratuit httpstatus.io](https://httpstatus.io) pour tester des URL individuelles.

### Comment aplatir les chaînes

Si la chaîne est A → B → C, mettez à jour A pour qu'il pointe directement vers C. Supprimez le saut intermédiaire.

Avant :
```
/ancienne-page → /page-renommee → /page-finale
```

Après :
```
/ancienne-page → /page-finale
/page-renommee → /page-finale
```

Les deux anciennes URL pointent maintenant directement vers la destination finale. Un seul saut chacune.

### Comment corriger les boucles

Les boucles se produisent généralement quand 2 règles de redirection sont en conflit. Vérifiez vos règles de redirection pour détecter les références circulaires. La solution est toujours la même : décidez quelle URL est la destination canonique et faites pointer toutes les autres URL vers elle.

Si vous utilisez à la fois des redirections au niveau serveur (`.htaccess`) et au niveau plugin (Redirection), vérifiez les deux. Les règles conflictuelles entre couches sont la cause la plus fréquente des boucles.

![Comparaison entre chaîne de redirections et redirection directe](/images/blog/redirect-chain-vs-direct.webp)

**Pourquoi cette étape est importante :** Les chaînes gaspillent le budget d'exploration et ralentissent le chargement des pages. Une chaîne de 3 sauts ajoute 150 à 300 ms de latence avant que l'utilisateur ne voie le moindre contenu. Les boucles sont encore pires. Elles bloquent l'accès entièrement et gaspillent le budget d'exploration sur des pages qui ne se résolvent jamais.

---

> **Évitez le travail technique. Gardez vos classements.** Stacc gère la structure des URL, les redirections et la maintenance SEO pour 30+ articles par mois.
> [Commencer pour 1 $ →](/pricing)

---

## Étape 5 : Tester chaque redirection avant la mise en ligne

Les redirections non testées provoquent des chutes de classement silencieuses. Une redirection qui renvoie `302` au lieu de `301` ne transfère pas le link equity de la même façon. Une redirection qui pointe vers une 404 est pire qu'aucune redirection du tout.

### Tester avec curl

Ouvrez votre terminal et exécutez :

```bash
curl -I https://exemple.com/ancienne-page
```

Recherchez `HTTP/1.1 301 Moved Permanently` et l'en-tête `Location:` pointant vers la bonne nouvelle URL.

Pour tester une chaîne, utilisez le flag `-L` pour suivre toutes les redirections :

```bash
curl -IL https://exemple.com/ancienne-page
```

Cela affiche chaque saut de la chaîne avec son code de statut.

### Tester avec Chrome DevTools

1. Ouvrez Chrome et appuyez sur `F12` pour ouvrir DevTools
2. Allez dans l'onglet **Réseau**
3. Cochez « Conserver le journal » (pour que les redirections restent visibles)
4. Saisissez l'ancienne URL dans la barre d'adresse
5. Examinez la première requête. La colonne Statut doit afficher `301`. Les en-têtes de réponse doivent indiquer le `Location` correct.

### Tester avec des outils en ligne

Des vérificateurs de redirections gratuits comme [httpstatus.io](https://httpstatus.io) ou le [vérificateur de redirections d'Ahrefs](https://ahrefs.com/blog/301-redirects/) vous permettent de tester sans terminal.

### Erreurs de test courantes

- **Divergence HTTP vs HTTPS.** Testez les versions `http://` et `https://` de l'ancienne URL. Manquer une redirection sur un protocole crée une faille.
- **Incohérence de barre oblique finale.** `/ancienne-page` et `/ancienne-page/` sont des URL différentes. Les deux ont besoin de redirections.
- **www vs non-www.** Assurez-vous que `www.exemple.com/ancienne-page` et `exemple.com/ancienne-page` redirigent correctement toutes les deux.

![Comment tester les redirections 301 avec curl et Chrome DevTools](/images/blog/test-301-redirects.webp)

**Pourquoi cette étape est importante :** Vous ne pouvez pas détecter une redirection cassée en naviguant normalement sur votre site. Les anciennes URL ne figurent pas dans votre navigation. Seul un test délibéré ou une alerte Google Search Console détectera le problème. D'ici là, vous aurez peut-être déjà perdu des semaines de classements.

---

## Étape 6 : Mettre à jour les liens internes pour pointer vers les nouvelles URL

Les redirections constituent un filet de sécurité. Elles ne remplacent pas définitivement un [maillage interne](/blog/internal-linking-blog-posts) correct.

Chaque lien interne passant par une redirection ajoute un saut inutile. Google suit toujours le lien, mais chaque redirection consomme du budget d'exploration. Sur un grand site avec des milliers de liens internes, cela s'accumule rapidement.

### Ce qu'il faut mettre à jour

- **Liens dans le corps du contenu.** Tout article de blog ou page liant vers l'ancienne URL
- **Menus de navigation.** Liens dans l'en-tête, le pied de page, les barres latérales
- **Sitemap XML.** Supprimez les anciennes URL et ajoutez les nouvelles. Si vous avez besoin d'aide, suivez notre guide sur [comment créer et optimiser votre sitemap XML](/blog/create-xml-sitemap).
- **Données structurées.** Mettez à jour tout [balisage schema](/blog/schema-markup-for-blog-posts) qui référence d'anciennes URL
- **Balises canonical.** Assurez-vous que la canonical de la nouvelle page pointe vers elle-même, pas vers l'ancienne URL

### Comment effectuer un remplacement à l'échelle du site

Pour WordPress, utilisez le plugin **Better Search Replace**. Saisissez l'ancien pattern d'URL et le nouveau. Effectuez d'abord une simulation pour prévisualiser les changements. Puis exécutez.

Pour les sites statiques ou les CMS personnalisés, utilisez la fonction rechercher-remplacer de votre éditeur de code dans l'ensemble du répertoire du projet.

Après la mise à jour, [soumettez votre sitemap mis à jour à Google](/blog/submit-website-google) via Search Console pour accélérer la réexploration.

**Pourquoi cette étape est importante :** Les liens internes passant par des redirections gaspillent le budget d'exploration et ajoutent de la latence. Les liens directs sont toujours plus rapides et plus efficaces. Nettoyez la source et gardez les redirections uniquement comme solution de repli pour les liens externes que vous ne contrôlez pas.

---

## Étape 7 : Surveiller dans Google Search Console

La redirection est active. Les tests ont réussi. Mais les redirections 301 peuvent se casser silencieusement lors de déploiements, de mises à jour CMS ou de modifications de la configuration serveur. Une surveillance continue détecte les problèmes avant qu'ils n'affectent les classements.

### Vérifier le rapport Pages

Dans Google Search Console, allez dans **Pages** (sous Indexation). Filtrez par :

- **Non trouvé (404).** Les nouvelles erreurs 404 apparaissant après l'activation de votre redirection indiquent une mauvaise configuration.
- **Erreur de redirection.** Google a détecté une boucle, une chaîne ou une redirection cassée.
- **Exploré. Actuellement non indexé.** La nouvelle page de destination n'est peut-être pas encore indexée.

### Utiliser l'outil d'inspection d'URL

Saisissez l'ancienne URL dans l'outil d'inspection d'URL. Google devrait indiquer « La page n'est pas dans l'index » avec une note qu'elle redirige vers la nouvelle URL. Si Google affiche toujours l'ancienne URL comme indexée, demandez l'indexation de la nouvelle URL.

### Vérifier les Core Web Vitals

Les chaînes de redirections augmentent le Time to First Byte (TTFB). Après la mise en œuvre des redirections, vérifiez les **Core Web Vitals** dans Search Console pour détecter d'éventuelles hausses de latence. Chaque saut ajoute 50 à 100 ms. Si votre TTFB a augmenté, vous avez probablement une chaîne non aplatie.

Vous pouvez également l'intégrer dans une stratégie plus large pour [améliorer les Core Web Vitals](/blog/improve-core-web-vitals) de votre site.

### Définir des points de contrôle de révision

- **Jour 7 :** Vérifiez les nouvelles erreurs 404 dans GSC. Confirmez que les anciennes URL se résolvent correctement.
- **Jour 30 :** Comparez le trafic organique avant et après la redirection. Utilisez le rapport Performance filtré par la nouvelle URL.
- **Jour 90 :** Confirmez que les classements se sont stabilisés. Les sites avec des redirections 301 propres conservent 95 % ou plus de leur trafic organique dans les 2 à 3 mois.

**Pourquoi cette étape est importante :** Les redirections peuvent se casser silencieusement. Une mise à jour CMS peut écraser votre fichier `.htaccess`. Une mise à jour de plugin peut réinitialiser les règles de redirection. Sans surveillance, vous ne le saurez qu'une fois que les classements chutent.

---

## Résultats : À quoi s'attendre

Google traite la plupart des redirections 301 dans un délai de 1 à 2 semaines. Vous verrez l'ancienne URL disparaître des résultats de recherche et la nouvelle URL prendre sa place.

Les classements se stabilisent généralement dans les 2 à 3 mois après une migration. [Les sites utilisant des redirections 301 propres ont conservé 95 % ou plus de leur trafic organique](https://ahrefs.com/blog/301-redirects/) pendant cette période.

Google recommande de maintenir les redirections 301 actives pendant au moins 1 an. Les supprimer trop tôt envoie les visiteurs récurrents et les anciens backlinks vers une erreur 404.

La chronologie complète :

| Étape | Délai |
|---|---|
| Google commence à traiter la redirection | 1 à 3 jours |
| Ancienne URL retirée de l'index | 1 à 2 semaines |
| Nouvelle URL se classe à la position de l'ancienne | 2 à 4 semaines |
| Trafic complètement stabilisé | 2 à 3 mois |
| Suppression sécurisée de la redirection | 1 an minimum |

![Chronologie de l'impact SEO des redirections 301](/images/blog/301-redirect-timeline.webp)

Associez des redirections propres à une publication de contenu régulière pour [augmenter le trafic organique](/blog/increase-organic-traffic) pendant la stabilisation de vos redirections.

---

## Dépannage : 5 problèmes courants avec les redirections 301

### Problème 1 : La redirection renvoie 302 au lieu de 301

Un `302` est une redirection temporaire. Il ne transfère pas le link equity de la même façon qu'un `301`. Cela se produit généralement lorsqu'un plugin est configuré par défaut sur `302` ou lorsque la configuration serveur utilise `Redirect` sans préciser le code de statut.

**Solution :** Vérifiez votre règle de redirection. Pour `.htaccess`, utilisez explicitement `Redirect 301` ou `[R=301,L]`. Dans votre plugin CMS, vérifiez que le type de redirection est défini sur « Permanent (301) ».

### Problème 2 : Chaîne de redirections (3 sauts ou plus)

Vous avez redirigé A vers B l'année dernière. Puis vous avez redirigé B vers C cette année. Maintenant A passe par 2 sauts pour atteindre C. Google le suit, mais la latence nuit aux performances.

**Solution :** Mettez à jour la règle pour A afin qu'il pointe directement vers C. Puis mettez à jour B pour qu'il pointe directement vers C. Aplatissez chaque chaîne sur un seul saut.

### Problème 3 : Boucle de redirections

L'URL A redirige vers B. L'URL B redirige vers A. Le navigateur affiche « ERR_TOO_MANY_REDIRECTS » et rien ne se charge.

**Solution :** Ouvrez vos règles de redirection et cherchez des références circulaires. Si vous utilisez à la fois un plugin et des redirections au niveau serveur, vérifiez les deux couches. Supprimez la règle en conflit.

### Problème 4 : Redirection mixte HTTP et HTTPS

La version HTTP de l'ancienne URL redirige vers la version HTTP de la nouvelle URL, qui redirige ensuite vers HTTPS. C'est une chaîne de 2 sauts qui devrait n'en avoir qu'un.

**Solution :** Toutes les redirections doivent pointer directement vers la version HTTPS de l'URL de destination. Mettez à jour chaque règle pour utiliser `https://` dans la cible.

### Problème 5 : Soft 404 après redirection

La redirection fonctionne. Le code de statut est `301`. Mais la page de destination a un contenu léger ou vide. Google traite cela comme une « soft 404 » et peut ne pas transférer le link equity. Cela se produit souvent lorsque vous redirigez vers une page au [contenu léger](/blog/fix-thin-content) ou une page de catégorie générique.

**Solution :** Assurez-vous que chaque destination de redirection est une page réelle et substantielle avec un contenu unique. Si la page de destination n'existe pas encore, créez-la avant d'activer la redirection.

![Problèmes courants avec les redirections 301 et leurs solutions](/images/blog/301-redirect-problems.webp)

---

> **Votre équipe SEO. 99 $ par mois.** 30 articles optimisés, publiés et maintenus. Redirections, liens internes et SEO technique pris en charge.
> [Commencer pour 1 $ →](/pricing)

---

## Questions fréquemment posées

**Combien de temps faut-il conserver les redirections 301 ?**

Google recommande de maintenir les redirections 301 actives pendant au moins 1 an. Les sites externes qui pointent vers votre ancienne URL continueront d'envoyer du trafic via cette redirection. La supprimer avant que ces liens externes ne soient mis à jour (la plupart ne le seront jamais) envoie leurs visiteurs vers une erreur 404. En cas de doute, conservez la redirection définitivement. La charge serveur est négligeable.

**Les redirections 301 nuisent-elles au SEO ?**

Non. Google a confirmé en 2016 que les redirections 30x ne causent plus de perte de PageRank. Un `301` correctement configuré transfère 90 à 99 % du link equity vers l'URL de destination. Le seul risque est lié aux erreurs d'implémentation telles que les chaînes, les boucles ou les redirections vers des pages non pertinentes.

**Quelle est la différence entre une redirection 301 et une redirection 302 ?**

Une [redirection 301](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301) signale un déplacement permanent. Google transfère le link equity et finit par désindexer l'ancienne URL. Un `302` signale un déplacement temporaire. Google conserve l'ancienne URL dans l'index et peut ne pas transférer l'intégralité du link equity. Utilisez `301` pour tout changement d'URL permanent.

**Un trop grand nombre de redirections 301 peut-il ralentir mon site ?**

Les redirections individuelles ajoutent une latence minimale (moins de 100 ms). Le problème, ce sont les chaînes de redirections. Chaque saut ajoute 50 à 100 ms. Une chaîne de 3 sauts ajoute 150 à 300 ms avant même que la page commence à se charger. Maintenez chaque redirection sur un seul saut et l'impact sur les performances reste négligeable.

**Comment vérifier si mes redirections 301 fonctionnent ?**

Utilisez `curl -I [URL]` dans votre terminal. La réponse doit afficher `HTTP/1.1 301 Moved Permanently` avec un en-tête `Location:` pointant vers la bonne destination. Vous pouvez aussi utiliser Chrome DevTools (onglet Réseau avec « Conserver le journal » activé) ou des outils en ligne gratuits comme httpstatus.io.

**Dois-je utiliser une redirection 301 ou une balise canonical ?**

Utilisez un `301` lorsque vous supprimez entièrement l'ancienne page. Utilisez une balise `canonical` lorsque les deux pages restent en ligne mais que vous souhaitez que Google consolide les signaux de classement vers une version. Exemple courant : les pages produit avec des paramètres d'URL. L'URL filtrée reste accessible, mais la canonical pointe vers l'URL propre. Pour la [cannibalisation de mots-clés](/blog/fix-keyword-cannibalization) entre 2 pages actives, une balise canonical est souvent la meilleure première étape.

---

Les redirections 301 protègent le link equity et les classements que vous avez déjà obtenus. Chaque changement d'URL sans redirection est une fuite dans les fondations de votre SEO.

Configurez les redirections correctement, testez-les, surveillez-les et associez ce travail à une publication régulière de contenu. C'est ainsi que vous [vous classez plus haut sur Google](/blog/how-to-rank-higher-google) et conservez les positions que vous gagnez.
