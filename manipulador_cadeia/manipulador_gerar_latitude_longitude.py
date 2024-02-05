import pandas as pd

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import coluna_latitude, coluna_url, coluna_longitude


class ManipuladorGerarLatitudeLongitude(ManipuladorAbstrato):
    def manipular(self, request: pd.DataFrame) -> pd.DataFrame:
        if isinstance(request, pd.DataFrame):
            df = request
        else:
            raise Exception(
                f"Tipo do dado esperado do dado 'pd.DataFrame', recebido '{type(request)}'")

        try:
            lista_url_atracoes = list(df[coluna_url])
        except KeyError as e:
            raise Exception(
                f"A coluna qtd_avaliacao não foi encontrada no df localizado em '{request}': {e}")

        lista_latitude = []
        lista_longitude = []

        try:
            for url in lista_url_atracoes:
                latitude, longitude = url.split('@')[1].split(',')[0:2]
                lista_latitude.append(float(latitude))
                lista_longitude.append(float(longitude))
        except Exception as e:
            raise Exception(
                f"Não foi possível extrair a latitude e longitude do df localizado em '{request}': {e}")

        df[coluna_latitude] = lista_latitude
        df[coluna_longitude] = lista_longitude

        return super().manipular(df)
