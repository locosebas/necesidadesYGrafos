# Preguntas adicionales de la misma prueba (Coderbyte)

## 1. Latencia intermitente en un servicio distribuido; los logs no dicen qué dependencia la causa

**Respuesta:** trazas distribuidas (distributed tracing) con OpenTelemetry, con el `trace_id` dentro de
los logs.

- Una traza sigue una petición de punta a punta; cada salto es un **span** con su duración, y en la
  vista de cascada (waterfall) se ve qué dependencia se lleva el tiempo.
- La **propagación de contexto** (header `traceparent`, W3C Trace Context) une los spans de todos los
  servicios en una sola traza.
- El `trace_id` en los logs une los errores aislados con la traza exacta donde ocurrieron.
- Muestreo **tail-based** para quedarse con las trazas lentas o con error (el problema es intermitente).
- Descartar: subir el nivel de logs a DEBUG o agregar más dashboards (más datos, pero sin correlación
  entre servicios).

**Palabra clave:** correlación de los tres pilares de la observabilidad (logs, métricas y trazas).

## 2. Servidor RHEL con latencia alta: CPU baja, disco lento y procesos en espera ininterrumpible

**Respuesta:** cuello de botella de I/O (Input/Output) de disco, es decir, saturación del almacenamiento.

- Espera ininterrumpible = **estado `D`** (uninterruptible sleep): el proceso espera al disco (o a un
  NFS, Network File System) y no se puede matar ni con `kill -9`.
- CPU baja + disco lento + estado `D` = **I/O wait**. El load average sube porque los procesos en
  estado `D` cuentan en el load average de Linux.
- Comandos: `top` (campo `wa`), `vmstat 1 5` (columnas `b` y `wa`), **`iostat -x 1 5`** (`%util`,
  `await`, `aqu-sz`), `ps -eo pid,stat,wchan:30,cmd | awk '$2 ~ /^D/'`, `iotop -o`, `pidstat -d 1`,
  `dmesg -T | grep -i -E "error|timeout|hung_task"`.
- Causas a descartar en orden: un proceso que satura el disco, swapping (`free -m`, `si`/`so` en
  `vmstat`), disco/SAN/NFS degradado o límite de IOPS, filesystem lleno (`df -h`).

**Palabra clave:** estado `D` + CPU baja + await alto = I/O wait; herramienta clave `iostat -x`.
