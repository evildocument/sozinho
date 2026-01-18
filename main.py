def sozinho():
    from modules.escavador import escavador_scrapper, escavador_exhibit
    import modules.tudosobretodos
    import modules.antifraudebrasil
    
    import cmd
    import inspect
    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.align import Align
    
    module_list = ["escavador", "antifraudebrasil"]
    module_dict = {"nome": {"escavador": [escavador_scrapper, inspect.signature(escavador_scrapper)], 
                            "antifraudebrasil_nome": [modules.antifraudebrasil.antifraude_name_scrapper, 
                                                      inspect.signature(modules.antifraudebrasil.antifraude_name_scrapper)]},
                   
                   "cpf": {"antifraudebrasil_cpf": [modules.antifraudebrasil.antifraude_cpf_scrapper, 
                                                    inspect.signature(modules.antifraudebrasil.antifraude_cpf_scrapper)]}
                   }
    console = Console()
    class Sozinho(cmd.Cmd):
        def __init__(self):
            super().__init__()
            self.flag_dict = {"name_in_sequence": False, "state": None}
            self.prompt = "> "
            self.intro = "Digite '?' ou 'help' para a lista de comandos.\nOpções de busca: nome\ncpf"
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
                        self.flag_dict[current_flag] = True
                    elif value == "false":
                        self.flag_dict[current_flag] = False
                    else:
                        print("Use: set_flag <flag> true|false")
                elif current_flag == "state":
                    self.flag_dict[current_flag] = value
            else:
                for key, value in self.flag_dict.items():
                    print(f"{key} => {value}")
                    
                    
        def _antifraude_panels(self, name):
            antifraude_cardname_list = modules.antifraudebrasil.antifraude_name_scrapper(name)
            mapped_items = list(map(lambda x: Panel("\n".join(x[1:]), title=x[0]), antifraude_cardname_list))
            return mapped_items
            
            
        def do_nome(self, arg):
            """
                Executa uma pesquisa de nome no nome selecionado
            """
            name = arg
            name = name.replace('"', "").replace("'", "")
            name_parts = name.split()
            
            if len(name_parts) > 1:
                
                full_name = " ".join(name_parts)
                
                console.print(Columns(self._antifraude_panels(full_name), align="center"))
                
                args = [full_name] + list(self.flag_dict.values())
                escavador_result = escavador_scrapper(*args)
                panel = Panel.fit(
                            escavador_result,
                            title="Escavador",
                        )
                console.print(Align.center(panel, vertical="middle"))
                
                
                
            elif len(name_parts) == 1:
                print("Aviso: você dificilmente vai conseguir um resultado preciso de volta pesquisando apenas por um nome\n")
                print(f"Resultados do escavador:\n{escavador_scrapper(name)}")
                
                console.print(Columns(self._antifraude_columns(full_name)))
            else:
                print("Use: nome <nome>")
                
                
        def do_exit(self, arg):
            """
                Exit(sai) do modulo atual, ou do console, caso nenhum módulo esteja selecionado.
                exit
            """
            return True
    Sozinho().cmdloop()
    

