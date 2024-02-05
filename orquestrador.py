import threading

from webscrapping_module.manipulador_cadeia.manipulador_agrupar_arquivos import ManipuladorAgruparArquivos
from webscrapping_module.manipulador_cadeia.manipulador_gerar_embeddings import ManipuladorGerarEmbeddings
from webscrapping_module.manipulador_cadeia.manipulador_gerar_latitude_longitude import \
    ManipuladorGerarLatitudeLongitude
from webscrapping_module.manipulador_cadeia.manipulador_gerar_palavras_chave import ManipuladorGerarPalavrasChave
from webscrapping_module.manipulador_cadeia.manipulador_gerar_tabela_horarios import ManipuladorGerarTabelaHorarios
from webscrapping_module.manipulador_cadeia.manipulador_inserir_dados_BD import ManipuladorInserirDadosBD
from webscrapping_module.manipulador_cadeia.manipulador_limpar_texto_comentarios import \
    ManipuladorLimparTextoComentarios
from webscrapping_module.manipulador_cadeia.manipulador_tratar_dados_avaliacoes import ManipuladorTratarDadosAvaliacoes
from webscrapping_module.webscraper.webscraper import webScrapping


class Orquestrador:
    def __init__(self, chrome_driver_path, lista_localidades, lista_tipo_lugar):
        self.chrome_driver_path = chrome_driver_path
        self.lista_localidades = lista_localidades
        self.lista_tipo_lugar = lista_tipo_lugar

    def _escolher_tipo_lugares_processar(self):
        """
        retorna 3 ou restantes elementos da lista self.lista_tipo_lugar

        :return: lista com tipo de lugar a ser processado
        """
        if len(self.lista_tipo_lugar) > 3:
            tipo_lugares_para_processar = [self.lista_tipo_lugar.pop(0) for i in range(0, 3)]
        else:
            tipo_lugares_para_processar = self.lista_tipo_lugar
            self.lista_tipo_lugar = []

        return tipo_lugares_para_processar

    def iniciar_cadeia(self):
        """
        Inicia a cadeia de manipuladores para processamento de dados

        :return: None
        """
        agrupador = ManipuladorAgruparArquivos()
        limpar_texto = ManipuladorLimparTextoComentarios()
        tratar_avaliacoes = ManipuladorTratarDadosAvaliacoes()
        gerar_lat_long = ManipuladorGerarLatitudeLongitude()
        gerar_palavras_chave = ManipuladorGerarPalavrasChave()
        gerar_embedding = ManipuladorGerarEmbeddings()
        gerar_tabela_horario = ManipuladorGerarTabelaHorarios()
        inserir_bd = ManipuladorInserirDadosBD()

        agrupador.definir_proximo(limpar_texto).definir_proximo(tratar_avaliacoes).definir_proximo(gerar_lat_long) \
            .definir_proximo(gerar_palavras_chave).definir_proximo(gerar_embedding) \
            .definir_proximo(gerar_tabela_horario).definir_proximo(inserir_bd)

        agrupador.manipular(
            './arquivos_sem_tratamento/atrações/')

    def iniciar_webscrapping(self):
        """
        Inicia o processo de web scraping em threads simultâneas

        :return: None
        """
        lista_tipo_lugares = self._escolher_tipo_lugares_processar()

        while len(lista_tipo_lugares) > 0:
            webscrapper_1 = webScrapping(self.chrome_driver_path)
            webscrapper_2 = webScrapping(self.chrome_driver_path)
            webscrapper_3 = webScrapping(self.chrome_driver_path)

            threads = []

            thread = threading.Thread(target=webscrapper_1.obter_links,
                                      args=(lista_tipo_lugares[0], self.lista_localidades,))
            threads.append(thread)
            thread.start()

            thread = threading.Thread(target=webscrapper_2.obter_links,
                                      args=(lista_tipo_lugares[1], self.lista_localidades,))
            threads.append(thread)
            thread.start()

            thread = threading.Thread(target=webscrapper_3.obter_links,
                                      args=(lista_tipo_lugares[2], self.lista_localidades,))
            threads.append(thread)
            thread.start()

            for thread in threads:
                thread.join()

            threads = []

            thread = threading.Thread(target=webscrapper_1.obter_dados_dicionario_lugares, args=())
            threads.append(thread)
            thread.start()

            thread = threading.Thread(target=webscrapper_2.obter_dados_dicionario_lugares, args=())
            threads.append(thread)
            thread.start()

            thread = threading.Thread(target=webscrapper_3.obter_dados_dicionario_lugares, args=())
            threads.append(thread)
            thread.start()

            for thread in threads:
                thread.join()

            lista_tipo_lugares = self.escolher_tipo_lugar_processar()
