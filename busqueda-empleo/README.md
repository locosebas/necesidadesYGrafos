# Búsqueda de empleo: traspaso para una sesión nueva

Lee esto al iniciar un chat nuevo de búsqueda de empleo. Reemplaza el historial largo del chat
original y permite trabajar gastando pocos tokens.

**Este repositorio es público.** Aquí no van datos de contacto, salario ni respuestas personales;
esos viven solo en la carpeta local `C:/Users/diazt/Documents/Postulaciones/lote/`.

## Piezas

| Pieza | Dónde | Para qué |
|---|---|---|
| Tablero ("Mesa de Postulaciones") | https://claude.ai/artifact/1TA5UUU7Tq6bmW71Gp5XaE | Estado de cada vacante (colección `vacantes`), banco de respuestas (`respuestas`), búsqueda (`meta/busqueda`). Se lee y escribe con la herramienta ArtifactData. |
| Scripts (fuente) | `busqueda-empleo/scripts/` (este repo) | Se copian a la carpeta local para ejecutarlos. |
| Scripts (ejecución) | `C:/Users/diazt/Documents/Postulaciones/lote/` | Con `datos_privados.json` y `reglas.json` (privados). |
| Scripts antiguos | `C:/Users/diazt/Documents/Postulaciones/*.py` | Ayudantes por portal (gob.py, ct_*.py, bamboo_*.py, gh_*.py, li_*.py…). Útiles como referencia. |
| Generador de CV | `C:/Users/diazt/Documents/Postulaciones/generador_cv.py` | Un CV por vacante; salida en `CVs/`. |
| Chrome de postulaciones | puerto 9222, perfil `Postulaciones/chrome-perfil` | Sesiones abiertas de Computrabajo, GetOnBoard, LinkedIn, Himalayas, Freelancer. Si está cerrado: `iniciar_chrome.py`. |
| Memoria de Claude | `~/.claude/projects/-home-locosebas-repos-necesidadesYGrafos/memory/` | Reglas de trabajo y banco de respuestas detallado. |
| Glosario de IA y lista de estudio | `devops-senior/glosario-ia-ofertas.md`, `devops-senior/pendientes-de-estudio.md` | Siglas de ofertas de IA; temas a estudiar. |

Ejecutar siempre así (la regla de permisos solo admite esta forma, sin tuberías si el script envía):
`/mnt/c/Users/diazt/AppData/Local/Programs/Python/Python313/python.exe C:/Users/diazt/Documents/Postulaciones/lote/<script>.py ... < /dev/null`

## Reglas que no cambian

- Aprobar en el tablero autoriza enviar la postulación completa.
- Honestidad: solo se afirma lo que está en el banco de respuestas; si no está, se pregunta a Sebastián.
- Nunca se comparte cédula, fecha de nacimiento ni dirección exacta; nunca se aceptan términos de privacidad,
  tratamiento de datos ni consentimientos legales por él (esas vacantes quedan "Requiere tu acción").
- CAPTCHA, cuentas nuevas, contraseñas y pagos los hace él.
- Respuestas informales de Sebastián se reescriben formales y autocontenidas.
- Salario: remoto/internacional USD 3.000/mes; local Colombia ~$9 M COP negociable ($10 M para líder/arquitecto).
  Remotos con pago bajo se aceptan como medio tiempo.
- Formato del CV: cada trabajo en 4 líneas (cargo / empresa / ciudad / fechas) para que los ATS lo lean bien.

## Flujo barato por lotes (usar esto primero)

1. Exportar del tablero solo lo necesario con ArtifactData (`get` por id o `query` con `out_dir` a
   `C:/Users/diazt/Documents/Postulaciones/lote/tablero`). No volcar listados grandes al chat.
2. Ejecutar el script del portal; imprime **una línea por vacante**: `ENVIADA`, `YA`, `PREGUNTAS`, `BLOQUEADA`, `LISTA`.
3. `PREGUNTAS` = hay preguntas sin regla: se escriben en la vacante del tablero (campo `preguntas`, estado
   `por_revisar`) para que Sebastián las responda una vez desde el celular; luego se agrega la regla a
   `reglas.json` y se reintenta. Nunca improvisar respuestas.
4. Actualizar el tablero con un solo `batch` a partir de `resultados_*.json`.

Scripts listos: `postular_ct.py` (Computrabajo). Probado el 7 oct 2026: 3 de 3 enviadas.
Pendientes por construir con el mismo patrón: GetOnBoard, LinkedIn Easy Apply (pausas de 3–6 min, máximo
10 por día, sin simular comportamiento humano), Greenhouse y BambooHR.

## Ahorro de tokens

- Sesión nueva con este README en vez de seguir el chat largo.
- Scripts con salida mínima; nada de capturas de pantalla salvo que algo falle sin explicación.
- Agentes en segundo plano: modelo pequeño, instrucciones cerradas, máximo 2 reintentos por vacante,
  informe de menos de 15 líneas.
- Priorizar encaje alto (≥ 65) y portales con script; formularios únicos de empresas = proceso asistido
  (Sebastián envía, Claude llena solo si él lo pide).
- Si Chrome no responde: `comun.destrabar()` activa (no cierra) las pestañas colgadas.

## Estado al 7 oct 2026

- ~75 postulaciones enviadas (ver "Resumen de postulaciones" en el tablero). Avanzaron: Cavca (en proceso),
  Itera y GME (hoja de vida vista), WhyHireWrong (envió cuestionario).
- Pendientes de Sebastián: cuestionario de WhyHireWrong (qué hizo él en el triage; qué proyecto de GitHub
  está publicado); elempleo (recuperar cuenta; 32+ vacantes esperando); Freelancer (perfil en onboarding,
  20 habilidades puestas; 10 propuestas listas en el tablero para publicar); Lemon.io (1 campo de perfil);
  Canonical (lo escribe él); vacantes con consentimiento de datos (Centro de Empleo, Applaudo, Inetum).
- ~240 aprobadas sin enviar, la mayoría LinkedIn (muchas solo con postulación externa) y elempleo.
