---
term: "Crawl budget (orçamento de rastreamento)"
slug: "crawl-budget"
definition: "Crawl budget é o número de páginas que um bot de mecanismo de busca rastreará no seu site dentro de um determinado período. Gerenciá-lo bem garante que suas páginas mais importantes sejam priorizadas."
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

## O que é crawl budget?

Crawl budget é o número total de URLs que o Googlebot buscará do seu site durante um determinado período, determinado por uma combinação de limite de taxa de rastreamento e demanda de rastreamento.

O Google não dá atenção ilimitada a cada site. O Googlebot aloca recursos baseado no tamanho, saúde e importância percebida do seu site. Para a maioria dos sites pequenos a médios (abaixo de 10.000 páginas), crawl budget não é preocupação. Mas para sites maiores. Lojas e-commerce, editores, diretórios. Pode ser a diferença entre conteúdo novo sendo indexado em horas ou semanas.

Gary Illyes do Google declarou que crawl budget "não é algo com que a maioria dos sites precise se preocupar", mas também confirmou que desperdiçá-lo em URLs de baixo valor pode atrasar a [indexação](/glossary/indexing) de páginas importantes.

## Por que crawl budget importa?

Se o Googlebot não pode alcançar suas páginas-chave, elas não podem ranquear. Ponto.

- **Indexação mais rápida**. Uso eficiente de crawl budget significa que conteúdo novo é descoberto e indexado mais cedo
- **Páginas priorizadas**. Quando o Googlebot desperdiça orçamento em [conteúdo duplicado](/glossary/duplicate-content), páginas 404 ou URLs de parâmetro, suas páginas principais podem nem ser rastreadas durante esse ciclo
- **Sinal de saúde do site**. Um site fácil de rastrear sinaliza qualidade aos sistemas do Google, enquanto armadilhas de rastreamento e erros fazem o oposto
- **Escalando conteúdo**. Sites publicando 30+ páginas por mês precisam que o Googlebot acompanhe novo conteúdo, tornando a eficiência de rastreamento crítica

Qualquer site com mais que alguns milhares de páginas deve gerenciar ativamente o crawl budget.

## Como crawl budget funciona

### Limite de taxa de rastreamento

O Google define uma velocidade máxima de rastreamento para evitar sobrecarregar seu servidor. Se seu servidor responde devagar ou retorna erros, o Googlebot recua. Hospedagem rápida e confiável aumenta diretamente seu limite de taxa de rastreamento.

### Demanda de rastreamento

Mesmo que o Googlebot *pudesse* rastrear mais, só o fará se tiver razão. Páginas populares com muitos [backlinks](/glossary/backlinks) são recrastreadas frequentemente. Páginas obsoletas e de baixa autoridade podem passar meses entre visitas. Atualizar conteúdo e conquistar links aumenta demanda de rastreamento para URLs específicas.

### Desperdiçadores comuns de crawl budget

Navegação facetada, IDs de sessão em URLs, scroll infinito sem paginação adequada, [links quebrados](/glossary/broken-link) retornando [erros 404](/glossary/404-error) e conteúdo duplicado entre variações de parâmetros todos consomem crawl budget. Use [robots.txt](/glossary/robots-txt) e [tags noindex](/glossary/noindex) para impedir o Googlebot de desperdiçar tempo nessas páginas.

## Exemplos de crawl budget

**Exemplo 1: Um e-commerce com URLs de filtro**
O site de uma loja de móveis gera 50.000 URLs únicas a partir de combinações de filtros (cor, tamanho, material, preço). Apenas 3.000 são páginas de produto reais. Sem bloquear URLs de filtro via robots.txt, o Googlebot gasta 94 % do seu crawl budget em páginas que não deveriam ser indexadas.

**Exemplo 2: Um blog pesado em conteúdo**
Uma empresa publica 30 artigos por mês através da theStacc. Com [arquitetura de site](/glossary/site-architecture) limpa e sitemap XML, o Googlebot descobre e indexa novos posts em 48 horas. Um concorrente publicando o mesmo volume em um site mal estruturado espera 2-3 semanas pela indexação.

### Ferramentas e Recursos

| Ferramenta | Propósito | Preço |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Dados de desempenho de busca | Grátis |
| **Ahrefs** | Backlinks, palavras-chave, auditoria de site | A partir de $99/mês |
| **Semrush** | Plataforma SEO tudo-em-um | A partir de $130/mês |
| **Screaming Frog** | Análise de rastreamento técnico | Grátis (500 URLs) |
| **theStacc** | Publicação automatizada de conteúdo SEO | A partir de $99/mês |

## Perguntas Frequentes

### Como verifico meu crawl budget?

O relatório de Estatísticas de Rastreamento do Google Search Console mostra quantas páginas o Googlebot rastreia por dia, tempo médio de resposta e tendências de solicitações de rastreamento. Verifique em Configurações > Estatísticas de Rastreamento. Procure padrões. Uma queda repentina na taxa de rastreamento frequentemente sinaliza problemas de servidor.

### Crawl budget afeta sites pequenos?

Para sites abaixo de 1.000 páginas, crawl budget raramente importa. O Googlebot pode facilmente lidar com sites pequenos em uma única sessão de rastreamento. Comece a prestar atenção quando exceder 10.000 URLs indexáveis ou notar indexação lenta de novo conteúdo.

### Como melhoro o crawl budget?

Remova ou noindexe páginas de baixo valor, conserte erros de rastreamento, melhore tempos de resposta do servidor, envie um [sitemap XML](/glossary/xml-sitemap) atualizado, e construa links internos para páginas importantes. Facilite ao Googlebot encontrar e acessar seu melhor conteúdo rapidamente.

---

Publicando conteúdo consistentemente? Garanta que o Google possa acompanhar. theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: Gerenciamento de Crawl Budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central Blog: O que crawl budget significa](https://developers.google.com/search/blog/2017/01/what-crawl-budget-means-for-googlebot)
- [Ahrefs: Crawl Budget e SEO](https://ahrefs.com/blog/crawl-budget/)
- [Moz: Crawl Budget Explicado](https://moz.com/blog/crawl-budget)
