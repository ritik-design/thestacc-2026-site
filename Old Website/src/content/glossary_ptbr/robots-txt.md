---
term: "robots.txt"
slug: "robots-txt"
definition: "robots.txt é um arquivo de texto na raiz do seu site que diz aos rastreadores dos buscadores quais URLs eles podem ou não acessar."
category: "SEO"
difficulty: "Intermediate"
keyword: "o que é robots.txt"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## O que é robots.txt?

**O arquivo robots.txt fica no diretório raiz do seu domínio (seusite.com/robots.txt) e informa aos rastreadores dos buscadores quais páginas ou seções do seu site eles têm permissão para acessar.**

Todos os grandes buscadores. Google, Bing, Yahoo. Consultam esse arquivo antes de [rastrear](/glossary/crawling) o seu site. Pense nele como a lista do segurança da porta. Não é uma fechadura, é um conjunto claro de instruções que os bots bem-comportados seguem.

Segundo a documentação do próprio Google, o Googlebot lê o robots.txt antes de fazer qualquer requisição ao seu servidor. Em sites com milhares de páginas, esse arquivo se torna uma das peças mais importantes do seu [SEO técnico](/glossary/technical-seo).

## Por que o robots.txt importa?

Errar o robots.txt pode derrubar suas posições da noite para o dia. Uma única diretiva fora de lugar e o Google deixa de enxergar suas páginas mais importantes.

- **Proteção do crawl budget**. Sites grandes têm [crawl budget](/glossary/crawl-budget) limitado. Bloquear páginas de baixo valor (painéis de admin, ambientes de staging, filtros duplicados) mantém o Googlebot focado no que importa.
- **Evita a indexação de áreas sensíveis**. Resultados de busca interna, páginas de login e carrinho não têm o que fazer na [SERP](/glossary/serp). O robots.txt mantém os bots de fora.
- **Descoberta mais rápida de novos conteúdos**. Quando os rastreadores não desperdiçam requisições em páginas inúteis, encontram seus novos posts e fichas de produto mais cedo.
- **Gestão da carga do servidor**. Bots agressivos podem sobrecarregar servidores pequenos. Bloquear o rastreamento desnecessário reduz o consumo de recursos.

Se você publica conteúdo com regularidade. Sejam 5 páginas ou 30 artigos por mês. Você precisa que os rastreadores gastem o tempo deles nas URLs certas.

## Como o robots.txt funciona

O arquivo usa uma sintaxe simples. Três diretivas centrais cobrem a maioria dos casos.

### User-agent

Essa linha define a qual rastreador a regra se aplica. `User-agent: *` mira todos os bots. `User-agent: Googlebot` mira só o rastreador do Google. Você pode empilhar várias regras para bots diferentes no mesmo arquivo.

### Disallow

A diretiva `Disallow` bloqueia um caminho específico. `Disallow: /admin/` impede que rastreadores acessem qualquer coisa dentro do diretório /admin/. Deixe vazia (`Disallow:`) e você libera tudo. Uma única barra (`Disallow: /`) bloqueia o site inteiro.

### Allow e Sitemap

`Allow` sobrepõe uma regra Disallow mais ampla para caminhos específicos. Útil quando você bloqueia um diretório mas quer que uma página dentro dele seja rastreada. A diretiva `Sitemap` aponta os rastreadores para o seu [sitemap XML](/glossary/xml-sitemap) e os ajuda a encontrar todas as URLs importantes sem chutar.

### Como o Google processa o arquivo

O Googlebot busca o seu robots.txt antes de rastrear qualquer outra coisa. Se o arquivo retorna status 200, o Google segue as regras. Um 404 significa "sem restrições". Tudo é rastreado. Um erro 5xx deixa o Google temporariamente cauteloso e ele limita o rastreamento até o arquivo voltar a ficar acessível.

## Tipos de diretivas robots.txt

As diretivas do robots.txt se dividem em 4 categorias principais:

- **Diretivas de acesso (Allow/Disallow)**. Controlam quais caminhos os bots podem visitar. A base de qualquer arquivo robots.txt.
- **Diretivas de user-agent**. Direcionam regras a bots específicos. Você pode bloquear o SemrushBot enquanto libera acesso total ao Googlebot.
- **Diretivas de crawl-delay**. Dizem aos bots para esperar entre as requisições. O Google ignora isso (use o Google Search Console no lugar), mas Bing e Yandex respeitam.
- **Diretivas de sitemap**. Apontam para o seu arquivo de sitemap. Tecnicamente não é uma "regra", é um mecanismo de descoberta que os bots usam.

A maioria dos sites pequenos e médios só precisa de diretivas de acesso e uma referência ao sitemap. O crawl-delay importa mais em sites de grande escala com restrições de servidor.

## Exemplos de robots.txt

**Exemplo 1: encanador local**
Um encanador em São Paulo tem um site em WordPress com os diretórios /wp-admin/, /carrinho/ e /precos-internos/. O robots.txt bloqueia os três e inclui uma referência ao sitemap. Resultado: o Googlebot gasta o tempo dele nas páginas de serviço e nos posts do blog. Não nos painéis de admin.

**Exemplo 2: e-commerce com páginas filtradas**
Um varejista online tem 50 produtos mas 3.000 combinações de filtros (tamanho + cor + preço). Sem um Disallow em `/produtos?filtro=`, o Googlebot desperdiça [crawl budget](/glossary/crawl-budget) em páginas filtradas duplicadas. Uma única linha Disallow resolve.

**Exemplo 3: bloquear o site inteiro sem querer**
Uma agência de marketing migrou de staging para produção e deixou `Disallow: /` no robots.txt. Por 3 semanas, nada foi [indexado](/glossary/indexing). O tráfego caiu para zero. Um único caractere causou isso. A barra depois do Disallow.

## robots.txt vs meta tag robots

Esses dois fazem trabalhos diferentes em momentos diferentes. O robots.txt para os rastreadores antes que cheguem a uma página. A [meta tag robots](/glossary/meta-robots-tag) dá instruções depois que um rastreador já acessou a página.

| | robots.txt | Meta tag robots |
|---|---|---|
| **Onde fica** | Arquivo no diretório raiz | `<head>` HTML de páginas individuais |
| **Quando age** | Antes do rastreamento | Depois do rastreamento |
| **Escopo** | Diretórios ou caminhos inteiros | Páginas individuais |
| **Impede a indexação?** | Não. Só bloqueia o rastreamento | Sim, `noindex` remove da busca |
| **Ideal para** | Bloquear seções do site | Remover páginas específicas da busca |

Aqui está a pegadinha: se você bloquear uma página com robots.txt, o Google não consegue ver uma tag noindex nela. Então essa página pode continuar aparecendo nos resultados (sem snippet) porque o Google encontrou um link em outro lugar. Para remover de verdade uma página da busca, use a meta tag robots. Não o robots.txt.

## Boas práticas para robots.txt

- **Sempre inclua uma diretiva Sitemap**. Aponte para o seu [sitemap XML](/glossary/xml-sitemap) para dar aos rastreadores um mapa completo do site. Uma linha: `Sitemap: https://seusite.com/sitemap.xml`.
- **Nunca bloqueie arquivos CSS ou JavaScript**. O Google precisa renderizar suas páginas para entendê-las. Bloquear esses recursos prejudica seu [SEO on-page](/glossary/on-page-seo).
- **Teste antes de publicar**. Use o testador de robots.txt do Google Search Console para conferir as regras. Um erro de digitação pode bloquear o site inteiro.
- **Revise a cada trimestre**. Conforme o site cresce, novos diretórios aparecem. O que fazia sentido há 6 meses pode estar bloqueando conteúdo importante hoje.
- **Combine com uma estratégia de conteúdo**. O robots.txt controla o que é rastreado, mas você ainda precisa de páginas que valham a pena rastrear. Serviços como theStacc publicam 30 artigos otimizados para SEO por mês, dando ao Googlebot conteúdo fresco a cada visita.

## Perguntas frequentes

### O robots.txt impede que páginas apareçam no Google?

Não diretamente. O robots.txt impede o rastreamento, não a [indexação](/glossary/indexing). Se outros sites linkam para uma página bloqueada, o Google ainda pode mostrá-la nos resultados. Só que sem snippet de descrição. Use uma meta tag noindex para remover totalmente uma página da busca.

### Onde coloco o arquivo robots.txt?

Coloque na raiz do seu domínio: `https://seusite.com/robots.txt`. Em subdiretórios não funciona. Cada subdomínio precisa do próprio robots.txt.

### O robots.txt pode melhorar meus rankings?

Indiretamente, sim. Bloquear páginas de baixo valor preserva o crawl budget para o seu conteúdo importante. Em sites grandes isso significa descoberta e indexação mais rápidas das páginas novas. O que pode acelerar a melhoria de posições.

### Todos os bots seguem as regras do robots.txt?

Bots legítimos dos buscadores (Googlebot, Bingbot) respeitam o robots.txt. Bots maliciosos e scrapers normalmente ignoram. Não conte com o robots.txt para segurança. É uma diretriz, não um firewall.

---

Quer garantir que seu conteúdo de SEO seja realmente rastreado e ranqueado? theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: especificações do robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central: como o Google interpreta o robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz: Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs: Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
