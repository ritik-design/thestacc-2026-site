---
term: "URL canónica / Canonicalización"
slug: "canonical-url"
definition: "Una URL canónica indica a los motores de búsqueda qué versión de una página es la copia principal. Aprende cómo la canonicalización previene problemas de contenido duplicado y cómo usarla correctamente."
category: "SEO"
difficulty: "Intermediate"
keyword: "url canónica"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "301-redirect"
  - "indexing"
  - "crawl-budget"
  - "technical-seo"
---

## ¿Qué es una URL canónica?

Una URL canónica es un elemento HTML que indica a los motores de búsqueda qué versión de una página es la copia preferida y autoritativa cuando varias URLs sirven el mismo contenido o uno muy similar.

En el `<head>` de una página tiene este aspecto: `<link rel="canonical" href="https://example.com/preferred-page">`. ¿Por qué existe? Porque en la web moderna, una sola pieza de contenido vive a menudo en varias URLs. La misma página de producto accesible con y sin www, con y sin barra final, con parámetros de seguimiento, a través de navegación filtrada. Google ve cada URL como una página separada. Sin una etiqueta canónica, Google tiene que adivinar cuál indexar. Y a menudo se equivoca.

Datos de Semrush de un estudio de 150.000 sitios web encontraron que el 65 % de los dominios tienen alguna forma de problema de [contenido duplicado](/glossary/duplicate-content). Las etiquetas canónicas son la herramienta principal para resolverlo a escala sin reestructurar todo tu sitio.

## ¿Por qué importa la canonicalización?

El contenido duplicado no es una penalización. Google lo ha dicho claramente. Pero crea problemas reales de SEO que te cuestan tráfico y posicionamientos.

- **El link equity se divide**. Si 30 sitios enlazan a tu página, pero la mitad enlazan a `example.com/page` y la mitad a `example.com/page/`, la autoridad se divide. Una canónica consolida todas las señales en una URL, haciéndola más fuerte.
- **El [crawl budget](/glossary/crawl-budget) se desperdicia**. Googlebot tiene un crawl budget finito para tu sitio. Cada URL duplicada que rastrea es una página que no rastreó. Para sitios grandes con miles de páginas, esto impacta directamente en cuán rápido se [indexa](/glossary/indexing) el contenido nuevo.
- **La página equivocada podría posicionarse**. Sin canonicalización, Google elige la versión que considera mejor. Podría ser tu URL móvil, una URL llena de parámetros o una página de categoría filtrada. No la versión limpia y optimizada que quieres posicionar.
- **Las analíticas se fragmentan**. Los datos de tráfico y engagement se reparten entre varias URLs. Tu rendimiento real se ve más débil de lo que es porque las métricas están divididas.

Si tu sitio tiene más de un puñado de páginas, casi seguro que tienes contenido duplicado que la canonicalización podría arreglar.

## Cómo funciona la canonicalización

La etiqueta canónica es una sugerencia, no una directiva. Google generalmente la respeta. Pero no siempre.

### Canónicas autorreferenciales

Cada página de tu sitio debería apuntar su etiqueta canónica a sí misma. Esto se llama canónica autorreferencial. Le dice a Google: "Esta es la URL preferida para este contenido, incluso si la descubres a través de un camino diferente". La mayoría de las plataformas [CMS](/glossary/content-management-system) y plugins de [SEO técnico](/glossary/technical-seo) lo manejan automáticamente.

### Canónicas entre dominios

Si sindicas contenido. Publicando el mismo artículo en tu blog y en Medium o LinkedIn. Puedes establecer una canónica entre dominios apuntando desde la versión sindicada de vuelta a tu original. Esto le dice a Google que acredite el [link equity](/glossary/link-equity) y las señales de ranking a tu dominio, no a la copia sindicada.

### Canónica vs. elección de Google

Google trata las etiquetas canónicas como una pista fuerte, no como un comando. Si la etiqueta canónica entra en conflicto con otras señales (sitemaps, enlaces internos, patrones de redirección), Google puede sobrescribir tu preferencia. Por eso importa la consistencia. Tu canónica, tus [enlaces internos](/glossary/internal-link), tu sitemap y tus [redirecciones 301](/glossary/301-redirect) deberían apuntar todos a la misma URL preferida.

### Variaciones comunes de URLs canónicas

Estos son los escenarios de contenido duplicado más frecuentes que la canonicalización resuelve:

- `http://` vs. `https://`
- `www.example.com` vs. `example.com`
- `/page` vs. `/page/` (barra final)
- `/page` vs. `/page?utm_source=google&utm_medium=cpc`
- `/page` vs. `/page?ref=homepage`
- URLs móviles (`m.example.com`) vs. URLs de escritorio

Cada variación es una URL separada para Google. Las etiquetas canónicas las fusionan en una.

## Tipos de canonicalización

Hay varias formas de señalar tu URL preferida. La etiqueta canónica es la más común, pero no la única opción.

- **Etiqueta canónica HTML**. La etiqueta `<link rel="canonical">` en el `<head>` de la página. La más flexible, funciona en cualquier página, fácil de implementar.
- **Canónica en cabecera HTTP**. Enviada como cabecera `Link:` en la respuesta HTTP. Se usa para archivos no HTML (PDFs, imágenes) donde no puedes añadir etiquetas HTML.
- **[Redirección 301](/glossary/301-redirect)**. Redirige permanentemente las URLs duplicadas a la versión preferida. Más fuerte que una etiqueta canónica porque usuarios y bots solo pueden acceder a la URL preferida.
- **Señales de [sitemap XML](/glossary/xml-sitemap)**. Incluir solo URLs canónicas en tu sitemap refuerza qué versiones prefieres. No es un método directo de canonicalización, pero es una señal de apoyo.
- **Consistencia en el enlazado interno**. Enlazar siempre a la misma versión de una URL en todo tu sitio envía a Google una señal clara sobre tu versión preferida.

Para la mayoría de sitios, la etiqueta canónica HTML combinada con un enlazado interno consistente cubre más del 90 % de los casos.

## Ejemplos de URL canónica

**Ejemplo 1: Una tienda online con URLs llenas de parámetros**
La página de producto de una tienda de ropa vive en `/zapatillas-running-azules`. Pero filtrar por talla genera `/zapatillas-running-azules?size=10`, y los códigos de seguimiento añaden `/zapatillas-running-azules?utm_source=email`. Las tres muestran el mismo producto. Sin etiquetas canónicas, Google podría indexar la URL de parámetro en lugar de la limpia. Añadir `<link rel="canonical" href="/zapatillas-running-azules">` a las tres versiones lo soluciona al instante.

**Ejemplo 2: Un negocio multi-localización con páginas de servicio duplicadas**
Una franquicia de fontanería tiene páginas de servicio para cada ciudad: `/madrid/desatasco`, `/barcelona/desatasco`, `/sevilla/desatasco`. El contenido es 90 % idéntico, solo cambia el nombre de la ciudad. Estas páginas no deberían canonicalizarse entre sí (apuntan a [palabras clave locales](/glossary/local-keywords) diferentes), pero cada una debería autorreferenciarse. La solución real es hacer cada página genuinamente única con contenido específico de la ciudad. Algo que theStacc maneja generando artículos específicos por ubicación automáticamente.

**Ejemplo 3: Un blog que sindica contenido a Medium**
Una empresa B2B republica sus posts de blog en Medium para exposición extra. Sin una etiqueta canónica, Google podría posicionar la versión de Medium en lugar del original. Al añadir una URL canónica apuntando de vuelta al blog de la empresa en cada post de Medium (Medium lo soporta en los ajustes), todas las señales de ranking fluyen al dominio original. El [tráfico orgánico](/glossary/organic-traffic) va a tu sitio, no al de Medium.

## URL canónica vs. redirección 301

Ambas resuelven problemas de contenido duplicado. La elección correcta depende de si la página duplicada debe seguir siendo accesible.

| | URL canónica | [Redirección 301](/glossary/301-redirect) |
|---|---|---|
| **El usuario ve** | Ambas páginas son accesibles | El usuario es enviado a la página preferida |
| **Fuerza de la señal** | Pista fuerte (Google puede sobrescribir) | Definitiva (redirección forzada) |
| **Usar cuando** | Ambas URLs deben existir (parámetros, sindicación) | La URL antigua no debe visitarse más |
| **Link equity** | Consolidado en la URL canónica | Pasa ~95-99 % al destino |
| **Ejemplo** | Página de producto con parámetros de filtro | URL antigua de blog movida a nueva estructura |

Cuando la página duplicada debe seguir siendo accesible (URLs con tracking, resultados filtrados, contenido sindicado), usa una canónica. Cuando la URL antigua está muerta y enterrada, usa una 301.

## Buenas prácticas con URL canónicas

- **Autorreferencia cada página**. Incluso las páginas sin duplicados deberían tener una etiqueta canónica autorreferencial. Es una red de seguridad contra URLs duplicadas inesperadas por parámetros, IDs de sesión o peculiaridades del CMS.
- **Usa URLs absolutas, no relativas**. Escribe siempre la URL completa: `https://example.com/page`. No `/page`. Las canónicas relativas pueden causar problemas con la resolución de protocolo y dominio.
- **Apunta las canónicas a páginas indexables**. Nunca establezcas una canónica a una página [noindexada](/glossary/noindex), redirigida o que devuelva un [404](/glossary/404-error). Confunde a Google y vence el propósito.
- **Audita las canónicas tras migraciones**. Cambios de CMS, mudanzas de dominio y rediseños rompen frecuentemente etiquetas canónicas. Ejecuta un rastreo con Screaming Frog o Sitebulb tras el lanzamiento para verificar que cada página apunta a la canónica correcta.
- **Mantén consistentes tus señales**. Tu etiqueta canónica, sitemap, enlaces internos y hreflang (para sitios internacionales) deberían coincidir todos en la URL preferida. Cuando las señales entran en conflicto, Google toma su propia decisión. Y puede no ser la que quieres. theStacc publica todos los artículos con etiquetas canónicas adecuadas y estructuras de URL limpias incorporadas.

## Preguntas frecuentes

### ¿Las etiquetas canónicas pasan link equity?

Sí. Google consolida las señales de ranking de páginas duplicadas a la URL canónica. Si 10 sitios enlazan a una versión con parámetros de tu página y la canónica apunta a la versión limpia, la versión limpia obtiene el beneficio de esos enlaces.

### ¿Puedo canonicalizar a un dominio diferente?

Sí. Las canónicas entre dominios le dicen a Google que el contenido original vive en un dominio diferente. Caso de uso común: sindicar contenido a Medium, LinkedIn o sitios partner manteniendo tu dominio como fuente canónica.

### ¿Qué pasa si mi etiqueta canónica está mal?

Google puede ignorarla. Si la canónica apunta a una página con contenido completamente diferente, Google reconoce el desajuste e indexará las URLs de forma independiente. Las etiquetas canónicas solo funcionan cuando las páginas tienen contenido sustancialmente similar.

### ¿Cómo compruebo mis etiquetas canónicas?

Ver el código fuente de la página y buscar `rel="canonical"`. O usar [Google Search Console](/glossary/google-search-console). La herramienta de Inspección de URL muestra qué canónica seleccionó Google para cualquier página. Si la canónica elegida por Google difiere de la tuya, hay un conflicto en tus señales.

---

¿Quieres cada artículo publicado con etiquetas canónicas adecuadas, URLs limpias y [SEO técnico](/glossary/technical-seo) gestionado automáticamente? theStacc publica 30 artículos optimizados al mes en tu sitio. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Consolidar URLs duplicadas](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Moz: Guía de etiqueta de URL canónica](https://moz.com/learn/seo/canonicalization)
- [Ahrefs: Etiquetas canónicas para SEO](https://ahrefs.com/blog/canonical-tags/)
- [Semrush: Estudio de contenido duplicado](https://www.semrush.com/blog/duplicate-content/)
- [Google Search Console: Herramienta de Inspección de URL](https://support.google.com/webmasters/answer/9012289)
