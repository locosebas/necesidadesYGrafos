"""Genera el audio de un episodio a partir de su guion .md.

Uso: python3 generar.py episodio-01-repaso-general.md
Requiere: pip install edge-tts, y ffmpeg en el PATH.
Si hay un proxy con CA propia, exportar CA_BUNDLE=/ruta/al/bundle.crt
"""
import asyncio, os, re, subprocess, sys, tempfile

import certifi
if os.environ.get("CA_BUNDLE"):
    certifi.where = lambda: os.environ["CA_BUNDLE"]
import edge_tts

VOCES = {"SALOMÉ": "es-CO-SalomeNeural", "GONZALO": "es-CO-GonzaloNeural"}
PAUSA_ENTRE_TURNOS = 0.6


def leer_turnos(ruta):
    cuerpo = open(ruta, encoding="utf-8").read().split("\n---\n", 1)[1]
    for linea in cuerpo.splitlines():
        if m := re.match(r"\[PAUSA (\d+)\]", linea):
            yield ("pausa", float(m.group(1)))
        elif m := re.match(r"(SALOMÉ|GONZALO): (.+)", linea):
            yield (m.group(1), m.group(2))


def silencio(seg, ruta):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=24000:cl=mono", "-t", str(seg), ruta], check=True)


async def main(guion):
    salida = os.path.splitext(guion)[0] + ".mp3"
    with tempfile.TemporaryDirectory() as tmp:
        partes = []
        for i, (quien, texto) in enumerate(leer_turnos(guion)):
            ruta = os.path.join(tmp, f"{i:04d}.wav")
            if quien == "pausa":
                silencio(texto, ruta)
            else:
                mp3 = ruta[:-4] + ".mp3"
                await edge_tts.Communicate(texto, VOCES[quien]).save(mp3)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3,
                                "-ar", "24000", "-ac", "1", ruta], check=True)
                partes.append(ruta)
                ruta = os.path.join(tmp, f"{i:04d}s.wav")
                silencio(PAUSA_ENTRE_TURNOS, ruta)
            partes.append(ruta)
            print(f"{i:3d} {quien}", flush=True)
        lista = os.path.join(tmp, "lista.txt")
        with open(lista, "w") as f:
            f.writelines(f"file '{p}'\n" for p in partes)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lista, "-ac", "1", "-b:a", "48k", salida], check=True)
    print("Listo:", salida)


asyncio.run(main(sys.argv[1]))
