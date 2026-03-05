import requests
from bs4 import BeautifulSoup
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

produto = input("Digite o produto: ").strip().replace(" ", "-")

BASE_URL = f"https://lista.mercadolivre.com.br/{produto}_Desde_"

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"Mozilla/5.0 (X11; Linux x86_64)",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
]

session = requests.Session()

produtos = []


def coletar_pagina(start):

    url = f"{BASE_URL}{start}_NoIndex_True"

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "pt-BR,pt;q=0.9"
    }

    for tentativa in range(3):

        try:

            r = session.get(url, headers=headers, timeout=10)

            if r.status_code != 200:
                time.sleep(2)
                continue

            soup = BeautifulSoup(r.content, "lxml")

            items = soup.select("li.ui-search-layout__item")

            if not items:
                return []

            pagina_produtos = []

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

                    pagina_produtos.append({
                        "titulo": titulo,
                        "preco": preco,
                        "preco_antigo": preco_antigo,
                        "desconto": desconto,
                        "link": link
                    })

                except:
                    pass

            time.sleep(random.uniform(1,3))

            return pagina_produtos

        except:
            time.sleep(random.uniform(1,3))

    return []


print("Iniciando scraping...")

# offsets de paginação (48 produtos por página)
offsets = list(range(1, 2000, 48))


with ThreadPoolExecutor(max_workers=10) as executor:

    futures = [executor.submit(coletar_pagina, offset) for offset in offsets]

    for future in as_completed(futures):

        resultado = future.result()

        if resultado:
            produtos.extend(resultado)

print("Total coletado:", len(produtos))


with open("produtos_mercadolivre.json", "w", encoding="utf-8") as f:

    json.dump(produtos, f, indent=4, ensure_ascii=False)


print("JSON salvo com sucesso.")