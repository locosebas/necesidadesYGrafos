"""Convierte analisis-alternativas.md en audios .mp3 (uno por sección), sin internet.

Usa Piper (voz neuronal local, el texto no sale del equipo) con la voz es_MX-claude-high.
Uso:  uv run --python 3.12 --with piper-tts --with lameenc python generar-audio.py
Primera vez, descargar la voz:
      uv run --python 3.12 --with piper-tts python -m piper.download_voices \
          --download-dir ~/.local/share/piper-voces es_MX-claude-high
Los .mp3 quedan en audio/ (ignorado por git: pesan demasiado para el repositorio).
(edge-tts, la voz colombiana de Microsoft, quedó bloqueado con error 403 en octubre de 2026.)
"""
import re
import unicodedata
import wave
from io import BytesIO
from pathlib import Path

import lameenc
from piper import PiperVoice

VOZ = Path.home() / ".local/share/piper-voces/es_MX-claude-high.onnx"
AQUI = Path(__file__).parent
ORIGEN = AQUI / "analisis-alternativas.md"
DESTINO = AQUI / "audio"


def limpiar(linea: str) -> str:
    t = linea
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)          # enlaces
    t = t.replace("**", "").replace("`", "").replace("*", "")
    t = re.sub(r"\$\$\$\$", "cuatro signos de pesos", t)
    t = re.sub(r"\$\$\$", "tres signos de pesos", t)
    t = re.sub(r"\$\$", "dos signos de pesos", t)
    t = re.sub(r"(?<![\w])\$(?![\w])", "un signo de pesos", t)
    t = re.sub(r"USD\s?([\d.,]+)", r"\1 dólares", t)
    t = re.sub(r"(\d)\s?[–-]\s?(\d)", r"\1 a \2", t)         # rangos 2–4
    t = re.sub(r"×\s?([\d,]+)", r"\1 veces", t)
    t = re.sub(r"([\d,]+)\s?×", r"\1 veces", t)
    t = t.replace("≈0", "casi cero")
    t = re.sub(r"(\d)\s?min\b", r"\1 minutos", t)
    t = re.sub(r"(\d)\s?ms\b", r"\1 milisegundos", t)
    t = re.sub(r"(\d)\s?s\b", r"\1 segundos", t)
    t = re.sub(r"(\d)\s?h\b", r"\1 horas", t)
    reemplazos = {
        "→": ", lleva a, ", "⇒": ", o sea, ", "·": ",", "≈": "aproximadamente ",
        "~": "unos ", "×": " veces", "≥": "mayor o igual a ", "≤": "menor o igual a ",
        " < ": " menos de ", " > ": " más de ", "<": "menos de ", ">": "más de ",
        "/mes": " al mes", "/año": " al año", "/GB": " por gigabyte", "D8-bis": "decisión 8 bis",
        "−": "menos ", "|": ",", "_": " ",
    }
    for a, b in reemplazos.items():
        t = t.replace(a, b)
    t = re.sub(r"\bD(\d+)\b", r"decisión \1", t)
    t = re.sub(r"[\U0001F300-\U0001FAFF☀-➿🟢🟡🔴🔵⬜✅]", "", t)
    return re.sub(r"\s+", " ", t).strip(" ,")


def a_texto(md: str) -> str:
    salida, en_codigo = [], False
    for linea in md.splitlines():
        if linea.strip().startswith("```"):
            en_codigo = not en_codigo
            if en_codigo:
                salida.append("Aquí hay un diagrama en el documento; se omite en el audio.")
            continue
        if en_codigo or re.fullmatch(r"\|?[\s|:-]*\|?", linea.strip()) or linea.strip() == "---":
            continue
        if linea.startswith("|"):
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if not any(celdas):
                continue
            if len(celdas) == 2:
                clave, valor = celdas
                salida.append(f"{limpiar(clave)}: {limpiar(valor) or 'pendiente'}.")
            else:
                salida.append(". ".join(limpiar(c) for c in celdas if c) + ".")
            continue
        linea = re.sub(r"^#+\s*", "", linea).lstrip("> ").strip()
        if linea:
            texto = limpiar(linea)
            salida.append(texto if texto.endswith((".", ":", "?")) else texto + ".")
    return "\n".join(salida)


def secciones(md: str):
    partes = re.split(r"(?m)^## ", md)
    yield "00-introduccion", partes[0]
    for i, parte in enumerate(partes[1:], start=1):
        titulo = parte.splitlines()[0]
        titulo = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
        nombre = re.sub(r"[^a-z0-9]+", "-", titulo.lower().split("(")[0]).strip("-")[:40].strip("-")
        yield f"{i:02d}-{nombre}", "## " + parte


def a_mp3(voz: PiperVoice, texto: str, ruta: Path) -> None:
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav:
        voz.synthesize_wav(texto, wav)
    buffer.seek(0)
    with wave.open(buffer, "rb") as wav:
        pcm, canales, tasa = wav.readframes(wav.getnframes()), wav.getnchannels(), wav.getframerate()
    codificador = lameenc.Encoder()
    codificador.set_bit_rate(64)
    codificador.set_in_sample_rate(tasa)
    codificador.set_channels(canales)
    codificador.set_quality(2)
    ruta.write_bytes(codificador.encode(pcm) + codificador.flush())


def main():
    DESTINO.mkdir(exist_ok=True)
    voz = PiperVoice.load(str(VOZ))
    for nombre, md in secciones(ORIGEN.read_text(encoding="utf-8")):
        texto = a_texto(md)
        (DESTINO / f"{nombre}.txt").write_text(texto, encoding="utf-8")
        a_mp3(voz, texto, DESTINO / f"{nombre}.mp3")
        print(f"listo: {nombre}.mp3", flush=True)


if __name__ == "__main__":
    main()
