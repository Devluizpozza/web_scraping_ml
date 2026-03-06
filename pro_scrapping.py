import requests
from bs4 import BeautifulSoup
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

produto = input("Digite o produto: ").strip().replace(" ", "-")

BASE_URL = f"https://lista.mercadolivre.com.br/{produto}_Desde_"

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"Mozilla/5.0 (X11; Linux x86_64)"
]

session = requests.Session()

produtos = []


def carregar_proxies():

    with open("proxies.json") as f:

        return json.load(f)


PROXY_POOL = carregar_proxies()

print("Proxies carregados:", len(PROXY_POOL))

print("Json criado")

def coletar_pagina(start):

    url = f"{BASE_URL}{start}_NoIndex_True"

    proxy = random.choice(PROXY_POOL)

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    try:

        r = session.get(url, headers=headers, proxies=proxies, timeout=10)

        soup = BeautifulSoup(r.content, "lxml")

        items = soup.select("li.ui-search-layout__item")

        pagina_produtos = []

        for item in items:

            try:

                titulo = item.select_one("h3").get_text(strip=True)

                link = item.select_one("a")["href"]

                preco = item.select_one("span.andes-money-amount__fraction")
                preco = preco.get_text(strip=True) if preco else None

                pagina_produtos.append({
                    "titulo": titulo,
                    "preco": preco,
                    "link": link
                })

            except:
                pass

        time.sleep(random.uniform(2,5))

        return pagina_produtos

    except:

        return []


offsets = list(range(1, 700, 48))

with ThreadPoolExecutor(max_workers=4) as executor:

    futures = [executor.submit(coletar_pagina, o) for o in offsets]

    for future in as_completed(futures):

        resultado = future.result()

        if resultado:
            produtos.extend(resultado)


print("Total coletado:", len(produtos))


with open(f"{produto}_mercadolivre.json", "w", encoding="utf-8") as f:

    json.dump(produtos, f, indent=4, ensure_ascii=False)

print("Json criado")

print("Scraping finalizado")