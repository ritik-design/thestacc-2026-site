---
title: "Cómo auditar la legibilidad de tu web para agentes de IA"
description: "Una auditoría en 7 pasos para que agentes de IA como ChatGPT, Perplexity y Gemini puedan leer tu web. Cubre robots.txt, llms.txt, schema y más. Abril 2026."
slug: "ai-agent-readability-audit"
keyword: "auditoría de legibilidad para agentes de IA"
author: "Siddharth Gangal"
date: "2026-04-02"
category: "SEO Tips"
image: "/blogs-preview-images/ai-agent-readability-audit.png"
---

Tu web se ve genial para los humanos. Pero los agentes de IA no pueden leer la mayor parte.

Una auditoría de legibilidad para agentes de IA comprueba si sistemas como ChatGPT, Perplexity, Gemini y Claude pueden acceder, analizar y citar tu contenido. Según un [estudio de 1.500 sitios web de Website AI Score](https://websiteaiscore.com/blog/case-study-1500-websites-ai-readability-audit), el 18,9 % de los sitios auditados eran completamente inaccesibles para los agentes de IA. Otro 30 % bloqueaba activamente a los rastreadores de IA sin saberlo.

Eso importa porque más del 60 % de las interacciones de investigación B2B ahora implican agentes de IA. Si tu sitio es invisible para ellos, pierdes tráfico que ni siquiera sabías que existía.

Hemos publicado más de 3.500 blogs en más de 70 sectores y hemos optimizado cada uno tanto para la búsqueda tradicional como para la legibilidad de IA. Esta guía recorre el proceso de auditoría exacto que utilizamos.

Esto es lo que aprenderás:

- Cómo comprobar si los rastreadores de IA pueden acceder a tu sitio
- Cómo desplegar un archivo `llms.txt` que guíe a los agentes de IA
- Cómo corregir la jerarquía de encabezados y los problemas de HTML semántico
- Cómo validar los datos estructurados para el análisis de IA
- Cómo probar el renderizado de JavaScript para los bots de IA
- Cómo estructurar el contenido para que los agentes de IA lo citen
- Cómo monitorizar la visibilidad en IA a lo largo del tiempo

**Tiempo necesario:** de 2 a 3 horas  
**Dificultad:** intermedio  
**Qué necesitarás:** acceso al servidor o panel de alojamiento de tu sitio, Google Search Console, un editor de texto

---

## Paso 1: audita tu `robots.txt` para el acceso de rastreadores de IA

La mayoría de los sitios web bloquean a los agentes de IA sin darse cuenta. Tu [archivo robots.txt](/blog/optimize-robots-txt) es lo primero que comprueba cualquier rastreador. Si bloquea a los bots de IA, nada más de esta auditoría importa.

### Qué comprobar

Abre tu archivo `robots.txt` en `tudominio.com/robots.txt`. Busca estos user agents:

| Rastreador de IA | Sirve para | Qué hace |
|---|---|---|
| `GPTBot` | ChatGPT | Entrena y potencia la búsqueda web de ChatGPT |
| `OAI-SearchBot` | ChatGPT Search | Recupera contenido para la búsqueda en tiempo real |
| `ChatGPT-User` | ChatGPT Browse | Obtiene páginas cuando los usuarios comparten URL |
| `ClaudeBot` | Claude | Entrena y recupera información para Anthropic |
| `PerplexityBot` | Perplexity | Potencia los resultados de búsqueda de Perplexity AI |
| `Google-Extended` | Gemini | Entrena los modelos de IA de Google |
| `CCBot` | Common Crawl | Alimenta conjuntos de datos abiertos utilizados por varios modelos de IA |

### Cómo corregirlo

Si alguno de estos agentes aparece en una directiva `Disallow`, estás bloqueando el tráfico de IA. Actualiza tu `robots.txt` para permitirlos explícitamente:

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

Puedes bloquear selectivamente directorios específicos (como `/admin/` o `/staging/`) mientras permites el acceso de IA a tu contenido público.

**Por qué importa este paso:** bloquear rastreadores de IA es la razón más común por la que los sitios web no reciben tráfico de búsqueda con IA. El 30 % de los sitios lo hace accidentalmente mediante reglas de robots.txt demasiado restrictivas.

**Consejo profesional:** utiliza el [comprobador de acceso de rastreadores de IA de MRS Digital](https://mrs.digital/tools/ai-crawler-access-checker/) para ver al instante qué bots de IA pueden llegar a tu sitio.

---

## Paso 2: despliega y configura tu archivo `llms.txt`

`robots.txt` dice a los agentes de IA dónde pueden ir. `llms.txt` les dice qué deben leer. Es un nuevo estándar que actúa como un directorio legible por máquinas de tu contenido más importante.

### Qué hace `llms.txt`

El archivo se sitúa en la raíz de tu dominio (`tudominio.com/llms.txt`) y proporciona un resumen estructurado en markdown de tu sitio. Los agentes de IA lo utilizan para comprender el propósito de tu sitio, navegar hasta las páginas clave y priorizar qué contenido procesar.

### Cómo crearlo

Crea un archivo llamado `llms.txt` en la raíz de tu dominio con esta estructura:

```markdown
## Nombre de tu empresa

> Descripción de una línea sobre lo que hace tu empresa.

## Páginas principales

- [Inicio](https://tudominio.com): Breve descripción
- [Nosotros](https://tudominio.com/about): Breve descripción
- [Precios](https://tudominio.com/pricing): Breve descripción
- [Blog](https://tudominio.com/blog): Breve descripción

## Contenido clave

- [Guía del tema](https://tudominio.com/blog/topic-guide): Descripción
- [Visión general del producto](https://tudominio.com/product): Descripción
```

Para profundizar en este estándar, lee nuestra [guía de llms.txt](/blog/llms-txt-guide).

### Avanzado: crea un espejo en markdown

Algunos equipos van más allá y crean versiones en markdown de las páginas clave. Cloudflare ofrece una función de "Markdown for Agents" que sirve automáticamente markdown cuando un agente de IA lo solicita mediante la cabecera HTTP `Accept: text/markdown`.

Si tu sitio funciona con un generador de sitios estáticos como Astro o Next.js, también puedes publicar versiones `.md` de cada página junto con el HTML. Añade una etiqueta `<link rel="alternate" type="text/markdown">` a tu HTML para que los agentes de IA descubran la versión markdown automáticamente.

Los espejos en markdown eliminan todo el ruido HTML. Los agentes de IA analizan texto limpio más rápido y extraen pasajes citables con mayor precisión.

### Lista de verificación de validación

- [ ] El archivo es accesible en `/llms.txt`
- [ ] Utiliza formato markdown
- [ ] Enumera de 10 a 20 de tus páginas más importantes
- [ ] Cada enlace incluye una breve descripción
- [ ] El archivo no supera los 10.000 tokens (los modelos de IA tienen límites de contexto)

**Por qué importa este paso:** los agentes de IA sin un archivo `llms.txt` deben rastrear todo tu sitio para encontrar páginas relevantes. Con el archivo, van directamente a tu mejor contenido. Un descubrimiento más rápido significa una mayor probabilidad de citación.

---

## Paso 3: corrige la jerarquía de encabezados y el HTML semántico

Los agentes de IA no ven tu sitio web como los humanos. No ven colores, fuentes ni diseños. Leen HTML en bruto. Si tu estructura HTML es desordenada, los agentes de IA malinterpretan tu contenido.

### Problemas comunes

El estudio de Website AI Score encontró que el 60 % de los sitios omite niveles de encabezado. Saltan de `<h1>` a `<h4>` solo para hacer el texto más pequeño. Los agentes de IA interpretan esto como una estructura de documento rota y pueden omitir el contenido por completo.

### Qué auditar

Comprueba cada página en busca de estos problemas:

| Elemento | Uso correcto | Error común |
|---|---|---|
| `<h1>` | 1 por página, el título de la página | Varios H1 o ningún H1 |
| `<h2>` | Encabezados de secciones principales | Saltar a H3 o H4 |
| `<h3>` | Subsecciones bajo un H2 | Usar solo para estilos |
| `<header>` | Área de encabezado de la página | Ausente por completo |
| `<main>` | Bloque de contenido principal | Todo el contenido en `<div>` genéricos |
| `<article>` | Contenido de blog o artículo | No se utiliza |
| `<nav>` | Secciones de navegación | Usar `<div>` en su lugar |

### Cómo corregirlo

Sustituye las decisiones de encabezado basadas en estilos por una jerarquía adecuada. Utiliza CSS para el tamaño visual. Utiliza etiquetas HTML para la estructura del documento.

Envuelve tu contenido principal en etiquetas `<main>` y `<article>`. Los agentes de IA utilizan estos elementos semánticos para identificar el contenido principal y omitir la navegación, las barras laterales y los pies de página.

Añade contenedores `<section>` alrededor de cada bloque de contenido principal. Cada sección debe contener un H2 y su contenido asociado. Esto refleja cómo los agentes de IA segmentan las páginas en temas discretos para la citación.

Comprueba tu ratio de texto a HTML. La [especificación de legibilidad para agentes de Vercel](https://vercel.com/kb/guide/agent-readability-spec) recomienda un ratio mínimo del 15 %. Las páginas con muchos scripts, estilos y divs pero poco contenido real obtienen puntuaciones bajas con los agentes de IA.

Verifica que cada página utilice `<link rel="canonical">` correctamente. Los agentes de IA utilizan las URL canónicas para evitar procesar contenido duplicado. Los canónicos ausentes o incorrectos desperdician el presupuesto de rastreo y confunden la resolución de entidades.

**Por qué importa este paso:** los agentes de IA utilizan la jerarquía de encabezados para comprender la estructura temática. Una jerarquía rota significa que el agente no puede determinar qué secciones responden a qué consultas. Tu contenido se vuelve incitable.

**Consejo profesional:** pasa tu página por el [servicio de validación de marcado del W3C](https://validator.w3.org/). Detecta errores de HTML semántico con los que los rastreadores de IA tendrán dificultades.

> **Tu equipo de SEO. 99 $ al mes.** Stacc publica 30 artículos al mes con la estructura semántica correcta incluida de serie.
> [Empieza por 1 $ →](/pricing)

---

## Paso 4: valida tus datos estructurados y el marcado schema

El [marcado schema](/blog/schema-markup-for-blog-posts) es la forma de decirle exactamente a los agentes de IA qué representa tu contenido. Sin él, los agentes de IA tienen que adivinar. Con él, lo saben.

### Tipos de schema prioritarios

No todos los tipos de schema tienen la misma importancia para la legibilidad de IA. Céntrate en estos:

| Tipo de schema | Cuándo usarlo | Por qué les importa a los agentes de IA |
|---|---|---|
| `Article` | Entradas de blog y páginas de noticias | Identifica el tipo de contenido, autor y fechas |
| `FAQPage` | Secciones de preguntas frecuentes en cualquier página | Los agentes de IA extraen pares de pregunta-respuesta directamente |
| `Organization` | Página de inicio y página de nosotros | Establece la identidad de la entidad |
| `BreadcrumbList` | Cada página | Muestra la jerarquía del sitio |
| `Product` | Páginas de producto y precios | Permite citaciones de comparación de productos |
| `HowTo` | Guías paso a paso como esta | Permite la extracción de pasos |

### Qué auditar

Utiliza la [Prueba de resultados enriquecidos de Google](https://search.google.com/test/rich-results) para comprobar cada página:

- [ ] Bloque de script JSON-LD presente en `<head>`
- [ ] El tipo de schema coincide con el contenido de la página
- [ ] Campos obligatorios completados (título, descripción, dateModified, autor)
- [ ] Sin errores ni advertencias de validación
- [ ] BreadcrumbList presente en cada página
- [ ] El schema de preguntas frecuentes coincide con el contenido visible de las FAQ

### Cómo corregirlo

Añade schema JSON-LD al `<head>` de cada página. Este es el mínimo para una entrada de blog:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Título de tu página",
  "description": "Tu meta descripción",
  "dateModified": "2026-04-02",
  "author": {
    "@type": "Organization",
    "name": "Tu empresa"
  }
}
```

Para una guía detallada paso a paso, consulta nuestra [guía de SEO con marcado schema](/blog/schema-markup-seo-guide).

**Por qué importa este paso:** los datos estructurados transforman tu contenido de "texto que una máquina tiene que interpretar" a "datos que una máquina ya comprende". Los agentes de IA priorizan las páginas ricas en schema a la hora de construir respuestas.

---

## Paso 5: prueba el renderizado de JavaScript para los rastreadores de IA

La mayoría de los rastreadores de IA no ejecutan JavaScript. Si tu sitio depende del renderizado del lado del cliente para mostrar contenido, los agentes de IA ven una página vacía.

### El problema del renderizado

Los sitios web modernos construidos con React, Vue, Angular o Next.js (en modo SPA) a menudo cargan contenido mediante JavaScript después de que el HTML inicial se carga. Googlebot espera y renderiza JavaScript. Los rastreadores de IA como GPTBot y ClaudeBot normalmente no lo hacen.

### Cómo probarlo

1. Abre tu sitio en Chrome
2. Haz clic derecho y selecciona "Ver código fuente de la página"
3. Busca el texto de tu contenido principal en el HTML en bruto

Si tu contenido no aparece en el código fuente de la página, los rastreadores de IA no pueden verlo. Solo leen la respuesta HTML inicial.

### Cómo corregirlo

| Solución | Cuándo usarla |
|---|---|
| Renderizado del lado del servidor (SSR) | Mejor para sitios dinámicos (Next.js, Nuxt, Astro) |
| Generación de sitios estáticos (SSG) | Mejor para blogs y sitios de contenido |
| Prerenderizado | Solución alternativa para marcos SPA |
| Reservas `<noscript>` | Solución mínima viable para contenido crítico |

La solución más sencilla: utiliza SSR o SSG para todas las páginas de contenido. Los sitios de marketing, blogs y páginas de producto siempre deben entregar el contenido en la respuesta HTML inicial.

**Por qué importa este paso:** los rastreadores de IA operan con tiempos de espera de 1 a 5 segundos. Si tu contenido requiere una ejecución de JavaScript que tarda más, el rastreador pasa de largo. Tu contenido nunca entra en el conocimiento del modelo de IA.

**Consejo profesional:** prueba con `curl` desde tu terminal. Ejecuta `curl -s https://tusitio.com/pagina | grep "tu titular principal"`. Si no devuelve nada, los rastreadores de IA no pueden ver tu contenido.

---

## Paso 6: estructura el contenido para la citación por IA

Hacer que el contenido sea accesible es la mitad de la batalla. La otra mitad es estructurarlo para que los agentes de IA realmente lo citen. Esto se conecta directamente con la [optimización para motores generativos](/blog/generative-engine-optimization-guide).

### Qué buscan los agentes de IA al citar

Los agentes de IA prefieren contenido que:

- Responde preguntas en 2 a 4 oraciones (la longitud ideal de citación)
- Incluye números, estadísticas y datos específicos
- Utiliza definiciones claras con el término y la explicación en la misma oración
- Proporciona tablas de comparación con datos estructurados
- Contiene secciones de preguntas frecuentes con pares independientes de pregunta-respuesta

### Lista de verificación de contenido listo para citar

Ejecuta esta lista de verificación en tus 20 páginas principales:

- [ ] Cada sección H2 contiene al menos 1 declaración clara y citable
- [ ] Las estadísticas incluyen el nombre de la fuente y el año
- [ ] Las definiciones siguen el patrón: "[Término] es [definición]"
- [ ] Las tablas de comparación tienen filas de encabezado con etiquetas de columna claras
- [ ] Las respuestas de las FAQ funcionan como pasajes independientes (sin referencias del tipo "como se mencionó anteriormente")
- [ ] Las listas utilizan el marcado de lista HTML correcto (`<ul>`, `<ol>`), no solo guiones en el texto
- [ ] Cada página tiene al menos 1 dato único que no se encuentra en las páginas de la competencia

### Ejemplo: antes y después

**Antes (difícil de citar por IA):**
"Hay muchos beneficios en optimizar tu sitio para los motores de búsqueda y los resultados pueden variar."

**Después (fácil de citar por IA):**
"Los sitios que optimizan la legibilidad para IA obtienen un 39 % más de citaciones en los resultados de búsqueda con IA, según el [informe de señales de confianza en IA de 2026 de Semrush](https://www.semrush.com/blog/ai-search-trust-signals/)."

La segunda versión le da al agente de IA un hecho específico, un número y una fuente. Eso es lo que se cita.

**Por qué importa este paso:** la accesibilidad sin citabilidad es un esfuerzo desperdiciado. Tu contenido puede ser perfectamente rastreable y aun así no aparecer nunca en las respuestas de IA si no está estructurado para la extracción.

> **Más de 3.500 blogs publicados. Puntuación SEO media del 92 %.** Cada artículo que publica Stacc está estructurado para la citación por IA.
> [Empieza por 1 $ →](/pricing)

---

## Paso 7: configura el monitorizado de visibilidad en IA

Una auditoría es una instantánea. El monitorizado convierte esa instantánea en un sistema continuo.

### Qué seguir

| Métrica | Herramienta | Frecuencia |
|---|---|---|
| Registros de acceso de rastreadores de IA | Registros del servidor o análisis de Cloudflare | Semanal |
| Tráfico de referencia de búsqueda con IA | [Google Analytics](/blog/google-analytics-4-setup) + parámetros UTM | Semanal |
| Seguimiento de citaciones en IA | Comprobaciones manuales en ChatGPT, Perplexity, Gemini | Mensual |
| Validación de schema | Prueba de resultados enriquecidos de Google | Mensual |
| Estado de renderizado de páginas | Pruebas `curl` en páginas clave | Mensual |

### Cómo configurar GA4 para el tráfico de IA

Crea un informe personalizado en GA4 que filtre el tráfico por fuentes de referencia de IA:

- `chat.openai.com` (ChatGPT)
- `perplexity.ai` (Perplexity)
- `gemini.google.com` (Gemini)
- `claude.ai` (Claude)

Para una configuración completa de seguimiento, consulta nuestra [guía de seguimiento de visibilidad en búsqueda con IA](/blog/track-ai-search-visibility).

### Ritmo de auditoría mensual

Realiza una comprobación rápida cada mes:

- [ ] `robots.txt` sigue permitiendo rastreadores de IA (las actualizaciones del CMS pueden restablecerlo)
- [ ] `llms.txt` refleja la estructura actual del sitio
- [ ] No hay páginas nuevas sin marcado schema
- [ ] Los Core Web Vitals siguen dentro del rango aceptable
- [ ] El tráfico de referencia de IA tiene tendencia ascendente o estable

**Por qué importa este paso:** los rastreadores de IA actualizan sus índices regularmente. Un cambio de configuración, una actualización del CMS o un despliegue de nueva página puede romper el acceso de IA sin avisar. El monitorizado mensual detecta problemas antes de que cuesten tráfico.

---

## Resultados: qué esperar

Después de completar los 7 pasos, deberías esperar:

- **Inmediato (día 1):** los rastreadores de IA pueden acceder a tu sitio completo. `robots.txt` y `llms.txt` están en su lugar.
- **En 2 a 4 semanas:** los motores de búsqueda con IA vuelven a rastrear e indexar tu contenido estructurado. El marcado schema aparece en las herramientas de validación.
- **En 60 a 90 días:** aumento medible del tráfico de referencia de IA. Tu contenido comienza a aparecer en las respuestas de ChatGPT, Perplexity y Gemini.

El calendario depende de la autoridad de tu dominio y la calidad de tu contenido. Los sitios con un rendimiento SEO existente sólido ven ganancias de visibilidad en IA más rápido. Los sitios que parten de cero deben combinar esta auditoría con una [publicación de contenido SEO](/blog/seo-content-writing) constante para obtener los mejores resultados.

Una cosa que conviene saber: la visibilidad en búsqueda con IA se acumula. Cada página que supera la auditoría de legibilidad se convierte en una fuente de citación potencial. 30 páginas optimizadas dan a los agentes de IA 30 oportunidades de citarte. 180 páginas les dan 180 oportunidades. El volumen importa tanto como la calidad individual de cada página.

![Lista de verificación de auditoría de legibilidad para agentes de IA en 7 pasos](/images/blog/ai-readability-audit-checklist.webp)

---

## Resolución de problemas

**Problema:** los rastreadores de IA aparecen en los registros del servidor pero tu contenido no aparece en las respuestas de IA.
**Solución:** comprueba la estructura de tu contenido (Paso 6). La accesibilidad no garantiza la citación. Reestructura las páginas principales con declaraciones citables, datos específicos y secciones de preguntas frecuentes.

**Problema:** los cambios en `robots.txt` se revierten después de las actualizaciones del CMS.
**Solución:** muchas plataformas de CMS regeneran `robots.txt` al actualizarse. Utiliza una sobrescritura de archivo estático o un plugin que bloquee tus reglas personalizadas en su lugar.

**Problema:** la validación de schema pasa pero los [rich results](/glossary/rich-results) no aparecen.
**Solución:** la implementación de schema y la visualización de rich results son cosas separadas. Google muestra rich results en función de la elegibilidad, no solo del marcado válido. Asegúrate de que tu contenido cumpla los umbrales de calidad y siga las [directrices E-E-A-T](/blog/eeat-google-quality-guide).

---

## Preguntas frecuentes

**¿Qué es una auditoría de legibilidad para agentes de IA?**

Una auditoría de legibilidad para agentes de IA comprueba si sistemas como ChatGPT, Perplexity y Gemini pueden acceder, analizar y citar el contenido de tu sitio web. Cubre el acceso de rastreadores, HTML semántico, datos estructurados, renderizado de JavaScript, estructura de contenido y monitorizado continuo.

**¿Cómo sé si los rastreadores de IA pueden acceder a mi sitio?**

Comprueba tu archivo `robots.txt` en busca de directivas `Disallow` dirigidas a GPTBot, ClaudeBot o PerplexityBot. Utiliza una herramienta como el comprobador de acceso de rastreadores de IA de MRS Digital para probar el acceso de cada rastreador de IA principal al instante.

**¿Qué es un archivo `llms.txt`?**

Un archivo `llms.txt` es un documento markdown situado en la raíz de tu dominio que actúa como un directorio para agentes de IA. Enumera tus páginas más importantes con descripciones para que los agentes de IA puedan encontrar y priorizar tu mejor contenido sin rastrear todo tu sitio.

**¿Ayudan los datos estructurados con la visibilidad en búsqueda con IA?**

Sí. El marcado schema proporciona a los agentes de IA contexto legible por máquinas sobre tu contenido. Los esquemas Article, FAQ, Organization y BreadcrumbList son los de mayor prioridad para la legibilidad de IA. Las páginas con marcado schema válido reciben más citaciones de IA que las páginas sin él.

**¿Cuánto tiempo lleva una auditoría de legibilidad para agentes de IA?**

La auditoría completa en 7 pasos lleva de 2 a 3 horas para un sitio web empresarial típico. Las comprobaciones de mantenimiento mensuales llevan de 30 a 45 minutos. La auditoría inicial produce las mayores ganancias. El monitorizado continuo previene regresiones.

**¿Puede Stacc ayudar con la legibilidad para agentes de IA?**

Cada artículo que publica Stacc incluye HTML semántico correcto, [marcado schema](/blog/schema-markup-seo-guide), jerarquía de encabezados limpia y contenido estructurado para la citación por IA. Stacc se encarga de los detalles técnicos automáticamente en los más de 30 artículos mensuales.

---

La legibilidad para agentes de IA ya no es opcional. Los sitios que superen esta auditoría hoy capturarán el tráfico de búsqueda con IA mañana. Los sitios que la ignoren verán cómo la competencia aparece en las respuestas de IA mientras ellos permanecen invisibles.

Ejecuta la auditoría. Corrige lo que esté roto. Monitoriza mensualmente. Deja que los resultados se acumulen.

> **Posiciónate en todas partes. Sin esfuerzo.** Blog SEO, SEO local y Social en piloto automático. Cada artículo optimizado para la legibilidad de IA.
> [Empieza por 1 $ →](/pricing)

## Herramientas y recursos relacionados

**Herramientas de SEO gratuitas:**
- [Auditoría SEO gratuita](/tools/seo-audit/)
- [Detector de contenido de IA](/tools/ai-content-detector/)

**Mejores listas:**
- [Mejores herramientas de SEO con IA](/best/ai-seo-tools/)
- [Mejores herramientas de escritura con IA para SEO](/best/ai-content-writing-tools-for-seo/)
