# Libreto de diapositivas - Llamada de filtro Metova Talent (AI Engineer)

Plan de la presentación para preparar la llamada inicial de 30 minutos con la reclutadora de
Metova Talent (empresa de reclutamiento con sede en México), 6 nov 2026. Cada diapositiva tiene:

- `Sección`: a qué parte de la llamada pertenece.
- `Diagrama`: el o los diagramas de [diagramas-c4.md](diagramas-c4.md).
- Viñetas: lo que se ve en pantalla.
- `>` guion: lo que dices en voz alta. En la presentación aparece al oprimir **N** (notas).

La presentación [presentacion.html](presentacion.html) se genera con
`python3 generar_presentacion.py` a partir de este archivo y del de diagramas.

Regla de oro de toda la llamada: **solo afirmar lo que puedes defender en la entrevista técnica.**
Con IA dices "participé", "trabajé en", "construí X parte". Nunca digas "sistemas multiagente
autónomos", ni que usaste LangChain o LangGraph. Si te preguntan por una herramienta que no has
usado, das el ejemplo real más cercano y agregas "me siento cómodo adoptándola".

---

## Llamada de filtro · Metova Talent · AI Engineer
**Sección:** Portada
- Primera llamada de **30 minutos** con la reclutadora (no es la técnica)
- Pitch, preguntas de filtro, salario, repaso de IA y preguntas para ella
- Teclas: ← → para moverse · N para ver el guion

> Esta presentación es para ensayar en voz alta. Cada diagrama es un mapa mental: si recuerdas el dibujo, recuerdas la respuesta.

---

## Cómo se reparten los 30 minutos
**Sección:** Antes de empezar
- **0-5 min**: saludo y "cuéntame de ti" (pitch de 60-90 s)
- **5-20 min**: preguntas de filtro (motivación, salida, IA, inglés, salario, modalidad)
- **20-27 min**: **tus preguntas** (cliente, stack, contratación, proceso)
- **27-30 min**: siguientes pasos, y le confirmas tu correo y tu disponibilidad
- Ten a la mano: CV, **certificado EF SET**, cifra salarial y esta lista de preguntas

> La reclutadora está revisando tres cosas: que encajes con el perfil, que el salario cuadre y que te comuniques bien. Respuestas cortas y concretas, de unos 30 a 60 segundos cada una, y dejándole espacio para que pregunte más.

---

## Pitch · "Cuéntame de ti"
**Sección:** Pitch
**Diagrama:** D1
- **~5 años** como DevOps / Platform Engineer
- **MercadoLibre** (jun 2024 – ago 2026), banca de **Mercado Pago**: Terraform, Kubernetes, AWS ECS, CI/CD, Datadog y CloudWatch
- **IA en producción**: triage de tickets con LLM (Large Language Model) + alertas de capacidad con LLM
- **Bizagi** (ene 2022 – jun 2024): Azure Pipelines, Jenkins, onboarding de Grafana, APIs REST en Python
- Cierre: **producción confiable + soluciones con LLM** · inglés C1 · disponibilidad inmediata

> Soy ingeniero DevOps y de plataforma, con unos cinco años de experiencia. Mis últimos dos años estuve en MercadoLibre, en la línea de banca de Mercado Pago, con infraestructura como código en Terraform, Kubernetes y AWS ECS, CI/CD y observabilidad con Datadog y CloudWatch. Allí empecé a trabajar con IA en producción: participé en un sistema de triage automatizado de tickets con un LLM, y trabajé en el mapeo de dependencias, la base de conocimiento, el diseño del servidor MCP con el equipo de observabilidad y las pruebas. También hice alertas de capacidad con una capa predictiva y análisis con LLM. Antes estuve en Bizagi con CI/CD en Azure Pipelines y Jenkins y APIs REST en Python. Me interesa el rol de AI Engineer porque junta las dos cosas que hago: llevar sistemas a producción de forma confiable y construir soluciones con LLM. Tengo inglés C1 y disponibilidad inmediata.

---

## Pitch en inglés (por si cambia de idioma)
**Sección:** Pitch
- "I'm a **DevOps and Platform Engineer** with about **five years** of experience."
- "At **MercadoLibre**, on Mercado Pago's banking line: **Terraform, Kubernetes, AWS ECS**, CI/CD, observability."
- "I **contributed to** an LLM-based **ticket triage system**, always with **human approval**."
- "I worked on **dependency mapping**, the **knowledge base**, the **MCP server** design and **testing**."
- "This role combines both things I do: **reliable production systems** and **LLM solutions**."

> I'm a DevOps and Platform Engineer with about five years of experience. For the last two years I worked at MercadoLibre, on Mercado Pago's banking line, doing infrastructure as code with Terraform, Kubernetes and AWS ECS, CI/CD and observability. That's also where I started working with AI in production: I contributed to an LLM-based ticket triage system that located the failing service, read its logs, used runbooks and past cases, and gave engineers a diagnosis with a proposed action, always with human approval. I'm interested in this AI Engineer role because it combines reliable production systems and LLM solutions. Si cambia a inglés, respira, habla despacio y no pidas disculpas por tu nivel.

---

## P · "¿Qué experiencia tienes con LLM?" (el contexto)
**Sección:** Experiencia en IA
**Diagrama:** D2
- **Triage automatizado de tickets** en MercadoLibre, **en producción**
- Modelo: **Claude (Anthropic)**
- Contexto desde **observabilidad** (logs vía **MCP**, Model Context Protocol) y desde **runbooks + casos pasados**
- Salida: **diagnóstico + ruta de acción** para el responsable del ticket
- **Siempre una persona aprueba**: nada se ejecuta solo

> Sí, en producción. En MercadoLibre participé en un sistema de triage automatizado de tickets. Cuando llegaba un ticket, el sistema usaba Claude, de Anthropic, para ubicar el servicio que fallaba, leía sus logs a través de un servidor MCP y consultaba runbooks y casos pasados. Al responsable del ticket le entregaba un diagnóstico ya digerido con una ruta de acción, y siempre era una persona la que aprobaba antes de ejecutar. Los casos repetitivos se resolvían casi solos.

---

## P · "¿Cómo funcionaba el triage?" (paso a paso)
**Sección:** Experiencia en IA
**Diagrama:** D3
- **1 · Mapa de dependencias**: el servicio que falla y su **blast radius** (radio de impacto)
- **2 · Logs + runbooks + casos pasados** → diagnóstico
- **3 · Entrega**: **certezas, incertidumbres** y una ruta de acción propuesta
- **4 · Human-in-the-loop**: una persona aprueba o reenruta **(nunca automático)**

> Eran cuatro pasos. Primero, con un mapa de dependencias de aplicaciones, se ubicaba el servicio que estaba fallando y su radio de impacto. Segundo, se leían los logs de esa aplicación y se diagnosticaba con los runbooks y los casos pasados. Tercero, se le entregaba al dueño del ticket un diagnóstico con una sección de certezas e incertidumbres y una ruta de acción. Cuarto, una persona revisaba, resolvía las incertidumbres y aprobaba la acción, o mandaba el ticket a otro equipo. Ese human-in-the-loop era obligatorio.

---

## P · "¿Qué hiciste tú exactamente?" (por dentro)
**Sección:** Experiencia en IA
**Diagrama:** D4
- **Harness + hooks**: bloqueaban vulnerabilidades y acciones no deseadas
- **Servidor MCP** co-diseñado con el equipo de **observabilidad (o11y)**
- **Mis aportes**: mapeo de dependencias, refinar runbooks, diseño del MCP, **pruebas**, **base de conocimiento** de casos pasados
- Recuperar runbooks y casos como contexto = **patrón RAG**

> Mi parte fue el mapeo de dependencias, que es cómo el sistema sabía qué servicio estaba fallando y a qué afectaba. También refiné los runbooks, co-diseñé el servidor MCP con el equipo de observabilidad, corrí las pruebas y organicé la base de conocimiento de casos pasados. El modelo iba envuelto en un harness con hooks que bloqueaban vulnerabilidades y acciones no deseadas. Y recuperar runbooks y casos pasados para dárselos como contexto al modelo es justamente el patrón RAG.

---

## P · "¿Otro ejemplo con IA?" Alertas de capacidad
**Sección:** Experiencia en IA
**Diagrama:** D5
- Métricas de cómputo de **Datadog** y **CloudWatch**
- **Capa reactiva**: cómputo **sobre-aprovisionado** (gasto de más) o **en riesgo**
- **Capa predictiva** sobre el histórico: "este servicio se va a quedar corto"
- **Análisis con LLM**: la alerta llega con contexto y una recomendación

> Otro ejemplo son las alertas de capacidad que hice en MercadoLibre. Detectaban cómputo sobre-aprovisionado, o sea plata desperdiciada, y cómputo en riesgo de quedarse corto. Tenían una capa reactiva con umbrales, una capa predictiva sobre el histórico y un análisis con LLM que le explicaba al equipo qué estaba pasando y qué hacer. Es FinOps y confiabilidad juntos.

---

## P · "¿Por qué te interesa este rol?" y "¿Por qué saliste de MercadoLibre?"
**Sección:** Preguntas de filtro
- **Motivación**: la IA en producción necesita **despliegue, observabilidad, costos y seguridad**, que es lo que ya hago
- Ya lo viví con el **triage**, y ahora quiero que la IA sea **mi foco principal**
- **Salida de MercadoLibre** (sin quejas, mirando hacia adelante): "Mi ciclo terminó en agosto y aproveché para enfocar mi carrera en IA aplicada"
- Nunca hablar mal de MercadoLibre ni de nadie

> Me interesa porque construir con LLM es solo la mitad del trabajo. La otra mitad es llevarlo a producción con despliegue confiable, observabilidad, control de costos y seguridad, y eso es lo que he hecho cinco años. En MercadoLibre lo viví con el triage de tickets y quiero que eso sea mi foco. Sobre la salida: mi ciclo en MercadoLibre terminó en agosto y aproveché ese momento para enfocar mi carrera en IA aplicada. Ajusta esta frase a tu motivo real, pero dilo corto y sin quejas.

---

## P · Disponibilidad, modalidad e inglés
**Sección:** Preguntas de filtro
- **Disponibilidad**: inmediata
- **Modalidad**: remoto de preferencia, híbrido en Bogotá también sirve
- **Horario**: me puedo acomodar a la zona horaria de México o Estados Unidos
- **Inglés**: **C1**, certificado **EF SET 61/100** (lo envío si lo necesitan)
- **RUT** activo y facturación electrónica ante la **DIAN**, por si es por servicios

> Mi disponibilidad es inmediata. Prefiero remoto, aunque un esquema híbrido en Bogotá también me funciona. Me acomodo al horario del equipo. Mi inglés es C1, tengo el certificado EF SET con 61 sobre 100 y se lo puedo enviar. Y si la contratación es por servicios, ya tengo RUT y facturo electrónicamente.

---

## P · "¿Cuál es tu expectativa salarial?"
**Sección:** Salario
**Diagrama:** D9
- Si te piden la cifra primero, **no la esquives**: **USD 3.000 al mes en remoto**
- Y enseguida: "¿qué rango maneja el cliente para la posición?"
- Si el rango es más alto, **ubícate dentro del rango**
- **COP**: convertir a la tasa del día y preguntar si el pago es **fijo o indexado al dólar**

> Mi expectativa está alrededor de USD 3.000 mensuales en remoto, pero me gustaría conocer el rango que tiene el cliente para la posición. Si es en pesos colombianos, conviertes con la tasa del día y preguntas si el pago queda fijo en pesos o indexado al dólar, porque si no, el salario baja cuando sube el dólar.

---

## Prestación de servicios vs contrato laboral
**Sección:** Salario
- **Laboral**: prima, cesantías, vacaciones pagadas y la empresa aporta a la seguridad social
- **Prestación de servicios**: nada de eso, tú pagas salud, pensión y ARL (**~11-12 %** de lo que facturas)
- Si los USD 3.000 ya eran como contratista, **se mantienen**
- Si te comparan con un salario laboral, pide **25-35 % más**
- Pregunta: "¿Es directo con el cliente, por **EOR** (Employer of Record, empleador de registro) o por servicios con Metova?"

> En prestación de servicios no hay prima, cesantías ni vacaciones pagadas, y la seguridad social la pagas tú, más o menos un once o doce por ciento de lo que facturas. Por eso un contrato por servicios tiene que pagar bastante más que un laboral para que valga lo mismo. Tu cifra de USD 3.000 ya está pensada como contratista remoto.

---

## P técnica básica · "¿Sabes qué es RAG?"
**Sección:** Repaso de IA
**Diagrama:** D6
- **RAG** (Retrieval-Augmented Generation, generación aumentada por recuperación)
- **Ingesta**: documentos → **chunking** → **embeddings** → **base vectorial**
- **Consulta**: pregunta → embedding → **top-k parecidos** (búsqueda ANN, Approximate Nearest Neighbor) → LLM con contexto
- **Para qué**: responder con **datos propios** y actualizados, con menos alucinaciones, y **citando la fuente**

> RAG es Retrieval-Augmented Generation. En vez de reentrenar el modelo, le das los datos en el momento de la pregunta. Primero partes los documentos en pedazos, que es el chunking, sacas el embedding de cada pedazo y lo guardas en una base vectorial. Cuando llega una pregunta, sacas su embedding, buscas los pedazos más parecidos y se los pasas al LLM como contexto. Así responde con tus datos y alucina menos. En el triage hacíamos ese patrón con los runbooks y los casos pasados.

---

## P técnica básica · "¿Embeddings y bases vectoriales?"
**Sección:** Repaso de IA
- **Embedding**: un texto convertido en un **vector de números**. Si dos textos significan algo parecido, sus vectores quedan **cerca**
- Se comparan con **similitud coseno** (cosine similarity)
- **Bases vectoriales**: **pgvector** (extensión de PostgreSQL), **OpenSearch**, **Pinecone**, **Weaviate**
- Usan índices **ANN** como **HNSW** (Hierarchical Navigable Small World) para buscar rápido
- **Búsqueda híbrida**: vector + palabras clave (BM25) suele dar mejores resultados

> Un embedding es un texto convertido en un vector de números, de manera que textos con significado parecido queden cerca. La cercanía se mide normalmente con similitud coseno. Las bases vectoriales, como pgvector, OpenSearch o Pinecone, guardan esos vectores y los buscan rápido con índices aproximados como HNSW. Y muchas veces se combina con búsqueda por palabras clave, lo que se llama búsqueda híbrida.

---

## P técnica básica · "¿Agentes? ¿LangChain o LangGraph?"
**Sección:** Repaso de IA
**Diagrama:** D7
- **Agente**: un LLM que **decide** qué herramienta usar, la ejecuta, mira el resultado y **repite** hasta terminar
- Las herramientas se conectan con **tool calling** o **MCP**
- **LangChain**: piezas para armar cadenas con LLM · **LangGraph**: el flujo del agente como un **grafo con estado**
- **Tu respuesta**: "Orquesté el flujo con el modelo, un harness y MCP. LangGraph resuelve lo mismo y me siento cómodo adoptándolo"
- He construido **servidores MCP** propios

> Un agente es un LLM en un ciclo: decide qué herramienta usar, la ejecuta, ve el resultado y vuelve a decidir hasta terminar. En producción lo importante son los guardarraíles y la aprobación humana. LangChain da piezas para armar cadenas con LLM y LangGraph modela ese ciclo como un grafo con nodos, aristas y estado. Yo orquesté el flujo directamente con el modelo, un harness con hooks y MCP, y he construido varios servidores MCP. LangGraph resuelve esa misma orquestación y me siento cómodo adoptándolo.

---

## P técnica básica · "¿Cómo evalúas un LLM? ¿MLOps / LLMOps?"
**Sección:** Repaso de IA
**Diagrama:** D8
- **Evaluación**: **golden dataset** (preguntas con respuesta esperada) + **LLM-as-a-judge**
- En RAG: **faithfulness** (fidelidad al contexto) y **relevancia**, con herramientas como **Ragas**
- **LLMOps**: versionar **prompts y modelos**, evaluar **en el CI/CD** antes de desplegar
- En producción: **latencia, costo por token, calidad**, más **caché** y **fallback** entre modelos
- Aquí es donde **más pesa tu perfil DevOps**

> Para evaluar un LLM armas un golden dataset, que son preguntas con la respuesta esperada, y usas otro LLM como juez para calificar. En RAG mides fidelidad al contexto y relevancia, por ejemplo con Ragas. LLMOps es MLOps aplicado a LLM: versionas prompts y modelos, corres esa evaluación dentro del pipeline de CI/CD y no despliegas si no pasa el umbral. En producción vigilas latencia, costo por token y calidad, con caché y fallback entre modelos. Es la parte del rol donde más aporta mi experiencia DevOps.

---

## Tus preguntas para la reclutadora
**Sección:** Preguntas para ella
**Diagrama:** D10
- **1 · Cliente final**: ¿qué empresa o industria, en qué país está el equipo?
- **2 · El rol**: ¿es más construir aplicaciones con LLM (RAG, agentes) o la plataforma y el MLOps?
- **3 · Stack**: ¿qué proveedor de LLM, qué nube, qué frameworks?
- **4 · Contratación**: ¿directo, EOR o por servicios? ¿en qué moneda?
- **5 · Horario**: ¿hay que coincidir con alguna zona horaria?
- **6 · Proceso**: ¿cuántas etapas, hay prueba técnica, cuándo esperan cerrar?
- **7 · Perfil ideal**: ¿qué es lo que más valora el cliente?

> Lleva estas siete preguntas y haz al menos cuatro o cinco. La segunda es la más importante: te dice si el rol es más de construir aplicaciones con LLM o de plataforma y LLMOps, y con eso preparas la entrevista técnica. La séptima te da pistas de qué resaltar después.

---

## Cierre: frases clave y qué no decir
**Sección:** Cierre
- ✅ "**Participé** en…", "**trabajé en**…", "**en producción**", "**siempre con aprobación humana**"
- ✅ "Me siento cómodo **adoptando** LangChain / LangGraph"
- ❌ "Construí agentes autónomos", "usé LangChain" o "entrené modelos"
- ❌ Hablar mal de MercadoLibre, o dar una cifra salarial sin preguntar por el rango
- **Al final**: "¿Cuáles son los siguientes pasos?" y confirmas tu correo

> Lo que te va a hacer pasar el filtro es sonar concreto y honesto: verbos de participación, la palabra producción y la aprobación humana. Nada de exagerar, porque la entrevista técnica lo va a revisar. Antes de colgar, pregunta cuáles son los siguientes pasos y confírmale tu correo.
