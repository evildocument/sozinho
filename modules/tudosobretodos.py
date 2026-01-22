import re
import requests
import argparse
from bs4 import BeautifulSoup
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
import traceback

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
    
    # se o resultado retornado for uma lista, entao trata-se de multiplos resultados
    # caso contrário, trata-se apenas de um painel
    scrap_result = tst_scrap(args.pesquisa, args.verify)
    if isinstance(scrap_result, list):
        for result in scrap_result:  
         console.print(result)     
    else:
        console.print(scrap_result)
def _tst_ehxibit(name, result):
    """
    =======
        Função responsável por formatar e exibir de forma legivel os argumentos
    =======
    """
    # a unica forma de se ter um ano de nascimento na requisição é
    # se há multiplos resultados, caso contrário o valor é None
    ano_nascimento = result[2]
    if ano_nascimento:
        tst_panel = Panel(
        f"Cidade: {result[0]}\n"
        f"Ano: {ano_nascimento}\n"
        f"Vizinhos: {', '.join(result[1]) if result[1] else 'Nenhum/Não Selecionado'}",
        title=name,
        style="gold3"
        )
        return Align.center(Columns([tst_panel], equal=True))
    else:
        tst_panel = Panel(
            f"Cidade: {result[0]}\n"
            f"Vizinhos: {', '.join(result[1]) if result[1] else 'Nenhum/Não Selecionado'}",
            title=name,
            style="gold3"
        )
        return Align.center(Columns([tst_panel], equal=True))

def tst_scrap(search_term, verify=False, user_url=None, year=None, local_url="http://localhost:8191/v1", rate_limit=5, display_limit=15):
    '''
        
        Função que executa a busca, o unico resultado que realmente importa é a cidade
        
        ps: funcao por enquanto so funciona caso haja apenas um resultado para o nome,
        caso haja mais de um nome, não vai achar os elementos corretamente
        SEPARADOR
        search_term -> <nome|cpf>               o termo a ser pesquisado, pode ser tanto nome quanto cpf
        verify      -> <true|false>             verificar por vizinhos
        
        rate_limit -> refere-se ao limite de downloads de pagina, sendo o valor padrão 5. Ou seja, se até 5 resultados
                      for retornado, essas 5 páginas seram baixadas. 
                      
                             
        display_limit -> refere-se ao limite de resultados mostrados na tela, sendo o valor padrão 5. Se 20 resultados retornarem,
                      apenas 15 serão exibidos na tela, os outros 5 seram omitidos.
    '''
    
    base_url = "https://tudosobretodos.info"
    headers = {"Content-Type": "application/json"}
    # essa verificação serve de suporte para a recursão nessa função,
    # fazendo requisições para cada resultado/URL achado (dependendo do rate_limit)
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
    page = requests.post(local_url, headers=headers, json=data)
    if page.status_code == 200:
        data = page.json()  
        html = data["solution"]["response"]
        soup = BeautifulSoup(html, "html.parser")
        # tenta selecionar o elemento indicativo de apenas um resultado
        try:
            city_bit = soup.select('.conteudoDadosDir h1')[0].get_text(strip=True)
            print(city_bit)
        # caso falhe, há mais de um resultado ou nenhum resultados
        except IndexError:
            # verifica tanto se há ou se não há resultados
            try:
                # elemento apenas disponivel quando não se há resultados
                # se o id #result estiver na página, significa que não há resultados
                no_result = soup.select(".detalhesPessoa #result")
            
                # se o elemento não está vazio, significa que não há resultados
                if not no_result == []:
                    tst_panel_failure = Panel(
                        "Sem resultados",
                        title=search_term.capitalize(),
                        style="gold3"
                    )
                    
                    return Align.center(Columns([tst_panel_failure], equal=True))
                
                dict_list = _data_extractor(html)
                results = []
                
                # se a lista estiver vazia, então não há resultados
                quantidade_resultados = len(dict_list)
                if quantidade_resultados == 0:
                    tst_panel_empty = Panel(
                    "Sem Resultados",
                    title=search_term.capitalize(),
                    style="gold3"
                    )
                    return Align.center(Columns([tst_panel_empty], equal=True))
                
                # caso esteja populada, há resultados; porém devem estar abaixo do rate_limit
                elif quantidade_resultados <= rate_limit and quantidade_resultados > 0:
                    for index in range(len(dict_list)):
                        nome = dict_list[index]['nome']
                        url = dict_list[index]['url']
                        ano = dict_list[index]['ano']
                        # chama a propria função, tst_scrap, formando uma lista
                        # com os paineis que ela retorna + o ano
                        results.append(tst_scrap(nome, verify, url, ano))
                    return results
                # caso a quantidade de resultados superar o limite de busca, porém não o de display
                elif quantidade_resultados > rate_limit and quantidade_resultados < display_limit:
                    multiplos_resultados = []
                    multiplos_resultados.append(Align.center(
                        f"Resultados({quantidade_resultados}) superam o limite de pesquisa (atualmente {rate_limit})\nE seram resumidos por estados.\n"
                        , vertical="middle", style="gold3"))
                    for index in range(quantidade_resultados):
                        item_atual = dict_list[index]
                        temp_panel =  Panel(
                                        f"Estado: {item_atual['estado']}\n"
                                        f"Nascimento: {item_atual['ano']}",
                                        title=item_atual['nome'].capitalize(),
                                        style="gold3"
                                        )
                        multiplos_resultados.append(Align.center(Columns([temp_panel], equal=True)))
                    return multiplos_resultados
                # caso até o limite de display seja superado
                else:
                    multiplos_resultados = []
                    multiplos_resultados.append(Align.center(
                        f"Resultados({quantidade_resultados}) superam o limite de display (atualmente {display_limit}\nE seram resumidos até o limite.\n"
                        , vertical="middle", style="gold3"))
                    for index in range(display_limit):
                        item_atual = dict_list[index]
                        temp_panel =  Panel(
                                        f"Estado: {item_atual['estado']}\n"
                                        f"Nascimento: {item_atual['ano']}",
                                        title=item_atual['nome'].capitalize(),
                                        style="gold3"
                                        )
                        multiplos_resultados.append(Align.center(Columns([temp_panel], equal=True)))
                    resto_resultados = quantidade_resultados - display_limit
                    multiplos_resultados.append(Align.center(f"E mais {resto_resultados} resultados...\n", vertical="middle", style="gold3"))
                    return multiplos_resultados
                    
                    
                    
            # nenhum resultado/erro
            except Exception as error:
                print(traceback.format_exc())
                tst_panel_failure = Panel(
                    "Ocorreu algum erro com a requisição,\npor favor tente novamente",
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
            return _tst_ehxibit(search_term, [city, vizinhos_result, year])
            """
            return_panel = Panel()
            return Align.center(
            _tst_ehxibit(search_term, [city, vizinhos_result]),
            vertical="middle"
            )
            """
        else:
            return _tst_ehxibit(search_term, [city, vizinhos_result, year])
    else:
        print("todo error")



def vizinhos_verifier(vizinhos_list, og_city):
    '''
    ================
        Função que serve para verificar se os "vizinhos" são da mesma cidade;
        na realidade não são vizinhos (não moram perto da pessoa), 
        apenas pessoas da mesma cidade. Útil para fazer buscas em redes sociais.
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

def _data_extractor(html):
    """
    ================
        Função utilizada para extrair os multiplos resultados da busca por nome
        [{nome, estado, ano, url}] 
    ================
    """
    soup = BeautifulSoup(html, "html.parser")
    resultados = []
    vistos = set()

    # Buscar apenas os sanfona divs dos estados (não os templates)
    container = soup.find("span", id="detalheResultadoContainer")
    if not container:
        return resultados

    # Buscar apenas divs de estados dentro do container correto
    estados_divs = container.find_all("div", class_="detalhesPessoa listaEstados")

    for estado_div in estados_divs:
        # Verificar se tem id válido de estado
        div_id = estado_div.get('id', '')
        if not re.match(r'^sanfona_[A-Z]{2}$', div_id):
            continue
            
        # Extrair estado
        estado_span = estado_div.find("span", class_="textoTituloDetalhesPessoa caixaParentes")
        if not estado_span:
            continue
        estado = estado_span.text.strip()
        
        # Buscar apenas os links diretos de pessoas (não recursivo para evitar templates)
        links = estado_div.find_all("a", href=re.compile(r'^/[A-Z+]+_\d+$'))
        
        for link in links:
            # Extrair URL
            url = link.get('href', '')
            if not url:
                continue
            
            # Encontrar o div.linkPessoa que vem logo após o link
            link_div = link.find_next_sibling("div", class_="linkPessoa")
            if not link_div:
                continue
            
            # Extrair nome e ano
            nome_div = link_div.find("div", class_="innerDetalheEsq")
            ano_div = link_div.find("div", class_="innerDetalheDir")
            
            if not nome_div or not ano_div:
                continue
                
            nome = nome_div.text.strip()
            ano = ano_div.text.replace("nascimentoMobile", "").strip()
            
            # Validar e filtrar
            if not nome or not ano or not ano.isdigit():
                continue
            if '{' in nome or '}' in nome or '{' in ano or '}' in ano:
                continue
            
            # Evitar duplicatas
            chave = f"{nome}|{estado}|{ano}"
            if chave in vistos:
                continue
            vistos.add(chave)
            
            resultados.append({
                'nome': nome,
                'estado': estado,
                'ano': int(ano),
                'url': url
            })

    return resultados


if __name__ == "__main__":
    from rich.console import Console
    console = Console()
    main()