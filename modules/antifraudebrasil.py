from playwright.sync_api import sync_playwright
import requests
import argparse
from random import choice
from datetime import datetime
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align

'''
    TODO: adicionar verificação por nome
    18/08/25 - não terminado
'''
def main():
    parser = argparse.ArgumentParser(description="antifraudebrasil --name <nome>\n"
                                    "antifraudebrasil --cpf <cpf>",
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--name", type=str, help="O nome a ser pesquisado")
    group.add_argument("-c", "--cpf", type=int, help="O cpf a ser pesquisado")

    args = parser.parse_args()
    if args.name is not None:
        # NOT FINISHED
        console.print(Align.center(antifraude_name_scrapper(args.name), vertical="middle"))
    elif args.cpf is not None:
        print(antifraude_cpf_scrapper(args.cpf))
    else:
        print("Sem resultados")
        

def antifraude_cpf_scrapper(cpf):
    """
    ================
        Função de busca por CPF, retornando nome completo.
        SEPARADOR
        cpf -> <cpf>                o cpf a ser pesquisado
    ================
    """
    url = "https://antifraudebrasil.com/consultar/consulta-r.php"
    data = {
        "email": f"{_email_generator()}",
        "placa": f"{cpf}",
        "recaptchaResponse": "empty"
    }

    response = requests.post(url, data=data).text
    response = response.replace("nome ", "")
    if len(response) == 0:
        return "Sem resultados"
    else:
        return response

def antifraude_name_scrapper(name):
    '''
        Função de busca por nome, contem JS
        TODO
        TODO
        TODO
    '''
    url = "https://antifraudebrasil.com/nome/"
    

    #response = requests.post(url, data=data).text
    
    with sync_playwright() as driver:
        
        if len(name) > 8:
            browser = driver.chromium.launch(headless=True)  
            page = browser.new_page()
            page.goto(url)
            
            
            page.fill("input[name='placa']", name)
            page.fill("input[name='email']", _email_generator())
            button = page.locator("button[type='submit']")
            button.click(force=True)
            
           

            # Armazena os cards de cpf e data de nascimento que retornaram,
            # sendo esses separados pela div .infoCard_Found, primeiro arguardando esse elemento retornar
            
            page.wait_for_selector(".infoCard__found", timeout=100000)
            
            cards = page.locator(".infoCard__found")
            raw_results = cards.all_inner_texts()
            
            
            # Se o dicionário final "parsed_results" conter algum resultado:
            parsed_results = _antifraude_raw_to_dict_parser(raw_results)
            if parsed_results:
                dict_results = _antifraude_result_dict_parser(parsed_results)
            else:
                browser.close()
                return None
            browser.close()
            
            final_results = []
            for dict_index in range(len(dict_results)):
                final_results.append([name.capitalize(), dict_results[dict_index]['cpf'], dict_results[dict_index]['nascimento']])
            return _antifraude_panels(final_results)
        else:
            return None
       
def _antifraude_panels(antifraude_cardname_list):
            mapped_items = list(map(lambda x: Panel("\n".join(x[1:]), title=x[0].capitalize(), style="gold3"), antifraude_cardname_list))
            return Align.center(Columns(mapped_items, align="center"))


def _antifraude_raw_to_dict_parser(raw_results):
    """
    Recebe a lista vinda de cards.all_inner_texts() e retorna
    uma lista de dicionários com cpf e nascimento.
    """
    
    # Junta tudo em uma única string (caso haja mais de 1 container)
    if len(raw_results) > 0:
        all_text = "\n".join(raw_results)

        # Divide em blocos a partir de "CPF:" e remove vazios
        blocos = [f"CPF:{x.strip()}" for x in all_text.split("CPF:") if x.strip()]

        resultados = []
        for bloco in blocos:
            linhas = bloco.split('\n')
            cpf = linhas[0].replace('CPF:', '').strip()
            nascimento = "".join(linhas[1:]).replace('Nascimento:', '').strip()
            resultados.append({'cpf': cpf, 'nascimento': nascimento})

        return resultados
    else:
        return None


def _email_generator():
    """
        Gera e-mails suficientemente aleatórios para não gerarem conflito com os
        de requisições passadas
    """
    chars = "abcdef123456xyz"
    email = [choice(chars) for times in range(3)] + ["@"] + [choice(chars) for times in range(3)] + [".com"]
    return "".join(email)


def _antifraude_result_dict_parser(parsed_results):
    """
        Função responsável por processar, formatar e armazenar de um dicionário para outro
        os resultados de requisições (cpf e data de nascimento)
    """
    current_year = datetime.now().year - 2000
    for dict_index in range(len(parsed_results)):
            updated_antifraude_date_result = ""
            nascimento_key = parsed_results[dict_index]['nascimento']
            
            antifraude_current_year = nascimento_key[19:21]
            antifraude_current_month = nascimento_key[15:16]
            antifraude_current_day = nascimento_key[11:13]
            
            
            # dia/
            updated_antifraude_date_result += antifraude_current_day + "/"
            
            # dia/mes
            if antifraude_current_month == 1 or antifraude_current_month == 2:
                    updated_antifraude_date_result += f"1{antifraude_current_month} ou 0{antifraude_current_month}/"
            else:
                    updated_antifraude_date_result += f"0{antifraude_current_month}/"
            
            # dia/mes/ano        
            if current_year >= int(antifraude_current_year):
                    updated_antifraude_date_result += f"19{antifraude_current_year} ou 20{antifraude_current_year}"
            else:
                    updated_antifraude_date_result += f"19{antifraude_current_year}"
            
            # Adiciona ao dicionário final "parsed_results"
            parsed_results[dict_index].update({"nascimento": updated_antifraude_date_result}) 
    return parsed_results

if __name__ == "__main__":
    from rich.console import Console
    console = Console()
    main()