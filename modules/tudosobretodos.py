import re
import requests
import argparse
from bs4 import BeautifulSoup


'''
    === status: 15/09/25 ====
        - a página voltou ao ar, porém com verificação do cloudfare -
    TODO: 
    - verificar se a página retorna apenas um resultado ou multiplos
        - adicionar a possibilidade de escolher entre os resultados
    
'''

def main():
    parser = argparse.ArgumentParser(description="tudosobretodos <pesquisa>"
                                     "opções: --verify",
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        
    parser.add_argument("pesquisa", type=str, help="Nome ou cpf a ser pesquisado")
    parser.add_argument("--verify", action="store_true", help="Habilita verificação de 'vizinhos'")
    args = parser.parse_args()
    print(tst_scrap(args.pesquisa, args.verify))


def tst_scrap(search_term, verify=False):
    '''
        
        Função que executa a busca, o unico resultado que realmente importa é a cidade
        
        ps: funcao por enquanto so funciona caso haja apenas um resultado para o nome,
        caso haja mais de um nome, não vai achar os elementos corretamente
        SEPARADOR
        search_term -> <nome|cpf>               o termo a ser pesquisado, pode ser tanto nome quanto cpf
        verify      -> <true|false>             verificar por vizinhos
    '''
    base_url = "https://tudosobretodos.info"
    url = f"https://tudosobretodos.info/{search_term}"
    page = requests.get(url)
    print(page)
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
    '''
    ================
        Filtra o resultado para apenas a cidade de onde a pessoa pesquisada é
    ================
    '''
    pattern = re.compile(r'(?<=, de\s)(.*?)(?=,\s*está no site)', re.IGNORECASE | re.UNICODE)
    return_city = pattern.search(city).group(1).strip()
    return return_city  

if __name__ == "__main__":
    main()