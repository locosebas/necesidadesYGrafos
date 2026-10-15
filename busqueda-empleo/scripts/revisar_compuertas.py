"""Revisa las compuertas sobre un export del tablero, sin abrir el navegador.

Uso: python revisar_compuertas.py CARPETA_EXPORT [PREFIJO]
Salida: una línea por vacante que NO pasa (DESCARTADA o MARCADA), un resumen al final,
y resultados_compuertas.json para actualizar el tablero con un solo batch.
"""
import json, os, sys
from comun import compuerta, linea, vacantes, BASE

carpeta = sys.argv[1]
prefijo = sys.argv[2] if len(sys.argv) > 2 else ""
resultados = []
for v in vacantes(carpeta, prefijo):
    estado, motivo = compuerta(v)
    if estado != "PASA":
        linea(v["id"], estado, motivo)
        resultados.append({"id": v["id"], "estado": estado, "detalle": motivo})
total = len(vacantes(carpeta, prefijo))
print(f"{total} revisadas, {total - len(resultados)} pasan, {len(resultados)} no pasan")
json.dump(resultados, open(os.path.join(BASE, "resultados_compuertas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
