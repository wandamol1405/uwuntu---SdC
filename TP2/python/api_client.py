import requests
import json

URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"

# Función para obtener los datos del índice de GINI desde la API del Banco Mundial
def fetch_gini_data() -> list:
    try:
        response = requests.get(URL, timeout=10)

        # Verificar status HTTP
        if response.status_code != 200:
            print(f"Error HTTP: {response.status_code}")
            return []

        data = response.json()

        # Validar estructura esperada
        if not isinstance(data, list) or len(data) < 2:
            print("Formato de respuesta inválido")
            return []

        records = data[1]  # acá estan los datos reales

        result = []

        for item in records:
            # Filtrar solo Argentina
            if item["country"]["value"] != "Argentina":
                continue

            value = item["value"]

            # Filtrar valores nulos
            if value is None:
                continue

            result.append({
                "country": item["country"]["value"],
                "year": int(item["date"]),
                "value": float(value)
            })

        return result

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return []

    except ValueError:
        print("Error parseando JSON")
        return []

# Función para guardar los datos en un archivo JSON
def save_to_json(data: list, filename="gini_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error guardando archivo: {e}")


if __name__ == "__main__":
    gini_data = fetch_gini_data()

    print("Datos obtenidos:")
    for entry in gini_data:
        print(entry)

    save_to_json(gini_data)