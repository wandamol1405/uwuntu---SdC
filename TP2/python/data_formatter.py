from api_client import fetch_gini_data
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "gini_values.txt")


def log(message: str, level: str = "INFO"):
    now = time.strftime("%H:%M:%S")
    print(f"[{level}] {now} | {message}")


def separator():
    print("=" * 50)


def extract_values(data):
    values = []
    skipped = 0

    for entry in data:
        value = entry.get("value")
        if value is None:
            skipped += 1
            continue
        values.append(float(value))

    return values, skipped


def export_to_file(data: list[float], path: str):
    try:
        with open(path, "w", encoding="utf-8") as f:
            for value in data:
                f.write(f"{value}\n")
        log(f"Exportados {len(data)} valores a: {path}", "OK")
    except IOError as e:
        log(f"No se pudo escribir en el archivo: {e}", "ERROR")


def main():
    start = time.perf_counter()
    separator()
    log("Inicio del proceso")
    log("Obteniendo datos desde API...")

    try:
        raw_data = fetch_gini_data()
    except Exception as e:
        log(f"Error al obtener datos: {e}", "ERROR")
        separator()
        return

    log(f"Datos obtenidos: {len(raw_data)} entradas")

    log("Extrayendo valores...")
    values, skipped = extract_values(raw_data)
    log(f"Valores extraídos: {len(values)}")
    log(f"Entradas ignoradas (value=None): {skipped}", "WARN" if skipped else "INFO")

    log("Exportando valores a archivo...")
    export_to_file(values, OUTPUT_PATH)

    elapsed = time.perf_counter() - start
    log(f"Proceso finalizado en {elapsed:.2f}s", "OK")
    separator()


if __name__ == "__main__":
    main()