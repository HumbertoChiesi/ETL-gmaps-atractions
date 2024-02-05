from __future__ import annotations
import pandas as pd
import re
import ast
import spacy
from nltk.corpus import stopwords
from unidecode import unidecode
from unicodedata import normalize
from nltk.tokenize import word_tokenize

from webscrapping_module.manipulador_cadeia.manipulador_abstrato import ManipuladorAbstrato
from webscrapping_module.manipulador_cadeia.cadeia_vars import coluna_comentario, spacy_pt


class ManipuladorLimparTextoComentarios(ManipuladorAbstrato):
    def __init__(self):
        self.nlp = spacy.load(spacy_pt)

    def processar_texto_comentario(self, text):
        text = " ".join(ast.literal_eval(text))

        texto_minusculo = text.lower()

        texto_sem_ascento = normalize('NFKD', texto_minusculo).encode('ASCII', 'ignore').decode('ASCII')

        texto_sem_char_especial = re.sub(r'[^a-zA-Z\s]', '', texto_sem_ascento)

        texto_tokens = word_tokenize(texto_sem_char_especial, language='portuguese')

        stop_words = set(stopwords.words('portuguese'))
        stop_words = [unidecode(palavra) for palavra in stop_words]
        texto_sem_stopwords = [palavra for palavra in texto_tokens if palavra not in stop_words]

        doc = self.nlp(str([palavra for palavra in texto_sem_stopwords]))

        palavras_lemma = [token.lemma_ for token in doc if token.pos_ == 'NOUN']

        return " ".join(palavras_lemma)

    def manipular(self, request: pd.DataFrame) -> pd.DataFrame:
        if isinstance(request, pd.DataFrame):
            df = request
        else:
            raise Exception(
                f"Tipo do dado esperado do dado 'pd.DataFrame', recebido '{type(request)}'")

        try:
            df[coluna_comentario] = df[coluna_comentario].apply(self.processar_texto_comentario)
        except KeyError as e:
            raise Exception(
                f"A coluna comentarios não foi encontrada no df localizado em '{request}': {e}")
        except Exception as e:
            raise Exception(
                f"ERRO': {e}")

        return super().manipular(df)
