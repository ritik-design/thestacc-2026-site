---
title: "Como Configurar Redirecionamentos 301 (Passo a Passo)"
description: "Aprenda a configurar redirecionamentos 301 para SEO. Abrange WordPress, .htaccess, Nginx, Shopify e Cloudflare. Com etapas de teste. Atualizado em março de 2026."
slug: "301-redirects-guide"
keyword: "redirecionamentos 301"
author: "Siddharth Gangal"
date: "2026-04-26"
category: "SEO Tips"
image: "/blogs-preview-images/301-redirects-guide.webp"
---

Você mudou uma URL. Talvez tenha migrado para um novo domínio. Talvez tenha consolidado 3 páginas em 1. Agora os visitantes encontram um erro 404 e o Google derruba suas posições da noite para o dia.

Cada URL quebrada vaza a equidade de links que você levou meses para conquistar. Os usuários saem do site. O Google sinaliza seu site como mal mantido. Uma única migração sem redirecionamentos 301 pode eliminar 40% ou mais do seu tráfego orgânico em uma semana.

Este guia apresenta 7 etapas para configurar redirecionamentos 301 da maneira certa. Você aprenderá o processo exato para WordPress, Apache `.htaccess`, Nginx, Shopify e Cloudflare. Sem suposições. Sem links quebrados. Sem perda de posições.

Publicamos mais de 3.500 blogs em mais de 70 setores. Mudanças de URL, consolidações de páginas e migrações de domínio são tarefas que gerenciamos toda semana. As etapas abaixo são as mesmas que seguimos nos nossos próprios sites e nos de nossos clientes.

Veja o que você vai aprender:

- Como encontrar todas as URLs que precisam de redirecionamento
- Como mapear URLs antigas para seus novos destinos corretos
- Como implementar redirecionamentos 301 em 5 plataformas diferentes
- Como corrigir cadeias e loops de redirecionamento antes que prejudiquem sua velocidade
- Como testar redirecionamentos antes e depois de entrar em produção
- Como monitorar a saúde dos redirecionamentos no Google Search Console

---

## Visão Geral

- **Tempo necessário:** 10 a 30 minutos (depende do número de redirecionamentos)
- **Dificuldade:** Iniciante a Intermediário
- **O que você precisa:** Acesso ao seu CMS, painel de hospedagem ou arquivos de configuração do servidor

---

## O Que é um Redirecionamento 301?

Um código de status `301` informa aos navegadores e mecanismos de busca que uma página foi movida permanentemente para uma nova URL. O navegador envia automaticamente os visitantes para o novo endereço. O Google transfere a equidade de links da URL antiga para a nova.

Antes de 2016, os redirecionamentos 301 causavam aproximadamente 15% de perda de PageRank por salto. Isso não ocorre mais. [O Google confirmou que redirecionamentos 30x não mais diluem o PageRank](https://searchengineland.com/google-no-pagerank-dilution-using-301-302-30x-redirects-anymore-254608). Hoje, um `301` corretamente configurado repassa de 90 a 99% da equidade de links, de acordo com o Moz.

Isso faz dos redirecionamentos 301 a ferramenta mais importante para preservar seu SEO durante qualquer mudança de URL. Pule-os e você começa do zero.

---

## Etapa 1: Identifique Quais URLs Precisam de Redirecionamento

Você não pode redirecionar o que não encontrou. A primeira etapa é criar uma lista completa de URLs que retornam erros ou foram alteradas.

Comece com o **Google Search Console**. Vá ao relatório de Páginas e filtre por "Não encontrada (404)". Isso mostra cada URL que o Google tentou rastrear, mas não conseguiu acessar. Exporte a lista completa.

Em seguida, verifique o **Google Analytics** (GA4). Analise o relatório de Páginas de destino para páginas que perderam tráfego repentinamente. Uma queda acentuada após uma mudança de URL é um forte sinal de que falta um redirecionamento.

Execute um **rastreamento de site** com uma ferramenta como Screaming Frog, Sitebulb ou Ahrefs Site Audit. Essas ferramentas encontram links internos quebrados, páginas órfãs e respostas 404 que o Google Search Console pode não detectar. Uma [auditoria de SEO](/blog/how-to-do-seo-audit) completa evidenciará esses problemas rapidamente.

Três cenários comuns que exigem redirecionamentos 301:

1. **Mudança de slug de URL**. Você renomeou `/blog/post-antigo` para `/blog/post-novo`
2. **Migração de domínio**. Você migrou de `siteantigo.com` para `siteNovo.com`
3. **Consolidação de páginas**. Você fundiu 3 páginas finas em 1 página mais robusta para [corrigir conteúdo fino](/blog/fix-thin-content)

### Quando Usar 301 vs 404 vs 410 vs Canonical

Nem toda URL inativa precisa de redirecionamento. Use este framework de decisão.

| Cenário | Ação | Por quê |
|---|---|---|
| Página movida para uma nova URL | Redirecionamento `301` | Preserva equidade de links e experiência do usuário |
| Página excluída, sem substituto | `410` Gone | Informa ao Google para desindexar mais rápido que um `404` |
| Página excluída, pode voltar | `404` Not Found | Resposta padrão para páginas temporariamente ausentes |
| Conteúdo duplicado, ambas as páginas permanecem no ar | Tag `canonical` | Consolida sinais sem remover a página |
| Domínio antigo para domínio novo | Redirecionamento `301` (nível de domínio) | Transfere toda a equidade para o novo domínio |

![Quando usar redirecionamentos 301 vs 404 vs 410 vs canonical](/images/blog/301-redirect-decision-framework.webp)

**Por que esta etapa importa:** Redirecionamentos ausentes são invisíveis. Os usuários veem um 404 e vão embora. O Google vê uma URL morta e a remove do índice. Você perde posições sem nenhum aviso no seu painel de análise.

**Dica profissional:** Exporte o XML do seu sitemap completo antes de fazer qualquer mudança de URL. Compare com o rastreamento pós-alteração para identificar cada discrepância.

---

## Etapa 2: Mapeie URLs Antigas para Novos Destinos

Um redirecionamento é tão bom quanto seu destino. Enviar todas as URLs antigas para a página inicial é um erro comum. O Google trata redirecionamentos para a homepage vindos de páginas profundas como [soft 404s](https://developers.google.com/search/docs/crawling-indexing/301-redirects). Você perde a equidade de qualquer forma.

Crie uma planilha com 4 colunas:

| URL Antiga | Nova URL | Tipo de Redirecionamento | Notas |
|---|---|---|---|
| `/blog/guia-seo-antigo` | `/blog/guia-seo-on-page` | 301 | Conteúdo fundido |
| `/servicos/web-design` | `/servicos/design` | 301 | Slug encurtado |
| `/blog/post-desatualizado` | , | 410 | Sem substituto |

Siga estas regras de mapeamento:

- **Sempre aponte para a página mais relevante.** Corresponda ao tópico e intenção, não apenas à categoria.
- **Para migrações de domínio, espelhe a estrutura de URL.** Se `/sobre` existia no domínio antigo, redirecione para `/sobre` no novo domínio.
- **Agrupe redirecionamentos por tipo.** Mudanças em massa de URL (como remover `/blog/` dos caminhos) podem usar regras baseadas em padrões em vez de entradas individuais.
- **Identifique páginas com muitos backlinks.** Use o Ahrefs ou o relatório de Links do Google Search Console para identificar suas páginas com mais links. Estas têm maior prioridade para mapeamento preciso.

Uma [auditoria de conteúdo](/blog/how-to-content-audit) ajuda a identificar quais páginas consolidar e quais desativar. Execute-a antes de começar o mapeamento.

**Por que esta etapa importa:** Mapeamentos ruins enviam usuários e equidade de links para páginas irrelevantes. O Google percebe a incompatibilidade e pode ignorar o redirecionamento completamente. Um mapeamento ruim pode desfazer meses de [autoridade temática](/blog/build-topical-authority) construída em torno de um cluster de palavras-chave.

---

## Etapa 3: Configure Redirecionamentos 301 na Sua Plataforma

A implementação depende do seu stack tecnológico. Abaixo estão as instruções exatas para 5 plataformas.

### WordPress (Método via Plugin)

A opção mais rápida para sites WordPress. Três plugins gerenciam redirecionamentos bem:

- **Redirection** (gratuito). O plugin de redirecionamento mais popular. Suporta regex, registra erros 404 e importa arquivos CSV.
- **Rank Math** (gratuito/pro). Gerenciador de redirecionamento integrado em Rank Math > Redirecionamentos.
- **Yoast SEO Premium**. Sugere automaticamente redirecionamentos quando você muda um slug.

Para adicionar um redirecionamento no **Redirection**:

1. Vá em Ferramentas > Redirection
2. Digite a URL de origem (caminho antigo)
3. Digite a URL de destino (novo caminho)
4. Selecione "301 Movido Permanentemente"
5. Clique em "Adicionar Redirecionamento"

Para redirecionamentos em massa, use o recurso de importação CSV. Formato: `URL de origem, URL de destino, 301`.

### Apache (.htaccess)

Se você usa Apache, adicione regras de redirecionamento ao seu arquivo `.htaccess` na raiz do site.

Redirecionamento único:

```
Redirect 301 /pagina-antiga https://exemplo.com.br/nova-pagina
```

Redirecionamento baseado em padrão usando `mod_rewrite`:

```
RewriteEngine On
RewriteRule ^diretorio-antigo/(.*)$ /novo-diretorio/$1 [R=301,L]
```

Redirecionamento de domínio completo (site inteiro):

```
RewriteEngine On
RewriteCond %{HTTP_HOST} ^siteantigo\.com\.br$ [NC]
RewriteRule ^(.*)$ https://sitenovo.com.br/$1 [R=301,L]
```

Sempre faça backup do seu arquivo `.htaccess` antes de editá-lo. Um erro de sintaxe aqui derruba o site inteiro.

### Nginx

O Nginx usa o bloco `server` no seu arquivo de configuração (geralmente `/etc/nginx/sites-available/`).

Redirecionamento único:

```
location = /pagina-antiga {
    return 301 https://exemplo.com.br/nova-pagina;
}
```

Redirecionamento baseado em padrão:

```
location /diretorio-antigo/ {
    rewrite ^/diretorio-antigo/(.*)$ /novo-diretorio/$1 permanent;
}
```

Após editar, teste a configuração com `nginx -t` e recarregue com `systemctl reload nginx`.

### Shopify

O Shopify tem uma ferramenta de redirecionamento integrada. Nenhum plugin é necessário.

1. Vá em **Configurações > Navegação > Redirecionamentos de URL**
2. Clique em "Adicionar redirecionamento de URL"
3. Insira o caminho antigo e o novo caminho
4. Salve

Para redirecionamentos em massa, clique em "Importar" e envie um CSV com 2 colunas: `Redirecionar de` e `Redirecionar para`.

Limitação do Shopify: Você não pode redirecionar para domínios externos com essa ferramenta. Para migrações de domínio fora do Shopify, você precisa de redirecionamentos no nível do DNS.

### Cloudflare (Nível de Edge)

Os redirecionamentos do Cloudflare ocorrem na borda do CDN. São a opção mais rápida porque o redirecionamento é executado antes mesmo de a solicitação chegar ao seu servidor.

1. Vá em **Regras > Regras de Redirecionamento**
2. Crie uma nova regra
3. Defina a condição de correspondência (hostname, caminho URI ou wildcard)
4. Defina a ação como "Redirecionamento Dinâmico" ou "Redirecionamento Estático"
5. Escolha `301` como código de status
6. Faça o deploy

O Cloudflare suporta padrões curinga (wildcard), tornando-o ideal para migrações de domínio em massa.

### Comparativo de Plataformas

| Plataforma | Dificuldade | Suporte em Massa | Velocidade | Melhor Para |
|---|---|---|---|---|
| Plugin WordPress | Fácil | Importação CSV | Padrão | Sites de blog e conteúdo |
| `.htaccess` | Médio | Padrões regex | Padrão | Hospedagem compartilhada Apache |
| Nginx | Médio | Regras de reescrita | Rápido | VPS e servidores dedicados |
| Shopify | Fácil | Importação CSV | Padrão | Lojas de e-commerce |
| Cloudflare | Fácil | Regras curinga | Mais rápido | Qualquer site usando Cloudflare |

![Configuração de redirecionamento 301 no WordPress, Apache, Nginx, Shopify e Cloudflare](/images/blog/301-redirect-platforms.webp)

**Por que esta etapa importa:** A sintaxe errada quebra o site inteiro. Um arquivo `.htaccess` mal configurado retorna erro 500. Uma regra ruim no Nginx cria um loop de redirecionamento. Teste em ambiente de staging sempre que possível.

---

## Etapa 4: Lide com Cadeias e Loops de Redirecionamento

Uma cadeia de redirecionamento ocorre quando a URL A redireciona para a URL B, que redireciona para a URL C. Em vez de 1 salto, o navegador faz 2 ou mais. Cada salto adiciona de 50 a 100 milissegundos de latência.

Um loop de redirecionamento ocorre quando a URL A redireciona para a URL B, e a URL B redireciona de volta para a URL A. O navegador fica preso em um ciclo infinito e eventualmente exibe uma página de erro.

O Google rastreia no máximo 5 saltos em uma cadeia de redirecionamento. Além disso, o Google para de seguir. A página de destino nunca é rastreada ou indexada.

### Como Encontrar Cadeias e Loops

Execute um rastreamento com Screaming Frog ou Ahrefs. Filtre por cadeias de redirecionamento (3xx > 3xx). Você também pode usar o [Redirect Checker do httpstatus.io](https://httpstatus.io) gratuito para testar URLs individuais.

### Como Achatar Cadeias

Se a cadeia é A → B → C, atualize A para apontar diretamente para C. Remova o salto intermediário.

Antes:
```
/pagina-antiga → /pagina-renomeada → /pagina-final
```

Depois:
```
/pagina-antiga → /pagina-final
/pagina-renomeada → /pagina-final
```

Ambas as URLs antigas agora apontam diretamente para o destino final. Um salto cada.

### Como Corrigir Loops

Os loops geralmente ocorrem quando 2 regras de redirecionamento entram em conflito. Verifique suas regras de redirecionamento em busca de referências circulares. A correção é sempre a mesma: decida qual URL é o destino canônico e faça com que todas as outras URLs apontem para ela.

Se você usa redirecionamentos tanto no nível do servidor (`.htaccess`) quanto no nível do plugin (Redirection), verifique ambos. Regras conflitantes entre camadas são a causa mais comum de loops.

![Comparação entre cadeia de redirecionamento e redirecionamento direto](/images/blog/redirect-chain-vs-direct.webp)

**Por que esta etapa importa:** Cadeias desperdiçam orçamento de rastreamento e tornam o carregamento das páginas mais lento. Uma cadeia de 3 saltos adiciona de 150 a 300 ms de latência antes que o usuário veja qualquer conteúdo. Loops são piores. Eles bloqueiam o acesso completamente e queimam o orçamento de rastreamento em páginas que nunca se resolvem.

---

> **Deixe o trabalho técnico para nós. Mantenha suas posições.** O Stacc cuida da estrutura de URL, redirecionamentos e manutenção de SEO para mais de 30 artigos por mês.
> [Comece por $1 →](/pricing)

---

## Etapa 5: Teste Cada Redirecionamento Antes de Entrar em Produção

Redirecionamentos não testados causam quedas silenciosas de posições. Um redirecionamento que retorna `302` em vez de `301` não repassa a equidade de links da mesma forma. Um redirecionamento que aponta para um 404 é pior do que nenhum redirecionamento.

### Teste com curl

Abra seu terminal e execute:

```bash
curl -I https://exemplo.com.br/pagina-antiga
```

Procure por `HTTP/1.1 301 Moved Permanently` e o cabeçalho `Location:` apontando para a URL nova correta.

Para testar uma cadeia, use a flag `-L` para seguir todos os redirecionamentos:

```bash
curl -IL https://exemplo.com.br/pagina-antiga
```

Isso mostra cada salto na cadeia com seu código de status.

### Teste com o Chrome DevTools

1. Abra o Chrome e pressione `F12` para abrir o DevTools
2. Vá para a aba **Network** (Rede)
3. Marque "Preserve log" (para que os redirecionamentos permaneçam visíveis)
4. Insira a URL antiga na barra de endereços
5. Observe a primeira requisição. A coluna Status deve mostrar `301`. Os cabeçalhos de resposta devem mostrar o `Location` correto.

### Teste com Ferramentas Online

Verificadores de redirecionamento gratuitos como [httpstatus.io](https://httpstatus.io) ou o [Redirect Checker do Ahrefs](https://ahrefs.com/blog/301-redirects/) permitem que você teste sem um terminal.

### Erros Comuns de Teste

- **Incompatibilidade HTTP vs HTTPS.** Teste as versões `http://` e `https://` da URL antiga. Deixar de redirecionar em um dos protocolos cria uma lacuna.
- **Inconsistência com barra final.** `/pagina-antiga` e `/pagina-antiga/` são URLs diferentes. Ambas precisam de redirecionamentos.
- **www vs não-www.** Certifique-se de que `www.exemplo.com.br/pagina-antiga` e `exemplo.com.br/pagina-antiga` redirecionem corretamente.

![Como testar redirecionamentos 301 com curl e Chrome DevTools](/images/blog/test-301-redirects.webp)

**Por que esta etapa importa:** Você não consegue ver um redirecionamento quebrado navegando normalmente pelo seu site. As URLs antigas não estão na sua navegação. Apenas um teste deliberado ou um alerta do Google Search Console detectará o problema. Até lá, você pode já ter perdido semanas de posicionamento.

---

## Etapa 6: Atualize os Links Internos para Apontar para as Novas URLs

Os redirecionamentos são uma rede de segurança. Eles não substituem permanentemente a [linkagem interna](/blog/internal-linking-blog-posts) correta.

Cada link interno que passa por um redirecionamento adiciona um salto desnecessário. O Google ainda segue o link, mas cada redirecionamento consome orçamento de rastreamento. Em um site grande com milhares de links internos, isso se acumula rapidamente.

### O Que Atualizar

- **Links no corpo do conteúdo**. Qualquer post de blog ou página que vincule à URL antiga
- **Menus de navegação**. Links no cabeçalho, rodapé e barra lateral
- **Sitemap XML**. Remova URLs antigas e adicione as novas. Se precisar de ajuda, siga nosso guia sobre [como criar e otimizar seu sitemap XML](/blog/create-xml-sitemap).
- **Dados estruturados**. Atualize qualquer [schema markup](/blog/schema-markup-for-blog-posts) que faça referência a URLs antigas
- **Tags canonical**. Certifique-se de que a tag canonical na nova página aponte para ela mesma, não para a URL antiga

### Como Fazer um Localizar e Substituir em Todo o Site

Para WordPress, use o plugin **Better Search Replace**. Insira o padrão de URL antigo e o novo. Execute uma simulação primeiro para visualizar as alterações. Depois, execute.

Para sites estáticos ou plataformas CMS personalizadas, use o recurso de localizar e substituir do seu editor de código em todo o diretório do projeto.

Após atualizar, [envie seu sitemap atualizado ao Google](/blog/submit-website-google) pelo Search Console para agilizar o novo rastreamento.

**Por que esta etapa importa:** Links internos que passam por redirecionamentos desperdiçam orçamento de rastreamento e adicionam latência. Links diretos são sempre mais rápidos e eficientes. Limpe a origem e mantenha os redirecionamentos apenas como fallback para links externos que você não consegue controlar.

---

## Etapa 7: Monitore no Google Search Console

O redirecionamento está no ar. Os testes passaram. Mas redirecionamentos 301 podem quebrar silenciosamente durante deploys, atualizações do CMS ou alterações na configuração do servidor. O monitoramento contínuo detecta problemas antes que afetem as posições.

### Verifique o Relatório de Páginas

No Google Search Console, vá para **Páginas** (em Indexação). Filtre por:

- **Não encontrada (404)**. Novos erros 404 aparecendo após a entrada do redirecionamento em produção significam que algo está mal configurado.
- **Erro de redirecionamento**. O Google detectou um loop, cadeia ou redirecionamento quebrado.
- **Rastreada. Atualmente não indexada**. A nova página de destino pode ainda não estar indexada.

### Use a Ferramenta de Inspeção de URL

Insira a URL antiga na ferramenta de Inspeção de URL. O Google deve mostrar "Página não está no índice" com uma nota de que ela redireciona para a nova URL. Se o Google ainda mostrar a URL antiga como indexada, solicite a indexação da nova URL.

### Verifique os Core Web Vitals

Cadeias de redirecionamento aumentam o Tempo até o Primeiro Byte (TTFB). Após implementar redirecionamentos, verifique os **Core Web Vitals** no Search Console para qualquer pico de latência. Cada salto adiciona de 50 a 100 ms. Se o seu TTFB aumentou, você provavelmente tem uma cadeia não achatada.

Você também pode usar isso como parte de uma estratégia mais ampla para [melhorar os Core Web Vitals](/blog/improve-core-web-vitals) em todo o seu site.

### Estabeleça Pontos de Revisão

- **Dia 7:** Verifique novos erros 404 no GSC. Confirme que as URLs antigas resolvem corretamente.
- **Dia 30:** Compare o tráfego orgânico antes e depois do redirecionamento. Use o relatório de Desempenho filtrado pela nova URL.
- **Dia 90:** Confirme que as posições se estabilizaram. Sites com redirecionamentos 301 limpos retêm 95% ou mais do tráfego orgânico em 2 a 3 meses.

**Por que esta etapa importa:** Redirecionamentos podem quebrar silenciosamente. Uma atualização do CMS pode sobrescrever seu arquivo `.htaccess`. Uma atualização de plugin pode redefinir as regras de redirecionamento. Sem monitoramento, você não saberá até que as posições caiam.

---

## Resultados: O Que Esperar

O Google processa a maioria dos redirecionamentos 301 em 1 a 2 semanas. Você verá a URL antiga desaparecer dos resultados de busca e a nova URL tomar seu lugar.

As posições geralmente se estabilizam em 2 a 3 meses após uma migração. [Sites que usam redirecionamentos 301 limpos retiveram 95% ou mais do tráfego orgânico](https://ahrefs.com/blog/301-redirects/) durante esse período.

O Google recomenda manter os redirecionamentos 301 ativos por pelo menos 1 ano. Removê-los muito cedo envia visitantes recorrentes e backlinks antigos para um 404.

O cronograma completo:

| Marco | Prazo |
|---|---|
| Google começa a processar o redirecionamento | 1 a 3 dias |
| URL antiga removida do índice | 1 a 2 semanas |
| Nova URL posiciona no lugar da URL antiga | 2 a 4 semanas |
| Tráfego totalmente estabilizado | 2 a 3 meses |
| Seguro para remover o redirecionamento | No mínimo 1 ano |

![Cronograma de impacto no SEO do redirecionamento 301](/images/blog/301-redirect-timeline.webp)

Combine redirecionamentos limpos com publicação consistente de conteúdo para [aumentar o tráfego orgânico](/blog/increase-organic-traffic) enquanto seus redirecionamentos se consolidam.

---

## Solução de Problemas: 5 Problemas Comuns com Redirecionamentos 301

### Problema 1: Redirecionamento Retorna 302 em Vez de 301

Um `302` é um redirecionamento temporário. Ele não repassa a equidade de links da mesma forma que um `301`. Isso geralmente acontece quando um plugin usa `302` por padrão ou quando a configuração do servidor usa `Redirect` sem especificar o código de status.

**Correção:** Verifique sua regra de redirecionamento. Para `.htaccess`, use explicitamente `Redirect 301` ou `[R=301,L]`. No plugin do CMS, verifique se o tipo de redirecionamento está definido como "Permanente (301)".

### Problema 2: Cadeia de Redirecionamento (3+ Saltos)

Você redirecionou A para B no ano passado. Depois redirecionou B para C este ano. Agora A passa por 2 saltos para chegar a C. O Google segue, mas a latência prejudica a performance.

**Correção:** Atualize a regra de A para apontar diretamente para C. Em seguida, atualize B para apontar diretamente para C. Achate cada cadeia para um único salto.

### Problema 3: Loop de Redirecionamento

A URL A redireciona para B. A URL B redireciona de volta para A. O navegador exibe "ERR_TOO_MANY_REDIRECTS" e nada carrega.

**Correção:** Abra suas regras de redirecionamento e procure referências circulares. Se você usa tanto um plugin quanto redirecionamentos no nível do servidor, verifique ambas as camadas. Remova a regra conflitante.

### Problema 4: Redirecionamento Misto HTTP e HTTPS

A versão HTTP da URL antiga redireciona para a versão HTTP da nova URL, que depois redireciona para HTTPS. Isso é uma cadeia de 2 saltos que deveria ter 1.

**Correção:** Todos os redirecionamentos devem apontar diretamente para a versão HTTPS da URL de destino. Atualize cada regra para usar `https://` no destino.

### Problema 5: Soft 404 Após Redirecionamento

O redirecionamento funciona. O código de status é `301`. Mas a página de destino tem conteúdo escasso ou vazio. O Google trata isso como um "soft 404" e pode não repassar a equidade de links. Isso acontece frequentemente quando você redireciona para uma página de [conteúdo fino](/blog/fix-thin-content) ou uma página de categoria genérica.

**Correção:** Certifique-se de que cada destino de redirecionamento seja uma página real e substancial com conteúdo único. Se a página de destino ainda não existir, crie-a antes de ativar o redirecionamento.

![Problemas comuns com redirecionamentos 301 e correções](/images/blog/301-redirect-problems.webp)

---

> **Seu time de SEO. $99 por mês.** 30 artigos otimizados, publicados e mantidos. Redirecionamentos, links internos e SEO técnico incluídos.
> [Comece por $1 →](/pricing)

---

## Perguntas Frequentes

**Por quanto tempo você deve manter os redirecionamentos 301 ativos?**

O Google recomenda manter os redirecionamentos 301 ativos por pelo menos 1 ano. Sites externos que linkam para sua URL antiga continuarão enviando tráfego por esse redirecionamento. Removê-lo antes que esses links externos sejam atualizados (a maioria nunca será) envia os visitantes deles para um 404. Na dúvida, mantenha o redirecionamento permanentemente. A sobrecarga no servidor é insignificante.

**Os redirecionamentos 301 prejudicam o SEO?**

Não. O Google confirmou em 2016 que redirecionamentos 30x não causam mais perda de PageRank. Um `301` corretamente configurado repassa de 90 a 99% da equidade de links para a URL de destino. O único risco são erros de implementação, como cadeias, loops ou redirecionamento para páginas irrelevantes.

**Qual é a diferença entre um redirecionamento 301 e 302?**

Um [redirecionamento 301](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301) sinaliza uma mudança permanente. O Google transfere a equidade de links e eventualmente desindica a URL antiga. Um `302` sinaliza uma mudança temporária. O Google mantém a URL antiga indexada e pode não transferir a equidade completa. Use `301` para qualquer mudança permanente de URL.

**Muitos redirecionamentos 301 podem deixar meu site mais lento?**

Redirecionamentos individuais adicionam latência mínima (menos de 100 ms). O problema são as cadeias de redirecionamento. Cada salto adiciona de 50 a 100 ms. Uma cadeia de 3 saltos adiciona de 150 a 300 ms antes mesmo de a página começar a carregar. Mantenha cada redirecionamento em um único salto e o impacto no desempenho permanece insignificante.

**Como verifico se meus redirecionamentos 301 estão funcionando?**

Use `curl -I [URL]` no seu terminal. A resposta deve mostrar `HTTP/1.1 301 Moved Permanently` com um cabeçalho `Location:` apontando para o destino correto. Você também pode usar o Chrome DevTools (aba Network com "Preserve log" ativado) ou ferramentas online gratuitas como httpstatus.io.

**Devo usar um redirecionamento 301 ou uma tag canonical?**

Use `301` quando estiver removendo a página antiga completamente. Use uma tag `canonical` quando ambas as páginas permanecerem no ar, mas você quiser que o Google consolide os sinais de posicionamento em uma versão. Um exemplo comum: páginas de produto com parâmetros de URL. A URL filtrada permanece acessível, mas a canonical aponta para a URL limpa. Para [canibalização de palavras-chave](/blog/fix-keyword-cannibalization) entre 2 páginas ativas, uma tag canonical é frequentemente o melhor primeiro passo.

---

Os redirecionamentos 301 protegem a equidade de links e as posições que você já conquistou. Cada mudança de URL sem um redirecionamento é um vazamento na sua fundação de SEO.

Configure os redirecionamentos corretamente, teste-os, monitore-os e combine o trabalho com publicação consistente de conteúdo. É assim que você [sobe nas posições do Google](/blog/how-to-rank-higher-google) e mantém as posições que conquista.
