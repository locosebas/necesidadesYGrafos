# Exámenes de autoevaluación

Mismo mecanismo que en `../../devops-senior/examenes/README.md`: no hay una
app ni un script — el examen lo genero yo (Claude) al pedirlo, en la
conversación.

## Cómo pedir un examen

Ejemplos de pedidos válidos:

- *"Dame un examen de Clojure nivel básico, 10 preguntas"*
- *"Dame un examen de arquitectura hexagonal y sistemas distribuidos nivel
  senior, mezclá teoría y escenarios"*
- *"Simulá una entrevista de system design de 30 minutos: diseñá un sistema
  de pagos"*
- *"Explicame el modelo EAVT de Datomic"*
- *"Mezclá preguntas de los temas 01, 02 y 03"* (examen combinado, para
  fases avanzadas del roadmap)
- *"Hacé de entrevistador y hacéme 3 preguntas de comportamiento tipo
  liderazgo técnico"* (para el tema 06, no es examen de conocimiento)

Podés pedir formato:

- **Opción múltiple** (rápido, bueno para repaso)
- **Pregunta abierta** (mejor para medir profundidad real)
- **Escenario/troubleshooting** o **system design** (mejor para simular
  entrevista senior)

## Qué hago yo al tomarte el examen

1. Genero las preguntas del tema/nivel pedido.
2. Las respondés en el chat, **una por vez** (preferencia pedagógica del
   repo, ver `../00-diagnostico/roadmap.md`).
3. Corrijo, explico lo que falló, y te doy el % de aciertos.
4. Registro el resultado en `registro/` (ver formato abajo) — o lo hago si
   me pedís explícitamente que lo guarde.

## Formato de registro

Cada resultado se guarda como una fila en `registro/resultados.md`.
Columnas: fecha, tema, nivel, formato, % de aciertos, puntos débiles
detectados. Esto permite ver con el tiempo qué temas necesitan repaso antes
de la entrevista real.
