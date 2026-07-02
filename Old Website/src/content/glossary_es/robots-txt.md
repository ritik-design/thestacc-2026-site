---
term: "robots.txt"
slug: "robots-txt"
definition: "robots.txt es un archivo de texto plano en la raíz de tu sitio web que indica a los rastreadores de motores de búsqueda qué URLs pueden y no pueden visitar."
category: "SEO"
difficulty: "Intermediate"
keyword: "qué es robots.txt"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## ¿Qué es robots.txt?

**El archivo robots.txt vive en la raíz de tu dominio (tusitio.com/robots.txt) y le dice a los rastreadores de los motores de búsqueda a qué páginas o secciones de tu sitio tienen permiso para acceder.**

Todos los grandes motores de búsqueda. Google, Bing, Yahoo. Consultan este archivo antes de [rastrear](/glossary/crawling) tu sitio. Piénsalo como la lista del portero de un local. No es un cerrojo en la puerta, sino un conjunto claro de instrucciones que los bots educados respetan.

Según la propia documentación de Google, Googlebot revisa robots.txt antes de hacer cualquier petición a tu servidor. En sitios con miles de páginas, ese archivo se convierte en una de las piezas más importantes de tu [SEO técnico](/glossary/technical-seo).

## ¿Por qué importa robots.txt?

Equivocarse con robots.txt puede hundir tus posiciones de un día para otro. Una directiva mal puesta y Google deja de ver tus páginas más importantes.

- **Protección del crawl budget**. Los sitios grandes tienen un [crawl budget](/glossary/crawl-budget) limitado. Bloquear páginas de bajo valor (paneles de admin, entornos de staging, filtros duplicados) mantiene a Googlebot enfocado en lo que importa.
- **Evita la indexación de zonas sensibles**. Resultados de búsqueda interna, páginas de login y carritos no pintan nada en la [SERP](/glossary/serp). robots.txt mantiene a los bots fuera.
- **Descubrimiento más rápido del contenido nuevo**. Cuando los rastreadores no malgastan peticiones en páginas basura, encuentran tus nuevas entradas de blog y fichas de producto antes.
- **Gestión de la carga del servidor**. Los bots agresivos pueden saturar servidores pequeños. Bloquear el rastreo innecesario reduce el consumo de recursos.

Si publicas contenido con regularidad. Da igual si son 5 páginas o 30 artículos al mes. Necesitas que los rastreadores dediquen su tiempo a las URLs correctas.

## Cómo funciona robots.txt

El archivo usa una sintaxis sencilla. Tres directivas centrales cubren la mayoría de los casos.

### User-agent

Esta línea indica a qué rastreador se aplica la regla. `User-agent: *` se dirige a todos los bots. `User-agent: Googlebot` solo al rastreador de Google. Puedes apilar varias reglas para distintos bots en el mismo archivo.

### Disallow

La directiva `Disallow` bloquea una ruta específica. `Disallow: /admin/` impide que los rastreadores accedan a cualquier cosa bajo el directorio /admin/. Si la dejas vacía (`Disallow:`), permites todo. Una única barra (`Disallow: /`) bloquea el sitio entero.

### Allow y Sitemap

`Allow` anula una regla Disallow más amplia para rutas concretas. Útil cuando bloqueas un directorio pero quieres que se rastree una página dentro. La directiva `Sitemap` apunta a tu [sitemap XML](/glossary/xml-sitemap) y ayuda a los rastreadores a encontrar todas tus URLs importantes sin adivinar.

### Cómo lo procesa Google

Googlebot pide tu robots.txt antes de rastrear nada más. Si el archivo devuelve un estado 200, Google sigue las reglas. Un 404 significa "sin restricciones". Todo se rastrea. Un error 5xx hace que Google se vuelva temporalmente prudente y limite el rastreo hasta que el archivo vuelva a estar accesible.

## Tipos de directivas en robots.txt

Las directivas de robots.txt se agrupan en 4 categorías principales:

- **Directivas de acceso (Allow/Disallow)**. Controlan a qué rutas pueden acceder los bots. La base de cualquier robots.txt.
- **Directivas de user-agent**. Dirigen reglas a bots concretos. Podrías bloquear SemrushBot mientras das vía libre a Googlebot.
- **Directivas de crawl-delay**. Indican a los bots que esperen entre peticiones. Google las ignora (usa Google Search Console en su lugar), pero Bing y Yandex sí las respetan.
- **Directivas de sitemap**. Apuntan a tu archivo de sitemap. Técnicamente no es una "regla" sino un mecanismo de descubrimiento del que dependen los bots.

La mayoría de los sitios pequeños y medianos solo necesitan directivas de acceso y una referencia al sitemap. Crawl-delay importa más en sitios a gran escala con limitaciones de servidor.

## Ejemplos de robots.txt

**Ejemplo 1: empresa local de fontanería**
Un fontanero en Madrid tiene un sitio en WordPress con los directorios /wp-admin/, /carrito/ y /precios-internos/. Su robots.txt bloquea los tres e incluye una referencia al sitemap. Resultado: Googlebot pasa el tiempo en las páginas de servicios y entradas de blog. No en paneles de admin.

**Ejemplo 2: tienda online con páginas filtradas**
Un comercio electrónico tiene 50 productos pero 3.000 combinaciones de filtros (talla + color + precio). Sin un robots.txt que bloquee `/productos?filtro=`, Googlebot malgasta [crawl budget](/glossary/crawl-budget) en páginas duplicadas. Una línea de Disallow lo arregla.

**Ejemplo 3: bloquear el sitio entero por accidente**
Una agencia de marketing pasó de staging a producción y dejó `Disallow: /` en robots.txt. Durante 3 semanas no se [indexó](/glossary/indexing) nada. El tráfico cayó a cero. Un solo carácter lo provocó. La barra después de Disallow.

## robots.txt vs etiqueta meta robots

Estos dos hacen trabajos distintos en momentos distintos. robots.txt frena a los rastreadores antes de que lleguen a una página. La [etiqueta meta robots](/glossary/meta-robots-tag) da instrucciones después de que un rastreador ya haya accedido.

| | robots.txt | Etiqueta meta robots |
|---|---|---|
| **Dónde vive** | Archivo en la raíz | `<head>` HTML de páginas individuales |
| **Cuándo actúa** | Antes del rastreo | Después del rastreo |
| **Alcance** | Directorios o rutas completas | Páginas individuales |
| **¿Evita la indexación?** | No. Solo bloquea el rastreo | Sí, `noindex` retira de la búsqueda |
| **Ideal para** | Bloquear secciones del sitio | Sacar páginas concretas de la búsqueda |

El detalle: si bloqueas una página con robots.txt, Google no puede ver una etiqueta noindex en ella. Así que esa página podría seguir apareciendo en los resultados de búsqueda (sin snippet) porque Google encontró un enlace en otro sitio. Para retirar de verdad una página, usa la etiqueta meta robots. No robots.txt.

## Buenas prácticas para robots.txt

- **Incluye siempre una directiva Sitemap**. Apunta a tu [sitemap XML](/glossary/xml-sitemap) para que los rastreadores tengan un mapa completo. Una línea: `Sitemap: https://tusitio.com/sitemap.xml`.
- **Nunca bloquees archivos CSS o JavaScript**. Google necesita renderizar tus páginas para entenderlas. Bloquear esos recursos perjudica tu [SEO on-page](/glossary/on-page-seo).
- **Prueba antes de desplegar**. Usa el probador de robots.txt de Google Search Console para revisar tus reglas. Una errata puede bloquear todo el sitio.
- **Revísalo cada trimestre**. A medida que tu sitio crece aparecen nuevos directorios. Lo que tenía sentido hace 6 meses puede estar bloqueando contenido importante hoy.
- **Combínalo con una estrategia de contenido**. robots.txt gestiona qué se rastrea, pero sigues necesitando páginas que merezca la pena rastrear. Servicios como theStacc publican 30 artículos optimizados para SEO al mes, dándole a Googlebot contenido fresco en cada visita.

## Preguntas frecuentes

### ¿robots.txt evita que las páginas aparezcan en Google?

No directamente. robots.txt impide el rastreo, no la [indexación](/glossary/indexing). Si otros sitios enlazan a una página bloqueada, Google puede seguir mostrándola en los resultados. Solo que sin descripción. Usa una etiqueta meta noindex para retirar una página por completo de la búsqueda.

### ¿Dónde coloco mi archivo robots.txt?

Colócalo en la raíz de tu dominio: `https://tusitio.com/robots.txt`. Ponerlo en un subdirectorio no funciona. Cada subdominio necesita su propio robots.txt.

### ¿Puede robots.txt mejorar mis posiciones?

De forma indirecta, sí. Bloquear páginas de bajo valor preserva el crawl budget para tu contenido importante. En sitios grandes, eso significa descubrimiento e indexación más rápidos de las páginas nuevas. Lo cual puede acelerar la mejora de posiciones.

### ¿Todos los bots respetan robots.txt?

Los bots legítimos de motores de búsqueda (Googlebot, Bingbot) respetan robots.txt. Los bots maliciosos y los scrapers normalmente lo ignoran. No te apoyes en robots.txt como medida de seguridad. Es una guía, no un firewall.

---

¿Quieres asegurarte de que tu contenido SEO se rastrea y posiciona de verdad? theStacc publica 30 artículos optimizados para buscadores en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Especificaciones de robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central: Cómo interpreta Google el archivo robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz: Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs: Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
