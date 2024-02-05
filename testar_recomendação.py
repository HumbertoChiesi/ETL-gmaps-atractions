# -*- coding: utf-8 -*-
import ast
import pandas as pd
from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.neighbors import NearestNeighbors


def transform_to_array(text):
    array = ast.literal_eval(text)
    return array[0]


if __name__ == "__main__":
    new_string = input("Digite palavras chave: ").lower()

    pd.set_option('display.max_columns', None)
    df = pd.read_csv('./arquivos_finais/atraçoes_tratadas.csv')
    df['embeddings'] = df['embeddings'].apply(transform_to_array)

    place_embeddings = list(df['embeddings'])
    place_names = list(df['nome'])

    k = 10
    nn_model = NearestNeighbors(n_neighbors=k)
    nn_model.fit(place_embeddings)

    tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
    model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')

    new_inputs = tokenizer(new_string, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        new_embedding = model(**new_inputs).last_hidden_state.mean(dim=1)  # Mean pooling of embeddings

    query_data = new_embedding.tolist()

    distances, indices = nn_model.kneighbors(query_data)

    print(f'LUGARES MAIS PROXIMOS DE "{new_string}"\n')
    i = 0
    for idx in indices[0]:
        i += 1
        print(str(i) + " - " + place_names[idx])
