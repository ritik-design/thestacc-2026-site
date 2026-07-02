---
term: "robots.txt"
slug: "robots-txt"
definition: "robots.txt est un fichier texte placé à la racine de votre site qui indique aux robots des moteurs de recherche quelles URL ils peuvent ou non explorer."
category: "SEO"
difficulty: "Intermediate"
keyword: "qu'est-ce que robots.txt"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## Qu'est-ce que robots.txt ?

**Le fichier robots.txt se trouve à la racine de votre domaine (votresite.com/robots.txt) et indique aux robots des moteurs de recherche quelles pages ou sections de votre site ils ont le droit d'explorer.**

Tous les grands moteurs de recherche. Google, Bing, Yahoo. Vérifient ce fichier avant de [crawler](/glossary/crawling) votre site. Voyez-le comme la liste d'un videur. Pas un verrou sur la porte, mais une consigne claire que les bots bien élevés respectent.

D'après la documentation officielle de Google, Googlebot consulte robots.txt avant la moindre requête à votre serveur. Sur des sites de plusieurs milliers de pages, ce fichier devient l'une des pièces maîtresses de votre [SEO technique](/glossary/technical-seo).

## Pourquoi robots.txt est-il important ?

Une erreur dans votre robots.txt peut faire chuter vos positions du jour au lendemain. Une seule directive mal placée et Google ne voit plus vos pages les plus stratégiques.

- **Protection du crawl budget**. Les gros sites ont un [crawl budget](/glossary/crawl-budget) limité. Bloquer les pages à faible valeur (panneaux d'admin, environnements de staging, filtres dupliqués) garde Googlebot concentré sur l'essentiel.
- **Évite l'indexation des zones sensibles**. Résultats de recherche internes, pages de connexion, paniers : rien à faire dans la [SERP](/glossary/serp). Le robots.txt tient les bots à l'écart.
- **Découverte plus rapide des nouveaux contenus**. Quand les robots ne gaspillent pas de requêtes sur des pages inutiles, ils trouvent vos nouveaux articles et fiches produits plus vite.
- **Gestion de la charge serveur**. Les bots agressifs peuvent saturer un petit serveur. Bloquer le crawl inutile réduit la consommation de ressources.

Si vous publiez régulièrement. 5 pages ou 30 articles par mois, peu importe. Vous avez besoin que les robots passent leur temps sur les bonnes URL.

## Comment fonctionne robots.txt

Le fichier utilise une syntaxe simple. Trois directives principales couvrent la plupart des cas.

### User-agent

Cette ligne précise à quel robot la règle s'applique. `User-agent: *` cible tous les bots. `User-agent: Googlebot` ne vise que le robot de Google. Vous pouvez empiler plusieurs règles pour différents bots dans le même fichier.

### Disallow

La directive `Disallow` bloque un chemin précis. `Disallow: /admin/` empêche les robots d'accéder à tout ce qui se trouve sous /admin/. Laissez-la vide (`Disallow:`) et vous autorisez tout. Une seule barre oblique (`Disallow: /`) bloque le site entier.

### Allow et Sitemap

`Allow` annule une règle Disallow plus large pour des chemins spécifiques. Pratique quand vous bloquez un répertoire mais voulez qu'une page à l'intérieur soit explorée. La directive `Sitemap` pointe vers votre [sitemap XML](/glossary/xml-sitemap) et aide les robots à trouver toutes vos URL importantes sans deviner.

### Comment Google le traite

Googlebot récupère votre robots.txt avant de crawler quoi que ce soit. Si le fichier renvoie un statut 200, Google suit les règles. Un 404 signifie « aucune restriction ». Tout est exploré. Une erreur 5xx rend Google temporairement prudent : il limite le crawl tant que le fichier n'est pas à nouveau accessible.

## Types de directives robots.txt

Les directives robots.txt se rangent en 4 grandes catégories :

- **Directives d'accès (Allow/Disallow)**. Elles contrôlent les chemins que les bots peuvent visiter. La base de tout fichier robots.txt.
- **Directives user-agent**. Elles ciblent des bots précis. Vous pouvez bloquer SemrushBot tout en laissant Googlebot passer librement.
- **Directives crawl-delay**. Elles imposent un délai entre les requêtes. Google les ignore (utilisez plutôt Google Search Console), mais Bing et Yandex les respectent.
- **Directives sitemap**. Elles pointent vers votre fichier sitemap. Pas vraiment une « règle », plutôt un mécanisme de découverte sur lequel les bots s'appuient.

La plupart des sites de petite et moyenne taille n'ont besoin que des directives d'accès et d'une référence sitemap. Le crawl-delay devient pertinent sur les gros sites avec des contraintes serveur.

## Exemples de robots.txt

**Exemple 1 : plombier local**
Un plombier de Lyon a un site WordPress avec les répertoires /wp-admin/, /panier/ et /tarifs-internes/. Son robots.txt bloque les trois et inclut une référence au sitemap. Résultat : Googlebot passe son temps sur les pages de services et les articles de blog. Pas dans les panneaux d'administration.

**Exemple 2 : boutique e-commerce avec pages filtrées**
Un détaillant en ligne a 50 produits mais 3 000 combinaisons de filtres (taille + couleur + prix). Sans un Disallow sur `/produits?filtre=`, Googlebot gaspille du [crawl budget](/glossary/crawl-budget) sur des pages filtrées dupliquées. Une seule ligne Disallow règle le problème.

**Exemple 3 : blocage accidentel du site entier**
Une agence marketing est passée de staging à production en laissant `Disallow: /` dans le robots.txt. Pendant 3 semaines, plus rien n'a été [indexé](/glossary/indexing). Le trafic est tombé à zéro. Un seul caractère a provoqué ça. La barre oblique après Disallow.

## robots.txt vs balise meta robots

Ces deux outils font des jobs différents à des moments différents. robots.txt arrête les robots avant qu'ils n'atteignent une page. La [balise meta robots](/glossary/meta-robots-tag) donne des consignes après qu'un robot a déjà accédé à la page.

| | robots.txt | Balise meta robots |
|---|---|---|
| **Où elle vit** | Fichier à la racine | `<head>` HTML des pages individuelles |
| **Quand elle agit** | Avant le crawl | Après le crawl |
| **Portée** | Répertoires ou chemins entiers | Pages individuelles |
| **Empêche l'indexation ?** | Non. Bloque seulement le crawl | Oui, `noindex` retire des résultats |
| **Idéal pour** | Bloquer des sections du site | Retirer des pages précises de la recherche |

Le piège : si vous bloquez une page avec robots.txt, Google ne peut pas voir la balise noindex dessus. Cette page peut donc rester dans les résultats (sans extrait) parce que Google a trouvé un lien ailleurs. Pour retirer vraiment une page, utilisez la balise meta robots. Pas robots.txt.

## Bonnes pratiques robots.txt

- **Incluez toujours une directive Sitemap**. Pointez vers votre [sitemap XML](/glossary/xml-sitemap) pour donner aux robots une carte complète. Une ligne : `Sitemap: https://votresite.com/sitemap.xml`.
- **Ne bloquez jamais les fichiers CSS ou JavaScript**. Google a besoin de rendre vos pages pour les comprendre. Bloquer ces ressources nuit à votre [SEO on-page](/glossary/on-page-seo).
- **Testez avant de déployer**. Utilisez le testeur robots.txt de Google Search Console pour vérifier vos règles. Une faute de frappe peut bloquer tout votre site.
- **Révisez chaque trimestre**. Au fil de la croissance de votre site, de nouveaux répertoires apparaissent. Ce qui avait du sens il y a 6 mois bloque peut-être des contenus importants aujourd'hui.
- **Associez-le à une stratégie de contenu**. robots.txt gère ce qui est crawlé, mais il vous faut quand même des pages qui méritent de l'être. Des services comme theStacc publient 30 articles optimisés SEO par mois et offrent à Googlebot du contenu frais à chaque visite.

## Foire aux questions

### robots.txt empêche-t-il les pages d'apparaître dans Google ?

Pas directement. robots.txt empêche le crawl, pas l'[indexation](/glossary/indexing). Si d'autres sites lient une page bloquée, Google peut continuer à l'afficher. Sans extrait descriptif. Pour retirer totalement une page, utilisez une balise meta noindex.

### Où placer mon fichier robots.txt ?

À la racine de votre domaine : `https://votresite.com/robots.txt`. Le placer dans un sous-répertoire ne fonctionne pas. Chaque sous-domaine a besoin de son propre robots.txt.

### robots.txt peut-il améliorer mes positions ?

Indirectement, oui. Bloquer les pages à faible valeur préserve le crawl budget pour les contenus importants. Sur les gros sites, cela signifie une découverte et une indexation plus rapides des nouvelles pages. Ce qui peut accélérer la progression dans les classements.

### Tous les bots respectent-ils les règles robots.txt ?

Les robots légitimes des moteurs de recherche (Googlebot, Bingbot) respectent robots.txt. Les bots malveillants et les scrapers l'ignorent souvent. Ne vous reposez pas sur robots.txt pour la sécurité. C'est une consigne, pas un pare-feu.

---

Vous voulez vous assurer que votre contenu SEO est vraiment crawlé et bien classé ? theStacc publie 30 articles optimisés SEO sur votre site chaque mois. Automatiquement. [Démarrez pour $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central : Spécifications robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central : Comment Google interprète robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz : Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs : Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
