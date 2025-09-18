from playwright.sync_api import sync_playwright
import requests
import argparse
from random import choice
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
        print(antifraude_name_scrapper(args.name))
    elif args.cpf is not None:
        print(antifraude_cpf_scrapper(args.cpf))
        

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
        "email": f"{email_generator()}",
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
    url = "https://antifraudebrasil.com/nome/consultar/"
    data = {
        "email": f"{email_generator}",
        "placa": f"{name}",
        "recaptchaResponse": "empty"
    }

    response = requests.post(url, data=data).text
    
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto(url)
        print(page.title())  
        browser.close()
        

def email_generator():
    chars = "abcdef123456xyz"
    email = [choice(chars) for times in range(3)] + ["@"] + [choice(chars) for times in range(3)] + [".com"]
    return "".join(email)
if __name__ == "__main__":
    main()