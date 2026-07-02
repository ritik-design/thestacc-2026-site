---
term: "hreflang"
slug: "hreflang"
definition: "hreflang é um atributo HTML que indica aos buscadores qual versão linguística ou regional de uma página entregar a cada usuário, evitando conteúdo duplicado."
category: "SEO"
difficulty: "Advanced"
keyword: "tag hreflang"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## O que é hreflang?

hreflang é um atributo HTML (`rel="alternate" hreflang="x"`) que sinaliza ao Google e aos demais buscadores qual idioma e qual país uma versão específica de uma página atende.

Se o seu site tem páginas em vários idiomas ou variantes regionais — português do Brasil e português de Portugal, por exemplo —, a tag hreflang impede que o Google as trate como [conteúdo duplicado](/glossary/duplicate-content). Sem ela, o Google escolhe uma única versão e a exibe globalmente. Raramente a certa para cada audiência.

Um estudo da Ahrefs mostrou que apenas 19 % dos sites multilíngues implementam hreflang corretamente. Os 81 % restantes acumulam erros: tags de retorno ausentes, URLs quebradas, códigos digitados errado. É um dos elementos do SEO técnico mais mal configurados que existem.

## Por que hreflang importa?

Acertar na implementação de hreflang determina se o público certo verá a página certa.

- **Entrega linguística correta**. Quem busca de São Paulo vê a versão brasileira, quem busca de Lisboa vê a portuguesa — sem redirecionamento manual nem JavaScript
- **Proteção contra o filtro de duplicidade**. O Google entende que suas páginas `/br/` e `/pt/` não são cópias, mas traduções intencionais
- **Melhor experiência do usuário**. Aterrissar numa página no idioma nativo reduz o bounce e aumenta a conversão
- **Preços e catálogos regionais**. Lojas online com preços, moedas ou produtos diferentes por país precisam de hreflang para servir a versão correta em cada mercado

Qualquer empresa que atua em mais de um país ou idioma precisa de hreflang. Sem exceção.

## Como o hreflang funciona

### Métodos de implementação

Há três caminhos para implementar hreflang: tags `<link>` no `<head>` do HTML, cabeçalhos HTTP (para PDFs e arquivos não-HTML) ou entradas no seu [sitemap XML](/glossary/xml-sitemap). O Google recomenda escolher um método e mantê-lo. A abordagem via sitemap costuma ser a mais administrável para sites grandes, com centenas de variantes.

### A regra do retorno bidirecional

Toda anotação hreflang precisa ser recíproca. Se a página A diz "meu equivalente em espanhol é a página B", a página B precisa dizer "meu equivalente em português é a página A". As tags de retorno ausentes são o erro de implementação número um. Sem reciprocidade, o Google ignora as anotações inteiras.

### A tag x-default

O valor `x-default` diz ao Google qual versão exibir quando não há correspondência precisa de idioma ou região. Seu plano B. Geralmente a versão em inglês ou a do mercado principal. Sem `x-default`, o Google escolhe sozinho. E nem sempre escolhe certo.

## Exemplos de hreflang

**Exemplo 1: uma loja online com versões Brasil e Portugal**
Um varejista paulista mantém `example.com/pt-br/sapatos` (preços em reais, ICMS brasileiro) e `example.com/pt-pt/sapatos` (preços em euros, IVA português, frete distinto). Sem hreflang, o Google pode mostrar a versão brasileira para quem busca em Lisboa. Com a tag hreflang correta, cada audiência vê os preços e a logística certos. A [URL canônica](/glossary/canonical-url) permanece independente em cada versão.

**Exemplo 2: uma empresa SaaS com páginas traduzidas**
Uma ferramenta de gestão de projetos tem sua home page em 8 idiomas. O time implementa hreflang via sitemap XML, com cada versão apontando para todas as outras. Quem busca em alemão chega na `/de/`, quem busca em espanhol na `/es/`, e os demais caem na versão inglesa marcada como `x-default`.

Quer publicar conteúdo internacional sem brigar com a fiação do hreflang? O theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por R$ 1 →](https://app.thestacc.com)

## Perguntas frequentes

### hreflang afeta o ranking?

hreflang não melhora o ranking diretamente. Apenas decide qual versão aparece em cada mercado. Mas servir o idioma certo para o público certo melhora sinais de engajamento — bounce mais baixo, [tempo de permanência](/glossary/dwell-time) maior — que podem influenciar o posicionamento ao longo do tempo.

### hreflang serve para o mesmo idioma em países diferentes?

Sim. É justamente um dos melhores usos do atributo. Inglês dos EUA (`en-us`), inglês do Reino Unido (`en-gb`) e inglês da Austrália (`en-au`) podem coexistir com anotações separadas. O Google usa o código do país, não só o do idioma, para decidir qual versão servir.

### O que acontece se hreflang for implementado errado?

O Google ignora completamente as anotações e decide sozinho qual versão exibir. Sem penalidade. Apenas perda de controle sobre qual página aparece em cada mercado. O relatório de Segmentação internacional do Google Search Console ajuda a identificar erros de hreflang em detalhe.

---

Quer ganhar visibilidade internacional sem montar um time de SEO em cada país? O theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por R$ 1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: implementação de hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs: guia das tags hreflang](https://ahrefs.com/blog/hreflang-tags/)
- [Moz: o guia definitivo de hreflang](https://moz.com/learn/seo/hreflang-tag)
