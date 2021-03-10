import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from glob import glob
from time import sleep
import tkinter
from tkinter import messagebox
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}
### LER/CRIAR FICHEIRO TRACK###
try:
    """Lê o csv com o track das coisas que queremos"""
    prod_tracker = pd.read_csv("TRACKER_TEST2.csv", sep=";")
    search_tracker_log = pd.DataFrame()
    tracker_log = pd.DataFrame()
except:
    """Cria o csv inicial para fazer Track do que queremos"""
    head_excel = ["url", "codigo", "comprar abaixo"]
    head = pd.DataFrame(columns=head_excel)
    head.to_csv("TRACKER_TEST2.csv", sep=";", index=0)
    """Lê o csv com o track das coisas que queremos"""
    prod_tracker = pd.read_csv("TRACKER_TEST2.csv", sep=";")
    search_tracker_log = pd.DataFrame()
    tracker_log = pd.DataFrame()

now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")  # DATA E HORA


class App:
    def __init__(
        self, window, window_title, prod_tracker, search_tracker_log, tracker_log
    ):  # por defeito a video source seria 0; #a funcao init é sempre executada no inicio
        self.window = window  # "tkinter.Tk()"
        self.window.title(window_title)
        self.window.geometry("500x500")
        # window.attributes('-fullscreen',True) # maximiza a janela

        self.prod_tracker = prod_tracker
        self.search_tracker_log = search_tracker_log
        self.tracker_log = tracker_log

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
        self.btn_close.place(x=385, y=0)

        """Botão que adiciona um link ao csv"""
        self.btn_append_track = tkinter.Button(
            window,
            text="Adicionar Dados à Busca",
            width=20,
            height=1,
            command=self.Append_CSV,
        )
        self.btn_append_track.place(x=210, y=70)

        ###############################################

        """Cria as labels iniciais"""
        self.Label_Inicial()

        self.window.mainloop()  # corre a janela em loop, todos os botões criados estão sempre prontos para serem carregados

    # Função para fechar as janelas quando o botão é pressionado
    def close_window(self):
        self.window.destroy()

    def Label_Inicial(self):
        # Entrada de texto relativamente ao que vamos fazer track
        self.leitor_track_text = tkinter.Label(
            self.window,
            text="Url do item",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.leitor_track_text.place(x=210, y=100)

        self.leitor_track = tkinter.Entry(self.window)
        self.leitor_track.place(x=190, y=125)

    """Funcao para adicionar novas urls ao csv tracker"""

    def Append_CSV(self):
        url_track_append = str(self.leitor_track.get())
        """Ver se a url é das lojas possíveis de analisar"""
        if ((url_track_append != "") and (
            (
                "pcdiga"
                or "worten"
                or "amazon"
                or "mediamarkt"
                or "chip7"
                or "chiptec"
                or "globaldata"
            )
            in url_track_append
        )) and :
            self.tracker_log = self.tracker_log.append(
                {"url": url_track_append}
            )  # alocar primeiro ao dataframe
            csv_prod_tracker = prod_tracker.url.append(self.tracker_log, sort=False)
            # save the  file with the information
            csv_prod_tracker.to_csv("TRACKER_TEST2.csv", sep=";", index=False)

        # after the run, checks last search history record, and appends this run results to it, saving a new file

        # {
        # "date": now.replace("h", ":").replace("m", ""),

        # "code": prod_tracker.code[count],
        # "url": url,
        # "title": title,
        # "buy_below": prod_tracker.buy_below[count],
        # "price": price,
        # "stock": stock,
        # },


# path to last file in the folde prod_tracker_URLS
# tracker_log = tracker_log.append(log)
# last_search = glob("search_history/*.xlsx")[-1]
# search_hist = pd.read_excel(last_search)
# final_df = prod_tracker.url.append(tracker_log, sort=False)


def search_product_list(interval_count=1, interval_hours=1):
    """
    This function lods a csv file named TRACKER_PRODUCTS.csv, with headers: [url, code, buy_below]
    It looks for the file under in ./trackers

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
    # prod_tracker = pd.read_csv("trackers/TRACKER_PRODUCTS.csv", sep=";")
    # prod_tracker_URLS = prod_tracker.url
    # tracker_log = pd.DataFrame()
    # now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")
    interval = 0  # counter reset

    while interval < interval_count:

        for count, url in enumerate(prod_tracker_URLS):
            print(url)
            page = requests.get(url, headers=HEADERS)
            # cria um objeto que contem a info da url mas de forma organizada != do page
            soup = BeautifulSoup(page.content, features="lxml")

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
                title = soup.select(".w-product__name")[0].get_text().strip()
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
                        soup.select('i[class*="a-icon a-icon-star a-star-"]')[0]
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
                            soup.select('i[class*="a-icon a-icon-star a-star-"]')[1]
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
                    soup.select("#availability .a-color-state")[0].get_text().strip()
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
                title = soup.select(".product-center-column h1")[0].get_text().strip()
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
                    if soup.find(id="AddToCartText").get_text().strip() == "Comprar":
                        stock = "Disponivel"
                        # print(stock)
                    else:
                        stock = "Sem Stock"
                        # print(stock)
                except:
                    stock = "ERRO NO STOCK"
                    print(stock)
            elif "chip7" in url:
                title = soup.select(".product-title h1")[0].get_text().strip()
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
                        soup.select(".chip7-disponibilidade")[0].get_text().strip()
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
                    st = soup.select(".availability-text")[0].get_text().strip()
                    # print(st)
                    if "Em stock" in st:
                        stock = "Disponivel"
                        # print(stock)
                    elif "Poucas unidades" in st:
                        stock = "Disponivel, mas com poucas unidades"
                        # print(stock)
                    else:
                        stock = "Sem Stock"
                        # print(stock)
                except:
                    stock = "ERRO NO STOCK"
                    print(stock)
            ####################Parte do Log########################################################
            if "amazon" in url:  # porque tem as reviews
                log = pd.DataFrame(
                    {
                        "date": now.replace("h", ":").replace("m", ""),
                        # this code comes from the TRACKER_PRODUCTS file
                        "code": prod_tracker.code[count],
                        "url": url,
                        "title": title,
                        # this price comes from the TRACKER_PRODUCTS file ###ATENCAO####
                        "buy_below": prod_tracker.buy_below[count],
                        "price": price,
                        "stock": stock,
                        "review_score": review_score,
                        "review_count": review_count,
                    },
                    index=[count],
                )
            else:
                log = pd.DataFrame(
                    {
                        "date": now.replace("h", ":").replace("m", ""),
                        # this code comes from the TRACKER_PRODUCTS file
                        "code": prod_tracker.code[count],
                        "url": url,
                        "title": title,
                        # this price comes from the TRACKER_PRODUCTS file ###ATENCAO####
                        "buy_below": prod_tracker.buy_below[count],
                        "price": price,
                        "stock": stock,
                    },
                    index=[count],
                )
            ############################################################################################
            try:
                # This is where you can integrate an email alert!
                if price < prod_tracker.buy_below[count] and (
                    stock == "Disponivel"
                    or stock == "Disponivel, mas com poucas unidades"
                ):
                    print(
                        "************************ ALERT! Buy the "
                        + prod_tracker.code[count]
                        + " ************************"
                    )

            except:
                # sometimes we don't get any price, so there will be an error in the if condition above
                pass
            tracker_log = tracker_log.append(log)
            # print('appended '+ prod_tracker.code[count] +'\n' + title + '\n' + stock + '\n\n')
            print(title + "\n" + stock + "\n\n")
            sleep(5)

        interval += 1  # counter update

        sleep(interval_hours * 1 * 1)
        print("end of interval " + str(interval))

    # after the run, checks last search history record, and appends this run results to it, saving a new file
    # path to last file in the folder
    last_search = glob("search_history/*.xlsx")[-1]
    search_hist = pd.read_excel(last_search)
    final_df = search_hist.append(tracker_log, sort=False)

    # save the new file with the information, now - data
    final_df.to_excel("search_history/SEARCH_HISTORY_{}.xlsx".format(now), index=False)
    print("end of search")


# search_product_list()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tracking", prod_tracker, search_tracker_log, tracker_log)

