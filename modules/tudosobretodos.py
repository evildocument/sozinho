import re
import requests
from bs4 import BeautifulSoup


'''
    TODO: seila
'''

def tst_scrap(search_term, verify=False):
    '''
    ================
        Função que executa a busca, o unico resultado que realmente importa é a cidade
        
        ps: funcao por enquanto so funciona caso haja apenas um resultado para o nome,
        caso haja mais de um nome, não vai achar os elementos corretamente
    ================
    '''
    base_url = "https://tudosobretodos.info"
    url = f"https://tudosobretodos.info/{search_term}"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        
        city_bit = soup.select('.conteudoDadosDir h1')[0].get_text(strip=True)
        city = format_city(city_bit)
        
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
            vizinhos_result.append({"nome": name, "link": full_link})
        if verify:
            vizinhos_result = vizinhos_verifier(vizinhos_result, city)
            return [city, vizinhos_result]
        else:
            return [city, vizinhos_result]
    else:
        print("todo error")



def vizinhos_verifier(vizinhos_list, og_city):
    '''
    ================
        Função que serve para verificar se os "vizinhos" são da mesma cidade;
        na realidade não são vizinhos (não moram perto da pessoa), 
        apenas pessoas da mesma cidade, então esse resultado é
        maior parte das vezes ignorável.
        
        descobri isso enquanto codava, o que reduz bastante a utilidade dessa função
        :facepalm:
    ================
    '''
    final_list = []
    for vizinho_dict in vizinhos_list:
            page = requests.get(vizinho_dict['link'])
            
            soup = BeautifulSoup(page.text, "html.parser")
            city_bit = soup.select('.conteudoDadosDir h1')[0].get_text(strip=True)
            city = format_city(city_bit)
            
            if city.lower() == og_city.lower():
                    final_list.append({"nome": vizinho_dict['link', "link": vizinho_dict['link'], ]})
            else:
                    pass
    return final_list



def format_city(city):
    pattern = re.compile(r'(?<=, de\s)(.*?)(?=,\s*está no site)', re.IGNORECASE | re.UNICODE)
    return_city = pattern.search(city).group(1).strip()
    return return_city  
   
