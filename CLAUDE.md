# Preferencias del usuario — Sebastián Díaz

Este repo es el plan de estudio personal de Sebastián para llegar a
Arquitecto de Plataforma (ver `devops-senior/00-diagnostico/roadmap.md`
para el plan completo). Las preferencias de acá abajo aplican **siempre**
que se trabaje en este repo — no hace falta que las repita cada sesión.

## Idioma y tono

- Responder en **español**, con acento/vocabulario **colombiano**, no
  argentino — usar **"tú"**, no **"vos"**. Evitar expresiones típicamente
  argentinas ("dale", "che", "boludo", etc.).
- Siglas siempre con su significado completo al lado la primera vez que
  aparecen en una explicación (ej.: "NSG (Network Security Group)"), no
  asumir que ya se recuerda solo porque se explicó antes en la sesión.
- Ser deliberadamente redundante con los nombres de herramientas/términos
  técnicos — repetir el nombre exacto varias veces en la misma explicación,
  en vez de reemplazarlo por "esto" o "dicho servicio" por variedad de
  estilo. Es una decisión pedagógica a propósito, no corregir a un estilo
  más variado.

## Formato de enseñanza/examen

- **Una pregunta por vez**, nunca una lista larga de preguntas juntas —
  esperar la respuesta, corregir/explicar esa respuesta puntual, y recién
  ahí pasar a la siguiente. Aplica a exámenes, explicaciones de temas, y
  cualquier interacción de enseñanza en este repo.
- Metodología general → específico: primero panorama conceptual del tema,
  después detalle técnico.
- **En evaluaciones/repasos (no necesariamente al enseñar un tema por
  primera vez): forzar el recuerdo del NOMBRE, no solo del funcionamiento.**
  Describir cómo funciona algo y pedirle que diga qué servicio/herramienta
  lo resuelve — no decir el nombre primero y preguntar si entiende cómo
  funciona. El usuario reporta que a veces entiende el mecanismo perfectamente
  cuando le dicen el nombre, pero no logra recordar el nombre por sí mismo;
  el objetivo es interiorizar el nombre, no solo el concepto.
- **Nunca ofrecer cerrar la sesión ni preguntar "¿seguimos o paramos acá?".**
  Si el usuario quiere parar, simplemente deja de responder — no hace falta
  que se lo preguntemos nosotros cada vez. Seguir proponiendo el siguiente
  paso/tema sin agregar la opción de cerrar.
- **Repaso estricto de listas enumeradas** (pilares de un framework, áreas de
  un examen, componentes de una arquitectura, etc.): cuando una lista
  enumerada ya se vio y el usuario pide "memorizarla de verdad", pedirle que
  la recite **completa, de memoria, sin ninguna pista** (ni la cantidad
  exacta de ítems si eso ya es una pista, ni el orden, ni sinónimos que
  insinúen la respuesta) — **nunca** dar feedback/corrección antes de que
  el usuario entregue su intento completo. Recién después de la respuesta
  completa, calificar estrictamente: qué acertó, qué le faltó, qué le
  sobró/inventó. El objetivo es que la brecha real quede visible, no
  suavizarla con pistas en la pregunta.

## Presentar el progreso como lista numerada y calificada

- Al usuario le sirve ver los temas **enumerados** (1, 2, 3...) con su
  **nivel actual** al lado (🔴/🟡/🟢/🔵, la misma escala de `progreso.md`) —
  la numeración le da sentido de avance total, y la calificación le dice
  dónde repasar. Presentar esto en el chat (no solo dejarlo en el archivo)
  al cerrar una fase, al empezar una sesión nueva, o cuando lo pida.

## Registro de avance

- Antes de dar por hecho que algo "ya se sabe", revisar
  `devops-senior/examenes/registro/progreso.md` — el nivel de dominio por
  tema no es binario (visto/no visto), sube o baja según el desempeño real
  en cada repaso.
- Actualizar `devops-senior/examenes/registro/resultados.md` y
  `progreso.md` después de sesiones de examen o repaso significativas.
- Commitear y pushear los cambios al repo (rama de trabajo actual) después
  de actualizaciones de contenido del plan de estudio.

## Mensajes listos para enviar (correos, WhatsApp, formularios)

- **Nunca entregar un texto para copiar y pegar con espacios sin llenar**
  (`[SALARIO]`, `[CONFIRMAR]`, etc.). Si falta un dato, **preguntárselo
  antes** y entregar el texto solo cuando esté completo.

## Revisión del correo

- Cada vez que se revise el correo, **terminar siempre con la lista de
  pendientes abiertos** (pruebas, videos, entrevistas con IA, formularios),
  aunque no haya llegado nada nuevo sobre ellos. Sebastián pidió que se le
  siga recordando hasta que diga que ya lo hizo.

## Guardar los chats con reclutadores

- **Todo chat, mensaje o correo de un reclutador que Sebastián pegue en la
  conversación se guarda** en la Mesa de Postulaciones (artifact
  `1TA5UUU7Tq6bmW71Gp5XaE`, colección `conversaciones`, con ArtifactData),
  sin que tenga que pedirlo. Cada documento lleva: `vacanteId` (el id del
  doc en `vacantes`), `empresa`, `contacto`, `canal`, `fecha`, `recibido`
  (el texto tal como lo pegó) y `respuestaPropuesta` (el borrador que se le
  dio). Si la vacante no existe en `vacantes`, crearla también.
- Antes de responder a un contacto, **consultar `conversaciones`** de esa
  empresa para tener el contexto de lo que ya se habló.
- No va al repo (es público): la Mesa es privada.
