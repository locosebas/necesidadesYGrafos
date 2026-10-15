#!/usr/bin/env bash
# ↑ Shebang: ejecuta el script con el bash que esté en el PATH (más portable que /bin/bash).

# Cada 5 segundos hace un GET a httpbin.org/get e imprime
# el tiempo total de respuesta y el campo "origin".
# Requiere: curl (usa jq si está instalado; si no, sed)

# -u: error si se usa una variable no definida (evita bugs por typos).
# -o pipefail: un pipe falla si falla cualquier comando del pipe, no solo el último.
# (No se usa -e a propósito: un fallo de red no debe matar el ciclo.)
set -uo pipefail

URL="https://httpbin.org/get"   # Endpoint a consultar
INTERVALO=5                     # Segundos de espera entre peticiones
REPETICIONES=0                  # Número de peticiones; 0 = infinito hasta cancelar (Ctrl+C)

# trap: al recibir Ctrl+C (INT) o kill (TERM) imprime un mensaje y sale limpio con código 0.
trap 'echo; echo "Detenido."; exit 0' INT TERM

contador=0                      # Cuántas peticiones se han hecho
# Repite mientras sea infinito (0) o no se haya llegado al límite. (( )) = aritmética de bash.
while (( REPETICIONES == 0 || contador < REPETICIONES )); do
  (( contador++ ))              # Suma 1 al contador
  # curl:
  #   -s  silencioso (sin barra de progreso)
  #   -S  pero sí muestra errores
  #   --max-time 10  corta la petición si tarda más de 10 s (no se queda colgado)
  #   -w '\n%{time_total}'  al final del cuerpo agrega un salto de línea y el tiempo total en segundos
  # $( ) captura la salida en la variable: JSON + última línea con el tiempo.
  respuesta=$(curl -sS --max-time 10 -w '\n%{time_total}' "$URL")
  if [[ $? -ne 0 ]]; then       # $? = código de salida de curl; distinto de 0 = falló
    echo "$(date '+%F %T') | error en la petición"   # Informa el error con fecha y sigue el ciclo
  else
    tiempo=$(tail -n1 <<< "$respuesta")   # Última línea = tiempo total (<<< pasa el texto como entrada)
    cuerpo=$(sed '$d' <<< "$respuesta")   # Todo menos la última línea = JSON ('$d' borra la última)
    if command -v jq >/dev/null 2>&1; then          # ¿Está instalado jq? (salida descartada, solo importa el código)
      origin=$(jq -r '.origin' <<< "$cuerpo")       # jq lee el campo "origin" del JSON; -r = sin comillas
    else
      # Sin jq: sed busca la línea "origin": "x.x.x.x" y se queda solo con el valor (grupo \1)
      origin=$(sed -n 's/.*"origin": *"\([^"]*\)".*/\1/p' <<< "$cuerpo")
    fi
    # Imprime fecha (%F = AAAA-MM-DD, %T = HH:MM:SS), tiempo y origin
    echo "$(date '+%F %T') | tiempo_total=${tiempo}s | origin=${origin}"
  fi
  # Si hay límite y ya se alcanzó, sale sin esperar los 5 s finales
  (( REPETICIONES != 0 && contador >= REPETICIONES )) && break
  sleep "$INTERVALO"            # Espera antes de la siguiente petición
done                            # Fin del ciclo
