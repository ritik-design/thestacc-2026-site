---
term: "hreflang"
slug: "hreflang"
definition: "hreflang es un atributo HTML que indica a los buscadores qué versión lingüística o regional de una página mostrar a cada usuario, evitando contenido duplicado."
category: "SEO"
difficulty: "Advanced"
keyword: "etiqueta hreflang"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## ¿Qué es hreflang?

hreflang es un atributo HTML (`rel="alternate" hreflang="x"`) que comunica a Google y al resto de motores de búsqueda a qué idioma y país está dirigida una versión concreta de una página.

Si tu sitio cuenta con páginas en varios idiomas o variantes regionales —por ejemplo, español para España y español para México—, la etiqueta hreflang impide que Google interprete esas páginas como [contenido duplicado](/glossary/duplicate-content). Sin ella, Google elige una sola versión y la muestra a todo el mundo. Y rara vez es la adecuada para cada audiencia.

Un estudio de Ahrefs revela que solo el 19 % de los sitios multilingües implementan hreflang correctamente. El 81 % restante presenta errores: rutas rotas, etiquetas de retorno ausentes, códigos mal escritos. Es uno de los elementos del SEO técnico que más se configura mal.

## ¿Por qué importa hreflang?

Acertar con hreflang determina si la audiencia correcta verá la página correcta.

- **Entrega lingüística adecuada**. Quien busca desde Madrid ve la versión de España, quien busca desde Buenos Aires ve la argentina, sin redirecciones manuales
- **Evita el filtrado por contenido duplicado**. Google entiende que tus páginas `/es/` y `/mx/` no son copias, sino traducciones intencionadas
- **Mejor experiencia del usuario**. Quien aterriza en una página en su propio idioma rebota menos y convierte más
- **Precios y catálogos regionales**. Los e-commerce con monedas, impuestos o productos distintos por país necesitan hreflang para servir la variante correcta en cada mercado

Cualquier negocio con presencia en varios países o idiomas necesita hreflang. Sin excepciones.

## Cómo funciona hreflang

### Métodos de implementación

Existen tres formas de implementar hreflang: etiquetas `<link>` en el `<head>` del HTML, cabeceras HTTP (para PDFs y archivos no HTML) o entradas en tu [sitemap XML](/glossary/xml-sitemap). Google recomienda elegir un método y mantenerlo. El sitemap es la opción más cómoda en sitios grandes con cientos de variantes lingüísticas.

### La regla del retorno bidireccional

Cada anotación hreflang debe ser recíproca. Si la página A dice "mi equivalente en francés es la página B", la página B debe decir "mi equivalente en español es la página A". Las etiquetas de retorno ausentes son el error de implementación más frecuente. Sin reciprocidad, Google ignora las anotaciones por completo.

### La etiqueta x-default

El valor `x-default` indica a Google qué versión mostrar cuando no existe una coincidencia exacta de idioma o región. Tu plan B. Suele ser la versión en inglés o la del mercado principal. Sin `x-default`, Google decide por su cuenta. Y no siempre acierta.

## Ejemplos de hreflang

**Ejemplo 1: una tienda online con versiones para España y México**
Un retailer con sede en Madrid mantiene `example.com/es/zapatos` (precios en euros, IVA español) y `example.com/mx/zapatos` (precios en pesos, IVA mexicano). Sin hreflang, Google podría mostrar la versión española a un usuario mexicano. Con la etiqueta hreflang correcta, cada audiencia ve los precios y la moneda adecuados. La [URL canónica](/glossary/canonical-url) se mantiene independiente en cada versión.

**Ejemplo 2: una empresa SaaS con páginas traducidas**
Una herramienta de gestión de proyectos tiene su home en 8 idiomas. Implementan hreflang vía sitemap XML, donde cada versión apunta a las demás. Quien busca en alemán llega a `/de/`, quien busca en español a `/es/`, y el resto cae en la versión inglesa marcada como `x-default`.

¿Quieres publicar contenido internacional sin pelearte con la configuración de hreflang? theStacc publica 30 artículos optimizados para buscadores en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Preguntas frecuentes

### ¿Afecta hreflang al posicionamiento?

hreflang no mejora el ranking de forma directa. Indica a Google qué versión mostrar en cada mercado. Pero servir el idioma correcto a la audiencia correcta mejora señales de engagement —menor tasa de rebote y mayor [tiempo de permanencia](/glossary/dwell-time)— que sí pueden influir en el posicionamiento con el tiempo.

### ¿Sirve hreflang para el mismo idioma en varios países?

Sí. Es justamente uno de sus mejores usos. Inglés de Estados Unidos (`en-us`), inglés de Reino Unido (`en-gb`) e inglés de Australia (`en-au`) pueden coexistir con anotaciones separadas. Google usa el código de país, no solo el de idioma, para decidir qué versión sirve.

### ¿Qué pasa si hreflang está mal implementado?

Google ignora las anotaciones por completo y decide por sí mismo qué versión mostrar. No hay penalización. Solo pierdes el control sobre qué página aparece en cada mercado. El informe de Segmentación internacional de Google Search Console te ayuda a detectar los errores.

---

¿Quieres ganar visibilidad internacional sin montar un equipo de SEO en cada país? theStacc publica 30 artículos optimizados para buscadores en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: implementación de hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs: guía sobre etiquetas hreflang](https://ahrefs.com/blog/hreflang-tags/)
- [Moz: la guía definitiva sobre hreflang](https://moz.com/learn/seo/hreflang-tag)
