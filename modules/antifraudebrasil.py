from playwright.sync_api import sync_playwright
import requests
import argparse
from random import choice
from datetime import datetime
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from bs4 import BeautifulSoup
import json

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

    url = "https://antifraudebrasil.com/nome/api/criar-consulta.php"

    data = {
        "nome": (None, name),
        "email": (None, _email_generator()),
    }

    response = requests.post(url, files=data, timeout=30)

    texto_response = json.loads(response.text)
    if isinstance(texto_response["success"], bool):
        site_resposta = texto_response['redirect_url']
        site_resposta_get = requests.get(site_resposta)
        soup = BeautifulSoup(site_resposta_get.text, "html.parser")
        resultados = []

        for item in soup.select(".cpf-item"):
            cpf = item.get("data-cpf-full")

            nascimento = None
            idade = None

            for field in item.select(".cpf-field"):
                label = field.find("label").get_text(strip=True)
                value = field.find("strong").get_text(strip=True)

                if label == "Nascimento:":
                    nascimento = value
                elif label == "Idade:":
                    idade = value

            resultados.append({
                "cpf": cpf,
                "nascimento": nascimento,
                "idade": idade
            })
        return _antifraude_panels(name, resultados)
    else:
        error_panel = Panel(f"{texto_response["message"]}", 
                                   title=name.title(), 
                                   style="gold3")
        return Align.center(Columns(error_panel, align="center"))  

       
def _antifraude_panels(name, antifraude_cardname_list):
            panels = []
            for dictionary in antifraude_cardname_list:
                temp_panel = Panel(f"CPF: {dictionary['cpf']}\n"
                                   f"Nascimento: {dictionary['nascimento']}\n"
                                   f"Idade: {dictionary['idade']}\n", 
                                   title=name.title(), 
                                   style="gold3")
                panels.append(temp_panel)
                
            return Align.center(Columns(panels, align="center"))


def _email_generator():
    """
        Gera e-mails suficientemente aleatórios para não gerarem conflito com os
        de requisições passadas
    """
    chars = "abcdef123456xyz"
    email = [choice(chars) for times in range(3)] + ["@"] + ["gmail"] + [".com"]
    return "".join(email)

''' Funções possivelmente legadas e sujeitas a remoção permanente      
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
'''
if __name__ == "__main__":
    from rich.console import Console
    console = Console()
    main()