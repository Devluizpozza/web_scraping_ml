import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

PROXY_API = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"

OUTPUT_FILE = "proxies.json"


def baixar_proxies():

    print("Baixando proxies...")

    r = requests.get(PROXY_API)

    proxies = [p.strip() for p in r.text.split("\n") if p.strip()]

    print("Total encontrados:", len(proxies))

    return proxies


def testar_proxy(proxy):

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    try:

        r = requests.get(
            "https://httpbin.org/ip",
            proxies=proxies,
            timeout=5
        )

        if r.status_code == 200:
            return proxy

    except:
        return None


def gerar_proxy_pool():

    proxies = baixar_proxies()

    validos = []

    print("Testando proxies...")

    with ThreadPoolExecutor(max_workers=50) as executor:

        futures = [executor.submit(testar_proxy, p) for p in proxies]

        for future in as_completed(futures):

            resultado = future.result()

            if resultado:
                validos.append(resultado)

    print("Proxies válidos:", len(validos))

    return validos


def salvar_proxies(proxies):

    with open(OUTPUT_FILE, "w") as f:

        json.dump(proxies, f, indent=4)

    print("Proxies salvos em", OUTPUT_FILE)


if __name__ == "__main__":

    pool = gerar_proxy_pool()

    salvar_proxies(pool)