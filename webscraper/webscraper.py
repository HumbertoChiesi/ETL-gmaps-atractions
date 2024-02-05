from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

class webScrapping:
    """
    Classe responsável por realizar web scraping no Google Maps para obter informações sobre atrações
    """
    def __init__(self, chrome_driver_path):
        self.df_lugares = None
        self.dicionario_links_atracoes = {}
        self.driver = webdriver.Chrome(chrome_driver_path)

    def obter_links(self, tipo_lugar, lista_localidades):
        """
        Obtém os links das atrações para um determinado tipo de lugar e lista de localidades

        :param tipo_lugar: Tipo de lugar a ser pesquisado.
        :param lista_localidades: Lista de localidades para pesquisar.
        :return: None
        """

        self.dicionario_links_atracoes[tipo_lugar] = []

        #para cada elemento de lista_localidades, procuro o tipo_lugar e salvo todos os URL achados em dicionario_links_atracoes
        for localidade in lista_localidades:
            self.driver.get(f'https://www.google.com.br/maps/search/{tipo_lugar},{localidade}')

            contador_scroll_fim_tela = 0

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')))

            while contador_scroll_fim_tela < 15:
                scrollable_div = self.driver.find_element(By.XPATH,
                                                          '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass

                time.sleep(2)
                contador_scroll_fim_tela = contador_scroll_fim_tela + 1

            elementos_lugares = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            self.dicionario_links_atracoes[tipo_lugar].extend([elem.get_attribute("href") for elem in elementos_lugares])

        self.dicionario_links_atracoes[tipo_lugar] = list(set(self.dicionario_links_atracoes[tipo_lugar]))

    def obter_dados_dicionario_links_atracoes(self):
        """
        Obtém os dados para as atrações com base nos links previamente coletados
        e armazenados em self.dicionario_links_atracoes

        :return: None
        """
        for tipo_lugar, links in self.dicionario_links_atracoes.items():
            self.obter_dados(links, tipo_lugar, tipo_lugar)

    def obter_dados(self, lista_links, tipo_lugar, nome_arquivo):
        """
        Obtém dados detalhados para cada atração a partir de uma lista de links

        :param lista_links: Lista de links das atrações.
        :param tipo_lugar: Tipo de lugar das atrações.
        :param nome_arquivo: Nome do arquivo para salvar os dados.
        :return: None
        """

        #lista_lugares: lista de dicionarios que guardam informações de cada atração
        lista_lugares = []

        for link in lista_links:
            self.driver.get(link)

            #dicionario_lugar: dicionario que irá representar um registro do lugar no BD, guarda os dados do lugar
            dicionario_atracao = {}

            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'DUwDvf')))
                nome_lugar = self.driver.find_element(By.CLASS_NAME, "DUwDvf").text
            except:
                continue

            #verifico se o lugar está fechado (temporariamente ou definitivamente)
            #se fechado -> passo para a próxima atração
            try:
                img_elements = self.driver.find_elements_by_xpath(
                    '//img[@src="//maps.gstatic.com/consumer/images/icons/1x/change_history_red600_24dp.png"]')
                if img_elements:
                    continue
            except:
                pass

            #procuro a quantidade de avaliações, se não encontrado -> informação faltante
            try:
                element = self.driver.find_element_by_xpath(
                    '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span')
                quantidade_avaliacoes = element.text
            except:
                quantidade_avaliacoes = ''

            #procuro o preço da atração, se não encontrado -> informação faltante
            try:
                preco = self.driver.find_element(By.CLASS_NAME, "drwWxc").text
            except:
                preco = ''

            #procuro o endereco da atração, se não encontrado -> passa para a próxima atração
            try:
                endereco = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']").get_attribute(
                    "aria-label")
                endereco = endereco[endereco.find(":") + 2:] if ":" in endereco else endereco
            except:
                continue

            #procuro a imagem da atração, se não encontrado -> informação faltante
            try:
                button_element = self.driver.find_element_by_class_name("aoRNLd")
                img_element = button_element.find_element_by_tag_name("img")
                imagem = img_element.get_attribute("src")
            except:
                imagem = ''

            #procuro a descrição da atração, se não encontrado -> informação faltante
            try:
                descricao = self.driver.find_element_by_class_name("PYvSYb").text
            except:
                descricao = ''

            #procuro o telefone da atração, se não encontrado -> informação faltante
            try:
                telefone = self.driver.find_element(By.XPATH,
                                                    "//button[starts-with(@data-item-id,'phone')]").get_attribute(
                    "aria-label")
                telefone = telefone[telefone.find("+"):] if "+" in telefone else telefone
            except:
                telefone = ''

            #procuro a média de avaliação do lugar, se não encontrado -> informação faltante
            try:
                avaliacao = self.driver.find_element(By.XPATH, "//div[@class='F7nice ']/span").text
            except:
                avaliacao = ''

            #procuro o mapa disponibilizado pelo google como elemento HTML, se não encontrado -> informação faltante
            try:
                button = self.driver.find_element_by_css_selector('button[data-value="Compartilhar"]')
                button.click()
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'YTfrze')))
                button = self.driver.find_element(By.CLASS_NAME, "YTfrze")
                button.click()
                input_element = self.driver.find_element_by_css_selector('input.yA7sBe')
                elemento_mapa = input_element.get_attribute('value')
                button = self.driver.find_element(By.CLASS_NAME, "AmPKde")
                button.click()
            except:
                elemento_mapa = ""

            #procuro as reviews escritas da atração, se não encontrado -> passa para a próxima atração
            try:
                botao = self.driver.find_element(By.XPATH,
                                                 '//button[contains(@class, "hh2c6") and @data-tab-index="1"]')
                botao.click()

                time.sleep(2.5)

                contador_scroll_fim_tela = 0
                while contador_scroll_fim_tela < 3:
                    scrollable_div = self.driver.find_element(By.XPATH,
                                                              '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
                    try:
                        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                    except:
                        pass
                    time.sleep(1)
                    contador_scroll_fim_tela = contador_scroll_fim_tela + 1

                botoes = self.driver.find_elements(By.CLASS_NAME, "w8nwRe")
                for botao in botoes:
                    botao.click()

                comentarios = []

                div_elements = self.driver.find_elements(By.CLASS_NAME, 'MyEned')
                for div_element in div_elements:
                    span_element = div_element.find_element(By.CLASS_NAME, 'wiI7pd')
                    comentarios.append(span_element.text.replace("…", ""))

            except:
                comentarios = []

            if comentarios == []:
                continue

            #procuro o horário de funcionamento da atração, se não encontrado -> informação faltante
            try:
                botao = self.driver.find_element(By.XPATH,
                                                 '//button[contains(@class, "hh2c6") and @data-tab-index="0"]')
                botao.click()
                time.sleep(0.75)
                img_element = self.driver.find_element_by_xpath("//img[contains(@src, 'schedule_gm_blue_24dp.png')]")
                self.driver.execute_script("arguments[0].parentNode.click();", img_element)
                time.sleep(0.5)

                tabela_horarios = self.driver.find_element_by_css_selector("table.eK4R0e.fontBodyMedium")

                dicionario_horarios = {}

                rows = tabela_horarios.find_elements_by_css_selector("tr.y0skZc")

                for row in rows:
                    div_element = row.find_element_by_css_selector("td.ylH6lf div")
                    td_adjacent = row.find_element_by_css_selector("td.mxowUb")
                    horario = td_adjacent.get_attribute("aria-label")
                    dicionario_horarios[div_element.text] = horario

            except:
                dicionario_horarios = {}

            #adiciono todas as informações no dicionario da atração e insiro o dicionario na lista de lugares
            dicionario_atracao['nome'] = nome_lugar
            dicionario_atracao['preco'] = preco
            dicionario_atracao['elemento_mapa'] = elemento_mapa
            dicionario_atracao['horarios'] = dicionario_horarios
            dicionario_atracao['descricao'] = descricao
            dicionario_atracao['imagem_url'] = imagem
            dicionario_atracao['endereco'] = endereco
            dicionario_atracao['avaliacao'] = avaliacao
            dicionario_atracao['qtd_avaliacao'] = quantidade_avaliacoes
            dicionario_atracao['comentarios'] = comentarios
            dicionario_atracao['telefone'] = telefone
            dicionario_atracao['lugar_tipo'] = tipo_lugar
            dicionario_atracao['url'] = self.driver.current_url
            lista_lugares.append(dicionario_atracao)

        df = pd.DataFrame(lista_lugares)
        self.df_lugares = df
        df.to_csv(f"./arquivos_sem_tratamento/{nome_arquivo}.csv", index=False)
