import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from glob import glob
from time import sleep
import tkinter
from tkinter import *
from tkinter import messagebox
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os

################################################################
# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}
### LER/CRIAR FICHEIRO TRACK###
try:
    """Lê o excel com o track das coisas que queremos"""
    prod_tracker = pd.read_excel("TRACKER_TEST2.xlsx")
    search_tracker_log = pd.DataFrame()
    tracker_log = pd.DataFrame()
except:
    """Cria o excel inicial para fazer Track do que queremos"""
    head_excel = ["url", "codigo", "comprar_abaixo"]
    head = pd.DataFrame(columns=head_excel)
    head.to_excel("TRACKER_TEST2.xlsx", index=0)
    """Lê o excel com o track das coisas que queremos"""
    prod_tracker = pd.read_excel("TRACKER_TEST2.xlsx")
    search_tracker_log = pd.DataFrame()
    tracker_log = pd.DataFrame()

### CRIAR FICHEIRO SEARCH CASO NAO EXISTA###
try:
    """Tenta ler o excel com as nossas pesquisas"""
    glob("search_history/*.xlsx")[-1]
except:
    """Cria o excel inicial para fazer registar as pesquisas"""
    head_search_excel = [
        "date",
        "code",
        "url",
        "title",
        "buy_below",
        "review_score",
        "review_count",
        "stock",
    ]
    path = os.getcwd().replace("\\", "/")  # deteta o folder onde estamos
    try:
        os.mkdir(path + "/search_history")
    except:
        pass
    head_search = pd.DataFrame(columns=head_search_excel)
    head_search.to_excel("search_history/SEARCH_HISTORY.xlsx", index=0)

# now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")  # DATA E HORA


class App:
    def __init__(
        self, window, window_title, prod_tracker, search_tracker_log, tracker_log
    ):  # por defeito a video source seria 0; #a funcao init é sempre executada no inicio
        self.window = window  # "tkinter.Tk()"
        self.window.title(window_title)
        self.window.geometry("800x500")
        # path = os.getcwd().replace("\\", "/")
        # path = path + "/icone.png"
        # self.window.iconphoto(False, tkinter.PhotoImage(file=path
        # ))
        # window.attributes('-fullscreen',True) # maximiza a janela

        self.prod_tracker = prod_tracker
        self.search_tracker_log = search_tracker_log
        self.tracker_log = tracker_log
        self.i_track = 0
        self.t_entre_url = 5

        """BOTÕES"""
        #############################################
        """Botão que fecha a aplicação"""
        self.btn_close = tkinter.Button(
            window,
            text="Fechar Aplicação",
            width=15,
            height=1,
            command=self.close_window,
        )
        self.btn_close.place(x=685, y=0)

        """Botão que adiciona um link ao excel do track"""
        self.btn_append_track = tkinter.Button(
            window,
            text="Adicionar Dados à Busca",
            width=20,
            height=1,
            command=self.Append_Excel,
        )
        self.btn_append_track.place(x=180, y=90)

        """Botão que corre o programa"""
        self.btn_append_track = tkinter.Button(
            window, text="Run", width=20, height=1, command=self.Run_Prg,
        )
        self.btn_append_track.place(x=10, y=470)

        """Botão de report"""
        self.btn_report = tkinter.Button(
            window, text="Reporta o problema", width=20, height=1, command=self.Report,
        )
        self.btn_report.place(x=600, y=470)

        ###############################################

        # criacao da listbox
        self.l_box = Listbox(self.window, selectmode="BROWSE", width=25)
        for item in self.prod_tracker.codigo:
            self.l_box.insert("end", item)
        self.l_box.place(x=385, y=0)

        """Cria as labels iniciais"""
        self.Label_Inicial()

        # corre a janela em loop, todos os botões criados estão sempre prontos para serem carregados
        self.window.mainloop()

    # Função para fechar as janelas quando o botão é pressionado
    def close_window(self):
        self.window.destroy()

    def Label_Inicial(self):
        """Entrada de texto relativamente à URL que vamos fazer track"""
        self.leitor_url_text = tkinter.Label(
            self.window,
            text="Url do item",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_url_text.place(x=10, y=30)

        self.leitor_url = tkinter.Entry(self.window)
        self.leitor_url.place(x=10, y=60)

        """Entrada de texto relativamente ao código do utilizador que vamos fazer utilizar para cada objeto"""
        self.leitor_code_text = tkinter.Label(
            self.window,
            text="Código do item",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=15,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_code_text.place(x=10, y=90)

        self.leitor_code = tkinter.Entry(self.window)
        self.leitor_code.place(x=10, y=120)

        """Entrada de texto relativamente ao valor a partir do
         qual o utilizador pretende comprar o objeto"""
        self.leitor_buybellow_text = tkinter.Label(
            self.window,
            text="Preço abaixo do qual pretende o aviso",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=30,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_buybellow_text.place(x=10, y=150)

        self.leitor_buybellow = tkinter.Entry(self.window)
        self.leitor_buybellow.place(x=10, y=180)

        """Entrada de texto relativamente ao intervalo entre pesquisas completas
            quantos dados a pessoa quer ter sobre cada objeto"""
        self.leitor_t_ciclo_text = tkinter.Label(
            self.window,
            text="Intervalo de tempo entre pesquisas completas",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=40,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_t_ciclo_text.place(x=10, y=260)

        self.leitor_t_ciclo = tkinter.Entry(self.window)
        self.leitor_t_ciclo.place(x=10, y=290)

        """Entrada de texto relativamente ao tempo que o programa vai correr"""
        self.leitor_t_total_text = tkinter.Label(
            self.window,
            text="Tempo que o programa corre em minutos",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=40,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_t_total_text.place(x=10, y=320)

        self.leitor_t_total = tkinter.Entry(self.window)
        self.leitor_t_total.place(x=10, y=350)

        """Entrada de texto relativamente ao email para onde vai receber o aviso"""
        self.leitor_mail_text = tkinter.Label(
            self.window,
            text="E-mail para o alerta",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=20,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_mail_text.place(x=10, y=380)

        self.leitor_mail = tkinter.Entry(self.window)
        self.leitor_mail.place(x=10, y=410)

        """Entrada de texto REPORT"""
        self.leitor_report_text = tkinter.Label(
            self.window,
            text="Reportar Erros",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=15,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_report_text.place(x=600, y=410)

        self.leitor_report = tkinter.Entry(self.window, width="30",)
        self.leitor_report.place(x=600, y=440)

        """Tempo mínimo para correr um ciclo"""
        self.t_minimo_text = tkinter.Label(
            self.window,
            text="Tempo mínimo para correr" + "\n"
            "um ciclo completo de pesquisa"
            + "\n"
            + str(int(self.t_entre_url * len(self.prod_tracker.url)))
            + " segundos",
            fg="black",
            font=("Arial", 8),
            width=30,
        )
        self.t_minimo_text.place(x=620, y=270)

        """Lojas permitidas"""
        lojas_permitidas_text = tkinter.Label(
            self.window,
            text="Lojas disponiveis:"
            + "\n"
            + "\n"
            + "PCDiga"
            + "\n"
            + "Worten"
            + "\n"
            + "Amazon"
            + "\n"
            + "Mediamarkt"
            + "\n"
            + "Chip7"
            + "\n"
            + "Globaldata"
            + "\n"
            + "Gamingreplay"
            + "\n"
            + "Mega-mania"
            + "\n"
            + "Clickfiel",
            fg="black",
            font=("Arial", 10),
            width=15,
        )
        lojas_permitidas_text.place(x=650, y=80)

        """Texto Informações"""
        informacoes_text = tkinter.Label(
            self.window,
            text="Informações",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=15,
            borderwidth=2,
            relief="groove",
        )
        informacoes_text.place(x=650, y=50)

    """Funcao para adicionar novas urls ao excel tracker"""

    def Append_Excel(self):
        url_track_append = str(self.leitor_url.get())
        code_track_append = str(self.leitor_code.get())
        buybellow_track_append = str(self.leitor_buybellow.get())
        """Apagar o que foi escrito pelo utilizador"""
        self.leitor_url.delete(0, "end")
        self.leitor_code.delete(0, "end")
        self.leitor_buybellow.delete(0, "end")
        """Ver se a url é das lojas possíveis de analisar"""
        if (
            url_track_append != ""
            and (
                ("pcdiga" in url_track_append)
                or ("worten" in url_track_append)
                or ("amazon" in url_track_append)
                or ("mediamarkt" in url_track_append)
                or ("chip7" in url_track_append)
                or ("chiptec" in url_track_append)
                or ("globaldata" in url_track_append)
                or ("gamingreplay" in url_track_append)
                or ("mega-mania" in url_track_append)
                or ("clickfiel" in url_track_append)
            )
            and code_track_append != ""
            and buybellow_track_append.isnumeric
        ):
            log_track = pd.DataFrame(
                {
                    "url": url_track_append,
                    "codigo": code_track_append,
                    "comprar_abaixo": buybellow_track_append,
                },
                index=[self.i_track],
            )  # alocar primeiro ao dataframe
            self.tracker_log = self.tracker_log.append(log_track)
            print(self.tracker_log)

            self.i_track += 1

            """Colocar os dados adicionados de tracking"""
            self.prod_tracker = self.prod_tracker.append(
                self.tracker_log
            )  # prod_tracker é o read_excel
            # save the  file with the information
            self.prod_tracker.to_excel("TRACKER_TEST2.xlsx", index=False)
            self.prod_tracker = pd.read_excel(
                "TRACKER_TEST2.xlsx"
            )  # Tem de voltar a ler o excel
        else:
            messagebox.showinfo(
                "Informação", "Não é possível pesquisar essa loja",
            )

    """Funcao que corre o programa e faz append da informação para o ficheiro de tracking"""

    def Run_Prg(self):
        # try:
        # if self.i_track != 0:
        # """Colocar os dados adicionados de tracking"""
        # self.prod_tracker = self.prod_tracker.append(
        # self.tracker_log
        # )  # prod_tracker é o read_excel
        # save the  file with the information
        # self.prod_tracker.to_excel("TRACKER_TEST2.xlsx", index=False)
        # self.prod_tracker = pd.read_excel(
        # "TRACKER_TEST2.xlsx"
        # )  # Tem de voltar a ler o excel
        # except:
        # pass
        """Definir tempo programa, tempo de ciclo e email"""
        t_int = str(self.leitor_t_ciclo.get())
        if t_int.isdecimal and t_int != "":  # pode ser zero
            t_entre_ciclos = int(t_int)
        else:
            messagebox.showinfo(
                "Informação", "O tempo entre procura deve ser um número inteiro",
            )
        t_tot = str(self.leitor_t_total.get())
        if (
            t_tot.isdecimal
            and t_tot != ""
            and int(t_tot) > int((self.t_entre_url * len(self.prod_tracker.url)) / 60)
        ):  # valor dado em minutos
            t_tot = (int(t_tot) * 60) / 1  # passsar de minutos para segundos
            n_ciclos = int(t_tot) / (
                t_entre_ciclos
                + (
                    self.t_entre_url * len(self.prod_tracker.url)
                )  # t_total/tempo de ciclo completo
            )
        else:
            messagebox.showinfo(
                "Informação",
                "O tempo de execução do programa dever ser colocado em minutos e deve ser um número inteiro superior ao tempo mínimo",
            )
        l_mail = str(self.leitor_mail.get())
        if l_mail != "" and (
            ("@hotmail.com" in l_mail)
            or ("@gmail.com" in l_mail)
            or ("@outlook.com" in l_mail)
            or ("@adral.pt" in l_mail)
            or ("@ua.pt" in l_mail)
        ):
            self.lista_mail = [l_mail]
        else:
            messagebox.showinfo(
                "Informação", "Insira um email válido",
            )

        print(n_ciclos)
        print(t_entre_ciclos)
        self.search_product_list(
            int(n_ciclos), int(t_entre_ciclos)
        )  # t_ciclos nunca é menor que 5s

    def search_product_list(self, interval_count, interval_seconds):
        """
        It also requires a file called SEARCH_HISTORY.xslx under the folder ./search_history to start saving the results.
        An empty file can be used on the first time using the script.

        Both the old and the new results are then saved in a new file named SEARCH_HISTORY_{datetime}.xlsx
        This is the file the script will use to get the history next time it runs.

        Parameters
        ----------
        interval_count : TYPE, optional
            DESCRIPTION. The default is 1. The number of iterations you want the script to run a search on the full list.
        interval_hours : TYPE, optional
            DESCRIPTION. The default is 6.

        Returns
        -------
        New .xlsx file with previous search history and results from current search

        """
        interval = 0  # counter reset
        # now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")  # DATA E HORA

        # path to last file in the folder
        last_search = glob("search_history/*.xlsx")[-1]
        search_hist = pd.read_excel(last_search)

        while interval < interval_count:

            for count, url in enumerate(self.prod_tracker.url):
                try:  # caso fique sem internet continua
                    now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")
                    # print(url)
                    page = requests.get(url, headers=HEADERS)
                    # cria um objeto que contem a info da url mas de forma organizada != do page
                    soup = BeautifulSoup(page.content, features="lxml")
                    try:  # este try e except garante que caso algo mude num site não interfira com o tracking
                        ##################DIFERENTES LEITURAS DOS SITES###########################################
                        if "pcdiga" in url:
                            # product title
                            title = soup.select(".page-title")[0].get_text().strip()
                            # print(title)
                            # to prevent script from crashing when there isn't a price for the product
                            try:
                                price = (
                                    soup.select(".price")[0]
                                    .get_text()
                                    .replace(".", "")
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""

                            # checking if there is "Out of stock"
                            try:
                                soup.select(".skrey_estimate_date_wrapper.unavailable")[
                                    0
                                ].get_text().strip()
                                stock = "Sem Stock"
                                # print(stock)
                            except:
                                stock = "Disponivel"
                                # print(stock)
                        elif "worten" in url:
                            title = (
                                soup.select(".w-product__name")[0].get_text().strip()
                            )
                            # print(title)
                            # to prevent script from crashing when there isn't a price for the product
                            try:
                                price = (
                                    soup.select(".w-product__price")[0]
                                    .get_text()
                                    .replace(".", "")
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                            # checking if there is "Out of stock"
                            try:
                                soup.select(".w-product__unavailability-title")[
                                    0
                                ].get_text().strip()
                                stock = "Sem Stock"
                                # print(stock)
                            except:
                                stock = "Disponivel"
                                # print(stock)
                        elif "amazon" in url:
                            # product title
                            title = soup.find(id="productTitle").get_text().strip()

                            # to prevent script from crashing when there isn't a price for the product
                            try:
                                price = float(
                                    soup.find(id="priceblock_ourprice")
                                    .get_text()
                                    .replace(".", "")
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .strip()
                                )
                            except:
                                # this part gets the price in dollars from amazon.com store
                                try:
                                    price = float(
                                        soup.find(id="priceblock_saleprice")
                                        .get_text()
                                        .replace("$", "")
                                        .replace(",", "")
                                        .strip()
                                    )
                                except:
                                    price = ""
                            try:
                                review_score = float(
                                    soup.select(
                                        'i[class*="a-icon a-icon-star a-star-"]'
                                    )[0]
                                    .get_text()
                                    .split(" ")[0]
                                    .replace(",", ".")
                                )
                                review_count = int(
                                    soup.select("#acrCustomerReviewText")[0]
                                    .get_text()
                                    .split(" ")[0]
                                    .replace(".", "")
                                )
                            except:
                                # sometimes review_score is in a different position... had to add this alternative with another try statement
                                try:
                                    review_score = float(
                                        soup.select(
                                            'i[class*="a-icon a-icon-star a-star-"]'
                                        )[1]
                                        .get_text()
                                        .split(" ")[0]
                                        .replace(",", ".")
                                    )
                                    review_count = int(
                                        soup.select("#acrCustomerReviewText")[0]
                                        .get_text()
                                        .split(" ")[0]
                                        .replace(".", "")
                                    )
                                except:
                                    review_score = ""
                                    review_count = ""

                            # checking if there is "Out of stock"
                            try:
                                soup.select("#availability .a-color-state")[
                                    0
                                ].get_text().strip()
                                stock = "Sem Stock"
                            except:
                                # checking if there is "Out of stock" on a second possible position
                                try:
                                    soup.select("#availability .a-color-price")[
                                        0
                                    ].get_text().strip()
                                    stock = "Sem Stock"
                                except:
                                    # if there is any error in the previous try statements, it means the product is available
                                    stock = "Disponivel"
                        elif "mediamarkt" in url:
                            title = (
                                soup.select(".product-center-column h1")[0]
                                .get_text()
                                .strip()
                            )
                            # print(title)

                            try:
                                price = soup.select(".bigprices")[0].get_text().split()
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                                # print(price)
                            try:
                                if (
                                    soup.find(id="AddToCartText").get_text().strip()
                                    == "Comprar"
                                ):
                                    stock = "Disponivel"
                                    # print(stock)
                                else:
                                    stock = "Sem Stock"
                                    # print(stock)
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)
                        elif "chip7" in url:
                            title = (
                                soup.select(".product-title h1")[0].get_text().strip()
                            )
                            # print(title)

                            try:
                                price = (
                                    soup.select(".our_price_display")[0]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                                # print(price)
                            try:
                                # print(soup.select('.chip7-disponibilidade')[0].get_text().strip())
                                if (
                                    soup.select(".chip7-disponibilidade")[0]
                                    .get_text()
                                    .strip()
                                    == "Dísponivel"
                                ):
                                    stock = "Disponivel"
                                    # print(stock)
                                else:
                                    stock = "Sem Stock"
                                    # print(stock)
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)
                        elif "chiptec" in url:
                            title = soup.select(".prod_tit")[0].get_text().strip()
                            # print(title)

                            try:
                                price = (
                                    soup.select(".price")[1]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                                # print(price)
                            try:
                                if (
                                    soup.select(".availability")[0].get_text().strip()
                                    == "Disponibilidade: Disponível"
                                ):
                                    stock = "Disponivel"
                                    # print(stock)
                                elif (
                                    soup.select(".availability")[0].get_text().strip()
                                    == "Disponibilidade: Por Encomenda"
                                ):
                                    stock = "Por Encomenda"
                                    # print(stock)
                                else:
                                    stock = "Sem Stock"
                                    # print(stock)
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)
                        elif "globaldata" in url:
                            title = soup.find(name="title").get_text().strip()
                            # print(title)

                            try:
                                price = (
                                    soup.select(".h1")[0]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                                # print(price)

                            try:
                                # print(soup.select('.availability-text')[0].get_text().strip())
                                st = (
                                    soup.select(".availability-text")[0]
                                    .get_text()
                                    .strip()
                                )
                                st = st.lower()
                                # print(st)
                                if "em stock" in st:
                                    stock = "Disponivel"
                                    # print(stock)
                                elif "poucas unidades" in st:
                                    stock = "Disponivel, mas com poucas unidades"
                                    # print(stock)
                                else:
                                    stock = "Sem Stock"
                                    # print(stock)
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)
                        elif "gamingreplay" in url:
                            title = soup.find(name="title").get_text().strip()
                            # print(title)

                            try:
                                price = (
                                    soup.select(".gr-label-new-price")[0]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                                # print(price)
                            except:
                                price = ""
                                # print(price)

                            try:
                                st = (
                                    soup.select("p.store_stock_feature.in_stock")[0]
                                    .get_text()
                                    .strip()
                                )
                                st = st.lower()
                                # print(st)
                                if "disponível" in st:
                                    stock = "Disponivel"
                                    # print(stock)
                                elif "poucas unidades" in st:
                                    stock = "Disponivel, mas com poucas unidades"
                                    # print(stock)
                                else:
                                    stock = "Sem Stock"
                                    # print(stock)
                            except:
                                stock = "ERRO NO STOCK"
                                # print(stock)
                        elif "mega-mania" in url:
                            title = soup.select("td")[0].get_text().strip()

                            try:
                                price = (
                                    soup.select(".produto_lista_botoes__bt_preco")[0]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                            except:
                                price = ""
                            try:
                                st = (
                                    soup.select(".produto_lista_stock_emstock")[0]
                                    .get_text()
                                    .strip()
                                )
                                st = st.lower()
                                # print(st)
                                if "stock" in st:
                                    stock = "Disponivel"
                                elif "poucas unidades" in st:
                                    stock = "Disponivel, mas com poucas unidades"
                                else:
                                    stock = "Sem Stock"
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)
                        elif "clickfiel" in url:
                            title = soup.select("h1")[0].get_text().strip()
                            try:
                                price = (
                                    soup.select(".price.new .whole")[0]
                                    .get_text()
                                    .replace("€", "")
                                    .replace(",", ".")
                                    .split()
                                )
                                if len(price) > 1:
                                    price = price[0] + price[1]
                                else:
                                    price = price[0]
                            except:
                                price = ""
                            try:
                                st = (
                                    soup.select_one(".disponibilidades")
                                    .get_text()
                                    .strip()
                                )
                                st = st.lower()
                                # print(st)
                                if "em stock" in st:
                                    stock = "Disponivel"
                                elif "poucas unidades" in st:
                                    stock = "Disponivel, mas com poucas unidades"
                                else:
                                    stock = "Sem Stock"
                            except:
                                stock = "ERRO NO STOCK"
                                print(stock)

                        ####################Parte do Log########################################################
                        if "amazon" in url:  # porque tem as reviews
                            log = pd.DataFrame(
                                {
                                    "date": now.replace("h", ":").replace("m", ""),
                                    # this code comes from the TRACKER_PRODUCTS file
                                    "code": self.prod_tracker.codigo[count],
                                    "url": url,
                                    "title": title,
                                    # this price comes from the TRACKER_PRODUCTS file ###ATENCAO####
                                    "buy_below": self.prod_tracker.comprar_abaixo[
                                        count
                                    ],
                                    "price": price,
                                    "stock": stock,
                                    "review_score": review_score,
                                    "review_count": review_count,
                                },
                                index=[count],
                            )
                        else:
                            review_score = "-"
                            review_count = "-"
                            log = pd.DataFrame(
                                {
                                    "date": now.replace("h", ":").replace("m", ""),
                                    # this code comes from the TRACKER_PRODUCTS file
                                    "code": self.prod_tracker.codigo[count],
                                    "url": url,
                                    "title": title,
                                    # this price comes from the TRACKER_PRODUCTS file ###ATENCAO####
                                    "buy_below": self.prod_tracker.comprar_abaixo[
                                        count
                                    ],
                                    "price": price,
                                    "stock": stock,
                                    "review_score": review_score,
                                    "review_count": review_count,
                                },
                                index=[count],
                            )
                        ############################################################################################
                        try:
                            # This is where you can integrate an email alert!
                            if float(price) < self.prod_tracker.comprar_abaixo[
                                count
                            ] and (
                                stock == "Disponivel"
                                or stock == "Disponivel, mas com poucas unidades"
                            ):
                                try:
                                    """Vou ver o que está antes no search_tracker_log e ver se é diferente\
                                        caso seja, mandar alerta. Vou ver o preco e o stock."""
                                    stock_atual = log.stock.array[0]
                                    stock_anterior = self.search_tracker_log.stock.array[
                                        (
                                            len(self.search_tracker_log.stock)
                                            - (
                                                len(prod_tracker.url)
                                            )  # 1 devido ao indice começar em 0
                                        ) :
                                    ]
                                    stock_anterior = stock_anterior[0]
                                    preco_atual = log.price.array[0]
                                    preco_anterior = self.search_tracker_log.price.array[
                                        (
                                            len(self.search_tracker_log.price)
                                            - (
                                                len(prod_tracker.url)
                                            )  # 1 devido ao indice começar em 0
                                        ) :
                                    ]
                                    preco_anterior = preco_anterior[0]
                                    # print(stock_atual + "\n" + stock_anterior)
                                    # print(preco_atual + "\n" + preco_anterior)
                                    """Ver se o estado anterior é igual ao presente em termos de preco baixo e disponibilidade"""
                                    if (
                                        (
                                            stock_atual != stock_anterior
                                            or preco_atual != preco_anterior
                                        )
                                        and len(self.search_tracker_log)
                                        > len(prod_tracker.url)
                                    ) or len(self.search_tracker_log) < len(
                                        prod_tracker.url
                                    ):
                                        # Disparar alerta
                                        print(
                                            "************************ ALERT! Buy the "
                                            + self.prod_tracker.codigo[count]
                                            + " ************************"
                                        )

                                        subject_title_mail = title
                                        texto_mail = "O produto {} está um preço bombástico de {} e tem stock URL {}".format(
                                            title, price, url
                                        )
                                        self.send_email(
                                            "Plynkss@hotmail.com",
                                            "Adral_2020_2021",
                                            self.lista_mail,
                                            subject_title_mail,
                                            texto_mail,
                                        )
                                except:
                                    pass
                        except:
                            # sometimes we don't get any price, so there will be an error in the if condition above
                            print("Erro na aquisição de dados")
                            # com a messagebox caso aconteça temos de estar sempre a dar ok
                            # messagebox.showinfo(
                            #     "Informação", "Erro na aquisição de dados"
                            # )

                        self.search_tracker_log = self.search_tracker_log.append(log)
                        # print('appended '+ prod_tracker.code[count] +'\n' + title + '\n' + stock + '\n\n')
                        print(
                            title
                            + " ---- "
                            + self.prod_tracker.codigo[count]
                            + "\n"
                            + stock
                            + "\n"
                            + price
                            + "\n\n"
                        )
                        sleep(self.t_entre_url)  # inicialmente 5s
                    except:
                        pass
                except:  # caso fique sem internet continua
                    pass

            interval += 1  # counter update

            print(
                "Fim do intervalo "
                + str(interval)
                + "   "
                + "falta "
                + str(int(interval_count - interval))
            )
            sleep(interval_seconds * 1 * 1)

        # after the run, checks last search history record, and appends this run results to it, saving a new file
        final_df = search_hist.append(self.search_tracker_log, sort=False)

        # save the new file with the information, now - data
        final_df.to_excel(
            "search_history/SEARCH_HISTORY_{}.xlsx".format(now), index=False
        )
        print("Fim do tracking")
        self.close_window()

    def send_email(
        self, email, password, targets, subject_title_mail, texto_mail
    ):  # tem de ser outlook o que envia
        print("almost email.....")
        server = smtplib.SMTP(host="smtp.outlook.com", port=587)
        server.starttls()

        sender = email
        server.ehlo()
        server.login(email, password)
        sleep(5)

        msg = MIMEText(texto_mail)
        msg["Subject"] = subject_title_mail
        msg["From"] = sender
        msg["To"] = ", ".join(targets)

        server.sendmail(sender, targets, msg.as_string())
        print("sent email.....")
        server.quit()

    def Report(self):
        texto_report = str(self.leitor_report.get())
        if texto_report != "":
            try:
                # para dividir o email entre o nome o diretorio do email
                indice_mail = self.lista_mail[0].find("@")
                # o titulo vai ser o nome do primeiro email da lista de email a que envia normalmente o alerta
                titulo = self.lista_mail[:indice_mail]
            except:
                titulo = "Report from someone"
            self.send_email(
                "Plynkss@hotmail.com",
                "Adral_2020_2021",
                ["Plynkss@hotmail.com"],
                titulo,
                texto_report,
            )


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tracking", prod_tracker, search_tracker_log, tracker_log)
