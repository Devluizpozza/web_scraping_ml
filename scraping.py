import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
# pip install requests beautifulsoup4 pandas lxml

produto = input("Digite o produto: ").replace(" ", "-")

base_url = f"https://lista.mercadolivre.com.br/{produto}_Desde_"

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

session = requests.Session()
session.headers.update(headers)

start = 1

produtos = []

while True:

    url = f"{base_url}{start}_NoIndex_True"

    print("Coletando:", url)

    r = session.get(url)

    if r.status_code != 200:
        print("Erro na requisição")
        break

    soup = BeautifulSoup(r.content, "lxml")

    items = soup.select("li.ui-search-layout__item")

    if not items:
        print("Fim das páginas")
        break

    for item in items:

        try:

            titulo = item.select_one("h3").get_text(strip=True)

            link = item.select_one("a")["href"]

            preco = item.select_one("span.andes-money-amount__fraction")

            preco = preco.get_text(strip=True) if preco else None

            preco_antigo = item.select_one("s .andes-money-amount__fraction")

            preco_antigo = preco_antigo.get_text(strip=True) if preco_antigo else None

            desconto = item.select_one("span.andes-money-amount__discount")

            desconto = desconto.get_text(strip=True) if desconto else None

            produtos.append({
                "titulo": titulo,
                "preco": preco,
                "preco_antigo": preco_antigo,
                "desconto": desconto,
                "link": link
            })

        except:
            pass

    start += 48

    time.sleep(random.uniform(1.5,3.5))

df = pd.DataFrame(produtos)

df.to_csv("produtos_mercadolivre.csv", index=False, encoding="utf-8-sig")

print("Arquivo CSV salvo!")
print("Total de produtos:", len(produtos))