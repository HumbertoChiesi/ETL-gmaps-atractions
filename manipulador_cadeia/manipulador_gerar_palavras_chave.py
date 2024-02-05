from __future__ import annotations
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import coluna_comentario


class ManipuladorGerarPalavrasChave(ManipuladorAbstrato):
    def manipular(self, request: pd.DataFrame) -> pd.DataFrame:
        if isinstance(request, pd.DataFrame):
            df = request
        else:
            raise Exception(
                f"Tipo do dado esperado do dado 'pd.DataFrame', recebido '{type(request)}'")

        try:
            comentarios_atracoes = list(df[coluna_comentario])

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(comentarios_atracoes)
            feature_names = tfidf_vectorizer.get_feature_names_out()

            num_palavras_chaves = 200
            palavras_chaves_por_documento = []

            for i in range(len(comentarios_atracoes)):
                doc_vector = tfidf_matrix[i].toarray().flatten()
                top_indices = doc_vector.argsort()[-num_palavras_chaves:][::-1]
                palavras_chaves = [feature_names[idx] for idx in top_indices]
                palavras_chaves_por_documento.append(palavras_chaves)

            palavras_chaves_por_documento = [' '.join(keywords) for keywords in palavras_chaves_por_documento]

            df['palavras_chave'] = palavras_chaves_por_documento
        except KeyError as e:
            raise Exception(
                f"A coluna comentarios não foi encontrada no df localizado em '{request}': {e}")
        except Exception as e:
            raise Exception(
                f"ERRO': {e}")

        return super().manipular(df)
