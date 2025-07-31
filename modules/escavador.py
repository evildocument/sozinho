import re
from playwright.sync_api import sync_playwright
# prototipo 1.5
'''
    Limitações:
        De forma gratuita, é possível carregar apenas 3 páginas
        Também só é possível exibir 4 processos, independente de ser inativo ou ativo
        In a free form its only possible to ehxibit 3 pages
        also only possible to ehxibit 4 legal actions, regardless of it being active or not
'''
'''
TODO:
    Adicionar highlight para estados (e.g processos encontrados na >Bahia<) e informações importantes em geral
    Adicionar a opção de ter uma causa para um processo (e.g processo por Estado da Bahia ser por causa de violencia contra mulher)
    Escalabilidade: adicionar argumentos opcionais (e.g Estado, Nome em sequencia, etc.) para melhor filtragem
    
    ERROR CHECKING!!!
    
    
    Add highlight to state keywords (e.g processes found in >Bahia<) and important info in general
    Add the option to showing a reason for a legal action
'''



def escavador_parser(content):
    '''
        Função que filtra todos os resultados que não sejam as pessoas físicas, como referências 
        e outros elementos HTML
        
        A function to filter every result that isn't actual people, like references or other HTML elements
    '''
    results = [content.nth(i).evaluate("el => el.innerText") for i in range(content.count())]
    
    # remove toda referência que não é a pessoa em si
    # também removendo os 4 primeiras resultados do HTML, 
    # que são só besteira
    
    # remove every reference that is not the person itself
    # also the first 4 results are just junk from the HTML
    filtered_res = [item for item in results if 'página' not in item.lower()]
    filtered_res = [filtered_res[i].split("\n") for i in range(len(filtered_res))]
    return [len(filtered_res[4:]), filtered_res[4:]]


def escavador_scrapper(name_search, in_sequence=False, state=False, ends_with=False):
    """
        Função que serve para realizar o scrapping nas 3 páginas iniciais do escavador, retornando um dicionário
        com o número de páginas como chaves, e os valoes uma lista com o primeiro index o numero de resultados
        e como segundo os valores em si.
        {1: [a [b,c]], 2: [a [b,c]]}
        
        name_search => o nome a ser pesquisado // implemented => to error check
        in_sequence => o nome está em sequência? é exatamente esse? // implemented => to error check
        state => o estado para ser pesquisado // to implement // 
        ends_with => se o nome do meio for desconhecido // to implement
    """
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        # definições necessárias porque a opção de headless não gera uma janela/ou gera com
        # dimensões nulas.
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
            viewport={"width":1280, "height": 800},
        )
        page = context.new_page()
        
        all_results = {}
        '''
            TODO: adicionar lógica para checar se houverem 3 ou menos resultados IDENTICOS na página inicial, automaticamente expandir nos motivos
            dos processos
        '''
        for current_page in range(3):
            page.goto(f"https://www.escavador.com/busca?q={name_search}&qo=t&page={current_page+1}")
            page.wait_for_selector('div.item')
            
            div_content = page.locator('div.item')
            parsed_result = escavador_parser(div_content)
            
            
            
            if in_sequence is True:
                # lista de resultados
                list_of_results = parsed_result[1]
                # valor de resultados
                number_of_results = parsed_result[0]
                new_parsed_result = [0, []]
                for list_of_lists in range(number_of_results):
                    person_name = list_of_results[list_of_lists][0]
                    if person_name.startswith(f"{name_search}"):
                        new_parsed_result[0] += 1
                        new_parsed_result[1].append(list_of_results[list_of_lists])
                    else:
                        pass
                
                all_results[current_page+1] = new_parsed_result
            else:
                all_results[current_page+1] = parsed_result
            return all_results
                        
                    
            
        browser.close()
        return all_results
 
def escavador_exhibit(dict_results):
    """
        TODO: diferenciar de resultados de apenas 1 pagina e resultados filtrados (e.g nome exato)
        que só preenchem a 1 pagina (o escavador mostra primeiro os nomes mais parecidos)
    """
    final_string = ""
    number_of_pages = len(dict_results)
    
    for page in range(number_of_pages):
        
        print(f"Resultado da {page+1} página:\n")
        number_of_elements = dict_results[page+1][0]
        list_of_elements = dict_results[page+1][1]
        for element in range(number_of_elements):
            final_string += "\n".join(list_of_elements[element])
    return final_string
       



