---
term: "Sitemap XML"
slug: "xml-sitemap"
definition: "Un sitemap XML es un archivo que enumera todas las URLs importantes de tu sitio y ayuda a buscadores como Google a descubrir, rastrear e indexar tus páginas más rápido."
category: "SEO"
difficulty: "Intermediate"
keyword: "qué es un sitemap xml"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "technical-seo"
  - "google-search-console"
---

## ¿Qué es un sitemap XML?

**Un sitemap XML es un archivo estructurado (en formato XML) que entrega a los buscadores una lista completa de las URLs de tu sitio que quieres que rastreen e indexen.**

Es básicamente un mapa para los [rastreadores](/glossary/crawling). Sin él, Googlebot tiene que descubrir tus páginas siguiendo enlaces. Funciona, pero es lento e incompleto. Las páginas huérfanas (sin enlaces internos apuntando hacia ellas) podrían no encontrarse nunca.

La propia documentación de Google indica que los sitemaps son "especialmente útiles" para sitios grandes, sitios nuevos con pocos enlaces externos y webs con mucho contenido multimedia. Un estudio de Oncrawl reveló que las páginas listadas en un sitemap XML se indexan, de media, entre 8 y 10 veces más rápido que las que no lo están.

## ¿Por qué importa un sitemap XML?

Si Google no encuentra tus páginas, no puede posicionarlas. Un sitemap XML elimina las suposiciones.

- **Indexación más rápida del contenido nuevo**. Cuando publicas una entrada de blog o una landing, el sitemap se lo dice a Google al instante. Sin esperar a que Googlebot la descubra siguiendo enlaces.
- **Cobertura para páginas huérfanas**. Las páginas sin enlaces internos son invisibles para los rastreadores. El sitemap las recupera. Es un caso típico en eCommerce grandes con páginas generadas por filtros.
- **Señales de prioridad y frescura**. Los sitemaps incluyen etiquetas `<lastmod>` que avisan a Google de cuándo se actualizó cada página por última vez. El contenido fresco se vuelve a rastrear antes.
- **Valor diagnóstico**. Enviar tu sitemap a [Google Search Console](/glossary/google-search-console) te da un informe de indexación. Ves exactamente qué páginas ha indexado Google y cuáles ha rechazado. Y por qué.

Para cualquier sitio que publique contenido con regularidad, un sitemap XML es innegociable.

## Cómo funciona un sitemap XML

El proceso es directo. Crea el archivo, dile a Google dónde está y mantenlo actualizado.

### Estructura del archivo

Un sitemap XML es una lista de entradas `<url>` envueltas en una etiqueta `<urlset>`. Cada entrada incluye la URL (`<loc>`), la fecha de última modificación (`<lastmod>`), la frecuencia de cambio (`<changefreq>`) y la prioridad (`<priority>`). Google ignora oficialmente `changefreq` y `priority`. Lo que importa es la URL y el `lastmod`.

### Métodos de envío

Tres formas de hacer llegar tu sitemap a Google. Primera: enviarlo directamente desde [Google Search Console](/glossary/google-search-console). Segunda: referenciarlo en tu archivo [robots.txt](/glossary/robots-txt) con `Sitemap: https://tusitio.com/sitemap.xml`. Tercera: usar la Ping API para notificar actualizaciones. La mayoría de los sitios combinan las dos primeras.

### Archivos índice de sitemaps

Un sitemap individual admite como máximo 50.000 URLs o 50 MB (sin comprimir). Los sitios grandes recurren a un archivo índice: un sitemap que apunta a otros sitemaps. Una web de 200.000 páginas suele tener un índice que apunta a 4 sitemaps de 50.000 URLs cada uno.

### Auto-generación

La mayoría de CMS (WordPress, Webflow, Shopify) genera sitemaps XML automáticamente. WordPress crea uno en `/wp-sitemap.xml` por defecto. Plugins SEO como Yoast y RankMath ofrecen más control sobre qué páginas aparecen.

## Tipos de sitemaps XML

No todos los sitemaps cumplen la misma función:

- **Sitemap XML estándar**. Lista tus páginas HTML. El tipo más común y al que se refiere casi todo el mundo cuando dice "sitemap".
- **Sitemap de imágenes**. Lista las imágenes de tu sitio para descubrirlas en Google Imágenes. Útil para fotógrafos, eCommerce y webs con mucho contenido visual.
- **Sitemap de vídeos**. Aporta metadatos del contenido en vídeo (título, descripción, miniatura, duración). Ayuda a que aparezcas en los carruseles de vídeo de Google.
- **Sitemap de noticias**. Específico para editores aprobados en Google News. Incluye fecha de publicación, título e idioma. Solo para sitios autorizados como fuente de noticias.
- **Índice de sitemaps**. Archivo maestro que enlaza a varios sitemaps. Obligatorio en sitios grandes que superan el límite de 50.000 URLs.

La mayoría de pymes solo necesita un sitemap XML estándar. Añade los de imágenes o vídeo si el contenido visual es una parte importante de tu estrategia.

## Ejemplos de sitemap XML

**Ejemplo 1: web nueva de un negocio local**
Una empresa de fontanería recién lanzada en Madrid tiene 15 páginas y cero [backlinks](/glossary/backlinks). Sin sitemap, Google podría tardar semanas en descubrir todas las páginas solo siguiendo enlaces. Tras enviar un sitemap a Search Console, las 15 páginas se indexan en 5 días.

**Ejemplo 2: tienda online con 10.000 productos**
Un retailer añade 50 productos nuevos cada semana. Su sitemap se autogenera vía Shopify y actualiza las fechas `<lastmod>` con cada producto. Google rastrea el sitemap con regularidad y encuentra los nuevos productos en días. No semanas.

**Ejemplo 3: blog que publica 30 entradas al mes**
Una empresa que usa theStacc publica 30 artículos optimizados al mes. Cada nueva entrada aparece automáticamente en el sitemap XML. El informe de cobertura de Search Console muestra crecimiento constante en páginas indexadas. Sin actualizaciones manuales del sitemap.

## Sitemap XML vs sitemap HTML

Archivos distintos para audiencias distintas.

| | Sitemap XML | Sitemap HTML |
|---|---|---|
| **Audiencia** | Rastreadores de buscadores | Visitantes humanos |
| **Formato** | Código XML | Página web normal con enlaces |
| **Ubicación** | `/sitemap.xml` | Suele estar en `/sitemap` o enlazada en el footer |
| **Propósito** | Ayudar a los rastreadores a descubrir todas las páginas | Ayudar al usuario a navegar |
| **Impacto SEO** | Mejora directamente la eficiencia de rastreo | Mínimo. Es más un detalle de UX |
| **¿Obligatorio?** | Muy recomendado | Opcional, un extra |

Ambos son útiles, pero el sitemap XML es el que impacta el [SEO](/glossary/seo) directamente. Si solo vas a implementar uno, que sea el XML.

## Buenas prácticas para sitemaps XML

- **Incluye solo páginas indexables**. Nada de páginas con [noindex](/glossary/noindex), URLs redirigidas o páginas bloqueadas por robots.txt. Un sitemap limpio genera confianza.
- **Mantén las fechas `<lastmod>` exactas**. Solo actualiza la fecha cuando el contenido cambie de verdad. Falsear frescura editando fechas sin cambiar nada erosiona la confianza de Google.
- **Envíalo desde Google Search Console**. El envío manual te da acceso al informe de indexación con detalle. Revísalo cada mes.
- **Limita a 50.000 URLs por archivo**. Si lo superas, usa un índice. Un sitemap enorme que falla al cargar es peor que no tener ninguno.
- **Combínalo con publicación constante**. Un sitemap solo brilla cuando tu sitio añade contenido nuevo digno de [indexar](/glossary/indexing). theStacc publica 30 artículos SEO al mes, dándole a Google motivos para volver a rastrear tu sitemap a menudo y descubrir páginas frescas.

## Preguntas frecuentes

### ¿Toda web necesita un sitemap XML?

No técnicamente. Los sitios pequeños con buen [enlazado interno](/glossary/internal-link) pueden funcionar sin él. Pero no hay desventaja en tenerlo, y los beneficios en velocidad de indexación y datos diagnósticos compensan el mínimo esfuerzo en cualquier proyecto.

### ¿Cómo creo un sitemap XML?

La mayoría de CMS lo genera automáticamente. WordPress, Webflow y Shopify crean sitemaps por defecto. Para sitios a medida, herramientas como Screaming Frog o XML-Sitemaps.com generan el archivo. Después se envía desde Google Search Console.

### ¿Con qué frecuencia debo actualizar mi sitemap?

Idealmente, tu sitemap se actualiza solo al publicar o modificar contenido. Los CMS lo hacen. Si lo mantienes a mano, actualízalo siempre que añadas, elimines o modifiques páginas de forma significativa.

### ¿Puede un sitemap mal hecho perjudicar mi SEO?

Un sitemap con URLs rotas, páginas con noindex o fechas lastmod incorrectas envía señales contradictorias a Google. No provoca una penalización, pero malgasta [crawl budget](/glossary/crawl-budget) y ralentiza la indexación de tus páginas importantes.

---

¿Quieres contenido fresco que Google realmente indexe? theStacc publica 30 artículos optimizados para SEO en tu sitio cada mes. De forma automática. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: aprende sobre sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google Search Central: crear y enviar un sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Ahrefs: sitemaps XML, la guía completa](https://ahrefs.com/blog/xml-sitemap/)
- [Moz: sitemaps XML](https://moz.com/learn/seo/xml-sitemaps)
