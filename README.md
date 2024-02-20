# Google Maps Attractions ETL

Project developed for extracting and processing information about places from Google Maps, to be used in a Touristic recommendation system.

## Process Steps:
Extraction is performed via Web Scraping using Python, Selenium, and threading.

Next, a sequence of steps for data processing begins, including the creation of new fields based on the obtained information (latitude, longitude, keywords, and embeddings).

Finally, the data is inserted into a SQL database.

## Embeddings Generation:
From the comments of each Google Maps places extracted, keywords are extracted using the TF-IDF statistical measure.

Then, for each place, the text containing all the keywords of the place is used to obtain embeddings using the BERTimbau* model.

## Recommendation Process:
Upon receiving an input text, an embedding is generated using the BERTimbau* model.

This embedding is compared with the embeddings of the places extracted using the KNN method with cosine similarity, to find the most similar places to the input text.


``` *BERTimbau is a pretrained BERT model for Brazilian Portuguese. ```

# Examples of recommendation results based on keywords:
![teste](https://i.imgur.com/LtcgeLe.png) ![teste](https://i.imgur.com/opKr1My.png) ![teste](https://i.imgur.com/u2iTjcq.png)

# Subset of the Database Populated by the Process:
![teste](https://i.imgur.com/IcwgRyG.png)
