import requests
from bs4 import BeautifulSoup


'''
    TODO: verificar se o vizinho é do mesmo estado/cidade antes de enviar o resultado de volta
'''

def tst_scrap(search_term, verify=True):
    base_url = "https://tudosobretodos.info"
    url = f"https://tudosobretodos.info/{search_term}"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        city = soup.select('.conteudoDadosDir h1')[0].get_text(strip=True)
        detalhes = soup.select('.detalhesPessoa a')
        vizinhos = []
        for i in range(len(detalhes)):
            if "linkLogue" not in str(detalhes[i]):
                vizinhos.append(detalhes[i])
            else:
                pass
        vizinhos_result = []
        for vizinho in vizinhos:
            href = vizinho.get("href", "")
            full_link = base_url+href
            name_div = vizinho.find("div", class_="itemMoradores")
            name = name_div.get_text(strip=True) if name_div else ""
            vizinhos_result.append({"link": full_link, "nome": name})
        print(vizinhos_result)
        print(city)
    else:
        print("todo error")
        
tst_scrap("VILMA NUNES DE SOUZA LIMA")