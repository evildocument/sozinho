import re
from playwright.sync_api import sync_playwright
# prototipo 1.5
'''
    Eu sei de agora que esse código não é o mais otimal, mas tenha pena da minha pobre alma, faz um bom tempo que não programo algo
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
    

    Add highlight to is_from_state keywords (e.g processes found in >Bahia<) and important info in general
    Add the option to showing a reason for a legal action
'''



def escavador_parser(content):
    '''
        Função que filtra todos os resultados que não sejam as pessoas físicas, como referências 
        e outros elementos HTML
        
        A function to filter every result that isn't actual people, like references or other HTML elements
    '''
    raw_request = [content.nth(i).evaluate("el => el.innerText") for i in range(content.count())]
    
    # remove toda referência que não é a pessoa em si
    # também removendo os 4 primeiras resultados do HTML, 
    # que são só besteira
    
    # remove every reference that is not the person itself
    # also the first 4 results are just junk from the HTML
    filtered_request = [item for item in raw_request if 'página' not in item.lower()]
    filtered_request = [filtered_request[i].split("\n") for i in range(len(filtered_request))]
    result_list = filtered_request[4:]
    list_of_dicts = []
    
    for each_result in range(len(result_list)):
        result_dict = {
        "nome": result_list[each_result][0],
        "url": result_list[each_result][1],
        "participacoes": result_list[each_result][3],
        "bio": result_list[each_result][5]
        }
        list_of_dicts.append(result_dict)
    
    return list_of_dicts


def escavador_scrapper(name_search, is_in_sequence=False, is_from_state=None, ends_with=False):
    """
        Função que serve para realizar o scrapping nas 3 páginas iniciais do escavador, retornando um dicionário
        com o número de páginas como chaves, e os valoes uma lista com o primeiro index o numero de resultados
        e como segundo os valores em si.
        {1: [a [b,c]], 2: [a [b,c]]}
        
        name_search => o nome a ser pesquisado // implemented => to error check
        is_in_sequence => o nome está em sequência? é exatamente esse? // implemented => to error check
        is_from_state => o estado para ser pesquisado // to implement // 
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
        
        
        dict_master = {}
        '''
            TODO: adicionar lógica para checar se houverem 3 ou menos resultados IDENTICOS na página inicial, automaticamente expandir nos motivos
            dos processos
        '''
        for current_page in range(3):
            page.goto(f"https://www.escavador.com/busca?q={name_search}&qo=t&page={current_page+1}")
            page.wait_for_selector('div.item')
            
            div_content = page.locator('div.item')
            parsed_list = escavador_parser(div_content)
            if is_in_sequence and is_from_state and ends_with:
                pass
            elif is_in_sequence and is_from_state != None:
                dict_master[current_page+1] = from_state(in_sequence(parsed_list, name_search), is_from_state)
            elif is_from_state and ends_with:
                pass
            else:
                if is_in_sequence:
                    dict_master[current_page+1] = in_sequence(parsed_list, name_search)
                if is_from_state != None:
                    dict_master[current_page+1] = from_state(parsed_list, is_from_state)
                if ends_with:
                    pass
    
        browser.close()
        return dict_master
 
def escavador_exhibit(dict_master):
    """
        TODO: diferenciar de resultados de apenas 1 pagina e resultados filtrados (e.g nome exato)
        que só preenchem a 1 pagina (o escavador mostra primeiro os nomes mais parecidos)
    """
    final_string = ""
    numberof_pages = len(dict_master)
    #numberof_res_pages = 0
    for list_of_lists in range(numberof_pages):
        current_page = dict_master[list_of_lists+1]
        for list_index in range(len(current_page)):
            
            final_string += ", \n".join(f"{key.capitalize()}: {value}" for key,value in current_page[list_index].items())
            final_string += "\n\n"
    return final_string
    
  
  
       
def in_sequence(result_dict, name_search):
    filtered_results = []
    for values in range(len(result_dict)):
        name = result_dict[values]["nome"]
        if name.lower().startswith(name_search.lower()):
            filtered_results.append(result_dict[values])
        else:
            pass
    return filtered_results


def from_state(result_dict, state_search):
    filtered_results = []
    brazilian_states = {
    "acre": ["acre", "ac"],
    "alagoas": ["alagoas", "al"],
    "amapá": ["amapa", "ap"],
    "amazonas": ["amazonas", "am"],
    "bahia": ["bahia", "ba"],
    "ceará": ["ceara", "ce"],
    "distrito federal": ["distritofederal", "df"],
    "espírito santo": ["espiritosanto", "es"],
    "goiás": ["goias", "go"],
    "maranhão": ["maranhao", "ma"],
    "mato grosso": ["matogrosso", "mt"],
    "mato grosso do sul": ["matogrossodosul", "ms"],
    "minas gerais": ["minasgerais", "mg"],
    "pará": ["para", "pa"],
    "paraíba": ["paraiba", "pb"],
    "paraná": ["parana", "pr"],
    "pernambuco": ["pernambuco", "pe"],
    "piauí": ["piaui", "pi"],
    "rio de janeiro": ["riodejaneiro", "rj"],
    "rio grande do norte": ["riograndedonorte", "rn"],
    "rio grande do sul": ["riograndedosul", "rs"],
    "rondônia": ["rondonia", "ro"],
    "roraima": ["roraima", "rr"],
    "santa catarina": ["santacatarina", "sc"],
    "são paulo": ["saopaulo", "sp"],
    "sergipe": ["sergipe", "se"],
    "tocantins": ["tocantins", "to"]
    }
    counter = 0
    # checa se um nome valido de estado foi fornecido
    for estado, siglas in brazilian_states.items():
        counter+=1
        if state_search == estado or state_search in siglas:
            state_search = estado
            break
        else:            
            if counter >= len(brazilian_states):
                print("todo: error")
    counter = 0
    # checa se esse estado foi citado na biografia, caso contrário
    # retorne o dicionario de volta
    for values in range(len(result_dict)):
        counter+=1
        bio = result_dict[values]["bio"]
        if state_search.lower() in bio.lower():
            filtered_results.append(result_dict[values])
        else:
           pass
           # OBS sem verificação se sequer existe uma menção de estado na biografia da pessoa
    return filtered_results


