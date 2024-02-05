from __future__ import annotations
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, INT, TEXT, FLOAT


from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import schemas, bd_nome_usuario, senha_usuario, bd_host, nome_db


class ManipuladorInserirDadosBD(ManipuladorAbstrato):
    def manipular(self, request: dict) -> str:
        username = bd_nome_usuario
        password = senha_usuario
        host = bd_host
        database_name = nome_db

        try:
            print('conectando com o banco...')
            engine = create_engine(f'mysql+pymysql://{username}@{host}/{database_name}')
            print('conectado')
        except Exception as e:
            raise Exception(
                f"Falha na conexão com o banco de dados: {e}")

        for tabela in request.keys():
            df = pd.read_csv(request[tabela])
            df.to_sql(tabela, con=engine, if_exists='append', index=False, dtype=schemas[tabela])

        return f'Tabelas {list(request.keys())} inseridas no BD com sucesso'