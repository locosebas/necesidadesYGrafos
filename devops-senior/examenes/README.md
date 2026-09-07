# Exámenes de autoevaluación

Mecanismo simple para medir conocimiento por tema y detectar puntos débiles.
No hay una app ni un script — el examen lo genero yo (Claude) al pedirlo, en
la conversación.

## Cómo pedir un examen

Ejemplos de pedidos válidos:

- *"Dame un examen de Bicep nivel intermedio, 10 preguntas"*
- *"Dame un examen de Azure Networking nivel senior, mezclá teoría y escenarios"*
- *"Simulá una entrevista técnica de 30 minutos sobre Kubernetes troubleshooting"*
- *"Dame un examen de práctica estilo AZ-400"*
- *"Dame un examen basado en el documento de Scopes/CoSMOS"*
- *"Mezclá preguntas de los temas 04, 05 y 06"* (examen combinado, para
  fases avanzadas del roadmap)

Podés pedir formato:
- **Opción múltiple** (rápido, bueno para repaso)
- **Pregunta abierta** (mejor para medir profundidad real — te fuerza a
  explicar, no reconocer)
- **Escenario/troubleshooting** (mejor para simular entrevista senior)

## Qué hago yo al tomarte el examen

1. Genero las preguntas del tema/nivel pedido.
2. Las respondés en el chat.
3. Corrijo, explico lo que falló, y te doy el % de aciertos.
4. Registro el resultado en `registro/` (ver formato abajo) — o lo hago si
   me pedís explícitamente que lo guarde.

## Formato de registro

Cada resultado se guarda como una fila en `registro/resultados.md` (se crea
la primera vez que rindas un examen). Columnas: fecha, tema, nivel, formato,
% de aciertos, puntos débiles detectados.

Esto permite, con el tiempo, ver qué temas necesitan repaso antes de rendir
la certificación real o ir a la entrevista.
