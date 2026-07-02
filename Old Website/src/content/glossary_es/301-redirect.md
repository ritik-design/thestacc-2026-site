---
term: "Redirección 301"
slug: "301-redirect"
definition: "Una redirección 301 envía permanentemente a los usuarios y a los motores de búsqueda de una URL a otra. Aprende cuándo usar redirecciones 301, cómo implementarlas y su impacto en el SEO."
category: "SEO"
difficulty: "Intermediate"
keyword: "qué es una redirección 301"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## ¿Qué es una Redirección 301?

Una redirección 301 es un código de estado HTTP que reenvía permanentemente una URL a otra. Le indica a los navegadores y a los motores de búsqueda que la dirección original se ha movido de forma definitiva.

Cuando Googlebot o un visitante llega a una redirección 301, es enviado automáticamente a la nueva URL. Sin página rota. Sin callejón sin salida. El "301" hace referencia al código de respuesta HTTP específico. Es la forma que tiene la web de decir "esta página se ha movido permanentemente a una nueva ubicación." Existe una [redirección 302](/glossary/302-redirect) para los movimientos temporales, pero la 301 es la que importa para el [SEO](/glossary/seo).

He aquí por qué esto es crítico: la investigación de Moz muestra que las redirecciones 301 transfieren aproximadamente el 95-99% de la [equidad de enlaces](/glossary/link-equity) a la URL de destino. Eso significa que el poder de posicionamiento que tu URL antigua ganó gracias a los [backlinks](/glossary/backlinks) no desaparece. Se transfiere a la nueva página. Si implementas mal las redirecciones 301, estás tirando por la borda años de autoridad acumulada.

## ¿Por Qué Importa una Redirección 301?

Cada vez que una URL cambia sin una redirección adecuada, algo se rompe. Posicionamiento, tráfico, experiencia del usuario. Elige dos.

- **Preserva el posicionamiento en buscadores**. Sin una redirección 301, Google trata la nueva URL como una página completamente nueva con cero autoridad. Tus posiciones desaparecen de la noche a la mañana.
- **Transfiere la equidad de enlaces**. ¿Esos [backlinks](/glossary/backlinks) que ganaste? Una redirección 301 pasa su valor a la nueva URL. Sin ella, ese link juice se evapora.
- **Previene los errores 404**. Los usuarios que guardaron la URL antigua como favorito o hacen clic en un enlace externo llegan a una página funcional en lugar de a un [error 404](/glossary/404-error). Mejor experiencia, menor [tasa de rebote](/glossary/bounce-rate).
- **Consolida el contenido duplicado**. Múltiples URLs con el mismo contenido diluyen tu autoridad. Las redirecciones 301 las fusionan en una sola página sólida.

Si alguna vez has movido un sitio web, cambiado una estructura de URL o fusionado dos páginas, necesitabas redirecciones 301. Omitirlas es uno de los errores de [SEO técnico](/glossary/technical-seo) más comunes y costosos.

## Cómo Funciona una Redirección 301

El proceso ocurre en milisegundos, pero esto es lo que realmente sucede bajo el capó.

### El Ciclo de Solicitudes HTTP

Un usuario o rastreador de motor de búsqueda solicita la URL antigua. El servidor responde con el código de estado HTTP 301 y un encabezado "Location" que apunta a la nueva URL. El navegador solicita automáticamente la nueva URL. El usuario ve la página final. Puede que ni siquiera note que ocurrió la redirección.

### Cómo Procesa Google las Redirecciones 301

Cuando [Googlebot](/glossary/crawling) encuentra una redirección 301, hace tres cosas: sigue la redirección a la nueva URL, transfiere la mayoría de las señales de posicionamiento de la página antigua a la nueva, y eventualmente elimina la URL antigua de su índice. Este proceso puede tardar días o semanas dependiendo de la frecuencia con la que Google rastree tu sitio.

### Implementación a Nivel de Servidor vs. a Nivel de Página

Las redirecciones 301 se configuran a nivel de servidor. No en tu HTML. Los métodos más comunes:

- **Apache (.htaccess):** `Redirect 301 /pagina-antigua https://ejemplo.com/pagina-nueva`
- **Nginx:** `rewrite ^/pagina-antigua$ /pagina-nueva permanent;`
- **Plugins de WordPress:** Yoast, Redirection o Rank Math lo gestionan desde el panel de administración
- **Cloudflare:** Reglas de página o Redirecciones masivas para cambios a nivel de dominio

Existen redirecciones meta refresh a nivel de página, pero son más lentas y no transfieren la equidad de enlaces con la misma fiabilidad. Usa siempre redirecciones 301 a nivel de servidor.

## Tipos de Redirecciones

Entender las diferencias previene errores costosos:

- **301 (Permanente)**. La página se ha movido para siempre. Transfiere aproximadamente el 95-99% de la equidad de enlaces. Úsala para cambios de URL, migraciones de dominio y consolidación de contenido.
- **[302 (Temporal)](/glossary/302-redirect)**. La página se ha movido temporalmente. Google puede o no transferir la equidad de enlaces. Úsala para pruebas A/B, páginas de mantenimiento o contenido de temporada.
- **307 (Temporal, HTTP/1.1)**. Igual que la 302, pero preserva estrictamente el método de solicitud (POST permanece POST). Solo para casos de uso técnicos.
- **308 (Permanente, HTTP/1.1)**. Igual que la 301 con preservación estricta del método. Rara vez se usa en contextos SEO.
- **Meta refresh**. Redirección basada en HTML. Lenta, escaso valor SEO. Evítala.

Ante la duda, usa una redirección 301. Es la opción segura para los cambios permanentes de URL.

## Ejemplos de Redirecciones 301

**Ejemplo 1: Una empresa local que rediseña su sitio web**
Un bufete de abogados rediseña su sitio y cambia la estructura de URL de `/servicios/abogado-lesiones-personales` a `/areas-practica/lesiones-personales`. Sin una redirección 301, la página antigua, que estaba en la posición #3 para "abogado de lesiones personales [ciudad]", devolvería un 404. Con la redirección, la nueva URL hereda la posición y los 47 [backlinks](/glossary/backlinks) que apuntaban a la página antigua siguen funcionando.

**Ejemplo 2: Fusionar dos entradas de blog en una página más sólida**
Una empresa de plomería tiene dos artículos delgados: "Cómo reparar un grifo con goteras" y "Guía de reparación de grifos con fugas." Ninguno posiciona bien. Fusionan ambos en una guía detallada en la URL más sólida y aplican una redirección 301 a la más débil. Las señales combinadas de [autoridad de dominio](/glossary/domain-authority) elevan la página fusionada de la posición 12 a la posición 4 en 6 semanas.

**Ejemplo 3: Migración de dominio que salió mal**
Una tienda de ecommerce se muda de dominioantiguo.com a dominionuevo.com pero solo redirige la página de inicio. Las 2.400 páginas de productos y los 180 artículos del blog devuelven errores 404. El [tráfico orgánico](/glossary/organic-traffic) cae un 78% en 2 semanas. Cada URL necesitaba una redirección 301 de uno a uno. Este error tarda meses en recuperarse. Si se detecta rápidamente.

## Redirección 301 vs. URL Canonical

Ambas abordan el contenido duplicado, pero funcionan de manera diferente.

| | Redirección 301 | [URL Canonical](/glossary/canonical-url) |
|---|---|---|
| **Qué hace** | Envía a usuarios y bots a una nueva URL | Le dice a Google cuál es la copia "maestra" |
| **Experiencia del usuario** | El usuario ve la nueva página (redirección automática) | El usuario puede acceder a la página original |
| **Cuándo usarla** | La página antigua ya no debe existir | Ambas páginas deben permanecer accesibles |
| **Equidad de enlaces** | Transfiere aproximadamente el 95-99% | Consolida señales en el canonical |
| **Ejemplo** | URL de blog antiguo movida a nueva estructura | Página de producto accesible desde 3 URLs diferentes |

Usa redirecciones 301 cuando la página antigua ha desaparecido. Usa canonicals cuando ambas páginas deban existir pero quieras que Google priorice una.

## Mejores Prácticas para las Redirecciones 301

- **Mapea cada URL antigua a una nueva URL relevante**. No redirijas todo a la página de inicio. Redirige cada página antigua a su equivalente más cercano. Google trata las redirecciones masivas a la página de inicio como soft 404s.
- **Implementa redirecciones de uno a uno durante las migraciones de sitio**. Antes de lanzar un nuevo sitio, rastrea el antiguo, exporta cada URL y crea un mapa de redirecciones. Omite este paso y verás cómo el [tráfico orgánico](/glossary/organic-traffic) se desploma.
- **Evita las cadenas de redirección**. A > B > C > D ralentiza al usuario, desperdicia el [presupuesto de rastreo](/glossary/crawl-budget) y puede perder equidad de enlaces en cada salto. Cada redirección debe apuntar directamente al destino final.
- **Monitorea con Google Search Console**. Revisa el informe de Cobertura en busca de errores de rastreo después de implementar las redirecciones. [Google Search Console](/glossary/google-search-console) muestra qué páginas devuelven errores 404 para que puedas detectar rápidamente las redirecciones faltantes.
- **Audita las redirecciones trimestralmente**. Las redirecciones antiguas que apuntan a páginas que ya no existen crean cadenas. Servicios como theStacc incluyen estructuras de URL adecuadas en cada artículo que publican, pero si estás migrando o reorganizando contenido, programa auditorías periódicas de redirecciones para mantener todo en orden.

## Preguntas Frecuentes

### ¿Las redirecciones 301 perjudican el SEO?

No, cuando se usan correctamente. Una redirección 301 correctamente implementada transfiere casi toda la equidad de enlaces a la nueva URL. John Mueller de Google ha confirmado que las redirecciones 301 no causan pérdida de posicionamiento. El riesgo viene de implementarlas incorrectamente: cadenas de redirección, redirecciones masivas a la página de inicio o páginas omitidas por completo.

### ¿Cuánto tiempo debes mantener una redirección 301?

Indefinidamente, o al menos un año. Google necesita tiempo para volver a rastrear la URL antigua, procesar la redirección y actualizar su índice. Eliminar una redirección 301 demasiado pronto significa que los enlaces externos a la URL antigua vuelven a encontrar errores 404.

### ¿Demasiadas redirecciones 301 pueden ralentizar un sitio?

Las redirecciones individuales añaden milisegundos. Pero las cadenas de redirección (página A > B > C) multiplican ese retraso. Mantén las redirecciones en un máximo de un salto. Un sitio con miles de redirecciones 301 limpias está bien. Son las cadenas y los bucles los que causan problemas.

### ¿Cuál es la diferencia entre una redirección 301 y una 302?

Una [redirección 301 es permanente](/glossary/301-redirect); una [302 es temporal](/glossary/302-redirect). Usa la 301 cuando la URL antigua haya desaparecido definitivamente. Usa la 302 cuando la página original vaya a volver (contenido de temporada, mantenimiento temporal). Google transfiere la equidad de enlaces de manera más fiable a través de las redirecciones 301.

---

¿Quieres una arquitectura de sitio construida para el SEO desde el primer día? theStacc publica 30 artículos optimizados para SEO en tu sitio cada mes con estructuras de URL limpias y enlazado interno adecuado. Automáticamente. [Comienza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Redirecciones y la Búsqueda de Google](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz: Guía de Redirecciones](https://moz.com/learn/seo/redirection)
- [Ahrefs: Redirecciones 301 para SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal: Redirecciones 301 vs 302](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Ayuda de Google Search Console: Corregir Errores de Rastreo](https://support.google.com/webmasters/answer/7440203)
