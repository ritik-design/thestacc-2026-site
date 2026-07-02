---
term: "Redirecionamento 301"
slug: "301-redirect"
definition: "Um redirecionamento 301 envia permanentemente usuários e mecanismos de busca de uma URL para outra. Saiba quando usar redirecionamentos 301, como implementá-los e seu impacto no SEO."
category: "SEO"
difficulty: "Intermediate"
keyword: "o que é um redirecionamento 301"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## O Que é um Redirecionamento 301?

Um redirecionamento 301 é um código de status HTTP que encaminha permanentemente uma URL para outra. Informa aos navegadores e mecanismos de busca que o endereço original foi movido definitivamente.

Quando o Googlebot ou um visitante acessa um 301, ele é automaticamente enviado para a nova URL. Sem página quebrada. Sem beco sem saída. O "301" refere-se ao código de resposta HTTP específico. É a forma que a web tem de dizer "esta página foi movida permanentemente para um novo endereço". Existe um [redirecionamento 302](/glossary/302-redirect) para movimentações temporárias, mas o 301 é o que importa para o [SEO](/glossary/seo).

Veja por que isso é crítico: pesquisas do Moz mostram que redirecionamentos 301 repassam aproximadamente 95-99% da [equidade de links](/glossary/link-equity) para a URL de destino. Isso significa que o poder de posicionamento que sua URL antiga conquistou com [backlinks](/glossary/backlinks) não desaparece. Ele é transferido para a nova página. Faça os 301s errados e você jogará fora anos de autoridade acumulada.

## Por Que um Redirecionamento 301 é Importante?

Toda vez que uma URL muda sem um redirecionamento adequado, algo quebra. Posições, tráfego, experiência do usuário. Escolha dois.

- **Preserva as posições nos mecanismos de busca**. Sem um 301, o Google trata a nova URL como uma página completamente nova com zero autoridade. Suas posições desaparecem da noite para o dia.
- **Transfere a equidade de links**. Aqueles [backlinks](/glossary/backlinks) que você conquistou? Um 301 repassa o valor deles para a nova URL. Sem ele, essa força de posicionamento evapora.
- **Evita erros 404**. Usuários que salvaram a URL antiga nos favoritos ou clicam em um link externo encontram uma página funcionando em vez de um [erro 404](/glossary/404-error). Melhor experiência, menor [taxa de rejeição](/glossary/bounce-rate).
- **Consolida conteúdo duplicado**. Várias URLs servindo o mesmo conteúdo diluem sua autoridade. Os 301s fundem todas elas em uma página forte.

Se você já migrou um site, mudou uma estrutura de URL ou fundiu duas páginas, você precisou de redirecionamentos 301. Ignorá-los é um dos erros de [SEO técnico](/glossary/technical-seo) mais comuns e custosos.

## Como Funciona um Redirecionamento 301

O processo ocorre em milissegundos, mas veja o que acontece por baixo do capô.

### O Ciclo de Requisição HTTP

Um usuário ou rastreador de mecanismo de busca solicita a URL antiga. O servidor responde com o código de status HTTP 301 e um cabeçalho "Location" apontando para a nova URL. O navegador então solicita automaticamente a nova URL. O usuário vê a página final. Ele pode nem perceber que o redirecionamento aconteceu.

### Como o Google Processa os 301s

Quando o [Googlebot](/glossary/crawling) encontra um 301, ele faz três coisas: segue o redirecionamento para a nova URL, transfere a maior parte dos sinais de posicionamento da página antiga para a nova página e eventualmente remove a URL antiga de seu índice. Esse processo pode levar dias ou semanas, dependendo da frequência com que o Google rastreia seu site.

### Implementação no Nível do Servidor vs. Nível da Página

Os redirecionamentos 301 são configurados no nível do servidor. Não no HTML. Os métodos mais comuns:

- **Apache (.htaccess):** `Redirect 301 /pagina-antiga https://exemplo.com.br/nova-pagina`
- **Nginx:** `rewrite ^/pagina-antiga$ /nova-pagina permanent;`
- **Plugins WordPress:** Yoast, Redirection ou Rank Math gerenciam isso pelo painel
- **Cloudflare:** Page Rules ou Bulk Redirects para mudanças no nível do domínio

Redirecionamentos meta refresh no nível da página existem, mas são mais lentos e não repassam a equidade de links com a mesma confiabilidade. Sempre use 301s no nível do servidor.

## Tipos de Redirecionamentos

Entender as diferenças evita erros custosos:

- **301 (Permanente)**. A página foi movida para sempre. Repassa ~95-99% da equidade de links. Use para mudanças de URL, migrações de domínio e consolidação de conteúdo.
- **[302 (Temporário)](/glossary/302-redirect)**. A página foi movida temporariamente. O Google pode ou não repassar a equidade de links. Use para testes A/B, páginas de manutenção ou conteúdo sazonal.
- **307 (Temporário, HTTP/1.1)**. Igual ao 302, mas preserva estritamente o método da requisição (POST continua POST). Apenas casos de uso técnico.
- **308 (Permanente, HTTP/1.1)**. Igual ao 301 com preservação estrita do método. Raramente usado em contextos de SEO.
- **Meta refresh**. Redirecionamento baseado em HTML. Lento, baixo valor de SEO. Evite.

Na dúvida, use um 301. É a escolha segura para mudanças permanentes de URL.

## Exemplos de Redirecionamento 301

**Exemplo 1: Um negócio local redesenhando seu site**
Um escritório de advocacia redesenha seu site e muda a estrutura de URL de `/servicos/advogado-acidente-trabalho` para `/areas-pratica/acidente-trabalho`. Sem um 301, a página antiga, que estava em 3º lugar para "advogado acidente de trabalho [cidade]", retornaria um 404. Com o redirecionamento, a nova URL herda a posição de ranking e os 47 [backlinks](/glossary/backlinks) apontando para a página antiga continuam funcionando.

**Exemplo 2: Fundindo dois posts de blog em uma página mais forte**
Uma empresa de encanamento tem dois artigos finos: "Como Consertar uma Torneira com Vazamento" e "Guia de Reparo de Torneira com Vazamento." Nenhum posiciona bem. Eles fundem ambos em um guia detalhado na URL mais forte e fazem o 301 do mais fraco. Os sinais combinados de [autoridade de domínio](/glossary/domain-authority) empurram a página fundida da posição 12 para a posição 4 em 6 semanas.

**Exemplo 3: Migração de domínio que deu errado**
Uma loja de e-commerce migra de dominioantigo.com para dominionovo.com mas só redireciona a homepage. As 2.400 páginas de produto e os 180 posts de blog retornam 404. O [tráfego orgânico](/glossary/organic-traffic) cai 78% em 2 semanas. Cada URL precisava de um redirecionamento 301 individual. Esse erro custa meses para se recuperar, se for detectado rapidamente.

## Redirecionamento 301 vs. URL Canonical

Ambos lidam com conteúdo duplicado, mas funcionam de forma diferente.

| | Redirecionamento 301 | [URL Canonical](/glossary/canonical-url) |
|---|---|---|
| **O que faz** | Envia usuários e bots para uma nova URL | Informa ao Google qual URL é a cópia "principal" |
| **Experiência do usuário** | Usuário vê a nova página (redirecionamento automático) | Usuário ainda pode acessar a página original |
| **Quando usar** | Página antiga não deve mais existir | Ambas as páginas devem permanecer acessíveis |
| **Equidade de links** | Repassa ~95-99% | Consolida sinais para a canonical |
| **Exemplo** | URL antiga de blog movida para nova estrutura | Página de produto acessível por 3 URLs diferentes |

Use 301s quando a página antiga estiver desativada. Use canonicals quando ambas as páginas precisam existir, mas você quer que o Google priorize uma.

## Melhores Práticas para Redirecionamentos 301

- **Mapeie cada URL antiga para uma nova URL relevante**. Não redirecione tudo para a homepage. Redirecione cada página antiga para seu equivalente mais próximo. O Google trata redirecionamentos em massa para a homepage como soft 404s.
- **Implemente redirecionamentos 1 para 1 durante migrações de site**. Antes de lançar um novo site, rastreie o antigo, exporte cada URL e crie um mapa de redirecionamentos. Pule esta etapa e você verá o [tráfego orgânico](/glossary/organic-traffic) despencar.
- **Evite cadeias de redirecionamento**. A > B > C > D torna a experiência mais lenta para o usuário, desperdiça [orçamento de rastreamento](/glossary/crawl-budget) e pode perder equidade de links em cada salto. Cada redirecionamento deve apontar diretamente para o destino final.
- **Monitore com o Google Search Console**. Verifique o relatório de Cobertura para erros de rastreamento após implementar redirecionamentos. O [Google Search Console](/glossary/google-search-console) mostra quais páginas retornam 404 para que você detecte rapidamente os redirecionamentos ausentes.
- **Audite redirecionamentos trimestralmente**. Redirecionamentos antigos que apontam para páginas que não existem mais criam cadeias. Serviços como o theStacc incluem estruturas de URL adequadas em cada artigo publicado, mas se você estiver migrando ou reorganizando conteúdo, programe auditorias regulares de redirecionamento para manter tudo limpo.

## Perguntas Frequentes

### Os redirecionamentos 301 prejudicam o SEO?

Não, quando usados corretamente. Um 301 implementado corretamente repassa quase toda a equidade de links para a nova URL. John Mueller do Google confirmou que os 301s não causam perda de posicionamento. O risco vem de implementações incorretas: cadeias de redirecionamento, redirecionamentos em massa para a homepage ou páginas completamente ignoradas.

### Por quanto tempo você deve manter um redirecionamento 301?

Indefinidamente, ou pelo menos por um ano. O Google precisa de tempo para rastrear novamente a URL antiga, processar o redirecionamento e atualizar seu índice. Remover um 301 cedo demais significa que links externos para a URL antiga irão retornar 404 novamente.

### Muitos redirecionamentos 301 podem deixar um site lento?

Redirecionamentos individuais adicionam milissegundos. Mas cadeias de redirecionamento (página A > B > C) multiplicam esse atraso. Mantenha os redirecionamentos a no máximo um salto. Um site com milhares de 301s limpos está bem. São as cadeias e os loops que causam problemas.

### Qual é a diferença entre um 301 e um 302?

Um [301 é permanente](/glossary/301-redirect); um [302 é temporário](/glossary/302-redirect). Use 301 quando a URL antiga não existir mais. Use 302 quando a página original voltar (conteúdo sazonal, manutenção temporária). O Google repassa a equidade de links de forma mais confiável por meio de 301s.

---

Quer uma arquitetura de site construída para SEO desde o primeiro dia? O theStacc publica 30 artigos otimizados para SEO no seu site todo mês, com estruturas de URL limpas e links internos adequados. Automaticamente. [Comece por $1 →](https://app.thestacc.com)

## Fontes

- [Google Search Central: Redirecionamentos e a Busca Google](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz: Guia de Redirecionamento](https://moz.com/learn/seo/redirection)
- [Ahrefs: Redirecionamentos 301 para SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal: Redirecionamentos 301 vs 302](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Google Search Console Help: Corrigir Erros de Rastreamento](https://support.google.com/webmasters/answer/7440203)
