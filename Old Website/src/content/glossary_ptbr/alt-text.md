---
term: "Texto alternativo (alt text)"
slug: "alt-text"
definition: "O texto alternativo (alt text) descreve imagens para mecanismos de busca e leitores de tela. Aprenda a escrever texto alternativo eficaz, exemplos e por que importa para SEO."
category: "SEO"
difficulty: "Beginner"
keyword: "texto alternativo"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## O que é texto alternativo?

O texto alternativo (alt text) é um atributo HTML que fornece uma descrição escrita de uma imagem. Usado por leitores de tela para usuários com deficiência visual e por mecanismos de busca para entender o que uma imagem mostra.

Você provavelmente já viu no código: `<img src="foto.jpg" alt="descrição aqui">`. Essa descrição é o alt text. Serve a duas audiências simultaneamente. Para pessoas que não conseguem ver a imagem. Seja porque usam um leitor de tela, têm conexão lenta ou a imagem não carrega. O alt text diz o que está lá. Para o Google, é um dos sinais primários usados para indexar e ranquear imagens no Google Imagens.

A análise de acessibilidade de 2024 do WebAIM encontrou que 54,5 % das imagens na web não têm texto alternativo. Mais da metade. Isso é tanto uma falha de [acessibilidade](/glossary/accessibility-content) quanto uma oportunidade de SEO esperando para qualquer um disposto a preencher um campo de texto.

## Por que texto alternativo importa?

Alt text está na interseção de acessibilidade, [SEO](/glossary/seo) e experiência do usuário. Ignore-o, e você perde nas três frentes.

- **Conformidade de acessibilidade**. As diretrizes ADA e WCAG 2.1 exigem alt text em imagens significativas. Processos sobre acessibilidade web aumentaram 300 %+ desde 2018. Não é opcional.
- **Tráfego de busca de imagens**. O Google Imagens gera [tráfego orgânico](/glossary/organic-traffic) significativo. Sem alt text, o Google não consegue indexar suas imagens corretamente, e você perde esse tráfego inteiramente.
- **Sinais de [SEO On-Page](/glossary/on-page-seo)**. Alt text dá ao Google contexto adicional sobre o conteúdo da sua página. Um artigo sobre reforma de cozinha com imagens corretamente descritas reforça a relevância tópica da página.
- **Fallback quando imagens quebram**. Se uma imagem falha em carregar (conexão lenta, URL quebrada, clientes de email bloqueando imagens), alt text aparece em seu lugar. Usuários ainda entendem o que deveria estar lá.

Cada imagem do seu site deve ter alt text. Imagens decorativas (bordas, espaçadores) recebem um atributo alt vazio (`alt=""`). Todo o resto recebe uma descrição.

## Como o texto alternativo funciona

Escrever alt text é simples em conceito. Fazê-lo bem requer entender o que sistemas diferentes precisam dele.

### Como leitores de tela o usam

Quando um leitor de tela encontra uma imagem, lê o alt text em voz alta. Se o alt text diz "foto de stock de reunião de negócios", isso é o que o usuário ouve. Inútil. Se diz "5 membros da equipe revisando relatório de marketing em torno de mesa de conferência", o usuário entende o contexto. Escreva para a pessoa ouvindo, não para um mecanismo de busca.

### Como o Google o usa

O Googlebot não pode "ver" imagens da forma que humanos fazem. Depende de alt text, texto circundante, nomes de arquivo e dados estruturados para entender conteúdo de imagem. A própria documentação do Google afirma que alt text é "extremamente útil" para ranking no Google Imagens. É um dos sinais de [SEO de imagem](/glossary/image-seo) mais fortes que você pode controlar.

### A implementação HTML

Alt text vive no atributo `alt` da tag `<img>`:

`<img src="recepcao-clinica-odontologica.jpg" alt="Recepção moderna de clínica odontológica com equipe da frente cumprimentando paciente">`

A maioria das plataformas CMS (WordPress, Webflow, Ghost) tem campos de alt text dedicados em suas interfaces de upload de imagem. Você não precisa editar HTML diretamente.

### O que acontece sem alt text

Se uma imagem não tem atributo alt nenhum, leitores de tela podem ler o nome do arquivo em vez disso. Algo como "IMG_4392.jpg." Inútil. Se o atributo alt está presente mas vazio (`alt=""`), leitores de tela pulam a imagem inteiramente, o que é comportamento correto para imagens decorativas mas errado para significativas.

## Tipos de alt text

Nem toda imagem precisa do mesmo tratamento:

- **Alt text informativo**. Descreve o que a imagem mostra e por que importa. Usado para fotos, ilustrações, gráficos e elementos gráficos que transmitem informação. "Gráfico de barras mostrando aumento de 40 % em tráfego orgânico de janeiro a junho de 2025."
- **Alt text funcional**. Descreve o que uma imagem clicável faz. Usado para botões, ícones e imagens linkadas. "Botão de busca" ou "Baixar relatório PDF."
- **Alt text decorativo (vazio)**. Usado para imagens puramente decorativas que não adicionam informação. Defina `alt=""` para que leitores de tela as pulem. Padrões de fundo, linhas divisórias e ícones decorativos caem aqui.
- **Alt text complexo**. Usado para gráficos, gráficos e infográficos que contêm dados densos. O alt text fornece um resumo, e uma descrição mais longa vai em um atributo `longdesc` ou texto próximo.

Acertar o tipo importa. Descrever demais imagens decorativas atrapalha a experiência do leitor de tela. Descrever de menos imagens informativas perde valor de acessibilidade e SEO.

## Exemplos de alt text

**Exemplo 1: A página de menu de um restaurante**
Alt text ruim: "comida" ou "foto de prato" ou nenhum alt text. Alt text bom: "Salmão grelhado com legumes assados e molho de manteiga e limão servido em prato branco." A versão descritiva ajuda o Google a ranquear a imagem para buscas de "salmão grelhado" e ajuda usuários com deficiência visual a entender o item do menu.

**Exemplo 2: Uma listagem de imóveis**
Ruim: "exterior da casa." Bom: "Casa colonial de dois andares com fachada de tijolos vermelhos, colunas brancas e jardim frontal paisagístico na Rua Principal, 123." Uma vitória de [SEO local](/glossary/local-seo). A descrição detalhada inclui características da propriedade que combinam com o que compradores de imóveis pesquisam no Google Imagens.

**Exemplo 3: Uma página de produto de e-commerce**
Ruim: "imagem de produto 1." Bom: "Tênis de corrida Nike Air Max 90 em branco e cinza, vista lateral." Esse alt text inclui marca, nome do produto, cor e ângulo. Exatamente o que o Google precisa para apresentá-lo em resultados de Shopping e busca de imagens. Usar conteúdo de blog publicado pela theStacc junto com imagens de produto corretamente otimizadas cria uma base sólida de [SEO On-Page](/glossary/on-page-seo).

## Alt text vs. texto de título

Esses são confundidos constantemente, mas servem a propósitos completamente diferentes.

| | Alt Text | Texto de Título |
|---|---|---|
| **Propósito** | Descreve a imagem para acessibilidade e SEO | Fornece info suplementar ao passar o mouse |
| **Obrigatório** | Sim (conformidade WCAG) | Não |
| **Impacto SEO** | Forte (sinal primário de ranking de imagem) | Mínimo |
| **Leitor de tela** | Lido em voz alta automaticamente | Às vezes, depende das configurações |
| **Visibilidade** | Mostrado quando imagem falha em carregar | Mostrado como tooltip ao passar mouse |

Alt text é obrigatório. Texto de título é opcional e principalmente cosmético. Concentre seu esforço no alt text.

## Boas práticas com alt text

- **Seja específico e conciso**. Descreva o que está na imagem em 125 caracteres ou menos. Leitores de tela podem cortar descrições mais longas. "Golden retriever pegando um frisbee em um parque" supera "cachorro" toda vez.
- **Inclua palavras-chave naturalmente, não forçadamente**. Se a imagem está numa página sobre [pesquisa de palavras-chave](/glossary/keyword-research) e a imagem mostra uma ferramenta de análise de palavras-chave, mencione isso. Mas não encha: "pesquisa de palavras-chave ferramenta de palavras-chave melhor pesquisa de palavras-chave SEO palavras-chave" é spam.
- **Não comece com "imagem de" ou "foto de"**. Leitores de tela já anunciam que é uma imagem. Começar com "imagem de" é redundante. Pule direto para a descrição.
- **Descreva função para imagens clicáveis**. Se uma imagem é um link ou botão, o alt text deve descrever a ação, não a imagem. Um ícone de lupa que aciona busca deve ter `alt="Buscar"`. Não `alt="lupa"`.
- **Automatize onde possível**. Ao publicar em escala, manter alt text consistente fica difícil. theStacc inclui alt text otimizado em cada artigo que publica, então imagens são acessíveis e prontas para SEO desde o dia um.

## Perguntas Frequentes

### Qual deve ser o comprimento do alt text?

Mantenha abaixo de 125 caracteres. A maioria dos leitores de tela corta alt text em torno desse comprimento. Para imagens complexas como infográficos, forneça um resumo breve em alt text e adicione uma descrição mais longa no conteúdo circundante da página.

### Alt text afeta rankings do Google?

Sim. Alt text é um fator de ranking confirmado para Google Imagens e fornece contexto de apoio para rankings de busca web. A documentação do Search Central do Google recomenda explicitamente escrever alt text descritivo para [SEO On-Page](/glossary/on-page-seo).

### Toda imagem deve ter alt text?

Toda imagem significativa precisa de alt text. Imagens decorativas (espaçadores, padrões de fundo, ornamentos visuais) devem ter atributos alt vazios (`alt=""`) para que leitores de tela as pulem. A pergunta-chave: essa imagem transmite informação? Se sim, descreva-a.

### Alt text pode ser muito longo?

Sim. Alt text excessivamente longo é frustrante para usuários de leitores de tela e pode parecer [keyword stuffing](/glossary/keyword-stuffing) para o Google. Mantenha descrições focadas. Se uma imagem precisa de um parágrafo de explicação, coloque isso no texto do corpo perto da imagem. Não no atributo alt.

---

Quer cada post de blog publicado com alt text adequado, [tags de cabeçalho](/glossary/heading-tags) e SEO on-page embutido? theStacc publica 30 artigos otimizados para SEO no seu site todo mês. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: Boas práticas de SEO de imagem](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM: Guia de texto alternativo](https://webaim.org/techniques/alttext/)
- [WebAIM: O WebAIM Million (relatório anual de acessibilidade)](https://webaim.org/projects/million/)
- [W3C: Requisitos de imagem WCAG 2.1](https://www.w3.org/WAI/tutorials/images/)
- [Moz: Guia de SEO de imagem](https://moz.com/learn/seo/image-seo)
