from playwright.sync_api import sync_playwright
import argparse
# prototipo 1.5
'''
    Eu sei de agora que esse código não é o mais ideal, mas tenha pena da minha pobre alma, faz um bom tempo que não programo algo
    Limitações:
        De forma gratuita, é possível carregar apenas 3 páginas
        Também só é possível exibir 4 processos, independente de ser inativo ou ativo

'''
'''
TODO:
    Adicionar highlight para estados (e.g processos encontrados na >Bahia<) e informações importantes em geral
    Adicionar a opção de ter uma causa para um processo (e.g processo por Estado da Bahia ser por causa de violencia contra mulher)
    
    
    >> todo >> ERROR CHECKING!!! << todo <<<<
    

    parar de comentar em ingles, sem necessidade
    also, o que mais adicionar?
'''

def main():
    parser = argparse.ArgumentParser(description="tudosobretodos <pesquisa>"
                                     "opções:" 
                                     "--in_sequence          =>      confirma que o nome está em sequência (nome e sobrenome corretos)"
                                     "--from_state  <state>  =>      filtra o nome por resultados <desse> estado"
                                     "--ends_with   <name>   =>      filtra por nomes terminados com <esse> sobrenome"
                                     "--it_has_name <name>   =>      filtra por nomes que contem <esse> sobrenome"
                                     ,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        
    parser.add_argument("name", type=str, help="Nome a ser pesquisado")
    parser.add_argument("--in_sequence", action="store_true", help="Confirma que o nome está em sequência correta")
    parser.add_argument("--from_state", type=str, help="Filtra a pessoa pesquisada por estado")
    parser.add_argument("--ends_with", type=str, help="Filtra a pessoa pelo último sobrenome")
    parser.add_argument("--has_name", type=str, help="Filtra a pessoa por um nome do meio")
    args = parser.parse_args()
    if args.in_sequence and args.has_name:
        parser.error("--in_sequence já indica que o nome está em sequência correta, não faz sentido filtrar mais que isso")
    #print(args.name, args.in_sequence, args.from_state, args.ends_with, args.has_name)
    print(escavador_exhibit(escavador_scrapper(args.name, args.in_sequence, args.from_state, args.ends_with, args.has_name)))

def escavador_parser(content):
    '''
    ================
        Função que filtra todos os resultados que não sejam as pessoas físicas, como referências 
        e outros elementos HTML, além de retornar os resultados como um dicionário 
        para facilitar o processamento  
    ================      
    '''
    raw_request = [content.nth(i).evaluate("el => el.innerText") for i in range(content.count())]
    
    # ---- remove toda referência que não é a pessoa em si
    # ---- também removendo os 4 primeiras resultados do HTML, 
    # ---- que são só besteira
    

    filtered_request = [item for item in raw_request if 'página' not in item.lower()]
    filtered_request = [filtered_request[i].split("\n") for i in range(len(filtered_request))]
    result_list = filtered_request[4:]
    list_of_dicts = []
    
    for each_result in range(len(result_list)):
            result_dict = {}
            if len(result_list[each_result]) == 6:
                    result_dict = {
                    "nome": result_list[each_result][0],
                    "url": result_list[each_result][1],
                    "participacoes": result_list[each_result][3],
                    "bio": result_list[each_result][5]
                    }
                    list_of_dicts.append(result_dict)
            else:
                    result_dict = {
                            "nome": result_list[each_result][0],
                            "url": result_list[each_result][1],
                            "bio": "\n".join(result_list[each_result][2:])
                    }
            list_of_dicts.append(result_dict)
    return list_of_dicts



def escavador_scrapper(name_search, is_in_sequence=False, is_from_state=None, it_ends_with=None, it_has_name=None):
    """
        Função que serve para realizar o scrapping nas 3 páginas iniciais do escavador, retornando um dicionário
        com o número de páginas como chaves, e os valoes uma lista com o primeiro index o numero de resultados
        e como segundo os valores em si.
        SEPARADOR
        name_search -> <nome>                   o nome a ser pesquisado
        is_in_sequence -> <true|false>          o nome está em sequência, como é escrito
        is_from_state -> <estado>               pesquisar por um estado especifico
        it_ends_with -> <sobrenome>             se o nome do meio for desconhecido
        it_has_name -> <nome|sobrenome>         um nome ou sobrenome do meio
        
    """
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        # ---- definições necessárias porque a opção de headless não gera uma janela/ou gera com
        # ---- dimensões nulas.
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
            
            # ---- checa por filtros
            # horripilante no momento, it just werks
            if is_in_sequence and it_has_name:
                print("error")
                break
            elif is_in_sequence and is_from_state and it_ends_with:
                dict_master[current_page+1] = in_sequence(
                    from_state(ends_with(parsed_list, it_ends_with), is_from_state), name_search)
                
            elif is_in_sequence and is_from_state:
                dict_master[current_page+1] = in_sequence(
                    from_state(parsed_list, is_from_state),name_search)
            
            elif is_in_sequence and it_ends_with:
                dict_master[current_page+1] = in_sequence(
                    ends_with(parsed_list, it_ends_with),name_search)
            
            elif is_from_state and it_ends_with and it_has_name:
                dict_master[current_page+1] = from_state(
                    ends_with(has_name(parsed_list, it_has_name), it_ends_with), is_from_state)
                
            elif is_from_state and it_ends_with:
                dict_master[current_page+1] = from_state(
                    ends_with(parsed_list, it_ends_with), is_from_state)
            
            elif is_from_state and it_has_name:
                dict_master[current_page+1] = from_state(
                    has_name(parsed_list, it_has_name), is_from_state)
            
            elif it_ends_with and it_has_name:
                dict_master[current_page+1] = ends_with(
                    has_name(parsed_list, it_has_name), is_from_state)
            
            else:
                if is_in_sequence:
                    dict_master[current_page+1] = in_sequence(parsed_list, name_search)
                    
                elif is_from_state:
                    dict_master[current_page+1] = from_state(parsed_list, is_from_state)
                    
                elif it_ends_with:
                    dict_master[current_page+1] = ends_with(parsed_list, it_ends_with)
                    
                elif it_has_name:
                    dict_master[current_page+1] = has_name(parsed_list, it_has_name)
                    
                else:
                    dict_master[current_page+1] = parsed_list
                   
        browser.close()
        #dict_master = escavador_exhibit(dict_master)
 
        return dict_master
 
 
 
def escavador_exhibit(dict_master):
    """
    ================
        TODO: diferenciar de resultados de apenas 1 pagina e resultados filtrados (e.g nome exato)
        que só preenchem a 1 pagina (o escavador mostra primeiro os nomes mais parecidos)
        
        tambem quero falar em qual pagina esse elemento foi encontrado, e qual elemento ele é na pagina
        (e.g encontrado na pagina 2, é a 5 referência) algo assim
    ================
    """
    final_string = ""
    
    numberof_pages = len(dict_master)
    #numberof_res_pages = 0
    for list_of_lists in range(numberof_pages):
        current_page = dict_master[list_of_lists+1]
        for list_index in range(len(current_page)):
            
            final_string += "\n".join(f"{key.capitalize()}: {value}" for key,value in current_page[list_index].items())
            final_string += "\n\n"
    return final_string
    
  
       
def in_sequence(result_dict, name_search):
    '''
    ================
        Função que indica se o nome pesquisado está em sequência
        (e.g se João Souza da Silva for pesquisado, qualquer resultado que defira disso, 
         como:  João Silva Souza, será removido do filtro)
    ================
    '''
    
    filtered_results = []
    for values in range(len(result_dict)):
        name = result_dict[values]["nome"]
        if name.lower().startswith(name_search.lower()):
            filtered_results.append(result_dict[values])
        else:
            pass
    return filtered_results


def has_name(result_dict, name_search):
    '''
    ================
        Função que serve para filtrar resultados que contenham certo nome/sobrenome entre eles
    ================
    '''

    filtered_results = []
    for values in range(len(result_dict)):
        name = result_dict[values]["nome"]
        full_name = map(lambda x: x.lower(), name.split())
        if name_search.lower() in full_name:
            filtered_results.append(result_dict[values])
        else:
            pass
    return filtered_results
 
    
def ends_with(result_dict, name_search):
    '''
    ================
        Função que serve para filtrar resultados que terminem com um certo sobrenome/contrário do in_sequence
    ================
    '''
    filtered_results = []
    for values in range(len(result_dict)):
        name = result_dict[values]["nome"]
        if name.lower().endswith(name_search.lower()):
            filtered_results.append(result_dict[values])
        else:
            pass
    return filtered_results


def from_state(result_dict, state_search):
    '''
    ================
        Função que serve para filtrar resultados por estados
    ================
    '''
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
    # ---- checa se um nome valido de estado foi fornecido
    for estado, siglas in brazilian_states.items():
        counter+=1
        if state_search == estado or state_search in siglas:
            state_search = estado
            break
        else:            
            if counter >= len(brazilian_states):
                print("todo: error")
    counter = 0
    # ---- checa se esse estado foi citado na biografia, caso contrário
    # ---- retorne o dicionario de volta
    for values in range(len(result_dict)):
        counter+=1
        bio = result_dict[values]["bio"]
        if state_search.lower() in bio.lower():
            filtered_results.append(result_dict[values])
        else:
           pass
           # --- OBS sem verificação se sequer existe uma menção de estado na biografia da pessoa
           # --- heheheheheheh xd
    return filtered_results


if __name__ == "__main__":
    main()