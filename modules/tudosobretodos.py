import re
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import quote
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align

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
    scrap_result = tst_scrap(args.pesquisa, args.verify)
    if type(scrap_result) == list:
        for result in scrap_result:  
         console.print(result)     
    else:
        console.print(scrap_result)
def _tst_ehxibit(name, result):
    tst_panel = Panel(
        f"Cidade: {result[0]}\n"
        f"Vizinhos: {', '.join(result[1]) if result[1] else 'Nenhum/Não Selecionado'}",
        title=name,
        style="gold3"
    )
    return Align.center(Columns([tst_panel], equal=True))

def tst_scrap(search_term, verify=False, user_url=None):
    '''
        
        Função que executa a busca, o unico resultado que realmente importa é a cidade
        
        ps: funcao por enquanto so funciona caso haja apenas um resultado para o nome,
        caso haja mais de um nome, não vai achar os elementos corretamente
        SEPARADOR
        search_term -> <nome|cpf>               o termo a ser pesquisado, pode ser tanto nome quanto cpf
        verify      -> <true|false>             verificar por vizinhos
    '''
        
    encoded_name = quote(search_term)
    local_url = "http://localhost:8191/v1"
    base_url = "https://tudosobretodos.info"
    headers = {"Content-Type": "application/json"}
    if user_url:
         data = {
        "cmd": "request.get",
        "url": f"{base_url}{user_url}",
        "maxTimeout": 60000
         }
    else:
        data = {
            "cmd": "request.get",
            "url": f"{base_url}/{search_term}",
            "maxTimeout": 60000
        }
    #url = f"https://tudosobretodos.info/{search_term}"
    page = requests.post(local_url, headers=headers, json=data)
    #page = requests.get(url)
    if page.status_code == 200:
        data = page.json()  
        html = data["solution"]["response"]
        soup = BeautifulSoup(html, "html.parser")
        # TODO
        # nao necessariamente sem resultados, pode ser só que tenha mais de um resultado tambem
        try:
            
            
            city_bit = soup.select('.conteudoDadosDir h1')[0].get_text(strip=True)
        except IndexError:
            
            
            try:
                elements = soup.select('#detalheResultadoContainer div ')
                elements_url = soup.select(".linkPessoa a")

                # isso informa ao usuario que tem mais de um etc
                dict_list = []
                for el in elements:
                    temp_list = [item for item in el.text.split("\n") if item != '']
                    if len(temp_list) == 5:
                        dict_list.append({"nome": temp_list[3], "estado": temp_list[0], "ano": int(temp_list[4])})

                # navegar a cada URL se for menos que
                url_list = []
                for url in elements_url:
                    current_url = url.get("href")
                    if search_term.split(" ")[0].lower() in url.get("href").lower():
                        url_list.append(current_url)

                for url_index in range(len(url_list)):
                    dict_list[url_index]["url"] = url_list[url_index]
                results = []
                for index in range(len(dict_list)):
                    nome = dict_list[index]['nome']
                    url = dict_list[index]['url']
                    results.append(tst_scrap(nome, False, url))
                #console.print(results)
                if len(results) == 0:
                    tst_panel_empty = Panel(
                    "Sem Resultados",
                    title=search_term.capitalize(),
                    style="gold3"
                    )
                    return Align.center(Columns([tst_panel_empty], equal=True))
                else:
                    return results
                
                
            except:
                tst_panel_failure = Panel(
                    "Sem Resultados",
                    title=search_term.capitalize(),
                    style="gold3"
                )
            return Align.center(Columns([tst_panel_failure], equal=True))
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
            return _tst_ehxibit(search_term, [city, vizinhos_result])
            """
            return_panel = Panel()
            return Align.center(
            _tst_ehxibit(search_term, [city, vizinhos_result]),
            vertical="middle"
            )
            """
            
        else:
            return _tst_ehxibit(search_term, [city, vizinhos_result])
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
    from rich.console import Console
    console = Console()
    main()