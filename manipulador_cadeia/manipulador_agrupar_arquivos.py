import os
import pandas as pd

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import caminho_csv_em_tratamento, coluna_id_atracao


class ManipuladorAgruparArquivos(ManipuladorAbstrato):
    def manipular(self, request: str) -> pd.DataFrame:
        arquivos_csv = [request + arquivo for arquivo in
                        os.listdir(request) if arquivo.endswith('.csv')]

        if not arquivos_csv:
            raise Exception(
                f"Não foi encontrado nenhum arquivo CSV no diretório '{request}' para Agrupação de arquivos")

        # df_dados_combinados: df utilizado para unir todos os arquivos de tipos de atrações
        df_dados_combinados = pd.DataFrame()

        # Leio cada arquivo CSV e anexo ao df_dados_combinados
        for csv_file in arquivos_csv:
            df = pd.read_csv(csv_file)
            df_dados_combinados = df_dados_combinados.append(df, ignore_index=True)

        df_dados_combinados.drop_duplicates(subset='nome', keep='first')
        df_dados_combinados[coluna_id_atracao] = [i for i in range(0, len(df_dados_combinados))]

        df_dados_combinados.to_csv(caminho_csv_em_tratamento, index=False)

        return super().manipular(df_dados_combinados)