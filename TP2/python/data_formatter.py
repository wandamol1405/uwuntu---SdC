from api_client import fetch_gini_data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "gini_values.txt")

def extract_values(data):
    values = []
    for entry in data:
        value = entry.get("value")

        if value is None:
            continue

        values.append(float(value))

    return values

def export_to_file(data: list[float], path: str):
    try:
        with open(path, "w") as f:
            for value in data:
                f.write(f"{value}\n")
        print(f"[INFO] Exportados {len(data)} valores a {path}")

    except IOError as e:
        print(f"[ERROR] No se pudo escribir en el archivo: {e}")

def main():
    print("[INFO] Obteniendo datos desde API...")
    raw_data = fetch_gini_data()
    print(f"[INFO] Datos obtenidos: {len(raw_data)} entradas")

    # debugging: mostrar algunos datos para verificar formato
    # print(type(raw_data))
    # print(raw_data[:2])  # Mostrar las primeras entradas para verificar formato
    # print(raw_data[0].keys())  # Mostrar las claves de la primera entrada

    print("[INFO] Extrayendo valores...")
    values = extract_values(raw_data)
    print(f"[INFO] Valores extraídos: {len(values)}")

    # debugging: mostrar algunos valores extraídos
    # print(f"[INFO] Valores: {values[:5]}")  # Mostrar los primeros 5 valores
    # print(f"[INFO] Tipo de valores: {type(values[0])}")

    print("[INFO] Exportando valores a archivo...")
    export_to_file(values, OUTPUT_PATH)

if __name__ == "__main__":
    main()