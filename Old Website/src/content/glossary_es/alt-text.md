---
term: "Texto alternativo (alt text)"
slug: "alt-text"
definition: "El texto alternativo (alt text) describe imágenes para motores de búsqueda y lectores de pantalla. Aprende a escribir texto alternativo efectivo, ejemplos y por qué importa para el SEO."
category: "SEO"
difficulty: "Beginner"
keyword: "texto alternativo"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## ¿Qué es el texto alternativo?

El texto alternativo (alt text) es un atributo HTML que proporciona una descripción escrita de una imagen. Usado por lectores de pantalla para usuarios con discapacidad visual y por motores de búsqueda para entender qué muestra una imagen.

Probablemente lo has visto en código: `<img src="foto.jpg" alt="descripción aquí">`. Esa descripción es el texto alternativo. Sirve a dos audiencias simultáneamente. Para personas que no pueden ver la imagen. Ya sea porque usan un lector de pantalla, tienen una conexión lenta o la imagen no carga. El texto alt les dice qué hay ahí. Para Google, es una de las principales señales usadas para indexar y posicionar imágenes en Google Imágenes.

El análisis de accesibilidad de WebAIM de 2024 encontró que al 54,5 % de las imágenes en la web les falta texto alternativo. Más de la mitad. Eso es tanto un fallo de [accesibilidad](/glossary/accessibility-content) como una oportunidad SEO esperando a quien esté dispuesto a rellenar un campo de texto.

## ¿Por qué importa el texto alternativo?

El texto alt está en la intersección de accesibilidad, [SEO](/glossary/seo) y experiencia de usuario. Ignóralo y pierdes en los tres frentes.

- **Cumplimiento de accesibilidad**. Las directrices ADA y WCAG 2.1 requieren texto alt en imágenes con significado. Las demandas por accesibilidad web han aumentado más de un 300 % desde 2018. No es opcional.
- **Tráfico desde búsqueda de imágenes**. Google Imágenes genera [tráfico orgánico](/glossary/organic-traffic) significativo. Sin texto alt, Google no puede indexar tus imágenes correctamente, y pierdes ese tráfico por completo.
- **Señales de [SEO On-Page](/glossary/on-page-seo)**. El texto alt da a Google contexto adicional sobre el contenido de tu página. Un artículo sobre reformas de cocina con imágenes correctamente descritas refuerza la relevancia temática de la página.
- **Respaldo cuando las imágenes fallan**. Si una imagen no carga (conexión lenta, URL rota, clientes de email bloqueando imágenes), el texto alt aparece en su lugar. Los usuarios siguen entendiendo qué se suponía que había.

Cada imagen de tu sitio debería tener texto alt. Las imágenes decorativas (bordes, espaciadores) reciben un atributo alt vacío (`alt=""`). El resto recibe una descripción.

## Cómo funciona el texto alternativo

Escribir texto alt es simple en concepto. Hacerlo bien requiere entender qué necesitan los distintos sistemas.

### Cómo lo usan los lectores de pantalla

Cuando un lector de pantalla encuentra una imagen, lee el texto alt en voz alta. Si el texto alt dice "foto de stock de reunión de negocios", eso es lo que oye el usuario. Inútil. Si dice "5 miembros del equipo revisando un informe de marketing en una mesa de reuniones", el usuario entiende el contexto. Escribe para la persona que escucha, no para un motor de búsqueda.

### Cómo lo usa Google

Googlebot no puede "ver" imágenes como los humanos. Depende del texto alt, texto circundante, nombres de archivo y datos estructurados para entender el contenido de la imagen. La propia documentación de Google indica que el texto alt es "extremadamente útil" para el ranking en Google Imágenes. Es una de las señales más fuertes de [SEO de imagen](/glossary/image-seo) que puedes controlar.

### La implementación HTML

El texto alt vive en el atributo `alt` de la etiqueta `<img>`:

`<img src="recepcion-clinica-dental.jpg" alt="Recepción moderna de clínica dental con personal saludando a un paciente">`

La mayoría de las plataformas CMS (WordPress, Webflow, Ghost) tienen campos dedicados para texto alt en sus interfaces de subida de imágenes. No necesitas editar HTML directamente.

### Qué pasa sin texto alternativo

Si una imagen no tiene atributo alt en absoluto, los lectores de pantalla pueden leer el nombre del archivo en su lugar. Algo como "IMG_4392.jpg". Inútil. Si el atributo alt está presente pero vacío (`alt=""`), los lectores de pantalla saltan la imagen por completo, lo cual es comportamiento correcto para imágenes decorativas pero incorrecto para las significativas.

## Tipos de texto alternativo

No todas las imágenes necesitan el mismo tratamiento:

- **Texto alt informativo**. Describe qué muestra la imagen y por qué importa. Usado para fotos, ilustraciones, gráficos y figuras que transmiten información. "Gráfico de barras mostrando un aumento del 40 % en tráfico orgánico de enero a junio de 2025".
- **Texto alt funcional**. Describe qué hace una imagen clicable. Usado para botones, iconos e imágenes enlazadas. "Botón de búsqueda" o "Descargar informe en PDF".
- **Texto alt decorativo (vacío)**. Usado para imágenes puramente decorativas que no añaden información. Establece `alt=""` para que los lectores de pantalla las salten. Patrones de fondo, líneas divisorias e iconos decorativos entran aquí.
- **Texto alt complejo**. Usado para gráficos y infografías que contienen datos densos. El texto alt da un resumen y una descripción más larga va en un atributo `longdesc` o texto cercano.

Acertar el tipo importa. Sobre-describir imágenes decorativas satura la experiencia del lector de pantalla. Sub-describir imágenes informativas pierde valor de accesibilidad y SEO.

## Ejemplos de texto alternativo

**Ejemplo 1: La página de menú de un restaurante**
Texto alt malo: "comida" o "foto del plato" o ningún texto alt. Texto alt bueno: "Salmón a la parrilla con verduras asadas y salsa de mantequilla y limón servido en un plato blanco". La versión descriptiva ayuda a Google a posicionar la imagen para búsquedas de "salmón a la parrilla" y ayuda a usuarios con discapacidad visual a entender el plato.

**Ejemplo 2: Un anuncio inmobiliario**
Malo: "exterior de la casa". Bueno: "Casa colonial de dos pisos con fachada de ladrillo rojo, columnas blancas y jardín delantero ajardinado en Calle Mayor 123". Una victoria de [SEO local](/glossary/local-seo). La descripción detallada incluye características de la propiedad que coinciden con lo que los compradores buscan en Google Imágenes.

**Ejemplo 3: Una página de producto e-commerce**
Malo: "imagen de producto 1". Bueno: "Zapatilla de running Nike Air Max 90 en blanco y gris, vista lateral". Este texto alt incluye la marca, nombre del producto, color y ángulo. Exactamente lo que Google necesita para mostrarlo en resultados de Shopping y búsqueda de imágenes. Usar contenido de blog publicado por theStacc junto a imágenes de producto correctamente optimizadas crea una sólida base de [SEO On-Page](/glossary/on-page-seo).

## Texto alt vs. texto de título (title)

Estos se confunden constantemente, pero sirven para propósitos completamente diferentes.

| | Texto alt | Texto de título |
|---|---|---|
| **Propósito** | Describe la imagen para accesibilidad y SEO | Proporciona información complementaria al pasar el cursor |
| **Requerido** | Sí (cumplimiento WCAG) | No |
| **Impacto SEO** | Fuerte (señal principal de ranking de imagen) | Mínimo |
| **Lector de pantalla** | Se lee en voz alta automáticamente | A veces, depende de la configuración |
| **Visibilidad** | Se muestra cuando la imagen no carga | Se muestra como tooltip al pasar el ratón |

El texto alt es obligatorio. El texto de título es opcional y mayormente cosmético. Concentra tu esfuerzo en el texto alt.

## Buenas prácticas con texto alternativo

- **Sé específico y conciso**. Describe lo que hay en la imagen en 125 caracteres o menos. Los lectores de pantalla pueden cortar descripciones más largas. "Golden retriever atrapando un frisbee en un parque" supera a "perro" cada vez.
- **Incluye palabras clave de forma natural, no forzada**. Si la imagen está en una página sobre [investigación de palabras clave](/glossary/keyword-research) y muestra una herramienta de análisis de palabras clave, menciónalo. Pero no metas a la fuerza: "investigación de palabras clave herramienta de palabras clave mejor investigación SEO palabras clave" es spam.
- **No empieces con "imagen de" o "foto de"**. Los lectores de pantalla ya anuncian que es una imagen. Empezar con "imagen de" es redundante. Salta directo a la descripción.
- **Describe la función para imágenes clicables**. Si una imagen es un enlace o botón, el texto alt debería describir la acción, no la imagen. Un icono de lupa que activa una búsqueda debería tener `alt="Buscar"`. No `alt="lupa"`.
- **Automatiza donde sea posible**. Al publicar a escala, mantener texto alt consistente se vuelve difícil. theStacc incluye texto alt optimizado en cada artículo que publica, así las imágenes son accesibles y están listas para SEO desde el día uno.

## Preguntas frecuentes

### ¿Cuánto debería medir el texto alternativo?

Mantenlo por debajo de 125 caracteres. La mayoría de los lectores de pantalla cortan el texto alt alrededor de esa longitud. Para imágenes complejas como infografías, ofrece un breve resumen en alt y añade una descripción más larga en el contenido circundante.

### ¿El texto alt afecta a los rankings de Google?

Sí. El texto alt es un factor de ranking confirmado para Google Imágenes y proporciona contexto de apoyo para los rankings de búsqueda web. La documentación de Search Central de Google recomienda explícitamente escribir texto alt descriptivo para [SEO On-Page](/glossary/on-page-seo).

### ¿Cada imagen debería tener texto alt?

Cada imagen significativa necesita texto alt. Las imágenes decorativas (espaciadores, patrones de fondo, adornos visuales) deberían tener atributos alt vacíos (`alt=""`) para que los lectores de pantalla las salten. La pregunta clave: ¿esta imagen transmite información? Si sí, descríbela.

### ¿El texto alt puede ser demasiado largo?

Sí. El texto alt excesivamente largo es frustrante para usuarios de lectores de pantalla y puede parecer [keyword stuffing](/glossary/keyword-stuffing) para Google. Mantén las descripciones enfocadas. Si una imagen necesita un párrafo de explicación, ponlo en el texto del cuerpo cerca de la imagen. No en el atributo alt.

---

¿Quieres cada post de blog publicado con texto alt adecuado, [etiquetas de encabezado](/glossary/heading-tags) y SEO on-page integrado? theStacc publica 30 artículos optimizados para SEO en tu sitio cada mes. Automáticamente. [Empieza por $1 →](https://app.thestacc.com)

## Fuentes

- [Google Search Central: Buenas prácticas de SEO de imagen](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM: Guía de texto alternativo](https://webaim.org/techniques/alttext/)
- [WebAIM: The WebAIM Million (Informe anual de accesibilidad)](https://webaim.org/projects/million/)
- [W3C: Requisitos de imagen WCAG 2.1](https://www.w3.org/WAI/tutorials/images/)
- [Moz: Guía de SEO de imagen](https://moz.com/learn/seo/image-seo)
