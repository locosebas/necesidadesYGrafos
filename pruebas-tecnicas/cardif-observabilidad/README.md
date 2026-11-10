# Entrevista para Cardif: observabilidad y sus herramientas

Entrevista con cliente final **Cardif** (BNP Paribas Cardif, aseguradora), noviembre 2026. Ya hubo
una entrevista con **Amaris** para el mismo cliente; esta es con otra empresa. Tema: **observabilidad,
herramientas y cómo se aplica en una aseguradora regulada**.

> Regla de honestidad: lo tuyo es Grafana y Datadog (uso diario en MercadoLibre), AWS CloudWatch,
> OpenTelemetry en una prueba de concepto y el servidor MCP diseñado con el equipo de o11y. Dynatrace,
> New Relic, Splunk, ELK administrado y PagerDuty se explican, no se dice que los usaste.

## Material de estudio

- [diagramas-c4.md](diagramas-c4.md): 14 diagramas C4 con íconos.
- [libreto-diapositivas.md](libreto-diapositivas.md): las 17 diapositivas con el guion de cada una.
- [presentacion.html](presentacion.html): la presentación (← → para navegar, **N** para ver el guion).
  Versión para el celular (privada): ver [presentaciones/README.md](../../presentaciones/README.md).
  Se regenera con `python3 generar_presentacion.py`.

## Para recitar de memoria

Señales (MELT): Metrics · Events · Logs · Traces.
Flujo: 1 instrumentar · 2 recolectar · 3 almacenar · 4 visualizar · 5 alertar · 6 actuar.
