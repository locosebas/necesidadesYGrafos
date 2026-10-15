# Datos: Datomic y DynamoDB

Datomic es la base de datos más diferencial de esta vacante (poco común
fuera del ecosistema Clojure). DynamoDB comparte estudio con la brecha ya
identificada en `../../devops-senior/temas/06-datos-secretos/` — no la
dupliques, complementala acá con el ángulo de diseño de aplicación (no solo
operación en AWS).

## Objetivos

- Explicar el modelo de datos de **Datomic**: hechos inmutables
  (`[entidad atributo valor transacción]`, conocido como EAVT), y por qué
  el **tiempo es una dimensión de primera clase** (podés consultar el
  estado de la base "como era" en cualquier momento pasado).
- Contrastar Datomic con una base relacional tradicional: en vez de
  `UPDATE` que sobreescribe una fila, Datomic **agrega** un nuevo hecho —
  el historial completo queda disponible siempre.
- Repasar DynamoDB con foco en diseño de aplicación: partition key, sort
  key, índices secundarios (GSI/LSI), y por qué el modelado en DynamoDB es
  "diseñado para las queries" (query-first design) en vez de normalizado.

## Subtemas

1. Datomic: arquitectura (peers, transactor, storage separado del cómputo),
   Datalog como lenguaje de consulta (vs. SQL)
2. Datomic: `datoms`, transacciones, `as-of`/`history` para consultar el
   pasado
3. DynamoDB: partition key vs. sort key, GSI/LSI, patrones de acceso
   (single-table design) — ver también `devops-senior/temas/06-datos-secretos/`
   para el ángulo de RCU/WCU y operación en AWS
4. Cuándo elegir cada una: Datomic cuando el historial/auditoría es
   inherente al dominio (ej. sistemas financieros, como el caso de Nubank);
   DynamoDB cuando el patrón de acceso es simple y el volumen/latencia son
   la prioridad

## Recursos

- Datomic: https://docs.datomic.com/
- "Learn Datalog Today" (tutorial interactivo): http://www.learndatalogtoday.org/
- DynamoDB (repaso): https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html

## Lab sugerido

Tomá una entidad simple (ej. "cuenta bancaria" con saldo) y modelá cómo se
vería un cambio de saldo en Datomic (como hecho nuevo, sin borrar el
anterior) vs. en DynamoDB (como update de un item). Explicá qué pregunta es
fácil de responder en cada modelo ("¿cuál era el saldo hace 3 días?" es
trivial en Datomic, no en DynamoDB sin diseño extra).

## Autoevaluación

Pedime: *"Dame un examen de Datomic nivel básico"* o *"Explicame el modelo
EAVT de Datomic"*.
