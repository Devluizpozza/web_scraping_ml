
import requests
from bs4 import BeautifulSoup

# Configurações


produto = input('Digite um produto: ')
produto = produto.replace(' ', '-')

url = f'https://lista.mercadolivre.com.br/{produto}'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}




start = 1

url_final = url + str(start) + '_NoIndex_True'

r = requests.get(url_final, headers=headers)
site = BeautifulSoup(r.content, 'html.parser')

descricoes = site.find_all('h3', class_='poly-component__title-wrapper')
for i in descricoes:
    print(i.get_text())