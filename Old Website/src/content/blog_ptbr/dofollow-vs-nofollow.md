---
title: "Dofollow vs Nofollow (2026): Estratégias, Táticas e Exemplos"
description: "Guia de dofollow vs nofollow para 2026: estratégias, táticas, exemplos reais e etapas de implementação para obter resultados mais rápido."
slug: "dofollow-vs-nofollow"
keyword: "dofollow vs nofollow"
author: "Siddharth Gangal"
date: "2026-06-09"
category: "SEO Tips"
image: "/blogs-preview-images/dofollow-vs-nofollow.webp"
---

Todo link na internet se enquadra em uma de duas categorias. Links dofollow transmitem autoridade de ranqueamento. Links nofollow dizem ao Google para não contar o link como um voto.

Entender a diferença entre dofollow vs nofollow determina como você constrói backlinks, estrutura links internos e audita o seu perfil de links. Errar nisso significa perder meses perseguindo links que não movem os ranqueamentos. Ou pior, disparar uma penalidade do Google por construir um perfil de links não natural.

89,4% de todos os backlinks entre os 110.000 principais sites são dofollow. Os 10,6% restantes são nofollow. Mas um perfil de links saudável precisa dos dois tipos. O Google espera uma mistura natural.

Publicamos mais de 3.500 artigos de SEO em mais de 70 setores. Estratégia de links faz parte de toda campanha. Este guia cobre tudo o que você precisa saber sobre links dofollow e nofollow, incluindo a atualização de 2019 do Google que mudou como o nofollow funciona.

Veja o que você vai aprender:

- A diferença exata entre links dofollow e nofollow
- Como o Google mudou o nofollow de uma diretriz para uma "dica" em 2019
- Quando usar `rel="nofollow"`, `rel="sponsored"` e `rel="ugc"`
- Como verificar o status de follow de qualquer link em segundos
- A proporção ideal de dofollow para nofollow em um perfil natural
- Erros comuns que disparam penalidades do Google

![Comparação entre links dofollow e nofollow mostrando como cada tipo afeta o SEO](/images/blog/dofollow-vs-nofollow-comparison.webp)

---

## O Que São Links Dofollow?

Um link dofollow é um link HTML padrão que transmite link equity (também chamado de "link juice" ou PageRank) de uma página para outra. Não existe o atributo `rel="dofollow"` em HTML. "Dofollow" é um termo do setor para um link sem o atributo nofollow aplicado.

Veja como um link dofollow se parece em HTML:

```html
<a href="https://example.com">Texto Âncora</a>
```

Nenhum atributo especial é necessário. Todo link é dofollow por padrão.

Quando o Google rastreia um link dofollow, 3 coisas acontecem:

1. O Google segue o link até a página de destino
2. O Google transmite uma parte da autoridade da página de origem para o destino
3. O Google usa o link como um sinal de ranqueamento para a página de destino

Links dofollow são a base do algoritmo original PageRank do Google. Quanto mais links dofollow apontam para uma página a partir de fontes autoritárias, maior essa página tende a ranquear. [Sites com perfis de backlink fortes](https://ahrefs.com/blog/backlink-growth-study/) recebem 67% mais tráfego orgânico do que sites com perfis fracos.

É por isso que a construção de links continua sendo uma das partes mais importantes (e mais difíceis) do SEO. 41% dos profissionais de marketing dizem que construir [backlinks](/glossary_ptbr/backlinks) de qualidade é a tarefa de SEO mais difícil que enfrentam.

---

## O Que São Links Nofollow?

Um link nofollow inclui o atributo `rel="nofollow"`. Esse atributo diz aos mecanismos de busca: "Não use este link como um sinal de ranqueamento."

Veja como um link nofollow se parece em HTML:

```html
<a href="https://example.com" rel="nofollow">Texto Âncora</a>
```

O Google introduziu o atributo nofollow em 2005 para combater spam em comentários. Spammers estavam inundando comentários de blogs e fóruns com links para impulsionar seus ranqueamentos. O nofollow deu aos proprietários de sites uma forma de linkar sem transmitir autoridade.

### Onde Links Nofollow Aparecem Naturalmente

A maioria dos links na internet é nofollow por padrão nessas plataformas:

- **Redes sociais:** Links do Facebook, X (Twitter), LinkedIn, Instagram, Pinterest e TikTok
- **Fóruns e comunidades:** Reddit, Quora, Stack Overflow e a maioria dos softwares de fórum
- **Comentários de blogs:** WordPress e a maioria das plataformas CMS aplicam nofollow automaticamente em links de comentários
- **Wikipedia:** Todos os links externos carregam nofollow
- **Comunicados de imprensa:** A maioria dos serviços de distribuição de comunicados de imprensa usa nofollow
- **Diretórios gerados por usuários:** Yelp, links do Google Business Profile e plataformas de avaliação

Links nofollow não impulsionam os ranqueamentos diretamente. Mas eles servem a outros propósitos. Eles geram tráfego de referência, constroem reconhecimento de marca e sinalizam ao Google que o seu site tem diversidade natural de links.

---

## Dofollow vs Nofollow: Principais Diferenças

A diferença se resume a uma pergunta: o link transmite autoridade de ranqueamento?

| Recurso | Dofollow | Nofollow |
|---|---|---|
| Transmite link equity | Sim | Não (mas o Google pode ignorar) |
| Atributo HTML | Nenhum (comportamento padrão) | `rel="nofollow"` |
| Impacto direto no SEO | Sim. Melhora os ranqueamentos | Sem impacto direto |
| Tráfego de referência | Sim | Sim |
| Rastreamento do Google | Sempre seguido e rastreado | Pode ou não ser rastreado |
| Visibilidade da marca | Sim | Sim |
| Necessidade em perfil natural | 60-80% dos links totais | 20-40% dos links totais |
| Risco de superotimização | Alto se 100% dofollow | Baixo |

O detalhe crítico que a maioria dos guias ignora: desde 2019, o Google trata o nofollow como uma "dica", não uma diretriz. O Google pode escolher seguir e contar um link nofollow se seus algoritmos determinarem que o link é relevante e confiável. Mais sobre isso na próxima seção.

> Links dofollow constroem autoridade de ranqueamento. Links nofollow constroem um perfil natural. Você precisa dos dois.

---

## Atualização de 2019 do Google: Nofollow Virou uma Dica

Em 10 de setembro de 2019, o Google publicou um post de blog intitulado ["Evolving nofollow"](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) que mudou como os links nofollow funcionam. Essa atualização é o desenvolvimento mais importante na atribuição de links em mais de uma década. Muitos guias de SEO ainda erram nisso.

### O Que Mudou

**Antes de 2019:** Nofollow era uma diretriz. O Google obedecia absolutamente. Um link nofollow transmitia zero autoridade, zero sinais de rastreamento e zero benefício de ranqueamento. Ponto final.

**Depois de 2019:** Nofollow virou uma dica. O Google se reserva o direito de considerar links nofollow como sinais de ranqueamento se seus algoritmos os acharem relevantes. O Google também pode descobrir e indexar novas páginas através de links nofollow.

### Três Novos Atributos de Link

O Google introduziu 2 novos atributos junto com o nofollow:

| Atributo | Caso de Uso | Exemplo |
|---|---|---|
| `rel="sponsored"` | Links pagos, anúncios, patrocínios | Links de afiliados, colocações pagas, links de banners de anúncios |
| `rel="ugc"` | Conteúdo gerado por usuários | Comentários de blogs, posts de fóruns, envios de comunidade |
| `rel="nofollow"` | Sinal geral de "não endosso" | Qualquer link para o qual você não queira se responsabilizar |

Você pode combinar atributos: `rel="nofollow sponsored"` ou `rel="nofollow ugc"`. O Google recomenda usar o atributo mais específico disponível.

![Evolução do nofollow do Google de diretriz para dica com novos atributos sponsored e ugc](/images/blog/google-nofollow-hint-evolution.webp)

### O Que Isso Significa na Prática

**Para construtores de links:** Links nofollow de sites autoritários (Wikipedia, grandes publicações, Reddit) podem agora carregar algum valor de ranqueamento. Você não deve ignorá-los.

**Para proprietários de sites:** Use `rel="sponsored"` em links pagos. Use `rel="ugc"` em links enviados por usuários. Use `rel="nofollow"` em qualquer link em que você não confie ou endosse. Links nofollow existentes não precisam ser alterados.

**Para auditores de SEO:** Uma auditoria de backlinks deve agora analisar links nofollow de domínios de alta autoridade separadamente. Eles podem contribuir para os ranqueamentos mesmo sem transmitir link equity tradicional.

78,8% dos profissionais de SEO acreditam que links nofollow ainda afetam os ranqueamentos até certo ponto. O modelo de "dica" significa que o tratamento do Google para nofollow não é mais binário.

---

> **Pare de escrever. Comece a ranquear.** A Stacc publica 30 artigos de SEO por mês por $99. Cada artigo constrói a sua autoridade de domínio com links internos e externos.
> [Comece por $1 →](/pricing)

---

## Quando Usar Cada Tipo de Link

Saber quando aplicar atributos dofollow ou nofollow previne penalidades e maximiza o valor do link.

### Quando Usar Dofollow (Padrão)

Deixe links como dofollow quando você genuinamente endossar o destino:

- **Links editoriais no seu próprio conteúdo:** Links para fontes, referências e recursos que você recomenda
- **Links internos:** Todos os [links internos](/blog_ptbr/internal-linking-strategy) devem ser dofollow (com raras exceções)
- **Links de biografia de posts convidados:** Prática padrão para contribuições convidadas legítimas
- **Links de páginas de recursos:** Listas curadas de ferramentas, guias ou referências em que você confia
- **Links de parceiros e fornecedores:** Quando o relacionamento é genuíno, não pago

### Quando Usar Nofollow

Aplique `rel="nofollow"` quando você não quiser se responsabilizar pelo destino:

- **Conteúdo não confiável:** Links para sites que você não verificou pessoalmente
- **Seções de comentários:** Qualquer link enviado por usuários (a maioria das plataformas CMS lida com isso automaticamente)
- **Links de login ou cadastro:** O Google não precisa rastrear essas páginas

### Quando Usar rel="sponsored"

Aplique `rel="sponsored"` em qualquer link que envolva troca monetária:

- **Links de afiliados:** Recomendações de produtos com parâmetros de rastreamento
- **Colocações pagas:** Conteúdo patrocinado, publieditoriais, listagens pagas em diretórios
- **Links de banners de anúncios:** Publicidade display que linka para sites externos
- **Parcerias com influenciadores:** Links de resenhas de produtos com compensação envolvida

O Google afirmou explicitamente que deixar de marcar links pagos com `rel="sponsored"` ou `rel="nofollow"` pode resultar em uma penalidade manual. Isso se aplica tanto ao site que linka quanto ao site linkado.

### Quando Usar rel="ugc"

Aplique `rel="ugc"` em links criados pelos seus usuários:

- **Comentários de blogs:** Comentários enviados por usuários com links
- **Posts de fóruns:** Conteúdo gerado pela comunidade
- **Avaliações de usuários:** Resenhas de produtos ou serviços enviadas por clientes
- **Conteúdo estilo wiki:** Páginas editáveis por membros da comunidade

### Árvore de Decisão de Referência Rápida

| Cenário de Link | Atributo a Usar |
|---|---|
| Você escreveu e endossa o destino | Dofollow (sem atributo) |
| Usuário enviou o link | `rel="ugc"` |
| Dinheiro mudou de mãos | `rel="sponsored"` |
| Você não confia no destino | `rel="nofollow"` |
| Link interno dentro do seu próprio site | Dofollow (sem atributo) |
| Link de afiliado com rastreamento | `rel="sponsored"` |

---

## Como Verificar Se um Link É Dofollow ou Nofollow

Você pode verificar o status de follow de qualquer link de 3 formas. Da inspeção manual a ferramentas de auditoria em massa.

### Método 1: Inspecionar Elemento (Manual)

Clique com o botão direito em qualquer link no seu navegador e selecione "Inspecionar" ou "Inspecionar Elemento". Olhe a tag `<a>` no HTML.

**Exemplo dofollow:**
```html
<a href="https://example.com">Texto do Link</a>
```
Nenhum atributo `rel="nofollow"` presente. O link é dofollow.

**Exemplo nofollow:**
```html
<a href="https://example.com" rel="nofollow">Texto do Link</a>
```
O atributo `rel="nofollow"` diz ao Google para não transmitir autoridade.

Esse método funciona para verificar links individuais. Não escala para auditar um site inteiro.

### Método 2: Extensões de Navegador (Verificação Rápida)

Instale uma extensão de navegador que destaque os tipos de link automaticamente:

- **NoFollow** (Chrome): Destaca links nofollow com uma borda pontilhada vermelha
- **SEOquake** (Chrome/Firefox): Mostra o status de follow em uma sobreposição da barra de ferramentas
- **MozBar** (Chrome): Exibe atributos de link junto com métricas de DA/PA

Essas extensões funcionam em qualquer página web. São úteis para análise rápida de concorrentes e verificação pontual do seu próprio conteúdo.

### Método 3: Ferramentas de Rastreamento (Auditoria em Massa)

Para uma auditoria completa do site, use uma ferramenta de rastreamento para analisar todos os links:

- **Screaming Frog:** Rastreia todo o seu site e exporta todos os links com seus atributos
- **Ahrefs Site Audit:** Identifica a sua proporção de dofollow/nofollow em todas as páginas
- **Semrush Backlink Audit:** Analisa o seu perfil de links de entrada por status de follow

Uma auditoria de [SEO completa](/blog_ptbr/how-to-do-seo-audit) deve incluir uma análise de atributos de link. Isso revela se o seu perfil parece natural ou superotimizado.

---

## Construindo um Perfil de Links Natural

O Google espera uma mistura natural de links dofollow e nofollow. Um perfil com 100% de links dofollow sinaliza manipulação. Um perfil com muitos links nofollow sugere baixa autoridade.

### A Proporção Ideal

| Tipo de Perfil | % Dofollow | % Nofollow | Nível de Risco |
|---|---|---|---|
| Natural / Saudável | 60-80% | 20-40% | Baixo |
| Ligeiramente agressivo | 80-90% | 10-20% | Médio |
| Superotimizado | 90-100% | 0-10% | Alto |
| Déficit de autoridade | Abaixo de 50% | Acima de 50% | Médio |

A média entre os 110.000 principais sites é 89,4% dofollow e 10,6% nofollow. Mas essa média é alta porque grandes sites de autoridade atraem naturalmente mais links editoriais dofollow.

![Proporções de perfil de links natural mostrando porcentagens de dofollow vs nofollow e níveis de risco](/images/blog/dofollow-nofollow-link-profile-ratio.webp)

Para pequenas e médias empresas, uma divisão de 70/30 é um alvo saudável. Alcance isso construindo links dofollow de qualidade através de conteúdo e outreach enquanto acumula naturalmente links nofollow de redes sociais, fóruns e diretórios.

### Como Construir Links Dofollow

Os melhores links dofollow vêm de menções editoriais. Alguém lê o seu conteúdo, acha valioso e linka para ele sem ser solicitado. Aqui estão estratégias que geram links dofollow editoriais:

- **Publique pesquisas ou dados originais.** Estudos de dados atraem citações. Jornalistas e blogueiros linkam para estatísticas originais.
- **Crie guias de alta utilidade.** Guias passo a passo que resolvem problemas reais ganham links de páginas de recursos.
- **Construa ferramentas gratuitas.** Uma ferramenta gratuita útil ganha links naturais de qualquer um que a recomende. Confira nossas [ferramentas de SEO](/tools/seo-audit) para exemplos.
- **Guest posting em sites relevantes.** Escreva para sites no seu setor. Inclua um link dofollow natural no corpo do conteúdo (não apenas na biografia).
- **Corrija links quebrados.** Encontre links de saída quebrados em sites de autoridade e ofereça o seu conteúdo como substituição. Isso é chamado de [broken link building](/blog_ptbr/broken-link-building).
- **Conquiste menções na imprensa.** Responda a consultas de jornalistas em plataformas como HARO, Connectively ou Qwoted.

### Como Conquistar Links Nofollow Naturalmente

Links nofollow se acumulam através da atividade comercial normal:

- Compartilhe o seu conteúdo em plataformas de redes sociais (todos os links sociais são nofollow)
- Participe de discussões relevantes no Reddit e Quora
- Mantenha listagens comerciais em diretórios e plataformas de avaliação
- Incentive avaliações de clientes que linkem para o seu site
- Comente em blogs do setor com insights genuínos (não spam)

---

> **O seu time de SEO. $99 por mês.** 30 artigos otimizados, publicados automaticamente. Cada artigo conquista backlinks e constrói autoridade tópica ao longo do tempo.
> [Comece por $1 →](/pricing)

---

## Erros Comuns de Dofollow vs Nofollow

Esses erros custam ranqueamentos e às vezes disparam penalidades. Evite todos eles.

**Erro 1: Aplicar nofollow nos seus próprios links internos.**
Links internos devem ser quase sempre dofollow. Adicionar nofollow a links internos bloqueia o fluxo de PageRank dentro do seu próprio site. Isso é chamado de "escultura de PageRank", e o [Google confirmou em 2009](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) que isso não funciona. O PageRank que fluiría através de um link interno com nofollow evapora. Ele não se redistribui para outros links.

**Erro 2: Construir 100% de links dofollow.**
Um perfil totalmente dofollow parece fabricado. Os algoritmos do Google detectam padrões não naturais. Um perfil saudável inclui links nofollow de plataformas sociais, diretórios e conteúdo gerado por usuários. Almeje uma proporção de 70/30 dofollow para nofollow.

**Erro 3: Não marcar links pagos como sponsored.**
O Google exige `rel="sponsored"` ou `rel="nofollow"` em qualquer link que envolva pagamento. Deixar de marcar links pagos pode resultar em uma penalidade de ação manual contra ambos os sites. Isso inclui links de afiliados, posts patrocinados e colocações pagas em diretórios.

**Erro 4: Ignorar links nofollow na sua análise de backlinks.**
Após a atualização de 2019, links nofollow de domínios de alta autoridade podem carregar valor de ranqueamento. Uma auditoria de backlinks completa deve analisar ambos os tipos de link. Descartar todos os links nofollow ignora potenciais sinais de ranqueamento.

**Erro 5: Obsessão com atributos de link individuais.**
Um link dofollow de um site de spam de baixa autoridade prejudica mais do que ajuda. Um link nofollow do New York Times gera milhares de visitantes de referência. Qualidade e relevância importam mais do que o status de follow. Foque em conquistar links de fontes relevantes e autoritárias, independentemente da política de nofollow delas.

**Erro 6: Usar nofollow em links editoriais de saída.**
Alguns proprietários de sites aplicam nofollow em todo link de saída para "acumular" PageRank. Isso é desnecessário e potencialmente prejudicial. O Google espera linkagem de saída natural. Aplicar nofollow em todo link externo faz o seu conteúdo parecer suspeito. Link para fontes autoritárias com dofollow. Isso não prejudica os seus ranqueamentos.

---

## Dofollow vs Nofollow e Linkagem Interna

Links internos merecem atenção especial. Eles funcionam de forma diferente dos backlinks externos.

Todo [link interno](/blog_ptbr/internal-linking-strategy) no seu site deve ser dofollow. Links internos distribuem PageRank entre as suas páginas. Eles ajudam o Google a descobrir e indexar novo conteúdo. Eles sinalizam quais páginas você considera mais importantes.

A única exceção: páginas de login, carrinhos de compras ou outras páginas que você não queira que o Google priorize. Mas mesmo essas raramente precisam de nofollow. O Google lida com a maioria delas através de `robots.txt` e tags `noindex`.

Uma estrutura de linkagem interna forte multiplica o valor de cada backlink dofollow que o seu site conquista. Quando um link dofollow externo aponta para a sua página inicial, links internos distribuem essa autoridade para os seus posts de blog, páginas de produtos e páginas de serviços.

Use otimização de [texto âncora](/glossary_ptbr/anchor-text) para links internos. Texto âncora descritivo diz ao Google sobre o que é a página de destino. Evite frases genéricas como "clique aqui" ou "leia mais".

---

## A Distinção Entre Nofollow e Noindex

Iniciantes frequentemente confundem nofollow com noindex. Eles servem a propósitos completamente diferentes.

| Atributo | O Que Faz | Escopo |
|---|---|---|
| `rel="nofollow"` | Diz ao Google para não transmitir autoridade através de um link específico | Nível de link |
| `<meta name="robots" content="noindex">` | Diz ao Google para não incluir uma página nos resultados de busca | Nível de página |

Um link nofollow ainda permite que o Google veja e potencialmente rastreie a página de destino. Ele apenas afeta se a autoridade passa através daquele link específico.

Uma tag noindex esconde uma página inteira dos resultados de busca. A página ainda existe e carrega para visitantes. Mas o Google a remove do índice.

Esses dois atributos resolvem problemas diferentes. Use nofollow quando você não quer que um link transmita autoridade. Use noindex quando você não quer que uma página apareça nos resultados de busca. Eles podem ser usados juntos na mesma página para controle máximo.

Para mais sobre como o Google lida com diretrizes de indexação, veja o nosso [checklist de SEO técnico](/blog_ptbr/technical-seo-checklist).

---

> **Mais de 3.500 blogs publicados. 92% de score de SEO médio.** Veja o que a Stacc pode fazer pela sua estratégia de construção de links. Publicamos conteúdo que conquista backlinks.
> [Comece por $1 →](/pricing)

---

## Perguntas Frequentes

**Qual é a diferença entre links dofollow e nofollow?**

Um link dofollow transmite autoridade de ranqueamento (PageRank) de uma página para outra. Um link nofollow inclui `rel="nofollow"`, que diz ao Google para não contá-lo como um sinal de ranqueamento. Dofollow melhora o SEO diretamente. Nofollow gera tráfego e visibilidade de marca sem impacto direto no ranqueamento.

**Links nofollow ajudam no SEO?**

Links nofollow não transmitem autoridade de ranqueamento diretamente. Mas eles contribuem para um perfil de links natural, geram tráfego de referência e constroem reconhecimento de marca. Desde a atualização de 2019 do Google, nofollow é uma "dica" em vez de uma diretriz. O Google pode escolher contar alguns links nofollow como sinais de ranqueamento. 78,8% dos profissionais de SEO acreditam que links nofollow ainda afetam os ranqueamentos.

**Qual é a proporção ideal de links dofollow para nofollow?**

Um perfil de links saudável contém 60 a 80% de links dofollow e 20 a 40% de links nofollow. A média entre os principais sites é 89,4% dofollow. Para pequenas e médias empresas, uma divisão de 70/30 sinaliza um perfil natural e orgânico. Um perfil 100% dofollow parece fabricado e corre o risco de disparar penalidades do Google.

**Links de redes sociais são dofollow ou nofollow?**

Todas as principais plataformas de redes sociais usam links nofollow. Isso inclui Facebook, X (Twitter), LinkedIn, Instagram, Pinterest e TikTok. Links de redes sociais não transmitem autoridade de ranqueamento direta. Eles geram tráfego de referência e contribuem para a sua porcentagem de links nofollow.

**Qual é a diferença entre nofollow e noindex?**

Nofollow é um atributo de nível de link que impede a autoridade de passar através de um link específico. Noindex é uma diretriz de nível de página que impede uma página inteira de aparecer nos resultados de busca. Eles resolvem problemas diferentes. Use nofollow em links que você não endossa. Use noindex em páginas que você não quer indexadas.

**Devo aplicar nofollow em todos os links de saída?**

Não. Aplicar nofollow em todo link de saída é desnecessário e parece não natural. Link para fontes autoritárias com dofollow quando você genuinamente endossa o conteúdo. O Google espera linkagem de saída natural. Use nofollow apenas em links em que você não confia, links pagos ou conteúdo gerado por usuários.

**O que são rel="sponsored" e rel="ugc"?**

O Google introduziu esses atributos em setembro de 2019 junto com a mudança do nofollow para "dica". Use `rel="sponsored"` em qualquer link que envolva troca monetária (links de afiliados, colocações pagas, patrocínios). Use `rel="ugc"` em conteúdo gerado por usuários (comentários, posts de fóruns, avaliações). Ambos dizem ao Google para não transmitir autoridade de ranqueamento através do link.

---

Links dofollow e nofollow servem a propósitos diferentes. Ambos são essenciais para uma estratégia de SEO saudável. Construa links dofollow para autoridade de ranqueamento. Conquiste links nofollow para tráfego, diversidade e sinais naturais. Monitore a sua proporção, marque links pagos corretamente e lembre-se de que o Google trata o nofollow como uma dica, não um comando.
