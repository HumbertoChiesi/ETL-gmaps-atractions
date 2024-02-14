# ETL atrações google maps
Projeto desenvolvido para extração e tratamento de informações sobre atrações do Google Maps, para serem utilizadas em um sistema de recomendação Turístico.

## Etapas do processo:

- A extração é feita via Web Scraping utilizando Python, Selenium e threading.
  
- Em seguida, inicia-se uma sequência de etapas para o tratamento dos dados, incluindo a criação de novos campos com base nas informações obtidas (latitude, longitude, palavras-chave e embeddings).
  
- Por fim, os dados são inseridos em um banco de dados SQL.

## Geração dos embeddings:

- A partir dos comentários de cada atração, são extraídas palavras-chave utilizando a medida estatística TF-IDF.

- Em seguida, o texto das palavras-chave é utilizado para obter os embeddings utilizando o modelo BERTimbau.

## Processo de recomendação:

- Recebendo um texto de entrada, é gerado um embedding utilizando o modelo BERTimbau.

- Este embedding é comparado com os embeddings das atrações utilizando o método KNN com similaridade por cosseno, para encontrar as atrações mais similares ao texto de entrada.

# Exemplos de resultados de recomendação com base em palavras chave:
![teste](https://i.imgur.com/LtcgeLe.png) ![teste](https://i.imgur.com/opKr1My.png) ![teste](https://i.imgur.com/u2iTjcq.png)

# Recorte de parte da DB que é alimentada pelo processo:
![teste](https://i.imgur.com/IcwgRyG.png)
