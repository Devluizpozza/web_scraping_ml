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

    try:

        r = session.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.content, "lxml")

        # container principal dos produtos
        items = soup.select("li.ui-search-layout__item")

        pagina_produtos = []

        for item in items:

            try:

                # titulo (algumas vezes h2, outras h3)
                titulo_tag = item.select_one("h2, h3")
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

                # link
                link_tag = item.select_one("a.ui-search-link") or item.select_one("a")
                link = link_tag["href"] if link_tag else None

                # preço atual
                preco_tag = item.select_one("span.andes-money-amount__fraction")
                preco = preco_tag.get_text(strip=True) if preco_tag else None

                # preço antigo
                preco_antigo_tag = item.select_one("s span.andes-money-amount__fraction")
                preco_antigo = preco_antigo_tag.get_text(strip=True) if preco_antigo_tag else None

                # desconto
                desconto_tag = item.select_one("span.andes-money-amount__discount")
                desconto = desconto_tag.get_text(strip=True) if desconto_tag else None

                pagina_produtos.append({
                    "titulo": titulo,
                    "preco": preco,
                    "preco_antigo": preco_antigo,
                    "desconto": desconto,
                    "link": link
                })

            except:
                pass

        time.sleep(random.uniform(3, 7))

        return pagina_produtos

    except:
        time.sleep(random.uniform(3, 7))
        return []


print("Iniciando scraping...")

# paginação (48 produtos por página)
offsets = list(range(1, 700, 48))

with ThreadPoolExecutor(max_workers=3) as executor:

    futures = [executor.submit(coletar_pagina, offset) for offset in offsets]

    for future in as_completed(futures):

        resultado = future.result()

        if resultado:
            produtos.extend(resultado)

print("Total coletado:", len(produtos))

with open(f"{produto}_mercadolivre.json", "w", encoding="utf-8") as f:
    json.dump(produtos, f, indent=4, ensure_ascii=False)

print("JSON salvo com sucesso.")