# Programación funcional y Clojure

Es el tema base de toda esta carpeta: Clojure es el lenguaje principal del
rol (la vacante aclara que dan entrenamiento, pero conviene llegar con
vocabulario y conceptos ya instalados). Clojure es un **Lisp** que corre
sobre la **JVM**, funcional, con foco fuerte en inmutabilidad.

## Objetivos

- Leer y escribir sintaxis Lisp con soltura: notación prefija,
  `(funcion arg1 arg2)`, paréntesis anidados en vez de operadores infijos.
- Explicar por qué la **inmutabilidad** (persistent data structures) es
  central en Clojure, y qué problema resuelve (estado compartido mutable en
  sistemas concurrentes/distribuidos).
- Distinguir **función pura** de función con efectos secundarios, y por qué
  las funciones puras son más fáciles de testear, paralelizar y razonar en
  un sistema distribuido.
- Usar el **REPL** como forma principal de desarrollo (REPL-driven
  development), no solo como consola de pruebas.

## De Python a Clojure: puntos de apoyo

Ya conocés estos conceptos en Python — el objetivo es mapearlos a su
equivalente en Clojure, no aprenderlos de cero:

| Concepto | Python | Clojure |
|---|---|---|
| Función anónima | `lambda x: x + 1` | `(fn [x] (+ x 1))` o `#(+ % 1)` |
| Map/filter/reduce | `map(f, coll)` | `(map f coll)` |
| Estructura inmutable | tuplas (parcial: listas son mutables) | **todo** es inmutable por defecto (vectores, mapas, listas, sets) |
| Definir variable | `x = 1` | `(def x 1)` |
| Definir función | `def f(x): return x + 1` | `(defn f [x] (+ x 1))` |

## Subtemas

1. Sintaxis básica: `def`, `defn`, `let`, `if`, `fn`, forms vs. special forms
2. Estructuras de datos persistentes: vectores `[]`, mapas `{}`, sets `#{}`,
   listas `()` — y por qué "persistente" no significa "en disco", significa
   que las versiones anteriores de la estructura siguen siendo válidas tras
   una "modificación" (que en realidad crea una nueva estructura)
3. Secuencias (`seq`) y las funciones core: `map`, `filter`, `reduce`,
   `into`, threading macros (`->`, `->>`)
4. Concurrencia: `atom`, `ref`, `agent` — modelos de estado mutable
   controlado sobre una base inmutable (relevante para sistemas distribuidos)
5. Manejo de errores idiomático en Clojure (vs. excepciones a la Python/Java)
6. Namespaces y organización de proyectos (`ns`, `require`, `deps.edn` o
   `project.clj`/Leiningen)

## Recursos

- Clojure oficial: https://clojure.org/guides/getting_started
- Clojure for the Brave and True (libro gratuito online, muy recomendado
  para background no-Lisp): https://www.braveclojure.com/
- ClojureDocs (referencia con ejemplos): https://clojuredocs.org/

## Lab sugerido

Resolvé el mismo problema pequeño (ej. contar palabras de un texto, o
agrupar una lista de transacciones por categoría) primero en Python y
después en Clojure, usando `map`/`filter`/`reduce` y threading macros
(`->>`). Compará cuánto del código es "traducible 1 a 1" y qué parte
requiere pensar distinto (inmutabilidad, ausencia de loops imperativos).

## Autoevaluación

Pedime: *"Dame un examen de Clojure nivel básico"* o *"Explicame persistent
data structures en Clojure"*.
