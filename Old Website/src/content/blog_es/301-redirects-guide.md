---
title: "Cómo Configurar Redirecciones 301 (Paso a Paso)"
description: "Aprende a configurar redirecciones 301 para SEO. Cubre WordPress, .htaccess, Nginx, Shopify y Cloudflare. Con pasos de prueba. Actualizado marzo 2026."
slug: "301-redirects-guide"
keyword: "redirecciones 301"
author: "Siddharth Gangal"
date: "2026-04-26"
category: "SEO Tips"
image: "/blogs-preview-images/301-redirects-guide.webp"
---

Cambiaste una URL. Quizás migraste a un nuevo dominio. Quizás consolidaste 3 páginas en una. Ahora los visitantes encuentran un error 404 y Google baja tus posiciones de la noche a la mañana.

Cada URL rota filtra la equidad de enlaces que tardaste meses en acumular. Los usuarios abandonan la página. Google marca tu sitio como mal mantenido. Una sola migración sin redirecciones 301 puede eliminar el 40% o más de tu tráfico orgánico en una semana.

Esta guía detalla 7 pasos para configurar redirecciones 301 correctamente. Aprenderás el proceso exacto para WordPress, Apache `.htaccess`, Nginx, Shopify y Cloudflare. Sin conjeturas. Sin enlaces rotos. Sin pérdida de posicionamiento.

Publicamos más de 3.500 blogs en más de 70 industrias. Los cambios de URL, consolidaciones de páginas y migraciones de dominio son cosas que gestionamos cada semana. Los pasos a continuación son los mismos que seguimos en nuestros propios sitios y con nuestros clientes.

Esto es lo que aprenderás:

- Cómo encontrar cada URL que necesita una redirección
- Cómo mapear las URL antiguas a sus nuevos destinos correctos
- Cómo implementar redirecciones 301 en 5 plataformas diferentes
- Cómo solucionar cadenas de redirección y bucles antes de que afecten tu velocidad
- Cómo probar las redirecciones antes y después de publicarlas
- Cómo monitorear el estado de las redirecciones en Google Search Console

---

## Resumen

- **Tiempo requerido:** 10 a 30 minutos (depende del número de redirecciones)
- **Dificultad:** Principiante a Intermedio
- **Lo que necesitas:** Acceso a tu CMS, panel de hosting o archivos de configuración del servidor

---

## ¿Qué es una Redirección 301?

Un código de estado `301` le indica a los navegadores y motores de búsqueda que una página se ha movido permanentemente a una nueva URL. El navegador envía automáticamente a los visitantes a la nueva dirección. Google transfiere la equidad de enlaces de la URL antigua a la nueva.

Antes de 2016, las redirecciones 301 causaban aproximadamente una pérdida del 15% de PageRank por salto. Eso ya no es el caso. [Google confirmó que las redirecciones 30x ya no diluyen el PageRank](https://searchengineland.com/google-no-pagerank-dilution-using-301-302-30x-redirects-anymore-254608). Hoy en día, una `301` correctamente configurada transfiere entre el 90 y el 99% de la equidad de enlaces, según Moz.

Esto convierte a las redirecciones 301 en la herramienta más importante para preservar tu SEO durante cualquier cambio de URL. Omítelas y empiezas desde cero.

---

## Paso 1: Identifica Qué URLs Necesitan Redirecciones

No puedes redirigir lo que no has encontrado. El primer paso es construir una lista completa de URLs que devuelven errores o que han cambiado.

Empieza con **Google Search Console**. Ve al informe de Páginas y filtra por "No encontrado (404)". Esto muestra cada URL que Google intentó rastrear pero no pudo alcanzar. Exporta la lista completa.

Luego, revisa **Google Analytics** (GA4). Observa el informe de Páginas de destino en busca de páginas que repentinamente perdieron tráfico. Una caída brusca después de un cambio de URL es una señal clara de que falta una redirección.

Ejecuta un **rastreo del sitio** con una herramienta como Screaming Frog, Sitebulb o Ahrefs Site Audit. Estas herramientas encuentran enlaces internos rotos, páginas huérfanas y respuestas 404 que Google Search Console podría pasar por alto. Una [auditoría SEO](/blog/how-to-do-seo-audit) completa revelará estos problemas rápidamente.

Tres escenarios comunes que requieren redirecciones 301:

1. **Cambio de slug de URL**. Renombraste `/blog/entrada-antigua` a `/blog/entrada-nueva`
2. **Migración de dominio**. Mudaste de `sitioviejo.com` a `dionuevo.com`
3. **Consolidación de páginas**. Fusionaste 3 páginas delgadas en 1 página más sólida para [corregir contenido delgado](/blog/fix-thin-content)

### Cuándo Usar 301 vs 404 vs 410 vs Canonical

No toda URL muerta necesita una redirección. Usa este marco de decisión.

| Escenario | Acción | Por qué |
|---|---|---|
| Página movida a una nueva URL | Redirección `301` | Preserva la equidad de enlaces y la experiencia del usuario |
| Página eliminada, no existe reemplazo | `410` Gone | Indica a Google que la desindexe más rápido que un `404` |
| Página eliminada, podría volver | `404` Not Found | Respuesta estándar para páginas temporalmente ausentes |
| Contenido duplicado, ambas páginas permanecen activas | Etiqueta `canonical` | Consolida señales sin eliminar la página |
| Dominio antiguo a dominio nuevo | Redirección `301` (nivel de dominio) | Transfiere toda la equidad al nuevo dominio |

![Cuándo usar redirecciones 301 vs 404 vs 410 vs canonical](/images/blog/301-redirect-decision-framework.webp)

**Por qué importa este paso:** Las redirecciones faltantes son invisibles. Los usuarios ven un 404 y se van. Google ve una URL muerta y la elimina del índice. Pierdes posicionamiento sin ninguna advertencia en tu panel de analítica.

**Consejo profesional:** Exporta tu XML sitemap completo antes de realizar cualquier cambio de URL. Compáralo con el rastreo posterior al cambio para detectar cada discrepancia.

---

## Paso 2: Mapea las URL Antiguas a sus Nuevos Destinos

Una redirección solo es tan buena como su destino. Enviar todas las URL antiguas a la página de inicio es un error común. Google trata las redirecciones a la página de inicio desde páginas profundas como [soft 404s](https://developers.google.com/search/docs/crawling-indexing/301-redirects). De todas formas pierdes la equidad.

Crea una hoja de cálculo con 4 columnas:

| URL Antigua | URL Nueva | Tipo de Redirección | Notas |
|---|---|---|---|
| `/blog/guia-seo-antigua` | `/blog/guia-seo-onpage` | 301 | Contenido fusionado |
| `/servicios/diseno-web` | `/servicios/diseno` | 301 | Slug acortado |
| `/blog/entrada-desactualizada` | , | 410 | Sin reemplazo |

Sigue estas reglas de mapeo:

- **Apunta siempre a la página más relevante.** Haz coincidir el tema y la intención, no solo la categoría.
- **Para migraciones de dominio, refleja la estructura de URL.** Si `/acerca` existía en el dominio antiguo, redirigelo a `/acerca` en el nuevo dominio.
- **Agrupa las redirecciones por tipo.** Los cambios masivos de URL (como eliminar `/blog/` de las rutas) pueden usar reglas basadas en patrones en lugar de entradas individuales.
- **Marca las páginas con muchos backlinks.** Usa Ahrefs o el informe de Links de Google Search Console para identificar tus páginas con más enlaces. Estas son las de mayor prioridad para un mapeo preciso.

Una [auditoría de contenido](/blog/how-to-content-audit) te ayuda a identificar qué páginas consolidar y cuáles retirar. Ejecútala antes de comenzar el mapeo.

**Por qué importa este paso:** Los malos mapeos envían a los usuarios y la equidad de enlaces a páginas irrelevantes. Google nota la discrepancia y puede ignorar la redirección por completo. Un mapeo incorrecto puede deshacer meses de [autoridad temática](/blog/build-topical-authority) que construiste alrededor de un clúster de palabras clave.

---

## Paso 3: Configura las Redirecciones 301 en tu Plataforma

La implementación depende de tu stack tecnológico. A continuación se presentan instrucciones exactas para 5 plataformas.

### WordPress (Método con Plugin)

La opción más rápida para sitios WordPress. Tres plugins gestionan las redirecciones correctamente:

- **Redirection** (gratuito). El plugin de redirecciones más popular. Soporta expresiones regulares, registra errores 404 e importa archivos CSV.
- **Rank Math** (gratuito/pro). Gestor de redirecciones integrado en Rank Math > Redirecciones.
- **Yoast SEO Premium**. Sugiere automáticamente redirecciones cuando cambias un slug.

Para agregar una redirección en **Redirection**:

1. Ve a Herramientas > Redirection
2. Ingresa la URL de origen (ruta antigua)
3. Ingresa la URL de destino (ruta nueva)
4. Selecciona "301 Moved Permanently"
5. Haz clic en "Add Redirect"

Para redirecciones masivas, usa la función de importación CSV. Formato: `URL de origen, URL de destino, 301`.

### Apache (.htaccess)

Si usas Apache, agrega las reglas de redirección a tu archivo `.htaccess` en la raíz del sitio.

Redirección simple:

```
Redirect 301 /pagina-antigua https://ejemplo.com/pagina-nueva
```

Redirección basada en patrón usando `mod_rewrite`:

```
RewriteEngine On
RewriteRule ^directorio-antiguo/(.*)$ /directorio-nuevo/$1 [R=301,L]
```

Redirección a nivel de dominio (sitio completo):

```
RewriteEngine On
RewriteCond %{HTTP_HOST} ^sitioantiguo\.com$ [NC]
RewriteRule ^(.*)$ https://dionuevo.com/$1 [R=301,L]
```

Siempre haz una copia de seguridad de tu archivo `.htaccess` antes de editarlo. Un error de sintaxis aquí puede derribar todo el sitio.

### Nginx

Nginx usa el bloque `server` en tu archivo de configuración (generalmente `/etc/nginx/sites-available/`).

Redirección simple:

```
location = /pagina-antigua {
    return 301 https://ejemplo.com/pagina-nueva;
}
```

Redirección basada en patrón:

```
location /directorio-antiguo/ {
    rewrite ^/directorio-antiguo/(.*)$ /directorio-nuevo/$1 permanent;
}
```

Después de editar, prueba la configuración con `nginx -t` y recarga con `systemctl reload nginx`.

### Shopify

Shopify tiene una herramienta de redirección integrada. No se necesitan plugins.

1. Ve a **Configuración > Navegación > Redirecciones de URL**
2. Haz clic en "Agregar redirección de URL"
3. Ingresa la ruta antigua y la ruta nueva
4. Guarda

Para redirecciones masivas, haz clic en "Importar" y sube un CSV con 2 columnas: `Redirigir desde` y `Redirigir a`.

Limitación de Shopify: no puedes redirigir a dominios externos con esta herramienta. Para migraciones de dominio fuera de Shopify, necesitas redirecciones a nivel de DNS.

### Cloudflare (Nivel de Edge)

Las redirecciones de Cloudflare ocurren en el edge de la CDN. Son la opción más rápida porque la redirección se activa antes de que la solicitud llegue a tu servidor.

1. Ve a **Reglas > Reglas de Redirección**
2. Crea una nueva regla
3. Establece la condición de coincidencia (hostname, ruta URI o comodín)
4. Establece la acción en "Redirección Dinámica" o "Redirección Estática"
5. Elige `301` como código de estado
6. Despliega

Cloudflare admite patrones comodín, lo que lo hace ideal para migraciones masivas de dominio.

### Comparación de Plataformas

| Plataforma | Dificultad | Soporte Masivo | Velocidad | Mejor Para |
|---|---|---|---|---|
| Plugin de WordPress | Fácil | Importación CSV | Estándar | Blogs y sitios de contenido |
| `.htaccess` | Medio | Patrones Regex | Estándar | Hosting compartido Apache |
| Nginx | Medio | Reglas de reescritura | Rápido | VPS y servidores dedicados |
| Shopify | Fácil | Importación CSV | Estándar | Tiendas de ecommerce |
| Cloudflare | Fácil | Reglas comodín | Más rápido | Cualquier sitio que use Cloudflare |

![Configuración de redirecciones 301 en WordPress, Apache, Nginx, Shopify y Cloudflare](/images/blog/301-redirect-platforms.webp)

**Por qué importa este paso:** Una sintaxis incorrecta rompe todo el sitio. Un archivo `.htaccess` mal configurado devuelve un error 500. Una mala regla de Nginx crea un bucle de redirección. Prueba en un entorno de staging cuando sea posible.

---

## Paso 4: Maneja las Cadenas y Bucles de Redirección

Una cadena de redirección ocurre cuando la URL A redirige a la URL B, que a su vez redirige a la URL C. En lugar de 1 salto, el navegador hace 2 o más. Cada salto añade entre 50 y 100 milisegundos de latencia.

Un bucle de redirección ocurre cuando la URL A redirige a la URL B, y la URL B redirige de vuelta a la URL A. El navegador queda atrapado en un ciclo infinito y eventualmente muestra una página de error.

Google rastrea un máximo de 5 saltos en una cadena de redirección. Más allá de eso, Google deja de seguirla. La página de destino nunca se rastrea ni se indexa.

### Cómo Encontrar Cadenas y Bucles

Ejecuta un rastreo con Screaming Frog o Ahrefs. Filtra por cadenas de redirección (3xx > 3xx). También puedes usar el [Redirect Checker de httpstatus.io](https://httpstatus.io) gratuito para probar URLs individuales.

### Cómo Aplanar las Cadenas

Si la cadena es A → B → C, actualiza A para que apunte directamente a C. Elimina el salto intermedio.

Antes:
```
/pagina-antigua → /pagina-renombrada → /pagina-final
```

Después:
```
/pagina-antigua → /pagina-final
/pagina-renombrada → /pagina-final
```

Ambas URL antiguas ahora apuntan directamente al destino final. Un salto cada una.

### Cómo Corregir los Bucles

Los bucles generalmente ocurren cuando 2 reglas de redirección entran en conflicto. Revisa tus reglas de redirección en busca de referencias circulares. La solución es siempre la misma: decide cuál URL es el destino canónico y haz que todas las demás URL apunten a ella.

Si estás ejecutando tanto redirecciones a nivel de servidor (`.htaccess`) como redirecciones a nivel de plugin (Redirection), revisa ambas. Las reglas conflictivas entre capas son la causa más común de bucles.

![Comparación entre cadena de redirección y redirección directa](/images/blog/redirect-chain-vs-direct.webp)

**Por qué importa este paso:** Las cadenas desperdician el presupuesto de rastreo y ralentizan la carga de páginas. Una cadena de 3 saltos añade entre 150 y 300 ms de latencia antes de que el usuario vea cualquier contenido. Los bucles son peores. Bloquean el acceso por completo y consumen el presupuesto de rastreo en páginas que nunca se resuelven.

---

> **Evita el trabajo técnico. Mantén tus posiciones.** Stacc gestiona la estructura de URLs, las redirecciones y el mantenimiento SEO para más de 30 artículos al mes.
> [Comienza por $1 →](/pricing)

---

## Paso 5: Prueba Cada Redirección Antes de Publicarla

Las redirecciones sin probar causan caídas silenciosas de posicionamiento. Una redirección que devuelve `302` en lugar de `301` no transfiere la equidad de enlaces de la misma manera. Una redirección que apunta a un 404 es peor que no tener redirección.

### Prueba con curl

Abre tu terminal y ejecuta:

```bash
curl -I https://ejemplo.com/pagina-antigua
```

Busca `HTTP/1.1 301 Moved Permanently` y el encabezado `Location:` apuntando a la nueva URL correcta.

Para probar una cadena, usa el indicador `-L` para seguir todas las redirecciones:

```bash
curl -IL https://ejemplo.com/pagina-antigua
```

Esto muestra cada salto de la cadena con su código de estado.

### Prueba con Chrome DevTools

1. Abre Chrome y presiona `F12` para abrir DevTools
2. Ve a la pestaña **Network** (Red)
3. Marca "Preserve log" (para que las redirecciones permanezcan visibles)
4. Ingresa la URL antigua en la barra de direcciones
5. Observa la primera solicitud. La columna Status debe mostrar `301`. Los encabezados de respuesta deben mostrar el `Location` correcto.

### Prueba con Herramientas en Línea

Los verificadores de redirecciones gratuitos como [httpstatus.io](https://httpstatus.io) o el [Redirect Checker de Ahrefs](https://ahrefs.com/blog/301-redirects/) te permiten probar sin necesidad de una terminal.

### Errores Comunes en las Pruebas

- **Incompatibilidad HTTP vs HTTPS.** Prueba tanto la versión `http://` como la `https://` de la URL antigua. Omitir una redirección en un protocolo deja una brecha.
- **Inconsistencia en la barra diagonal final.** `/pagina-antigua` y `/pagina-antigua/` son URLs diferentes. Ambas necesitan redirecciones.
- **www vs no-www.** Asegúrate de que `www.ejemplo.com/pagina-antigua` y `ejemplo.com/pagina-antigua` redirijan correctamente.

![Cómo probar redirecciones 301 con curl y Chrome DevTools](/images/blog/test-301-redirects.webp)

**Por qué importa este paso:** No puedes detectar una redirección rota navegando normalmente por tu sitio. Las URL antiguas no están en tu navegación. Solo una prueba deliberada o una alerta de Google Search Console detectará el problema. Para entonces, es posible que ya hayas perdido semanas de posicionamiento.

---

## Paso 6: Actualiza los Enlaces Internos para que Apunten a las Nuevas URLs

Las redirecciones son una red de seguridad. No son un reemplazo permanente para el [enlazado interno](/blog/internal-linking-blog-posts) correcto.

Cada enlace interno que pasa por una redirección añade un salto innecesario. Google sigue el enlace de todas formas, pero cada redirección consume presupuesto de rastreo. En un sitio grande con miles de enlaces internos, esto se acumula rápidamente.

### Qué Actualizar

- **Enlaces en el cuerpo del contenido**. Cualquier entrada de blog o página que enlace a la URL antigua
- **Menús de navegación**. Encabezado, pie de página, enlaces de la barra lateral
- **XML sitemap**. Elimina las URL antiguas y añade las nuevas. Si necesitas ayuda, sigue nuestra guía sobre [cómo crear y optimizar tu XML sitemap](/blog/create-xml-sitemap).
- **Datos estructurados**. Actualiza cualquier [markup de schema](/blog/schema-markup-for-blog-posts) que haga referencia a URLs antiguas
- **Etiquetas canonical**. Asegúrate de que el canonical en la nueva página apunte a sí mismo, no a la URL antigua

### Cómo Hacer un Buscar y Reemplazar en Todo el Sitio

Para WordPress, usa el plugin **Better Search Replace**. Ingresa el patrón de la URL antigua y la nueva. Ejecuta primero una prueba en seco para obtener una vista previa de los cambios. Luego ejecuta los cambios.

Para sitios estáticos o plataformas CMS personalizadas, usa la función buscar y reemplazar de tu editor de código en todo el directorio del proyecto.

Después de actualizar, [envía tu sitemap actualizado a Google](/blog/submit-website-google) a través de Search Console para acelerar el nuevo rastreo.

**Por qué importa este paso:** Los enlaces internos a través de redirecciones desperdician el presupuesto de rastreo y añaden latencia. Los enlaces directos son siempre más rápidos y eficientes. Limpia el origen y mantén las redirecciones solo como respaldo para los enlaces externos que no puedes controlar.

---

## Paso 7: Monitorea en Google Search Console

La redirección está activa. Las pruebas pasaron. Pero las redirecciones 301 pueden romperse silenciosamente durante despliegues, actualizaciones del CMS o cambios de configuración del servidor. El monitoreo continuo detecta problemas antes de que afecten el posicionamiento.

### Revisa el Informe de Páginas

En Google Search Console, ve a **Páginas** (bajo Indexación). Filtra por:

- **No encontrado (404)**. Los nuevos errores 404 que aparezcan después de que tu redirección esté activa indican una mala configuración.
- **Error de redirección**. Google detectó un bucle, cadena o redirección rota.
- **Rastreada. Actualmente no indexada**. Es posible que la nueva página de destino aún no esté indexada.

### Usa la Herramienta de Inspección de URLs

Ingresa la URL antigua en la herramienta de Inspección de URLs. Google debe mostrar "La página no está en el índice" con una nota de que redirige a la nueva URL. Si Google aún muestra la URL antigua como indexada, solicita la indexación de la nueva URL.

### Revisa las Core Web Vitals

Las cadenas de redirección aumentan el Time to First Byte (TTFB). Después de implementar las redirecciones, revisa las **Core Web Vitals** en Search Console para detectar picos de latencia. Cada salto añade entre 50 y 100 ms. Si tu TTFB aumentó, probablemente tengas una cadena sin aplanar.

También puedes usar esto como parte de una estrategia más amplia para [mejorar las Core Web Vitals](/blog/improve-core-web-vitals) en todo tu sitio.

### Establece Puntos de Revisión

- **Día 7:** Revisa los nuevos errores 404 en GSC. Verifica que las URL antiguas se resuelvan correctamente.
- **Día 30:** Compara el tráfico orgánico antes y después de la redirección. Usa el informe de Rendimiento filtrado por la nueva URL.
- **Día 90:** Confirma que el posicionamiento se haya estabilizado. Los sitios con redirecciones 301 limpias retienen el 95% o más de su tráfico orgánico en 2 a 3 meses.

**Por qué importa este paso:** Las redirecciones pueden romperse silenciosamente. Una actualización del CMS podría sobreescribir tu archivo `.htaccess`. Una actualización de plugin podría restablecer las reglas de redirección. Sin monitoreo, no lo sabrás hasta que caigan las posiciones.

---

## Resultados: Qué Esperar

Google procesa la mayoría de las redirecciones 301 en 1 a 2 semanas. Verás cómo la URL antigua desaparece de los resultados de búsqueda y la nueva URL toma su lugar.

El posicionamiento normalmente se estabiliza entre 2 y 3 meses después de una migración. [Los sitios que usan redirecciones 301 limpias retuvieron el 95% o más de su tráfico orgánico](https://ahrefs.com/blog/301-redirects/) durante este período.

Google recomienda mantener las redirecciones 301 activas durante al menos 1 año. Eliminarlas demasiado pronto envía a los visitantes que regresan y a los backlinks antiguos a un 404.

La línea de tiempo completa:

| Hito | Plazo |
|---|---|
| Google comienza a procesar la redirección | 1 a 3 días |
| URL antigua eliminada del índice | 1 a 2 semanas |
| Nueva URL posiciona en el lugar de la URL antigua | 2 a 4 semanas |
| Tráfico completamente estabilizado | 2 a 3 meses |
| Seguro para eliminar la redirección | Mínimo 1 año |

![Línea de tiempo del impacto SEO de las redirecciones 301](/images/blog/301-redirect-timeline.webp)

Combina las redirecciones limpias con la publicación consistente de contenido para [aumentar el tráfico orgánico](/blog/increase-organic-traffic) mientras tus redirecciones se consolidan.

---

## Solución de Problemas: 5 Problemas Comunes con las Redirecciones 301

### Problema 1: La Redirección Devuelve 302 en Lugar de 301

Una `302` es una redirección temporal. No transfiere la equidad de enlaces de la misma manera que una `301`. Esto suele ocurrir cuando un plugin usa `302` por defecto o cuando la configuración del servidor usa `Redirect` sin especificar el código de estado.

**Solución:** Revisa tu regla de redirección. Para `.htaccess`, usa explícitamente `Redirect 301` o `[R=301,L]`. En tu plugin CMS, verifica que el tipo de redirección esté configurado como "Permanent (301)."

### Problema 2: Cadena de Redirección (3 o Más Saltos)

Redirigiste A a B el año pasado. Luego redirigiste B a C este año. Ahora A pasa por 2 saltos para llegar a C. Google la sigue, pero la latencia afecta el rendimiento.

**Solución:** Actualiza la regla de A para que apunte directamente a C. Luego actualiza B para que apunte directamente a C. Aplana cada cadena a un solo salto.

### Problema 3: Bucle de Redirección

La URL A redirige a B. La URL B redirige de vuelta a A. El navegador muestra "ERR_TOO_MANY_REDIRECTS" y nada carga.

**Solución:** Abre tus reglas de redirección y busca referencias circulares. Si usas tanto un plugin como redirecciones a nivel de servidor, revisa ambas capas. Elimina la regla conflictiva.

### Problema 4: Redirección Mixta HTTP y HTTPS

La versión HTTP de la URL antigua redirige a la versión HTTP de la nueva URL, que luego redirige a HTTPS. Eso es una cadena de 2 saltos que debería ser de 1 salto.

**Solución:** Todas las redirecciones deben apuntar directamente a la versión HTTPS de la URL de destino. Actualiza cada regla para usar `https://` en el destino.

### Problema 5: Soft 404 Después de la Redirección

La redirección funciona. El código de estado es `301`. Pero la página de destino tiene contenido escaso o vacío. Google lo trata como un "soft 404" y puede no transferir la equidad de enlaces. Esto suele ocurrir cuando rediiges a una página de [contenido delgado](/blog/fix-thin-content) o a una página de categoría genérica.

**Solución:** Asegúrate de que cada destino de redirección sea una página real y sustancial con contenido único. Si la página de destino aún no existe, créala antes de activar la redirección.

![Problemas comunes de redirecciones 301 y sus soluciones](/images/blog/301-redirect-problems.webp)

---

> **Tu equipo SEO. $99 al mes.** 30 artículos optimizados, publicados y mantenidos. Redirecciones, enlaces internos y SEO técnico gestionados.
> [Comienza por $1 →](/pricing)

---

## Preguntas Frecuentes

**¿Cuánto tiempo debes mantener activas las redirecciones 301?**

Google recomienda mantener las redirecciones 301 activas durante al menos 1 año. Los sitios externos que enlazan a tu URL antigua seguirán enviando tráfico a través de esa redirección. Eliminarla antes de que esos enlaces externos se actualicen (la mayoría nunca lo hará) envía a sus visitantes a un 404. Ante la duda, mantén la redirección de forma permanente. La carga del servidor es despreciable.

**¿Las redirecciones 301 perjudican el SEO?**

No. Google confirmó en 2016 que las redirecciones 30x ya no causan pérdida de PageRank. Una `301` correctamente configurada transfiere entre el 90 y el 99% de la equidad de enlaces a la URL de destino. El único riesgo son los errores de implementación, como cadenas, bucles o redirigir a páginas irrelevantes.

**¿Cuál es la diferencia entre una redirección 301 y una 302?**

Una [redirección 301](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301) indica un movimiento permanente. Google transfiere la equidad de enlaces y eventualmente desindexe la URL antigua. Una `302` indica un movimiento temporal. Google mantiene la URL antigua indexada y puede no transferir toda la equidad. Usa `301` para cualquier cambio de URL permanente.

**¿Demasiadas redirecciones 301 pueden ralentizar mi sitio?**

Las redirecciones individuales añaden una latencia mínima (menos de 100 ms). El problema son las cadenas de redirección. Cada salto añade entre 50 y 100 ms. Una cadena de 3 saltos añade entre 150 y 300 ms antes de que la página comience a cargarse. Mantén cada redirección en un solo salto y el impacto en el rendimiento será despreciable.

**¿Cómo verifico si mis redirecciones 301 funcionan?**

Usa `curl -I [URL]` en tu terminal. La respuesta debe mostrar `HTTP/1.1 301 Moved Permanently` con un encabezado `Location:` apuntando al destino correcto. También puedes usar Chrome DevTools (pestaña Network con "Preserve log" habilitado) o herramientas en línea gratuitas como httpstatus.io.

**¿Debo usar una redirección 301 o una etiqueta canonical?**

Usa una `301` cuando estés eliminando completamente la página antigua. Usa una etiqueta `canonical` cuando ambas páginas permanezcan activas pero quieras que Google consolide las señales de posicionamiento en una versión. Un ejemplo común: páginas de productos con parámetros de URL. La URL filtrada sigue siendo accesible, pero el canonical apunta a la URL limpia. Para la [canibalización de palabras clave](/blog/fix-keyword-cannibalization) entre 2 páginas activas, una etiqueta canonical suele ser el mejor primer paso.

---

Las redirecciones 301 protegen la equidad de enlaces y el posicionamiento que ya ganaste. Cada cambio de URL sin una redirección es una fuga en tu base SEO.

Configura las redirecciones correctamente, pruébalas, monitoréalas y combina el trabajo con publicaciones de contenido consistentes. Así es como [posicionas más alto en Google](/blog/how-to-rank-higher-google) y mantienes las posiciones que conquistas.
