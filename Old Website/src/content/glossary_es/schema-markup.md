---
term: "Schema Markup"
slug: "schema-markup"
definition: "Schema Markup es código estandarizado (normalmente JSON-LD) que añades a tus páginas para que los buscadores entiendan tu contenido y muestren resultados enriquecidos."
category: "SEO"
difficulty: "Intermediate"
keyword: "qué es schema markup"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "rich-results"
  - "serp"
  - "technical-seo"
  - "json-ld"
  - "e-e-a-t"
---

## ¿Qué es Schema Markup?

**Schema Markup es un vocabulario de datos estructurados que añades a tu HTML para decirle a los buscadores exactamente qué representa tu contenido: un producto, una receta, un evento, un negocio, una FAQ.**

Sin schema, Google tiene que adivinar de qué trata tu página. Con schema, le entregas un diagrama etiquetado. El marcado sigue el estándar Schema.org, mantenido conjuntamente por Google, Microsoft, Yahoo y Yandex.

Un estudio de Milestone Research encontró que las páginas con schema markup posicionan, de media, 4 posiciones más arriba que las que no lo usan. No porque schema sea un factor de ranking directo. Google ha dicho que no lo es. Pero los [resultados enriquecidos](/glossary/rich-results) que genera schema disparan la tasa de clics, y un mejor CTR sí termina influyendo en los rankings con el tiempo.

## ¿Por qué importan los datos estructurados?

La mayoría de los sitios todavía no usan schema. Una oportunidad para cualquier empresa dispuesta a invertir 30 minutos en implementarlo.

- **Resultados enriquecidos en búsquedas**. Estrellas de valoración, desplegables FAQ, rangos de precios y fechas de eventos aparecen directamente en la [SERP](/glossary/serp). Estos elementos visuales pueden subir el CTR entre un 20 y un 30 %.
- **Mejor visibilidad en IA**. Las AI Overviews de Google y otras experiencias impulsadas por IA tiran de datos estructurados. Schema hace que tu contenido sea más fácil de citar para las máquinas.
- **Mayor presencia local** – el [schema LocalBusiness](/glossary/localbusiness-schema) envía horarios, dirección y reseñas directamente a los paneles de conocimiento de Google y al [local pack](/glossary/local-pack).
- **Listo para búsqueda por voz**. Cuando alguien le pregunta algo a un asistente de voz, los datos estructurados ayudan a que tu respuesta aparezca primero. FAQ y How-To schema brillan especialmente aquí.

Si estás invirtiendo en contenido [SEO](/glossary/seo) sin añadir schema, estás dejando visibilidad sobre la mesa.

## Cómo funciona Schema Markup

Schema vive en el HTML de tu página. Los rastreadores lo leen, lo validan y lo usan para generar resultados de búsqueda mejorados.

### El formato del código

Existen tres formatos: JSON-LD, Microdata y RDFa. Google recomienda JSON-LD. Es un bloque de script que colocas en la sección `<head>`. No se mezcla con tu HTML visible, lo que lo hace más fácil de mantener y menos propenso a romper el diseño.

### El proceso de validación

Tras añadir schema, el informe de Resultados Enriquecidos de Google Search Console te muestra si tu marcado es válido. Los errores —campos requeridos faltantes, tipos incorrectos— impiden que aparezcan los resultados enriquecidos. La herramienta Rich Results Test de Google te permite revisar URLs individuales antes de desplegar en todo el sitio.

### Cómo lo procesa Google

Googlebot rastrea tu página, parsea el JSON-LD y lo coteja contra los tipos de schema conocidos. Si todo cuadra y la página cumple las directrices de calidad, el listado mejorado aparece en búsqueda en cuestión de días o semanas. No todo schema válido genera un resultado enriquecido. Google decide según el contexto de la consulta y la calidad de la página.

## Tipos de Schema Markup

Schema.org lista más de 800 tipos. Pero para la mayoría de los negocios, un puñado cubre el 90 % de los casos:

- **Article schema**. Le dice a Google que esta página es un post de blog o un artículo de noticias. Ayuda con Google Discover y los carruseles de noticias.
- **FAQ schema**. Añade pares pregunta-respuesta desplegables directamente en tu listado. Alto impacto en consultas informacionales.
- **LocalBusiness schema**. Envía nombre, dirección, horario y reseñas a Google. Imprescindible para [SEO local](/glossary/local-seo).
- **Product schema**. Muestra precio, disponibilidad y valoraciones en búsqueda. Crítico para eCommerce.
- **How-To schema**. Despliega instrucciones paso a paso con imágenes en los resultados. Funciona muy bien para contenido tutorial.
- **Review/Rating schema**. Esas estrellas amarillas que ves en los resultados. Suben el CTR de forma notable.

El schema correcto depende del tipo de página. La página de servicios de un fontanero necesita LocalBusiness. Un post de blog necesita Article y posiblemente FAQ.

## Ejemplos de Schema Markup

**Ejemplo 1: Clínica dental con FAQ schema**
Una dentista en Madrid añade FAQ schema a su página de servicio "Blanqueamiento dental" con 5 preguntas habituales de pacientes. Su listado en búsqueda ahora muestra Q&A desplegables, ocupando 3 veces el espacio visual de la competencia. Los clics a esa página suben un 35 % en 2 meses.

**Ejemplo 2: Empresa de climatización con LocalBusiness schema**
Una empresa de aire acondicionado añade LocalBusiness schema con área de servicio, horario y valoración agregada (4,8 estrellas con más de 200 reseñas). Google muestra la valoración con estrellas directamente en los resultados orgánicos —no solo en el map pack. La empresa nota un aumento claro en llamadas desde búsqueda orgánica.

**Ejemplo 3: Blog de SaaS con Article schema**
Una empresa de software B2B publica guías how-to cada semana. Tras añadir Article schema con información de autor y fechas de publicación, sus posts empiezan a aparecer en Google Discover. Solo el tráfico de Discover suma un 15 % a las visitas orgánicas mensuales.

## Schema Markup vs. Rich Snippets

La gente usa estos términos como si fueran lo mismo. No lo son.

| | Schema Markup | Rich Snippets / Resultados Enriquecidos |
|---|---|---|
| **Qué es** | Código que añades a tus páginas | Listados mejorados que muestra Google |
| **Quién lo controla** | Tú (el webmaster) | Google (decide si los muestra) |
| **¿Garantizado?** | Siempre puedes añadir el marcado | Google puede mostrarlos o no |
| **Propósito** | Comunicar el significado de la página a los rastreadores | Mejorar la apariencia visual en las [SERPs](/glossary/serp) |
| **Ejemplo** | Script JSON-LD en tu HTML | Estrellas de valoración bajo tu listado |

Schema markup es el input. Los resultados enriquecidos son el (posible) output. Añadir marcado no garantiza listados mejorados. Pero sin él, nunca los conseguirás.

## Buenas prácticas de Schema Markup

- **Empieza por lo más importante**. No intentes añadir todos los tipos de schema a la vez. Si eres un negocio local, empieza con LocalBusiness y FAQ. Suma más con el tiempo.
- **Usa JSON-LD, no Microdata**. Google lo prefiere. Es más fácil de implementar, más fácil de depurar y no ensucia tu HTML.
- **Valida cada página**. Pasa el schema nuevo por el Rich Results Test de Google antes de publicar. Un campo faltante puede invalidar el bloque entero.
- **Mantén el schema preciso**. Si cambias horarios, actualiza el schema. Datos estructurados inexactos violan las directrices de Google y pueden hacer que te retiren los resultados enriquecidos.
- **Combina schema con contenido de calidad**. Schema sobre páginas pobres no genera resultados enriquecidos. Servicios como theStacc publican 30 artículos optimizados al mes. Cada uno es una oportunidad para añadir Article y FAQ schema que sí merezca rich results.

## Preguntas frecuentes

### ¿Schema markup es un factor de ranking?

Google dice que schema no es un factor de ranking directo. Pero las páginas con schema obtienen [resultados enriquecidos](/glossary/rich-results), que mejoran el CTR. Un mejor CTR envía señales positivas de engagement, que pueden mejorar los rankings de forma indirecta.

### ¿Cómo añado schema a mi sitio web?

El método más sencillo es JSON-LD: un bloque de script en la sección `<head>` de tu página. Plugins de WordPress como Yoast y RankMath lo generan automáticamente. Para sitios a medida, usa el Structured Data Markup Helper de Google.

### ¿Funciona schema para pequeñas empresas?

Por completo. Los negocios locales suelen ver el mayor impacto porque LocalBusiness y FAQ schema están infrautilizados por sus competidores pequeños. Añadir schema básico a un sitio local de 10 páginas lleva menos de una hora.

### ¿Cuánto tarda en aparecer en resultados enriquecidos?

Tras añadir schema válido, Google suele procesarlo en pocos días o hasta 2 semanas. Comprueba el estado en el informe de Resultados Enriquecidos de Google Search Console.

---

¿Quieres tu contenido SEO optimizado y publicado sin mover un dedo? theStacc publica 30 artículos en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Cómo funcionan los datos estructurados](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
- [Milestone Research: Impacto de Schema Markup en los rankings](https://www.milestoneinternet.com/thought-leadership/research/schema-markup-drives-results)
- [Moz: Guía para principiantes sobre datos estructurados](https://moz.com/blog/beginners-guide-to-structured-data)
