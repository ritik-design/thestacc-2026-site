---
title: "Dofollow vs Nofollow (2026): Estrategias, Tácticas y Ejemplos"
description: "Guía dofollow vs nofollow para 2026: estrategias, tácticas, ejemplos reales y pasos de implementación para obtener resultados más rápido."
slug: "dofollow-vs-nofollow"
keyword: "dofollow vs nofollow"
author: "Siddharth Gangal"
date: "2026-03-29"
category: "SEO Tips"
image: "/blogs-preview-images/dofollow-vs-nofollow.webp"
---

Cada enlace de internet pertenece a una de dos categorías. Los enlaces dofollow transmiten autoridad de posicionamiento. Los enlaces nofollow indican a Google que no cuente el enlace como un voto.

Comprender la diferencia entre dofollow vs nofollow determina cómo construyes backlinks, estructuras enlaces internos y auditas tu perfil de enlaces. Si te equivocas, desperdicias meses persiguiendo enlaces que no mueven posiciones. O peor, activas una penalización de Google al construir un perfil de enlaces poco natural.

El 89,4 % de todos los backlinks en los 110 000 sitios web principales son dofollow. El 10,6 % restante son nofollow. Pero un perfil de enlaces saludable necesita ambos tipos. Google espera una mezcla natural.

Hemos publicado más de 3500 artículos de SEO en más de 70 sectores. La estrategia de enlaces forma parte de cada campaña. Esta guía cubre todo lo que necesitas saber sobre los enlaces dofollow y nofollow, incluida la actualización de Google de 2019 que cambió cómo funciona nofollow.

Esto es lo que aprenderás:

- La diferencia exacta entre los enlaces dofollow y nofollow
- Cómo Google cambió nofollow de directriz a "pista" en 2019
- Cuándo usar `rel="nofollow"`, `rel="sponsored"` y `rel="ugc"`
- Cómo comprobar el estado de seguimiento de cualquier enlace en segundos
- La proporción ideal dofollow/nofollow para un perfil natural
- Errores comunes que activan penalizaciones de Google

![Comparación de enlaces dofollow vs nofollow mostrando cómo cada tipo afecta al SEO](/images/blog/dofollow-vs-nofollow-comparison.webp)

---

## ¿Qué son los enlaces Dofollow?

Un enlace dofollow es un enlace HTML estándar que transmite equidad de enlace (también llamada "link juice" o PageRank) de una página a otra. No existe el atributo `rel="dofollow"` en HTML. "Dofollow" es una abreviatura del sector para un enlace sin el atributo nofollow aplicado.

Así es como se ve un enlace dofollow en HTML:

```html
<a href="https://example.com">Texto del ancla</a>
```

No se necesita ningún atributo especial. Todos los enlaces son dofollow por defecto.

Cuando Google rastrea un enlace dofollow, ocurren 3 cosas:

1. Google sigue el enlace hasta la página de destino
2. Google transmite una parte de la autoridad de la página de origen al destino
3. Google utiliza el enlace como señal de posicionamiento para la página de destino

Los enlaces dofollow son la base del algoritmo PageRank original de Google. Cuanto más enlaces dofollow apuntan a una página desde fuentes autorizadas, más alto tiende a posicionarse esa página. [Los sitios web con perfiles de backlink sólidos](https://ahrefs.com/blog/backlink-growth-study/) reciben un 67 % más de tráfico orgánico que los sitios con perfiles débiles.

Por eso la construcción de enlaces sigue siendo una de las partes más importantes (y más difíciles) del SEO. El 41 % de los profesionales del marketing dice que construir [backlinks](/glossary/backlinks) de calidad es la tarea de SEO más difícil a la que se enfrentan.

---

## ¿Qué son los enlaces Nofollow?

Un enlace nofollow incluye el atributo `rel="nofollow"`. Este atributo indica a los motores de búsqueda: "No utilices este enlace como señal de posicionamiento."

Así es como se ve un enlace nofollow en HTML:

```html
<a href="https://example.com" rel="nofollow">Texto del ancla</a>
```

Google introdujo el atributo nofollow en 2005 para combatir el spam en comentarios. Los spammers inundaban los comentarios de blogs y foros con enlaces para mejorar sus posiciones. Nofollow dio a los propietarios de sitios una forma de enlazar sin transmitir autoridad.

### Dónde aparecen naturalmente los enlaces Nofollow

La mayoría de los enlaces en internet son nofollow por defecto en estas plataformas:

- **Redes sociales:** Enlaces de Facebook, X (Twitter), LinkedIn, Instagram, Pinterest y TikTok
- **Foros y comunidades:** Reddit, Quora, Stack Overflow y la mayoría del software de foros
- **Comentarios de blogs:** WordPress y la mayoría de las plataformas CMS aplican automáticamente nofollow a los enlaces de comentarios
- **Wikipedia:** Todos los enlaces externos llevan nofollow
- **Comunicados de prensa:** La mayoría de los servicios de distribución de comunicados de prensa usan nofollow
- **Directorios generados por usuarios:** Yelp, enlaces de Google Business Profile y plataformas de reseñas

Los enlaces nofollow no impulsan directamente los posicionamientos. Pero sirven para otros propósitos. Generan tráfico de referencia, construyen notoriedad de marca y señalan a Google que tu sitio tiene una diversidad natural de enlaces.

---

## Dofollow vs Nofollow: Diferencias clave

La diferencia se reduce a una pregunta: ¿el enlace transmite autoridad de posicionamiento?

| Característica | Dofollow | Nofollow |
|---|---|---|
| Transmite equidad de enlace | Sí | No (pero Google puede anularlo) |
| Atributo HTML | Ninguno (comportamiento por defecto) | `rel="nofollow"` |
| Impacto SEO directo | Sí. Mejora posiciones | Sin impacto directo |
| Tráfico de referencia | Sí | Sí |
| Rastreo de Google | Siempre seguido y rastreado | Puede o no ser rastreado |
| Visibilidad de marca | Sí | Sí |
| Necesidad de perfil natural | 60-80 % del total de enlaces | 20-40 % del total de enlaces |
| Riesgo de sobreoptimización | Alto si es 100 % dofollow | Bajo |

El detalle crítico que la mayoría de guías pasan por alto: desde 2019, Google trata nofollow como una "pista", no como una directriz. Google puede elegir seguir y contar un enlace nofollow si sus algoritmos determinan que el enlace es relevante y fiable. Más sobre esto en la siguiente sección.

> Los enlaces dofollow construyen autoridad de posicionamiento. Los enlaces nofollow construyen un perfil natural. Necesitas ambos.

---

## La actualización de Google de 2019: Nofollow se convirtió en una pista

El 10 de septiembre de 2019, Google publicó una entrada de blog titulada ["Evolving nofollow"](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) que cambió cómo funcionan los enlaces nofollow. Esta actualización es el desarrollo más importante en la atribución de enlaces en más de una década. Muchas guías de SEO siguen equivocándose.

### Qué cambió

**Antes de 2019:** Nofollow era una directriz. Google la obedecía absolutamente. Un enlace nofollow transmitía cero autoridad, cero señales de rastreo y cero beneficio de posicionamiento. Punto.

**Después de 2019:** Nofollow se convirtió en una pista. Google se reserva el derecho de considerar los enlaces nofollow como señales de posicionamiento si sus algoritmos los encuentran relevantes. Google también puede descubrir e indexar nuevas páginas a través de enlaces nofollow.

### Tres nuevos atributos de enlace

Google introdujo 2 nuevos atributos junto a nofollow:

| Atributo | Caso de uso | Ejemplo |
|---|---|---|
| `rel="sponsored"` | Enlaces de pago, anuncios, patrocinios | Enlaces de afiliados, colocaciones de pago, enlaces de banners publicitarios |
| `rel="ugc"` | Contenido generado por usuarios | Comentarios de blogs, publicaciones de foros, envíos de la comunidad |
| `rel="nofollow"` | Señal general de "no respaldo" | Cualquier enlace por el que no quieras avalar |

Puedes combinar atributos: `rel="nofollow sponsored"` o `rel="nofollow ugc"`. Google recomienda usar el atributo más específico disponible.

![Evolución del nofollow de Google de directriz a pista con los nuevos atributos sponsored y ugc](/images/blog/google-nofollow-hint-evolution.webp)

### Qué significa esto en la práctica

**Para los creadores de enlaces:** Los enlaces nofollow de sitios autorizados (Wikipedia, publicaciones principales, Reddit) pueden ahora tener algún valor de posicionamiento. No deberías descartarlos.

**Para los propietarios de sitios:** Usa `rel="sponsored"` en enlaces de pago. Usa `rel="ugc"` en enlaces enviados por usuarios. Usa `rel="nofollow"` en cualquier enlace en el que no confíes o respaldes. Los enlaces nofollow existentes no necesitan cambiarse.

**Para los auditores SEO:** Una [auditoría de backlinks](/blog/backlink-audit-guide) debería ahora analizar los enlaces nofollow de dominios de alta autoridad por separado. Estos pueden contribuir a los posicionamientos incluso sin transmitir la equidad de enlace tradicional.

El 78,8 % de los profesionales de SEO ahora cree que los enlaces nofollow afectan a los posicionamientos en cierta medida. El modelo de "pista" significa que el tratamiento de Google hacia nofollow ya no es binario.

---

> **Deja de escribir. Empieza a posicionar.** Stacc publica 30 artículos de SEO al mes por 99 $. Cada artículo construye tu [autoridad de dominio](/blog/domain-authority-guide) con enlaces internos y externos.
> [Empieza por 1 $ →](/pricing)

---

## Cuándo usar cada tipo de enlace

Saber cuándo aplicar atributos dofollow o nofollow previene penalizaciones y maximiza el valor del enlace.

### Cuándo usar Dofollow (por defecto)

Deja los enlaces como dofollow cuando respaldes genuinamente el destino:

- **Enlaces editoriales en tu propio contenido:** Enlaces a fuentes, referencias y recursos que recomiendas
- **Enlaces internos:** Todos los [enlaces internos](/blog/internal-linking-blog-posts) deberían ser dofollow (con raras excepciones)
- **Enlaces de biografía de autor en posts invitados:** Práctica estándar para contribuciones de invitados legítimas
- **Enlaces de páginas de recursos:** Listas curadas de herramientas, guías o referencias en las que confías
- **Enlaces de socios y proveedores:** Cuando la relación es genuina, no de pago

### Cuándo usar Nofollow

Aplica `rel="nofollow"` cuando no quieras avalar el destino:

- **Contenido no confiable:** Enlaces a sitios que no has verificado personalmente
- **Secciones de comentarios:** Cualquier enlace enviado por usuarios (la mayoría de las plataformas CMS lo gestionan automáticamente)
- **Enlaces de inicio de sesión o registro:** Google no necesita rastrear estas páginas

### Cuándo usar rel="sponsored"

Aplica `rel="sponsored"` en cualquier enlace que implique intercambio monetario:

- **Enlaces de afiliados:** Recomendaciones de productos con parámetros de seguimiento
- **Colocaciones de pago:** Contenido patrocinado, advertoriales, listados de directorios de pago
- **Enlaces de banners publicitarios:** Publicidad display que enlaza a sitios externos
- **Colaboraciones con influencers:** Enlaces de reseñas de productos con compensación involucrada

Google ha declarado explícitamente que no marcar los enlaces de pago con `rel="sponsored"` o `rel="nofollow"` puede resultar en una penalización manual. Esto aplica tanto al sitio que enlaza como al enlazado.

### Cuándo usar rel="ugc"

Aplica `rel="ugc"` en enlaces creados por tus usuarios:

- **Comentarios de blogs:** Comentarios enviados por usuarios con enlaces
- **Publicaciones de foros:** Contenido generado por la comunidad
- **Reseñas de usuarios:** Reseñas de productos o servicios enviadas por clientes
- **Contenido tipo wiki:** Páginas editables por miembros de la comunidad

### Árbol de decisión de referencia rápida

| Escenario de enlace | Atributo a usar |
|---|---|
| Tú lo escribiste y respaldas el destino | Dofollow (sin atributo) |
| El usuario envió el enlace | `rel="ugc"` |
| Hubo intercambio de dinero | `rel="sponsored"` |
| No confías en el destino | `rel="nofollow"` |
| Enlace interno dentro de tu propio sitio | Dofollow (sin atributo) |
| Enlace de afiliado con seguimiento | `rel="sponsored"` |

---

## Cómo comprobar si un enlace es Dofollow o Nofollow

Puedes comprobar el estado de seguimiento de cualquier enlace de 3 formas. Desde la inspección manual hasta herramientas de auditoría masiva.

### Método 1: Inspeccionar elemento (manual)

Haz clic derecho en cualquier enlace de tu navegador y selecciona "Inspeccionar" o "Inspeccionar elemento". Busca la etiqueta `<a>` en el HTML.

**Ejemplo de dofollow:**
```html
<a href="https://example.com">Texto del enlace</a>
```
No hay atributo `rel="nofollow"` presente. El enlace es dofollow.

**Ejemplo de nofollow:**
```html
<a href="https://example.com" rel="nofollow">Texto del enlace</a>
```
El atributo `rel="nofollow"` indica a Google que no transmita autoridad.

Este método funciona para comprobar enlaces individuales. No escala para auditar un sitio completo.

### Método 2: Extensiones de navegador (comprobación rápida)

Instala una extensión de navegador que resalte los tipos de enlace automáticamente:

- **NoFollow** (Chrome): Resalta los enlaces nofollow con un borde punteado rojo
- **SEOquake** (Chrome/Firefox): Muestra el estado de seguimiento en una barra de herramientas superpuesta
- **MozBar** (Chrome): Muestra los atributos de enlace junto con métricas DA/PA

Estas extensiones funcionan en cualquier página web. Son útiles para análisis rápidos de competidores y comprobaciones puntuales de tu propio contenido.

### Método 3: Herramientas de rastreo (auditoría masiva)

Para una auditoría completa del sitio, usa una herramienta de rastreo para analizar todos los enlaces:

- **Screaming Frog:** Rastrea todo tu sitio y exporta todos los enlaces con sus atributos
- **Ahrefs Site Audit:** Identifica tu proporción dofollow/nofollow en todas las páginas
- **Semrush Backlink Audit:** Analiza tu perfil de enlaces entrantes por estado de seguimiento

Una [auditoría SEO](/blog/how-to-do-seo-audit) completa debería incluir un análisis de atributos de enlace. Esto revela si tu perfil parece natural o sobreoptimizado.

---

## Construir un perfil de enlaces natural

Google espera una mezcla natural de enlaces dofollow y nofollow. Un perfil con 100 % de enlaces dofollow señala manipulación. Un perfil con demasiados enlaces nofollow sugiere baja autoridad.

### La proporción ideal

| Tipo de perfil | % Dofollow | % Nofollow | Nivel de riesgo |
|---|---|---|---|
| Natural / Saludable | 60-80 % | 20-40 % | Bajo |
| Ligeramente agresivo | 80-90 % | 10-20 % | Medio |
| Sobreoptimizado | 90-100 % | 0-10 % | Alto |
| Déficit de autoridad | Por debajo del 50 % | Por encima del 50 % | Medio |

La media en los 110 000 sitios web principales es 89,4 % dofollow y 10,6 % nofollow. Pero esta media se inclina hacia arriba porque los grandes sitios de autoridad atraen naturalmente más enlaces editoriales dofollow.

![Proporciones de perfil de enlaces natural mostrando porcentajes dofollow vs nofollow y niveles de riesgo](/images/blog/dofollow-nofollow-link-profile-ratio.webp)

Para pequeñas y medianas empresas, una división 70/30 es un objetivo saludable. Consíguelo construyendo enlaces dofollow de calidad a través de contenido y outreach mientras acumulas naturalmente enlaces nofollow de redes sociales, foros y directorios.

### Cómo construir enlaces Dofollow

Los mejores enlaces dofollow provienen de menciones editoriales. Alguien lee tu contenido, lo encuentra valioso y enlaza a él sin que se lo pidas. Estas son estrategias que generan enlaces dofollow editoriales:

- **Publica investigaciones o datos originales.** Los estudios de datos atraen citaciones. Periodistas y bloggers enlazan a estadísticas originales.
- **Crea guías de alta utilidad.** Las guías paso a paso que resuelven problemas reales ganan enlaces de páginas de recursos.
- **Construye herramientas gratuitas.** Una herramienta gratuita útil gana enlaces naturales de cualquiera que la recomiende. Consulta nuestras [herramientas de SEO](/tools/seo-audit) para ejemplos.
- **Publica como invitado en sitios relevantes.** Escribe para sitios de tu sector. Incluye un enlace dofollow natural en el cuerpo del contenido (no solo en la biografía).
- **Repara enlaces rotos.** Encuentra enlaces salientes rotos en sitios de autoridad y ofrece tu contenido como reemplazo. Esto se llama [construcción de enlaces rotos](/blog/fix-broken-links).
- **Gana menciones en prensa.** Responde a consultas de periodistas en plataformas como HARO, Connectively o Qwoted.

### Cómo ganar enlaces Nofollow naturalmente

Los enlaces nofollow se acumulan a través de la actividad empresarial normal:

- Comparte tu contenido en plataformas de redes sociales (todos los enlaces sociales son nofollow)
- Participa en discusiones relevantes de Reddit y Quora
- Mantén listados de negocios en directorios y plataformas de reseñas
- Anima a las reseñas de clientes que enlacen a tu sitio
- Comenta en blogs del sector con aportes genuinos (no spam)

---

> **Tu equipo de SEO. 99 $ al mes.** 30 artículos optimizados, publicados automáticamente. Cada artículo gana backlinks y construye [autoridad temática](/blog/build-topical-authority) con el tiempo.
> [Empieza por 1 $ →](/pricing)

---

## Errores comunes de Dofollow vs Nofollow

Estos errores cuestan posiciones y a veces activan penalizaciones. Evítalos todos.

**Error 1: Aplicar nofollow a tus propios enlaces internos.**
Los enlaces internos deberían ser casi siempre dofollow. Añadir nofollow a enlaces internos bloquea el flujo de PageRank dentro de tu propio sitio. Esto se llama "esculpir PageRank", y [Google confirmó en 2009](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) que no funciona. El PageRank que habría fluido a través de un enlace interno con nofollow se evapora. No se redistribuye a otros enlaces.

**Error 2: Construir 100 % de enlaces dofollow.**
Un perfil totalmente dofollow parece fabricado. Los algoritmos de Google detectan patrones poco naturales. Un perfil saludable incluye enlaces nofollow de plataformas sociales, directorios y contenido generado por usuarios. Apunta a una proporción 70/30 dofollow/nofollow.

**Error 3: No etiquetar los enlaces de pago como sponsored.**
Google requiere `rel="sponsored"` o `rel="nofollow"` en cualquier enlace que implique pago. No etiquetar los enlaces de pago puede resultar en una acción manual contra ambos sitios. Esto incluye enlaces de afiliados, posts patrocinados y colocaciones de directorios de pago.

**Error 4: Ignorar los enlaces nofollow en tu análisis de backlinks.**
Tras la actualización de 2019, los enlaces nofollow de dominios de alta autoridad pueden tener valor de posicionamiento. Una [auditoría de backlinks](/blog/backlink-audit-guide) completa debería analizar ambos tipos de enlace. Descartar todos los enlaces nofollow pierde señales de posicionamiento potenciales.

**Error 5: Obsesionarse con los atributos de enlace individuales.**
Un enlace dofollow de un sitio spam de baja autoridad hace más daño que bien. Un enlace nofollow del New York Times genera miles de visitantes de referencia. La calidad y relevancia importan más que el estado de seguimiento. Enfócate en ganar enlaces de fuentes relevantes y autorizadas independientemente de su política de nofollow.

**Error 6: Usar nofollow en enlaces editoriales salientes.**
Algunos propietarios de sitios aplican nofollow a todos los enlaces salientes para "acaparar" PageRank. Esto es innecesario y potencialmente perjudicial. Google espera enlaces salientes naturales. Aplicar nofollow a todos los enlaces externos hace que tu contenido parezca sospechoso. Enlaza a fuentes autorizadas con dofollow. No perjudica tus posiciones.

---

## Dofollow vs Nofollow y enlaces internos

Los enlaces internos merecen atención especial. Funcionan de forma diferente a los backlinks externos.

Cada [enlace interno](/blog/internal-linking-blog-posts) de tu sitio debería ser dofollow. Los enlaces internos distribuyen PageRank entre tus páginas. Ayudan a Google a descubrir e indexar nuevo contenido. Señalan qué páginas consideras más importantes.

La única excepción: páginas de inicio de sesión, carritos de compra u otras páginas que no quieres que Google priorice. Pero incluso estas raramente necesitan nofollow. Google gestiona la mayoría de estas a través de `robots.txt` y etiquetas `noindex`.

Una estructura de enlaces internos sólida multiplica el valor de cada backlink dofollow que gana tu sitio. Cuando un enlace dofollow externo apunta a tu página de inicio, los enlaces internos distribuyen esa autoridad a tus posts de blog, páginas de producto y páginas de servicio.

Usa [optimización de texto de ancla](/blog/anchor-text-optimization) para enlaces internos. El texto de ancla descriptivo indica a Google de qué trata la página de destino. Evita frases genéricas como "haz clic aquí" o "lee más".

---

## La distinción entre Nofollow y Noindex

Los principiantes a menudo confunden nofollow con noindex. Sirven para propósitos completamente diferentes.

| Atributo | Qué hace | Alcance |
|---|---|---|
| `rel="nofollow"` | Indica a Google que no transmita autoridad a través de un enlace específico | A nivel de enlace |
| `<meta name="robots" content="noindex">` | Indica a Google que no incluya una página en los resultados de búsqueda | A nivel de página |

Un enlace nofollow sigue permitiendo que Google vea y potencialmente rastree la página de destino. Solo afecta si la autoridad pasa a través de ese enlace específico.

Una etiqueta noindex oculta una página completa de los resultados de búsqueda. La página sigue existiendo y cargando para los visitantes. Pero Google la elimina del índice.

Estos dos atributos resuelven problemas diferentes. Usa nofollow cuando no quieras que un enlace transmita autoridad. Usa noindex cuando no quieras que una página aparezca en los resultados de búsqueda. Pueden usarse juntos en la misma página para un control máximo.

Para más información sobre cómo Google gestiona las directivas de indexación, consulta nuestra [lista de verificación de SEO técnico](/blog/technical-seo-checklist).

---

> **Más de 3500 blogs publicados. 92 % de puntuación SEO media.** Descubre lo que Stacc puede hacer por tu estrategia de construcción de enlaces. Publicamos contenido que gana backlinks.
> [Empieza por 1 $ →](/pricing)

---

## Preguntas frecuentes

**¿Cuál es la diferencia entre los enlaces dofollow y nofollow?**

Un enlace dofollow transmite autoridad de posicionamiento (PageRank) de una página a otra. Un enlace nofollow incluye `rel="nofollow"` que indica a Google que no lo cuente como señal de posicionamiento. Dofollow mejora directamente el SEO. Nofollow genera tráfico y visibilidad de marca sin impacto directo en posiciones.

**¿Los enlaces nofollow ayudan al SEO?**

Los enlaces nofollow no transmiten directamente autoridad de posicionamiento. Pero contribuyen a un perfil de enlaces natural, generan tráfico de referencia y construyen notoriedad de marca. Desde la actualización de Google de 2019, nofollow es una "pista" en lugar de una directriz. Google puede elegir contar algunos enlaces nofollow como señales de posicionamiento. El 78,8 % de los profesionales de SEO cree que los enlaces nofollow afectan aún a los posicionamientos.

**¿Cuál es la proporción ideal de enlaces dofollow a nofollow?**

Un perfil de enlaces saludable contiene entre 60 y 80 % de enlaces dofollow y entre 20 y 40 % de enlaces nofollow. La media en los sitios web principales es 89,4 % dofollow. Para pequeñas y medianas empresas, una división 70/30 señala un perfil natural y orgánico. Un perfil 100 % dofollow parece fabricado y arriesga activar penalizaciones de Google.

**¿Los enlaces de redes sociales son dofollow o nofollow?**

Todas las principales plataformas de redes sociales usan enlaces nofollow. Esto incluye Facebook, X (Twitter), LinkedIn, Instagram, Pinterest y TikTok. Los enlaces de redes sociales no transmiten autoridad de posicionamiento directa. Sí generan tráfico de referencia y contribuyen a tu porcentaje de enlaces nofollow.

**¿Cuál es la diferencia entre nofollow y noindex?**

Nofollow es un atributo a nivel de enlace que impide que la autoridad pase a través de un enlace específico. Noindex es una directriz a nivel de página que impide que una página completa aparezca en los resultados de búsqueda. Resuelven problemas diferentes. Usa nofollow en enlaces que no respaldas. Usa noindex en páginas que no quieres indexar.

**¿Debería aplicar nofollow a todos los enlaces salientes?**

No. Aplicar nofollow a todos los enlaces salientes es innecesario y parece poco natural. Enlaza a fuentes autorizadas con dofollow cuando respaldes genuinamente el contenido. Google espera enlaces salientes naturales. Solo usa nofollow en enlaces en los que no confíes, enlaces de pago o contenido generado por usuarios.

**¿Qué son rel="sponsored" y rel="ugc"?**

Google introdujo estos atributos en septiembre de 2019 junto con el cambio de nofollow a "pista". Usa `rel="sponsored"` en cualquier enlace que implique intercambio monetario (enlaces de afiliados, colocaciones de pago, patrocinios). Usa `rel="ugc"` en contenido generado por usuarios (comentarios, publicaciones de foros, reseñas). Ambos indican a Google que no transmita autoridad de posicionamiento a través del enlace.

---

Los enlaces dofollow y nofollow sirven para propósitos diferentes. Ambos son esenciales para una estrategia de SEO saludable. Construye enlaces dofollow para autoridad de posicionamiento. Gana enlaces nofollow para tráfico, diversidad y señales naturales. Monitoriza tu proporción, etiqueta correctamente los enlaces de pago y recuerda que Google trata nofollow como una pista, no como una orden.
