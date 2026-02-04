def sozinho():
    from modules.escavador import escavador_scrapper
    from modules.tudosobretodos import tst_scrap
    from modules.antifraudebrasil import antifraude_name_scrapper, antifraude_cpf_scrapper
    import cmd
    # import inspect
    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.align import Align
    from rich.tree import Tree
    from rich.console import Group
    # import traceback

    '''
    ==== talvez volte no futuro
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
            # ----- dicionario responsavel por armazenar as flags de cada modulo/funcao
            self.flag_dict = {"escavador": {"name_in_sequence": False, "state": None}, 
                              "tudosobretodos": {"verify": False,  "url": None, "year": None, "flareproxy": "http://localhost:8191/v1", "state": None, "rate_limit": 3, "display_limit":15} }
            self.cpf = False
            self.prompt = "[sozinho]> "
            self.warning = "[!]"
            self.error = "[X]"
            # ----- sem uso ----- self.intro = "Digite '?' ou 'help' para a lista de comandos.\nOpções de busca:\nnome"
        def do_set_flag(self, arg):
            """
            ================
                Seta as flags opcionais para as pesquisas
                
                Escavador
                    •  name_in_sequence => se o nome digitado está na sequencia correta (evita buscas por nomes parecidos)
                    •  state => o estado para filtragem
                
                TudoSobreTodos
                    •   verify => verificar por vizinhos
                    •   flareproxy => a url do flare proxy
                    •   rate_limit => limite de pagins baixadas
                    •   display_limit => limite de resultados a serem mostrado
            ================
            """
            flag = arg
            flags = flag.split()
            if len(flags) > 2:
                console.print(f"[red3]{self.warning}Apenas uma flag por vez.[/]")
            elif len(flags) == 2:
                current_flag = flags[0].lower()
                value = flags[1].lower()
                
                # ================ 
                #   Escavador
                # ================
                if current_flag == "name_in_sequence":
                    if value == "true":
                        self.flag_dict["escavador"][current_flag] = True
                    elif value == "false":
                        self.flag_dict["escavador"][current_flag] = False
                    else:
                        console.print(f"[red3]{self.warning}Use: set_flag name_in_sequence true|false[/]")
                
                
                # ================ 
                #   TudoSobreTodos
                # ================
                elif current_flag == "state":
                    self.flag_dict["escavador"][current_flag] = value
                    self.flag_dict["tudosobretodos"][current_flag] = value
                
                elif current_flag == "verify":
                    if value == "true":
                        self.flag_dict["tudosobretodos"][current_flag] = True
                    elif value == "false":
                        self.flag_dict["tudosobretodos"][current_flag] = False
                    else:
                        console.print(f"[red3]{self.warning}Use: set_flag verify true|false[/]")
                
                elif current_flag == "flareproxy":
                    self.flag_dict["tudosobretodos"][current_flag] = value
                
                elif current_flag == "rate_limit":
                    try:
                        self.flag_dict["tudosobretodos"][current_flag] = int(value)
                    except ValueError:
                        # print(traceback.format_exc())
                        console.print(f"[red]{self.warning}Use: set_flag rate_limit <numero>[/]")
                
                elif current_flag == "display_limit":
                    try:
                        self.flag_dict["tudosobretodos"][current_flag] = int(value)
                    except ValueError:
                        #print(traceback.format_exc())
                        console.print(f"[red]{self.warning}Use: set_flag display_limit <numero>[/]")
            elif len(flags) == 1:
                console.print(f"[red3]{self.warning}Argumento não existe.\nUse: self_flag\nsem argumentos para obter a lista de flags[/]")                       

            # ----- set_flag sem argumentos, converte o dicionario de argumentos em arvore e imprime
            else:
                tree = self.dict_to_tree(self.flag_dict)
                console.print(tree)


        """
        def do_test(self, arg):
            args = list(self.flag_dict["escavador"].values())            
            print(args)
        """
        

        def do_nome(self, arg):
            """
            ================
                Executa uma pesquisa de nome no nome selecionado
            ================
            """
            name = arg
            name = name.replace('"', "").replace("'", "")
            name_parts = name.split()
            
            if len(name_parts) > 1:
                
                full_name = " ".join(name_parts)
                
                # ----- cria um painel especifico para o antifraude
                antifraude_result = antifraude_name_scrapper(full_name)
                antifraude_panel = Panel.fit(
                            antifraude_result,
                            title="AntiFraudeBrasil",
                        )
                console.print(Align.center(antifraude_panel, vertical="middle"))


                # ----- cria a lista de argumentos e um painel especifico para os resultados do tudosobretodos
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

               
                # ----- cria a lista de argumentos e um painel especifico para os resultados do escavador
                args_escavador = [full_name] + list(self.flag_dict["escavador"].values())
                escavador_result = escavador_scrapper(*args_escavador)
                escavador_panel = Panel.fit(
                            escavador_result,
                            title="Escavador",
                        )
                
                console.print(Align.center(escavador_panel, vertical="middle"))
                
                
            elif len(name_parts) == 1:
                console.print(Align.center("[red]É necessário um nome e sobrenome![/]\n"))
            else:
                console.print("[red]Use: nome <nome>[/]")
                

        def do_cpf(self, arg):
            if len(arg) == 11:
                cpf = arg
                # ----- cria um painel especifico para o antifraude
                antifraude_result = antifraude_cpf_scrapper(cpf)
                antifraude_panel = Panel.fit(
                            antifraude_result,
                            title="AntiFraudeBrasil",
                        )
                console.print(Align.center(antifraude_panel, vertical="middle"))
            else:
                console.print("[red]Use: cpf <cpf>[/]")
            
            
        def do_exit(self, arg):
            """
            ================
                Sai do console.
            ================
            """
            return True
        

        
        def dict_to_tree(self, data: dict, root_name="[bold]Argumentos[/]"):
            """
            ================
                Transforma o dicionário de flags (argumentos) em uma árvore
            ================
            """
            tree = Tree(root_name)
            def format_value(value):
                if value is None:
                    return "[dim]None[/]"
                if isinstance(value, bool):
                    if value == False:
                        return f"[red]{value}[/]"
                    else:
                        return f"[green]{value}[/]"
                if isinstance(value, int):
                    return f"[blue]{value}[/]"
                return f"[cyan]{value}[/]"
            
            def add_branch(branch, obj):
                for key, value in obj.items():
                    if isinstance(value, dict):
                        sub = branch.add(f"[bold]{key}[/]")
                        add_branch(sub, value)
                    else:
                        branch.add(f"{key} : {format_value(value)}")

            add_branch(tree, data)

            return tree
        


    Sozinho().cmdloop()
    

