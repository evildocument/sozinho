def sozinho():
    from modules.escavador import escavador_scrapper
    from modules.tudosobretodos import tst_scrap
    from modules.antifraudebrasil import antifraude_name_scrapper
    
    import cmd
    import inspect
    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.align import Align
    
    from rich.console import Group

    '''
    module_list = ["escavador", "antifraudebrasil"]
    module_dict = {"nome": {"escavador": [escavador_scrapper, inspect.signature(escavador_scrapper)], 
                            "antifraudebrasil_nome": [modules.antifraudebrasil.antifraude_name_scrapper, 
                                                      inspect.signature(modules.antifraudebrasil.antifraude_name_scrapper)]},
                   
                   "cpf": {"antifraudebrasil_cpf": [modules.antifraudebrasil.antifraude_cpf_scrapper, 
                                                    inspect.signature(modules.antifraudebrasil.antifraude_cpf_scrapper)]}
                   }
    '''
    console = Console()
    class Sozinho(cmd.Cmd):
        def __init__(self):
            super().__init__()
            self.flag_dict = {"escavador": {"name_in_sequence": False, "state": None}, 
                              "tudosobretodos": {"verify": False,  "url": None, "year": None, "proxy_url": "http://localhost:8191/v1", "state": None, "rate_limit": 3, "display_limit":15} }
            self.cpf = False
            self.prompt = "> "
            #self.intro = "Digite '?' ou 'help' para a lista de comandos.\nOpções de busca:\nnome"
        def do_set_flag(self, arg):
            """
                Seta as flags opcionais para as pesquisas\n
                name_in_sequence => se o nome digitado está na sequencia correta (evita buscas por nomes parecidos)
                state => o estado para filtragem
            """
            flag = arg
            flags = flag.split()
            if len(flags) > 2:
                print("Apenas uma flag por vez.")
            elif len(flags) == 2:
                current_flag = flags[0].lower()
                value = flags[1].lower()
                
                if current_flag == "name_in_sequence":
                    if value == "true":
                        self.flag_dict["escavador"][current_flag] = True
                    elif value == "false":
                        self.flag_dict["escavador"][current_flag] = False
                    else:
                        print("Use: set_flag <flag> true|false")
                elif current_flag == "state":
                    self.flag_dict["escavador"][current_flag] = value
                    self.flag_dict["tudosobretodos"][current_flag] = value
                
            else:
                for key, value in self.flag_dict.items():
                    print(f"{key} => {value}")
        def do_test(self, arg):
            args = list(self.flag_dict["escavador"].values())            
            print(args)

        def do_nome(self, arg):
            """
                Executa uma pesquisa de nome no nome selecionado
            """
            name = arg
            name = name.replace('"', "").replace("'", "")
            name_parts = name.split()
            
            if len(name_parts) > 1:
                
                full_name = " ".join(name_parts)
                
                # cria um painel especifico para o antifraude
                antifraude_result = antifraude_name_scrapper(full_name)
                antifraude_panel = Panel.fit(
                            antifraude_result,
                            title="AntiFraudeBrasil",
                        )
                console.print(Align.center(antifraude_panel, vertical="middle"))

                # cria um painel especifico para os resultados do tudosobretodos
                tst_arguments = [full_name] + list(self.flag_dict["tudosobretodos"].values())
                tst_result = tst_scrap(*tst_arguments)

                if isinstance(tst_result, list):
                    conteudo = Group(*tst_result)
                else:
                    conteudo = tst_result

                tst_panel = Panel.fit(
                    conteudo,
                    title="TudoSobreTodos",
                )

                console.print(Align.center(tst_panel, vertical="middle"))

               
                
                # lista de argumentos para o escavador
                args_escavador = [full_name] + list(self.flag_dict["escavador"].values())
                escavador_result = escavador_scrapper(*args_escavador)
                # cria um painel especifico para o escavador
                escavador_panel = Panel.fit(
                            escavador_result,
                            title="Escavador",
                        )
                
                console.print(Align.center(escavador_panel, vertical="middle"))
                
                
            elif len(name_parts) == 1:
                console.print(Align.center("[red]É necessário um nome e sobrenome![/]\n"))
            else:
                print("Use: nome <nome>")
                
                
        def do_exit(self, arg):
            """
                Exit(sai) do modulo atual, ou do console, caso nenhum módulo esteja selecionado.
                exit
            """
            return True
    Sozinho().cmdloop()
    

