# ETL atrações google maps
Projeto feito para extração de informações sobre atrações do Google Maps para serem utilizadas em um sistema de recomendação Turístico.

- A extração é feita via Web Scraping utilizando Python e Selenium, em até 3 threadings simultâneas.
  
- Logo em seguida é iniciada uma cadeia de tratamento onde os dados serão tratados e também acontece a geração de alguns novos campos com base nos dados coletados (latitude, longitude, palavras-chaves e embeddings).
  
- E finalmente e feito a inserção desses dados em um DB SQL.


# Recorte de parte da DB que é alimentada pelo processo:
![teste](https://i.imgur.com/IcwgRyG.png)

# Exemplos de resultados de recomendação com base em palavras chave:
![teste](https://i.imgur.com/LtcgeLe.png) ![teste](https://i.imgur.com/opKr1My.png) ![teste](https://i.imgur.com/u2iTjcq.png)
