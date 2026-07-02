---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "Core Web Vitals son las tres métricas de Google para medir la experiencia de página: LCP, INP y CLS. Aprende qué miden y cómo mejorarlas."
category: "SEO"
difficulty: "Intermediate"
keyword: "qué son core web vitals"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## ¿Qué son los Core Web Vitals?

Los Core Web Vitals son tres métricas específicas que Google usa para medir cuán rápida, receptiva y visualmente estable se siente una página web para los usuarios reales.

Google las introdujo en 2020 y las convirtió en señal oficial de ranking en 2021. Forman parte de la conversación más amplia sobre [velocidad de página](/glossary/page-speed), pero más específicas. En lugar de una única "puntuación de velocidad", los Core Web Vitals descomponen la experiencia del usuario en tres componentes medibles. Carga, interactividad y estabilidad visual.

Según los datos de Google, las páginas que cumplen los tres umbrales registran un 24 % menos de abandonos. No es una mejora menor de UX. Es una vía directa a más conversiones y mejor [tráfico orgánico](/glossary/organic-traffic).

## ¿Por qué importan los Core Web Vitals?

Ignorar los Core Web Vitals no hundirá tus posiciones de un día para otro. Pero, en igualdad de condiciones, Google favorecerá las páginas que pasan estos umbrales sobre las que no.

- **Factor de ranking desde 2021**. Google confirmó los Core Web Vitals como parte de sus señales de page experience, lo que influye directamente en dónde apareces en los [resultados de búsqueda](/glossary/serp)
- **24 % menos abandonos**. Las páginas que pasan los tres umbrales retienen al usuario significativamente más tiempo (Google, 2021)
- **Impacto mobile-first**. Con la [indexación mobile-first](/glossary/mobile-first-indexing) por defecto, las páginas móviles lentas son las más castigadas
- **Correlación con ingresos publicitarios**. Los publishers que mejoraron sus puntuaciones CWV vieron hasta un 15 % más de ingresos por publicidad gracias a sesiones más largas

Si llevas un negocio local o una pyme, esto importa porque tus competidores probablemente tampoco están optimizando los CWV. Aprobar cuando ellos no lo hacen es una ventaja real.

## Cómo funcionan los Core Web Vitals

Google recopila los datos de Core Web Vitals desde usuarios reales de Chrome a través del Chrome User Experience Report (CrUX). Eso significa que tus puntuaciones vienen de visitantes reales. No de una simulación de laboratorio.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) mide cuánto tarda en cargar el elemento visible más grande de tu página. Piensa: la imagen hero, un bloque de texto grande o la miniatura de un vídeo. Google quiere esto por debajo de 2,5 segundos. Cualquier valor por encima de 4 segundos se considera "deficiente".

La solución suele ser sencilla: comprimir imágenes, usar una [CDN](/glossary/content-delivery-network-cdn), aplazar recursos fuera de pantalla y mejorar el tiempo de respuesta del servidor.

### Interaction to Next Paint (INP)

INP reemplazó a First Input Delay (FID) en marzo de 2024. Mide la rapidez con la que tu página responde a las interacciones del usuario. Clics, toques y pulsaciones. Durante toda la visita, no solo en la primera interacción.

Un buen INP está por debajo de 200 milisegundos. Si tu página se congela medio segundo cuando alguien pulsa un botón, suspendes. JavaScript pesado suele ser el culpable.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) mide la estabilidad visual. ¿Has intentado pulsar un botón y de repente la página salta porque un anuncio o una imagen carga tarde? Eso es layout shift.

Google quiere un CLS por debajo de 0,1. Las causas más comunes: imágenes sin dimensiones definidas, anuncios inyectados encima del contenido y fuentes web que cambian de tamaño durante la carga.

## Tipos de evaluación de Core Web Vitals

Los datos de Core Web Vitals vienen en dos sabores, y a menudo cuentan historias distintas:

- **Datos de campo (RUM)**. Real User Metrics recogidos de visitantes reales vía CrUX. Esto es lo que Google usa para decisiones de ranking. Los ves en [Google Search Console](/glossary/google-search-console) y PageSpeed Insights.
- **Datos de laboratorio**. Pruebas de rendimiento simuladas con herramientas como Lighthouse, WebPageTest y Chrome DevTools. Útiles para depurar, pero no se usan directamente para los rankings.
- **Nivel de origen vs. nivel de URL**. Google evalúa los CWV tanto a nivel de dominio completo como de página individual. Si tu sitio aprueba en general pero una landing clave suspende, esa página puede verse afectada igualmente.
- **Móvil vs. escritorio**. Las puntuaciones se miden por separado para móvil y escritorio. La mayoría de sitios rinden peor en móvil, que es la versión que Google prioriza.

Para auditorías de [SEO técnico](/glossary/technical-seo), empieza siempre con datos de campo. Los datos de laboratorio te ayudan a encontrar el problema, pero los de campo te dicen si ese problema realmente está perjudicando a visitantes reales.

## Ejemplos de Core Web Vitals

**Ejemplo 1: La página lenta de un fontanero**
Un fontanero local en Madrid tiene una home con LCP de 4,8 segundos por una imagen hero sin comprimir (3,2 MB). Tras convertirla a WebP y redimensionarla correctamente, el LCP baja a 1,9 segundos. La tasa de rebote cae un 18 % al mes siguiente.

**Ejemplo 2: Un ecommerce con layout shift**
Una tienda Shopify de productos para mascotas tiene un CLS de 0,34 porque las imágenes de producto cargan sin atributos width/height. Añadir dimensiones explícitas a cada etiqueta de imagen lleva el CLS a 0,04. Se acabaron los clics accidentales en "Añadir al carrito" de compradores frustrados.

**Ejemplo 3: Un blog con demasiado JavaScript**
El blog de una agencia de marketing usa 14 scripts de terceros. Analytics, widgets de chat, embeds sociales, trackers publicitarios. El INP está en 480 ms. Tras auditar y eliminar 6 scripts no utilizados, el INP cae a 160 ms. Las páginas creadas y publicadas con theStacc ya salen con código limpio y optimizado. Sin scripts hinchados.

## Core Web Vitals vs. velocidad de página

La gente los usa indistintamente. No deberían.

| | Core Web Vitals | Velocidad de página |
|---|---|---|
| **Qué mide** | 3 métricas específicas de UX (LCP, INP, CLS) | Tiempo de carga global y puntuación de rendimiento |
| **Fuente de datos** | Datos reales de usuario (CrUX) | Simulaciones de laboratorio (Lighthouse) |
| **Señal de ranking de Google** | Sí, directamente | Indirectamente (a través de los CWV) |
| **Alcance** | Centrado en la experiencia percibida | Paraguas más amplio de rendimiento |
| **Métrica de ejemplo** | LCP: 2,1 s | Puntuación PageSpeed: 74/100 |

La [velocidad de página](/glossary/page-speed) es el concepto amplio. Los Core Web Vitals son las métricas concretas que Google realmente usa.

## Buenas prácticas para Core Web Vitals

- **Comprime y dimensiona correctamente todas las imágenes**. Usa formatos WebP o AVIF, y siempre define atributos width y height explícitos para evitar el layout shift
- **Minimiza los scripts de terceros**. Cada script externo (chat, analítica, trackers) suma al INP. Audita sin piedad y elimina lo que no necesites.
- **Usa una CDN para los recursos estáticos**. Servir imágenes y CSS desde servidores edge cercanos a tus visitantes reduce el LCP drásticamente
- **Aplaza el JavaScript no crítico**. Carga primero el contenido above-the-fold; deja que los scripts secundarios se carguen una vez la página sea interactiva
- **Monitoriza los datos de campo cada mes en Google Search Console**. Las puntuaciones de laboratorio fluctúan, pero los datos de campo muestran si los visitantes reales están teniendo una buena experiencia. Servicios como theStacc publican automáticamente contenido que sigue buenas prácticas de HTML limpio, reduciendo problemas de CWV desde el principio.

## Preguntas frecuentes

### ¿Son los Core Web Vitals un factor de ranking?

Google confirmó los Core Web Vitals como señal de ranking en junio de 2021. Forman parte del sistema de page experience. El impacto es real pero secundario respecto a la relevancia del contenido y los [backlinks](/glossary/backlinks). Más desempate que decisivo.

### ¿Qué reemplazó a First Input Delay?

Interaction to Next Paint (INP) reemplazó oficialmente a FID como Core Web Vital en marzo de 2024. INP mide la capacidad de respuesta a lo largo de todas las interacciones de una visita, no solo el primer clic.

### ¿Cómo compruebo mis Core Web Vitals?

Usa el informe de Core Web Vitals de Google Search Console para datos de campo. PageSpeed Insights te da datos de campo y de laboratorio para cualquier URL. Chrome DevTools y Lighthouse funcionan para pruebas locales durante el desarrollo.

### ¿Qué es una buena puntuación de LCP?

Google considera "buena" una LCP por debajo de 2,5 segundos, "necesita mejora" entre 2,5 y 4 segundos, y "deficiente" por encima de 4 segundos. La mayoría de sitios sufre con la LCP por imágenes sin optimizar y respuestas lentas del servidor.

---

¿Quieres que tu contenido cargue rápido y posicione bien sin gestionar detalles técnicos? theStacc publica 30 artículos optimizados para SEO en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google: Web Vitals](https://web.dev/vitals/)
- [Google Search Central: Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev: Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs: Core Web Vitals y SEO](https://ahrefs.com/blog/core-web-vitals/)
