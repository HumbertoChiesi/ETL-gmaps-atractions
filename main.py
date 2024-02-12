from webscrapping_module.orquestrador import Orquestrador


def main():
    caminho_driver_chrome = ''  # caminho para o chrome driver
    lista_localidades = []  # ex: ['são paulo, centro', 'são paulo, zona oeste']
    lista_tipo_lugar = []  # ex ['restaurante', 'museu']

    orquestrador = Orquestrador(caminho_driver_chrome, lista_localidades, lista_tipo_lugar)
    orquestrador.iniciar_webscrapping()
    orquestrador.iniciar_cadeia()


if __name__ == "__main__":
    main()
