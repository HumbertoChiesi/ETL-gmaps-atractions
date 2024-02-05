import pandas as pd
from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import coluna_qtd_avaliacao, coluna_avaliacao


class ManipuladorTratarDadosAvaliacoes(ManipuladorAbstrato):
    def transformar_avaliacao_float(self, text):
        return float(text.replace(',', '.'))

    def transformar_qtd_avaliacao_int(self, text):
        return int(text.replace('(', '').replace(')', '').replace('.', ''))

    def manipular(self, request: pd.DataFrame) -> pd.DataFrame:
        if isinstance(request, pd.DataFrame):
            df = request
        else:
            raise Exception(
                f"Tipo do dado esperado do dado 'pd.DataFrame', recebido '{type(request)}'")

        try:
            df[coluna_avaliacao] = df[coluna_avaliacao].apply(self.transformar_avaliacao_float)
        except KeyError as e:
            raise Exception(
                f"A coluna avaliacao não foi encontrada no df localizado em '{request}': {e}")
        except Exception as e:
            raise Exception(
                f"ERRO': {e}")

        try:
            df[coluna_qtd_avaliacao] = df[coluna_qtd_avaliacao].apply(self.transformar_qtd_avaliacao_int)
        except KeyError as e:
            raise Exception(
                f"A coluna qtd_avaliacao não foi encontrada no df localizado em '{request}': {e}")
        except Exception as e:
            raise Exception(
                f"ERRO': {e}")

        return super().manipular(df)
