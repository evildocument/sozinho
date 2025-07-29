import re
from playwright.sync_api import sync_playwright
# prototipo 1
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
    
    Add highlight to state keywords (e.g processes found in >Bahia<) and important info in general
    Add the option to showing a reason for a legal action
'''
def escavador_parser(content):
    '''
        Função que filtra todos os resultados que não sejam as pessoas físicas, como referências 
        e outros elementos HTML
        
        A function to filter every result that isn't actual people, like references or other HTML elements
    '''
    results = [div_content.nth(i).evaluate("el => el.innerText") for i in range(content.count())]
    
    # remove every reference that is not the person itself
    # also the first 4 results are just junk from the HTML
    filtered_res = [item for item in results if 'página' not in item.lower()]
    filtered_res = [filtered_res[i].split("\n") for i in range(len(filtered_res))]
    return [filtered_res[4:], len(filtered_res[4:])]

with sync_playwright() as driver:
    browser = driver.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
        viewport={"width":1280, "height": 800},
    )
    page = context.new_page()
    name_search = input("> ")
    all_results = {}
    '''
        TODO: adicionar lógica para checar se houverem 3 ou menos resultados na página inicial, automaticamente expandir nos motivos
        dos processos
    '''
    for current_page in range(2):
        page.goto(f"https://www.escavador.com/busca?q={name_search}&qo=t&page={current_page+1}")
        page.wait_for_selector('div.item')
        div_content = page.locator('div.item')
        parsed_result = escavador_parser(div_content)
        # {1 (primeira pagina): [[[lista1],[lista2]], numero_de_resultados], 2: (segunda pagina)...}
        all_results[current_page+1] = parsed_result
    browser.close()

