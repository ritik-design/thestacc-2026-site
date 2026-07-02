---
term: "Schema Markup"
slug: "schema-markup"
definition: "Schema Markup é um código padronizado (geralmente JSON-LD) que você adiciona às páginas para que buscadores entendam o conteúdo e exibam resultados enriquecidos."
category: "SEO"
difficulty: "Intermediate"
keyword: "o que é schema markup"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "rich-results"
  - "serp"
  - "technical-seo"
  - "json-ld"
  - "e-e-a-t"
---

## O que é Schema Markup?

**Schema Markup é um vocabulário de dados estruturados que você adiciona ao seu HTML para dizer aos buscadores exatamente o que o seu conteúdo representa: um produto, uma receita, um evento, um negócio, uma FAQ.**

Sem schema, o Google precisa adivinhar do que se trata a sua página. Com schema, você entrega um diagrama com etiquetas. A marcação segue o padrão Schema.org, mantido em conjunto por Google, Microsoft, Yahoo e Yandex.

Um estudo da Milestone Research apontou que páginas com schema markup posicionam, em média, 4 posições acima das que não têm. Não porque schema seja fator de ranqueamento direto – o Google já disse que não é. Mas os [resultados enriquecidos](/glossary/rich-results) gerados pelo schema disparam a taxa de cliques, e um CTR maior, com o tempo, influencia ranqueamentos.

## Por que dados estruturados importam?

A maior parte dos sites ainda não usa schema. Uma janela de oportunidade para qualquer empresa disposta a investir 30 minutos na implementação.

- **Resultados enriquecidos na busca**. Estrelas de avaliação, FAQs em sanfona, faixas de preço e datas de eventos aparecem direto na [SERP](/glossary/serp). Esses elementos visuais podem subir o CTR em 20–30 %.
- **Mais visibilidade em IA**. O AI Overviews do Google e outras experiências guiadas por IA puxam dos dados estruturados. Schema deixa o seu conteúdo mais fácil de ser citado por máquinas.
- **Presença local reforçada** – o [schema LocalBusiness](/glossary/localbusiness-schema) envia horários, endereço e avaliações direto para os Knowledge Panels do Google e para o [local pack](/glossary/local-pack).
- **Pronto para busca por voz**. Quando alguém pergunta algo a um assistente de voz, os dados estruturados ajudam a sua resposta a aparecer. FAQ e How-To schema brilham aqui.

Se você investe em conteúdo de [SEO](/glossary/seo) e não adiciona schema, está deixando visibilidade na mesa.

## Como o Schema Markup funciona

Schema mora no HTML da sua página. Os robôs leem, validam e usam para gerar resultados de busca enriquecidos.

### O formato do código

Existem três formatos: JSON-LD, Microdata e RDFa. O Google recomenda JSON-LD. É um bloco de script que você coloca dentro do `<head>`. Não se mistura com o HTML visível, o que torna a manutenção mais limpa e reduz o risco de quebrar o layout.

### O processo de validação

Depois de adicionar schema, o relatório de Resultados Avançados do Google Search Console mostra se a sua marcação é válida. Erros – campos obrigatórios faltando, tipos incorretos – impedem a exibição dos resultados enriquecidos. A ferramenta Rich Results Test do Google permite checar URLs uma a uma antes do deploy em todo o site.

### Como o Google processa

O Googlebot rastreia a página, faz o parse do JSON-LD e cruza com os tipos de schema conhecidos. Se tudo bate e a página atende às diretrizes de qualidade, o listing enriquecido aparece na busca dentro de alguns dias a poucas semanas. Nem todo schema válido dispara um resultado enriquecido. O Google decide pelo contexto da consulta e pela qualidade da página.

## Tipos de Schema Markup

O Schema.org lista mais de 800 tipos. Mas, para a maioria dos negócios, um punhado cobre 90 % dos casos:

- **Article schema**. Diz ao Google que a página é um post de blog ou matéria de notícias. Ajuda no Google Discover e nos carrosséis de notícias.
- **FAQ schema**. Adiciona pares pergunta-resposta expansíveis direto no seu resultado. Alto impacto para consultas informacionais.
- **LocalBusiness schema**. Envia nome, endereço, horários e avaliações para o Google. Indispensável para [SEO local](/glossary/local-seo).
- **Product schema**. Exibe preço, disponibilidade e notas na busca. Crítico para e-commerce.
- **How-To schema**. Mostra instruções passo a passo com imagens nos resultados. Vai bem com conteúdo tutorial.
- **Review/Rating schema**. Aquelas estrelas amarelas que aparecem nos resultados. Sobem o CTR consideravelmente.

O schema certo depende do tipo de página. A página de serviços de um encanador precisa de LocalBusiness. Um post de blog precisa de Article e, possivelmente, FAQ.

## Exemplos de Schema Markup

**Exemplo 1: Clínica odontológica com FAQ schema**
Uma dentista em São Paulo adiciona FAQ schema na página de serviço "Clareamento dental" com 5 perguntas comuns de pacientes. O resultado dela na busca passa a mostrar Q&A expansíveis, ocupando 3 vezes o espaço visual dos concorrentes. Os cliques para essa página sobem 35 % em 2 meses.

**Exemplo 2: Empresa de climatização com LocalBusiness schema**
Uma empresa de ar-condicionado adiciona LocalBusiness schema com área de atendimento, horários e nota agregada (4,8 estrelas a partir de mais de 200 avaliações). O Google passa a mostrar as estrelas direto nos resultados orgânicos – não só no map pack. A empresa percebe um aumento visível nas ligações vindas da busca orgânica.

**Exemplo 3: Blog SaaS com Article schema**
Uma empresa de software B2B publica guias how-to toda semana. Depois de adicionar Article schema com informações de autor e datas de publicação, os posts começam a aparecer no Google Discover. Só o tráfego do Discover já soma 15 % nas visitas orgânicas mensais.

## Schema Markup vs. Rich Snippets

Os dois termos são usados como sinônimos. Não deveriam ser.

| | Schema Markup | Rich Snippets / Resultados enriquecidos |
|---|---|---|
| **O que é** | Código que você adiciona às páginas | Listings enriquecidos que o Google exibe |
| **Quem controla** | Você (o webmaster) | O Google (decide se mostra) |
| **Garantido?** | A marcação você sempre pode adicionar | O Google pode ou não mostrar resultados enriquecidos |
| **Objetivo** | Comunicar o significado da página aos robôs | Melhorar a aparência visual nas [SERPs](/glossary/serp) |
| **Exemplo** | Script JSON-LD no seu HTML | Estrelas de avaliação abaixo do seu listing |

Schema markup é o input. Resultados enriquecidos são o (possível) output. Adicionar marcação não garante listings enriquecidos. Mas, sem ela, você nunca vai conseguir um.

## Boas práticas de Schema Markup

- **Comece pelo que importa mais**. Não tente adicionar todos os tipos de schema de uma vez. É um negócio local? Comece com LocalBusiness e FAQ. Vá somando depois.
- **Use JSON-LD, não Microdata**. O Google prefere. Mais simples de implementar, mais fácil de debugar e não polui o HTML.
- **Valide cada página**. Passe todo schema novo pelo Rich Results Test do Google antes de publicar. Um único campo faltando pode invalidar o bloco inteiro.
- **Mantenha o schema preciso**. Mudou os horários? Atualize o schema. Dados estruturados imprecisos violam as diretrizes do Google e podem revogar seus resultados enriquecidos.
- **Combine schema com conteúdo de qualidade**. Schema em páginas fracas não gera resultados enriquecidos. Serviços como o theStacc publicam 30 artigos otimizados para SEO por mês. Cada um é uma chance de aplicar Article e FAQ schema que realmente conquistem rich results.

## Perguntas frequentes

### Schema markup é fator de ranqueamento?

O Google diz que schema não é fator de ranqueamento direto. Mas páginas com schema ganham [resultados enriquecidos](/glossary/rich-results), que sobem o CTR. CTR maior envia sinais positivos de engajamento, que podem melhorar ranqueamentos de forma indireta.

### Como adiciono schema ao meu site?

O caminho mais simples é JSON-LD: um bloco de script dentro do `<head>` da página. Plugins de WordPress como Yoast e RankMath geram automaticamente. Para sites sob medida, use o Structured Data Markup Helper do Google.

### Schema funciona para pequenas empresas?

Com certeza. Negócios locais costumam ver o maior impacto porque LocalBusiness e FAQ schema são subutilizados pelos concorrentes pequenos. Adicionar schema básico a um site local de 10 páginas leva menos de uma hora.

### Quanto tempo até aparecerem resultados enriquecidos?

Depois de adicionar schema válido, o Google costuma processar em poucos dias ou até 2 semanas. Acompanhe o status no relatório de Resultados Avançados do Google Search Console.

---

Quer conteúdo de SEO otimizado e publicado sem mexer um dedo? O theStacc publica 30 artigos no seu site todo mês. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: Como os dados estruturados funcionam](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
- [Milestone Research: O impacto do Schema Markup nos ranqueamentos](https://www.milestoneinternet.com/thought-leadership/research/schema-markup-drives-results)
- [Moz: O guia para iniciantes em dados estruturados](https://moz.com/blog/beginners-guide-to-structured-data)
