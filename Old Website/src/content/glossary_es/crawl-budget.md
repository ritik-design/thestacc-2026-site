---
term: "Crawl budget (presupuesto de rastreo)"
slug: "crawl-budget"
definition: "El crawl budget es el número de páginas que un bot de motor de búsqueda rastreará en tu sitio en un periodo dado. Gestionarlo bien asegura que tus páginas más importantes sean rastreadas e indexadas."
category: "SEO"
difficulty: "Intermediate"
keyword: "crawl budget"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "site-architecture"
  - "xml-sitemap"
---

## ¿Qué es el crawl budget?

El crawl budget es el número total de URLs que Googlebot recogerá de tu sitio durante un periodo dado, determinado por una combinación de límite de tasa de rastreo y demanda de rastreo.

Google no presta atención ilimitada a cada sitio. Googlebot asigna recursos basándose en el tamaño, salud e importancia percibida de tu sitio. Para la mayoría de los sitios pequeños y medianos (menos de 10.000 páginas), el crawl budget no es preocupación. Pero para sitios mayores. Tiendas e-commerce, editores, directorios. Puede ser la diferencia entre que el contenido nuevo se indexe en horas o semanas.

Gary Illyes de Google ha declarado que el crawl budget "no es algo de lo que la mayoría de los sitios deba preocuparse", pero también confirmó que desperdiciarlo en URLs de poco valor puede retrasar la [indexación](/glossary/indexing) de páginas importantes.

## ¿Por qué importa el crawl budget?

Si Googlebot no puede llegar a tus páginas clave, no pueden posicionar. Punto.

- **Indexación más rápida**. Un uso eficiente del crawl budget significa que el contenido nuevo se descubre e indexa antes
- **Páginas priorizadas**. Cuando Googlebot desperdicia presupuesto en [contenido duplicado](/glossary/duplicate-content), páginas 404 o URLs con parámetros, tus páginas clave pueden no rastrearse en absoluto durante ese ciclo
- **Señal de salud del sitio**. Un sitio fácil de rastrear señala calidad a los sistemas de Google, mientras que las trampas de rastreo y errores hacen lo contrario
- **Escalado de contenido**. Sitios publicando 30+ páginas al mes necesitan que Googlebot siga el ritmo del nuevo contenido, haciendo crítica la eficiencia de rastreo

Cualquier sitio con más de unos pocos miles de páginas debería gestionar activamente el crawl budget.

## Cómo funciona el crawl budget

### Límite de tasa de rastreo

Google establece una velocidad máxima de rastreo para evitar sobrecargar tu servidor. Si tu servidor responde lento o devuelve errores, Googlebot se contiene. Hosting rápido y fiable aumenta directamente tu límite de tasa de rastreo.

### Demanda de rastreo

Aunque Googlebot *pudiera* rastrear más, solo lo hará si tiene una razón. Las páginas populares con muchos [backlinks](/glossary/backlinks) se recrastrean con frecuencia. Páginas obsoletas y de baja autoridad pueden pasar meses entre visitas. Actualizar contenido y ganar enlaces aumenta la demanda de rastreo para URLs específicas.

### Desperdiciadores comunes de crawl budget

La navegación por facetas, IDs de sesión en URLs, scroll infinito sin paginación adecuada, [enlaces rotos](/glossary/broken-link) que devuelven [errores 404](/glossary/404-error) y contenido duplicado entre variantes de parámetros se comen todos crawl budget. Usa [robots.txt](/glossary/robots-txt) y [etiquetas noindex](/glossary/noindex) para impedir que Googlebot pierda el tiempo en estas páginas.

## Ejemplos de crawl budget

**Ejemplo 1: Una tienda e-commerce con URLs de filtro**
La web de una tienda de muebles genera 50.000 URLs únicas a partir de combinaciones de filtros (color, tamaño, material, precio). Solo 3.000 son páginas de producto reales. Sin bloquear las URLs de filtro mediante robots.txt, Googlebot gasta el 94 % de su crawl budget en páginas que no deberían indexarse.

**Ejemplo 2: Un blog con mucho contenido**
Una empresa publica 30 artículos al mes mediante theStacc. Con una [arquitectura de sitio](/glossary/site-architecture) limpia y sitemap XML, Googlebot descubre e indexa los nuevos posts en 48 horas. Un competidor publicando el mismo volumen en un sitio mal estructurado espera 2-3 semanas para la indexación.

### Herramientas y recursos

| Herramienta | Propósito | Precio |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Datos de rendimiento de búsqueda | Gratis |
| **Ahrefs** | Backlinks, palabras clave, auditoría de sitio | Desde $99/mes |
| **Semrush** | Plataforma SEO todo-en-uno | Desde $130/mes |
| **Screaming Frog** | Análisis de rastreo técnico | Gratis (500 URLs) |
| **theStacc** | Publicación automatizada de contenido SEO | Desde $99/mes |

## Preguntas frecuentes

### ¿Cómo compruebo mi crawl budget?

El informe de Estadísticas de rastreo de Google Search Console muestra cuántas páginas rastrea Googlebot al día, el tiempo medio de respuesta y las tendencias de solicitudes de rastreo. Compruébalo en Configuración > Estadísticas de rastreo. Busca patrones. Una caída repentina en la tasa de rastreo a menudo señala problemas de servidor.

### ¿Afecta el crawl budget a sitios pequeños?

Para sitios de menos de 1.000 páginas, el crawl budget rara vez importa. Googlebot puede manejar fácilmente sitios pequeños en una sola sesión de rastreo. Empieza a prestar atención cuando superes las 10.000 URLs indexables o notes una indexación lenta de contenido nuevo.

### ¿Cómo mejoro el crawl budget?

Elimina o noindexa páginas de poco valor, arregla errores de rastreo, mejora los tiempos de respuesta del servidor, envía un [sitemap XML](/glossary/xml-sitemap) actualizado y construye enlaces internos a páginas importantes. Pónselo fácil a Googlebot para encontrar y acceder a tu mejor contenido rápidamente.

---

¿Publicas contenido constantemente? Asegúrate de que Google pueda seguir el ritmo. theStacc publica 30 artículos optimizados para SEO en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Gestión del crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central Blog: Qué significa el crawl budget](https://developers.google.com/search/blog/2017/01/what-crawl-budget-means-for-googlebot)
- [Ahrefs: Crawl budget y SEO](https://ahrefs.com/blog/crawl-budget/)
- [Moz: Crawl budget explicado](https://moz.com/blog/crawl-budget)
