from __future__ import annotations
import json
import pandas as pd

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import nome_tabela_atracoes, nome_tabela_atracoes_horarios, \
    caminho_csv_tabela_horarios, coluna_horario, coluna_id_dia_semana, coluna_id_atracao, coluna_aberto


class ManipuladorGerarTabelaHorarios(ManipuladorAbstrato):
    def manipular(self, request: dict) -> dict:
        try:
            caminho_df = request[nome_tabela_atracoes]
        except Exception as e:
            raise Exception(
                f"Campo atracoes não encontrado no dict recebido no request: {e}")

        try:
            df = pd.read_csv(caminho_df)
        except Exception as e:
            raise Exception(
                f"CSV não encontrado no caminho '{caminho_df}': {e}")

        try:
            lista_atracoes_id = df['atracao_id']
        except KeyError as e:
            raise Exception(
                f"A coluna atracao_id não foi encontrada no df localizado em '{caminho_df}': {e}")

        lista_horarios_atracoes = [json.loads(horario.replace("'", '"')) for horario in
                                   list(df['horarios'])]

        lista_registros_tabela_horario = []
        dicionario_registro_horario = {}

        dicionario_dia_id = {'segunda-feira': 0, 'terça-feira': 1, 'quarta-feira': 2, 'quinta-feira': 3,
                             'sexta-feira': 4, 'sábado': 5, 'domingo': 6}

        for index in range(0, len(lista_atracoes_id)):
            for dia, horario in lista_horarios_atracoes[index].items():
                dicionario_registro_horario[coluna_id_atracao] = lista_atracoes_id[index]
                dicionario_registro_horario[coluna_id_dia_semana] = dicionario_dia_id[dia]
                dicionario_registro_horario[coluna_horario] = horario

                if horario == "Fechado":
                    dicionario_registro_horario[coluna_aberto] = 0
                else:
                    dicionario_registro_horario[coluna_aberto] = 1

                lista_registros_tabela_horario.append(dicionario_registro_horario)
                dicionario_registro_horario = {}

        atracoes_horarios_df = pd.DataFrame(lista_registros_tabela_horario)
        atracoes_horarios_df.to_csv(caminho_csv_tabela_horarios, index=False)

        request[nome_tabela_atracoes_horarios] = caminho_csv_tabela_horarios

        return super().manipular(request)
