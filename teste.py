import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import smtplib
from email.mime.text import MIMEText


# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


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
    prod_tracker = pd.read_csv("trackers/TRACKER_PRODUCTS.csv", sep=";")
    prod_tracker_URLS = prod_tracker.url
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime("%Y-%m-%d %Hh%Mm")
    interval = 0  # counter reset

    while interval < interval_count:

        for x, url in enumerate(prod_tracker_URLS):

            page = requests.get(url, headers=HEADERS)
            sleep(10)
            # page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(
                page.content, features="lxml"
            )  # cria um objeto que contem a info da url mas de forma organizada != do page
            print(soup)
            title = soup.find(name="title").get_text().strip()
            print(title)

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

        interval += 1  # counter update

        sleep(interval_hours * 1 * 1)
        print("end of interval " + str(interval))


search_product_list()
