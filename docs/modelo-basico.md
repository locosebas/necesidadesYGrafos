# Modelo básico de interacciones (Necesidades y Grafos)

Borrador de trabajo. Define actores (nodos), dos dimensiones de interacción
(económica y social) y una lista corta de tipos de interacción que cubra la
mayoría de casos económicos, sociales o de otro tipo. Pensado para iterar:
cada sección puede refinarse a medida que aparezcan casos que no encajen.

## 1. Actores (nodos)

| Actor | Descripción | Atributos típicos |
|---|---|---|
| Individuo / Persona | Unidad mínima de agencia | necesidades, recursos, capacidades, tiempo disponible |
| Hogar / Familia | Unidad de convivencia y reproducción | recursos compartidos, dependientes a cargo |
| Empresa / Organización productiva | Agente que produce bienes/servicios con fin de lucro u otro | recursos productivos, capital, mano de obra |
| Estado / Institución pública | Agente con poder normativo y redistributivo | capacidad coercitiva, presupuesto, normas |
| Comunidad / Asociación / Grupo | Colectivo con lazos no necesariamente productivos | reglas informales, capital social |
| Naturaleza / Ecosistema *(opcional)* | Fuente/sumidero de recursos, no agente pero sí nodo | recursos naturales, capacidad de regeneración |

La lista puede acotarse a los primeros cinco si por ahora no interesa la
dimensión ambiental; se deja como nodo opcional porque muchas interacciones
económicas (extracción, contaminación) lo requieren tarde o temprano.

## 2. Dimensiones de la interacción (atributos de las aristas)

### Dimensión económica
- **Tipo de flujo**: bienes, servicios, dinero, trabajo/tiempo, información con valor de uso.
- **Reciprocidad**: unilateral (donación, extracción) / bilateral balanceada (trueque, compraventa) / generalizada (se devuelve en el futuro, no necesariamente al mismo actor).
- **Mediación**: mercado (precio) / no mercado (costumbre, mando).
- **Formalidad**: formal (contrato, ley) / informal (acuerdo tácito, confianza).

### Dimensión social
- **Tipo de vínculo**: parentesco, jerárquico, entre pares, institucional/rol.
- **Asimetría de poder**: simétrica / asimétrica (quién puede imponer condiciones).
- **Confianza / afectividad**: alta / media / baja.
- **Formalidad institucional**: formal (rol reconocido) / informal (lazo personal).

Cada interacción del grafo se puede etiquetar con un valor (o rango) en cada
atributo de ambas dimensiones, incluso si predomina una sobre la otra.

## 3. Lista corta de tipos de interacción

Tipología transversal (aplica a lo económico, social o ambiental) basada en
antropología económica y sociología clásica. Se buscó el mínimo de
categorías que cubra la mayoría de casos:

1. **Reciprocidad** — intercambio no mediado por precio, con expectativa de
   devolución (favores, ayuda mutua, trueque). *Dimensión: económica + social.*
2. **Intercambio de mercado** — intercambio mediado por precio, voluntario.
   *Dimensión: económica.*
3. **Redistribución** — flujo que pasa por un centro (Estado, jefe de hogar,
   organización) y se reparte. *Dimensión: económica + social.*
4. **Cooperación** — acción conjunta hacia un objetivo compartido, sin
   contraprestación directa (producción colectiva, proyectos comunes).
   *Dimensión: social + económica.*
5. **Competencia** — búsqueda paralela de un recurso o posición escasa, sin
   agresión directa. *Dimensión: económica + social.*
6. **Coerción / conflicto** — imposición no consentida (extracción forzada,
   violencia, disputa). *Dimensión: social + económica.*
7. **Cuidado** — soporte asimétrico y no recíproco a quien no puede
   retribuir (crianza, cuidado de dependientes). *Dimensión: social (con
   componente económico no monetizado).*
8. **Comunicación / influencia** — transferencia de información, persuasión,
   socialización de normas. *Dimensión: social.*

Si se quiere una lista aún más corta, 3–4–7 pueden fusionarse en
"cooperación" en sentido amplio, y 6–8 pueden quedar como casos límite de
"conflicto" vs. "influencia". Se deja desagregado porque la matriz
económica/social distingue mejor los casos reales.

## 4. Bibliografía (ampliada)

**Antropología económica**
- Karl Polanyi, *The Great Transformation* (1944) — formas de integración
  económica: reciprocidad, redistribución, intercambio de mercado (base de
  la lista de la sección 3).
- Marcel Mauss, *Ensayo sobre el don* (1925) — reciprocidad y obligación de
  devolver.
- Marshall Sahlins, *Stone Age Economics* (1972) — reciprocidad
  generalizada/balanceada/negativa.

**Sociología económica y de redes**
- Georg Simmel, *Sociología* (1908) — formas puras de interacción:
  intercambio, conflicto, competencia, dominación.
- Peter Blau, *Exchange and Power in Social Life* (1964) — teoría del
  intercambio social.
- Mark Granovetter, "Economic Action and Social Structure: The Problem of
  Embeddedness" (1985) — por qué lo económico no puede separarse de lo
  social (justifica el modelo de dos dimensiones).
- Harrison White, *Identity and Control* (1992) — interacción como
  formación de identidad en redes.

**Economía institucional y de los comunes**
- Elinor Ostrom, *Governing the Commons* (1990) — cooperación sostenida
  sobre recursos compartidos.
- Douglass North, *Institutions, Institutional Change and Economic
  Performance* (1990) — formalidad/informalidad de las reglas de
  interacción.

**Necesidades humanas y cuidado**
- Manfred Max-Neef, *Human Scale Development* (1986) — matriz de
  necesidades y satisfactores (referencia directa del nombre del proyecto).
- Nancy Folbre, *The Invisible Heart: Economics and Family Values* (2001) —
  economía del cuidado, justifica el tipo de interacción "cuidado" como
  categoría propia y no solo redistribución.
- Pierre Bourdieu, "The Forms of Capital" (1986) — capital económico,
  social, cultural y simbólico; útil si más adelante se agregan más
  dimensiones.

## 5. Pendientes / preguntas abiertas

- ¿Los tipos de interacción son mutuamente excluyentes por arista, o una
  misma arista puede tener más de un tipo activo a la vez (p. ej.
  intercambio de mercado + vínculo de confianza)?
- ¿Se necesita una tercera dimensión (ambiental/ecológica) ahora o se
  pospone hasta incluir el nodo "Naturaleza"?
- ¿Qué escala de valores usar en los atributos (binaria, ordinal 1–5,
  continua)?
