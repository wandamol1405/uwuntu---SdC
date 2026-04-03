from api_client import fetch_gini_data


def main():
    data = fetch_gini_data()

    print("Datos GINI procesados:")
    for d in data:
        print(d)

    # FUTURO:
    # pasar datos a C


if __name__ == "__main__":
    main()