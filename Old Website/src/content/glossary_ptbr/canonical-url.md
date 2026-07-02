---
term: "URL canônica / Canonicalização"
slug: "canonical-url"
definition: "Uma URL canônica diz aos mecanismos de busca qual versão de uma página é a cópia principal. Aprenda como a canonicalização previne problemas de conteúdo duplicado e como usá-la corretamente."
category: "SEO"
difficulty: "Intermediate"
keyword: "url canônica"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "301-redirect"
  - "indexing"
  - "crawl-budget"
  - "technical-seo"
---

## O que é uma URL canônica?

Uma URL canônica é um elemento HTML que diz aos mecanismos de busca qual versão de uma página é a cópia preferida e autoritativa quando múltiplas URLs servem o mesmo conteúdo ou um muito similar.

No `<head>` de uma página parece assim: `<link rel="canonical" href="https://example.com/preferred-page">`. Por que isso existe? Porque na web moderna, um único conteúdo frequentemente vive em múltiplas URLs. Mesma página de produto acessível com e sem www, com e sem barra final, com parâmetros de rastreamento, através de navegação filtrada. O Google vê cada URL como uma página separada. Sem uma tag canonical, o Google tem que adivinhar qual indexar. E frequentemente adivinha errado.

Dados da Semrush de um estudo de 150.000 sites encontraram que 65 % dos domínios têm alguma forma de problema de [conteúdo duplicado](/glossary/duplicate-content). Tags canônicas são a ferramenta principal para resolver isso em escala sem reestruturar todo o site.

## Por que a canonicalização importa?

Conteúdo duplicado não é uma penalidade. O Google já disse isso claramente. Mas cria problemas reais de SEO que custam tráfego e ranqueamentos.

- **Link equity é dividida**. Se 30 sites linkam para sua página mas metade linka para `example.com/page` e metade para `example.com/page/`, a autoridade é dividida. Uma canonical consolida todos os sinais para uma URL, tornando-a mais forte.
- **[Crawl budget](/glossary/crawl-budget) é desperdiçado**. O Googlebot tem um crawl budget finito para seu site. Cada URL duplicada que rastreia é uma página que não rastreou. Para sites grandes com milhares de páginas, isso impacta diretamente a rapidez com que novo conteúdo é [indexado](/glossary/indexing).
- **A página errada pode ranquear**. Sem canonicalização, o Google escolhe a versão que considera melhor. Pode ser sua URL mobile, uma URL cheia de parâmetros, ou uma página de categoria filtrada. Não a versão limpa e otimizada que você quer ranqueando.
- **Analytics ficam fragmentados**. Dados de tráfego e engajamento se espalham por múltiplas URLs. Seu desempenho real parece mais fraco do que é porque as métricas estão divididas.

Se seu site tem mais que um punhado de páginas, você quase certamente tem conteúdo duplicado que a canonicalização resolveria.

## Como a canonicalização funciona

A tag canonical é uma sugestão, não uma diretiva. O Google geralmente a respeita. Mas nem sempre.

### Canonicals auto-referenciais

Cada página do seu site deve apontar sua tag canonical para si mesma. Isso se chama canonical auto-referencial. Diz ao Google: "Esta é a URL preferida para este conteúdo, mesmo que você descubra através de um caminho diferente." A maioria das plataformas [CMS](/glossary/content-management-system) e plugins de [SEO técnico](/glossary/technical-seo) lida com isso automaticamente.

### Canonicals entre domínios

Se você sindica conteúdo. Publicando o mesmo artigo no seu blog e no Medium ou LinkedIn. Você pode definir uma canonical entre domínios apontando da versão sindicada de volta para o seu original. Isso diz ao Google para creditar a [link equity](/glossary/link-equity) e sinais de ranking ao seu domínio, não à cópia sindicada.

### Canonical vs. escolha do Google

O Google trata tags canonical como uma dica forte, não um comando. Se a tag canonical conflita com outros sinais (sitemaps, links internos, padrões de redirecionamento), o Google pode sobrescrever sua preferência. Por isso a consistência importa. Sua canonical, seus [links internos](/glossary/internal-link), seu sitemap e seus [redirecionamentos 301](/glossary/301-redirect) devem todos apontar para a mesma URL preferida.

### Variações comuns de URL canônica

Estes são os cenários de conteúdo duplicado mais frequentes que a canonicalização resolve:

- `http://` vs `https://`
- `www.example.com` vs `example.com`
- `/page` vs `/page/` (barra final)
- `/page` vs `/page?utm_source=google&utm_medium=cpc`
- `/page` vs `/page?ref=homepage`
- URLs mobile (`m.example.com`) vs URLs desktop

Cada variação é uma URL separada para o Google. Tags canonical as unem em uma só.

## Tipos de canonicalização

Existem múltiplas formas de sinalizar sua URL preferida. A tag canonical é a mais comum, mas não a única opção.

- **Tag canonical HTML**. A tag `<link rel="canonical">` no `<head>` da página. Mais flexível, funciona em qualquer página, fácil de implementar.
- **Canonical em cabeçalho HTTP**. Enviada como cabeçalho `Link:` na resposta HTTP. Usada para arquivos não-HTML (PDFs, imagens) onde você não pode adicionar tags HTML.
- **[Redirecionamento 301](/glossary/301-redirect)**. Redireciona permanentemente URLs duplicadas para a versão preferida. Mais forte que uma tag canonical porque usuários e bots só podem acessar a URL preferida.
- **Sinais de [sitemap XML](/glossary/xml-sitemap)**. Incluir apenas URLs canônicas no seu sitemap reforça quais versões você prefere. Não é um método direto de canonicalização, mas um sinal de apoio.
- **Consistência de linkagem interna**. Sempre linkar para a mesma versão de uma URL em todo o seu site envia ao Google um sinal claro sobre sua versão preferida.

Para a maioria dos sites, a tag canonical HTML combinada com linkagem interna consistente cobre 90 %+ dos casos.

## Exemplos de URL canônica

**Exemplo 1: Um e-commerce com URLs cheias de parâmetros**
A página de produto de uma loja de roupas vive em `/tenis-corrida-azul`. Mas filtrar por tamanho gera `/tenis-corrida-azul?size=10`, e códigos de rastreamento adicionam `/tenis-corrida-azul?utm_source=email`. Os três mostram o mesmo produto. Sem tags canonical, o Google pode indexar a URL de parâmetro em vez da limpa. Adicionar `<link rel="canonical" href="/tenis-corrida-azul">` às três versões resolve instantaneamente.

**Exemplo 2: Um negócio multi-localização com páginas de serviço duplicadas**
Uma franquia de encanamento tem páginas de serviço para cada cidade: `/sao-paulo/desentupimento`, `/rio-de-janeiro/desentupimento`, `/belo-horizonte/desentupimento`. O conteúdo é 90 % idêntico com apenas o nome da cidade trocado. Essas páginas não devem canonicalizar entre si (miram em [palavras-chave locais](/glossary/local-keywords) diferentes), mas cada uma deve auto-referenciar. A solução real é tornar cada página genuinamente única com conteúdo específico da cidade. Algo que theStacc lida gerando artigos específicos por localização automaticamente.

**Exemplo 3: Um blog sindicando conteúdo no Medium**
Uma empresa B2B republica seus posts de blog no Medium para exposição extra. Sem uma tag canonical, o Google pode ranquear a versão do Medium em vez do original. Adicionando uma URL canônica apontando de volta para o blog da empresa em cada post do Medium (Medium suporta isso nas configurações), todos os sinais de ranking fluem para o domínio original. O [tráfego orgânico](/glossary/organic-traffic) vai para o seu site, não para o do Medium.

## URL canônica vs. redirecionamento 301

Ambos resolvem problemas de conteúdo duplicado. A escolha certa depende se a página duplicada deve permanecer acessível.

| | URL canônica | [Redirecionamento 301](/glossary/301-redirect) |
|---|---|---|
| **Usuário vê** | Ambas as páginas estão acessíveis | Usuário é enviado para a página preferida |
| **Força do sinal** | Dica forte (Google pode sobrescrever) | Definitivo (redirecionamento forçado) |
| **Use quando** | Ambas URLs precisam existir (parâmetros, sindicação) | URL antiga não deve mais ser visitada |
| **Link equity** | Consolidada para URL canônica | Passa ~95-99 % para o destino |
| **Exemplo** | Página de produto com parâmetros de filtro | URL antiga de blog movida para nova estrutura |

Quando a página duplicada deve permanecer acessível (URLs rastreadas, resultados filtrados, conteúdo sindicado), use uma canonical. Quando a URL antiga está morta e enterrada, use uma 301.

## Boas práticas com URL canônica

- **Auto-referencie cada página**. Mesmo páginas sem duplicatas devem ter uma tag canonical auto-referencial. É uma rede de segurança contra URLs duplicadas inesperadas de parâmetros, IDs de sessão ou peculiaridades do CMS.
- **Use URLs absolutas, não relativas**. Sempre escreva a URL completa: `https://example.com/page`. Não `/page`. Canonicals relativas podem causar problemas com resolução de protocolo e domínio.
- **Aponte canonicals para páginas indexáveis**. Nunca defina uma canonical para uma página [noindexada](/glossary/noindex), redirecionada ou que retorna [404](/glossary/404-error). Isso confunde o Google e derrota o propósito.
- **Audite canonicals após migrações de site**. Mudanças de CMS, mudanças de domínio e redesigns frequentemente quebram tags canonical. Execute um crawl com Screaming Frog ou Sitebulb após o lançamento para verificar se cada página aponta para a canonical correta.
- **Mantenha seus sinais consistentes**. Sua tag canonical, sitemap, links internos e hreflang (para sites internacionais) devem todos concordar com a URL preferida. Quando sinais conflitam, o Google faz sua própria escolha. E pode não ser a que você quer. theStacc publica todos os artigos com tags canonical adequadas e estruturas de URL limpas embutidas.

## Perguntas Frequentes

### Tags canonical passam link equity?

Sim. O Google consolida sinais de ranking de páginas duplicadas para a URL canônica. Se 10 sites linkam para uma versão de parâmetro da sua página e a canonical aponta para a versão limpa, a versão limpa recebe o benefício desses links.

### Posso canonicalizar para um domínio diferente?

Sim. Canonicals entre domínios dizem ao Google que o conteúdo original vive em um domínio diferente. Caso de uso comum: sindicar conteúdo no Medium, LinkedIn ou sites parceiros mantendo seu domínio como fonte canônica.

### O que acontece se minha tag canonical estiver errada?

O Google pode ignorá-la. Se a canonical aponta para uma página com conteúdo completamente diferente, o Google reconhece a incompatibilidade e indexará as URLs independentemente. Tags canonical só funcionam quando as páginas têm conteúdo substancialmente similar.

### Como verifico minhas tags canonical?

Veja o código fonte da página e procure por `rel="canonical"`. Ou use o [Google Search Console](/glossary/google-search-console). A ferramenta de Inspeção de URL mostra qual canonical o Google selecionou para qualquer página. Se a canonical escolhida pelo Google difere da sua, há um conflito nos seus sinais.

---

Quer cada artigo publicado com tags canonical adequadas, URLs limpas e [SEO técnico](/glossary/technical-seo) gerenciado automaticamente? theStacc publica 30 artigos otimizados para SEO no seu site todo mês. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: Consolidar URLs duplicadas](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Moz: Guia de tag de URL canônica](https://moz.com/learn/seo/canonicalization)
- [Ahrefs: Tags canonical para SEO](https://ahrefs.com/blog/canonical-tags/)
- [Semrush: Estudo de conteúdo duplicado](https://www.semrush.com/blog/duplicate-content/)
- [Google Search Console: Ferramenta de Inspeção de URL](https://support.google.com/webmasters/answer/9012289)
