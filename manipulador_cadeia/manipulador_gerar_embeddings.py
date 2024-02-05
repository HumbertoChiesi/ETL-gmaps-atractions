from __future__ import annotations
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import coluna_palavras_chave, coluna_embedding, modelo_bert \
     , caminho_csv_atracoes_tratado


class ManipuladorGerarEmbeddings(ManipuladorAbstrato):
    def manipular(self, request: pd.DataFrame) -> dict:
        if isinstance(request, pd.DataFrame):
            df = request
        else:
            raise Exception(
                f"Tipo do dado esperado do dado 'pd.DataFrame', recebido '{type(request)}'")

        try:
            palavras_chaves_por_documento = list(df[coluna_palavras_chave])
        except KeyError as e:
            raise Exception(
                f"A coluna palavras_chave não foi encontrada no df localizado em '{request}': {e}")

        try:
            tokenizer = AutoTokenizer.from_pretrained(modelo_bert)
            model = AutoModel.from_pretrained(modelo_bert)
        except Exception as e:
            raise Exception(
                f"ERRO enquanto carregava o modelo BERTimbau: {e}")

        embeddings_list = []
        for string in palavras_chaves_por_documento:
            inputs = tokenizer(string, return_tensors="pt", padding=True, truncation=True)

            with torch.no_grad():
                embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Mean pooling of embeddings
                embeddings_list.append(embeddings)

        data_list = [tensor.tolist() for tensor in embeddings_list]

        df[coluna_embedding] = data_list

        df.to_csv(caminho_csv_atracoes_tratado, index=False)

        return super().manipular({'atracoes': caminho_csv_atracoes_tratado})
