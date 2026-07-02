---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "Core Web Vitals são as três métricas do Google para medir a experiência da página: LCP, INP e CLS. Aprenda o que medem e como melhorá-las."
category: "SEO"
difficulty: "Intermediate"
keyword: "o que é core web vitals"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## O que são Core Web Vitals?

Core Web Vitals são um conjunto de três métricas específicas que o Google usa para medir o quão rápida, responsiva e visualmente estável uma página da web parece para usuários reais.

O Google as introduziu em 2020 e as transformou em sinal oficial de ranqueamento em 2021. Elas fazem parte da conversa mais ampla sobre [velocidade de página](/glossary/page-speed), mas são mais específicas. Em vez de uma única "pontuação de velocidade", os Core Web Vitals dividem a experiência do usuário em três componentes mensuráveis. Carregamento, interatividade e estabilidade visual.

Segundo dados do próprio Google, páginas que atendem aos três limites têm 24 % menos abandonos. Isso não é uma melhoria pequena de UX. É uma linha direta para mais conversões e melhor [tráfego orgânico](/glossary/organic-traffic).

## Por que os Core Web Vitals importam?

Ignorar Core Web Vitals não vai detonar seus rankings da noite para o dia. Mas, em condições iguais, o Google vai favorecer páginas que passam nesses benchmarks em vez das que não passam.

- **Fator de ranqueamento desde 2021**. O Google confirmou os Core Web Vitals como parte dos sinais de page experience, o que influencia diretamente onde você aparece nos [resultados de busca](/glossary/serp)
- **24 % menos abandonos**. Páginas que passam nos três limites mantêm os usuários por significativamente mais tempo (Google, 2021)
- **Impacto mobile-first**. Com a [indexação mobile-first](/glossary/mobile-first-indexing) como padrão, páginas mobile lentas são as mais penalizadas
- **Correlação com receita publicitária**. Editores que melhoraram as pontuações CWV viram até 15 % a mais de receita de anúncios graças a sessões mais longas

Se você toca um negócio local ou uma pequena empresa, isso importa porque seus concorrentes provavelmente também não estão otimizando para CWV. Tirar uma nota que passa enquanto eles não passam é uma vantagem real.

## Como os Core Web Vitals funcionam

O Google coleta dados de Core Web Vitals de usuários reais do Chrome através do Chrome User Experience Report (CrUX). Isso significa que suas pontuações vêm de visitantes de verdade. Não de uma simulação em laboratório.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) mede quanto tempo o maior elemento visível da sua página leva para carregar. Pense: a imagem hero, um bloco grande de texto ou uma miniatura de vídeo. O Google quer isso abaixo de 2,5 segundos. Acima de 4 segundos é classificado como "ruim".

A solução costuma ser direta: comprimir imagens, usar uma [CDN](/glossary/content-delivery-network-cdn), adiar recursos fora da tela e melhorar o tempo de resposta do servidor.

### Interaction to Next Paint (INP)

O INP substituiu o First Input Delay (FID) em março de 2024. Ele mede a velocidade com que sua página responde às interações do usuário. Cliques, toques e teclas pressionadas. Durante toda a visita, não apenas a primeira interação.

Um INP bom fica abaixo de 200 milissegundos. Se a sua página congela por meio segundo quando alguém clica em um botão, é uma nota reprovada. JavaScript pesado costuma ser o culpado.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) mede a estabilidade visual. Já tentou tocar em um botão e a página pulou porque um anúncio ou imagem carregou atrasado? Isso é layout shift.

O Google quer um CLS abaixo de 0,1. Causas mais comuns: imagens sem dimensões definidas, anúncios injetados acima do conteúdo e fontes web que trocam de tamanho durante o carregamento.

## Tipos de avaliação de Core Web Vitals

Os dados de Core Web Vitals vêm em dois sabores, e muitas vezes contam histórias diferentes:

- **Dados de campo (RUM)**. Real User Metrics coletadas de visitantes reais via CrUX. É o que o Google usa para decisões de ranqueamento. Você vê no [Google Search Console](/glossary/google-search-console) e no PageSpeed Insights.
- **Dados de laboratório**. Testes de performance simulados em ferramentas como Lighthouse, WebPageTest e Chrome DevTools. Úteis para depurar, mas não usados diretamente para rankings.
- **Nível de origem vs. nível de URL**. O Google avalia CWV no nível do domínio completo e no nível da página individual. Se o seu site passa no geral mas uma landing-page importante reprova, essa página ainda pode ser afetada.
- **Mobile vs. desktop**. As pontuações são medidas separadamente para mobile e desktop. A maioria dos sites tem desempenho pior no mobile, que é a versão priorizada pelo Google.

Para auditorias de [SEO técnico](/glossary/technical-seo), comece sempre pelos dados de campo. Dados de laboratório ajudam a achar o problema, mas dados de campo dizem se o problema está realmente prejudicando visitantes reais.

## Exemplos de Core Web Vitals

**Exemplo 1: a home lenta de uma empresa de encanamento**
Um encanador local em São Paulo tem uma home com LCP de 4,8 segundos por causa de uma imagem hero não comprimida (3,2 MB). Depois de converter para WebP e redimensionar para as dimensões corretas, o LCP cai para 1,9 segundo. A taxa de rejeição cai 18 % no mês seguinte.

**Exemplo 2: uma loja de e-commerce com layout shift**
Uma loja Shopify que vende produtos para pets tem CLS de 0,34 porque as imagens dos produtos carregam sem atributos width/height. Adicionar dimensões explícitas em cada tag de imagem leva o CLS para 0,04. Acabaram os cliques acidentais em "Adicionar ao carrinho" de compradores frustrados.

**Exemplo 3: um blog pesado de JavaScript**
O blog de uma agência de marketing usa 14 scripts de terceiros. Analytics, widgets de chat, embeds sociais, trackers de anúncios. O INP fica em 480 ms. Após uma auditoria e a remoção de 6 scripts não usados, o INP cai para 160 ms. Páginas criadas e publicadas pela theStacc já saem com código limpo e otimizado. Sem scripts inchados.

## Core Web Vitals vs. velocidade de página

As pessoas usam os dois como sinônimos. Não deveriam.

| | Core Web Vitals | Velocidade de página |
|---|---|---|
| **O que mede** | 3 métricas específicas de UX (LCP, INP, CLS) | Tempo total de carregamento e pontuação de performance |
| **Fonte dos dados** | Dados reais de usuários (CrUX) | Simulações de laboratório (Lighthouse) |
| **Sinal de ranqueamento do Google** | Sim, diretamente | Indiretamente (através dos CWV) |
| **Escopo** | Foco na experiência percebida | Guarda-chuva mais amplo de performance |
| **Métrica de exemplo** | LCP: 2,1 s | Pontuação PageSpeed: 74/100 |

A [velocidade de página](/glossary/page-speed) é o conceito mais amplo. Os Core Web Vitals são as métricas específicas que o Google realmente usa.

## Boas práticas para Core Web Vitals

- **Comprima e dimensione corretamente todas as imagens**. Use os formatos WebP ou AVIF, e sempre defina atributos width e height explícitos para evitar layout shift
- **Reduza scripts de terceiros**. Cada script externo (widgets de chat, analytics, trackers de anúncios) aumenta o INP. Audite sem dó e remova o que não usa.
- **Use uma CDN para ativos estáticos**. Servir imagens e CSS de edge servers próximos aos seus visitantes reduz drasticamente o LCP
- **Adie JavaScript não crítico**. Carregue o conteúdo acima da dobra primeiro, e deixe scripts secundários carregarem depois que a página estiver interativa
- **Monitore dados de campo todo mês no Google Search Console**. Pontuações de laboratório oscilam, mas dados de campo mostram se visitantes reais estão tendo uma boa experiência. Serviços como a theStacc publicam automaticamente conteúdo que segue boas práticas de HTML limpo, reduzindo problemas de CWV desde o começo.

## Perguntas frequentes

### Core Web Vitals são fator de ranqueamento?

O Google confirmou os Core Web Vitals como sinal de ranqueamento em junho de 2021. Eles fazem parte do sistema de page experience. O impacto é real, mas secundário em relação à relevância do conteúdo e aos [backlinks](/glossary/backlinks). Mais critério de desempate do que decisivo.

### O que substituiu o First Input Delay?

O Interaction to Next Paint (INP) substituiu oficialmente o FID como Core Web Vital em março de 2024. O INP mede a responsividade em todas as interações durante uma visita, não apenas no primeiro clique.

### Como verifico meus Core Web Vitals?

Use o relatório de Core Web Vitals do Google Search Console para dados de campo. O PageSpeed Insights traz dados de campo e de laboratório para qualquer URL. Chrome DevTools e Lighthouse funcionam para testes locais durante o desenvolvimento.

### O que é uma boa pontuação de LCP?

O Google classifica LCP abaixo de 2,5 segundos como "bom", entre 2,5 e 4 segundos como "precisa melhorar" e acima de 4 segundos como "ruim". A maioria dos sites tem dificuldade com o LCP por causa de imagens não otimizadas e tempos lentos de resposta do servidor.

---

Quer que seu conteúdo carregue rápido e ranqueie bem sem ter que gerenciar detalhes técnicos? A theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google: Web Vitals](https://web.dev/vitals/)
- [Google Search Central: Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev: Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs: Core Web Vitals e SEO](https://ahrefs.com/blog/core-web-vitals/)
