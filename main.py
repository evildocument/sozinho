def sozinho():
    from modules.escavador import escavador_scrapper, escavador_exhibit
    import modules.tudosobretodos
    import modules.antifraudebrasil
    import argparse
    import cmd
    import inspect
    
    module_list = ["escavador", "antifraudebrasil"]
    module_dict = {"nome": {"escavador": [escavador_scrapper, inspect.signature(escavador_scrapper)], 
                            "antifraudebrasil_nome": [modules.antifraudebrasil.antifraude_name_scrapper, 
                                                      inspect.signature(modules.antifraudebrasil.antifraude_name_scrapper)]},
                   
                   "cpf": {"antifraudebrasil_cpf": [modules.antifraudebrasil.antifraude_cpf_scrapper, 
                                                    inspect.signature(modules.antifraudebrasil.antifraude_cpf_scrapper)]}
                   }
    class Sozinho(cmd.Cmd):
        def __init__(self):
            super().__init__()
            self.flag_dict = {"name_in_sequence": False, "state": None}
            self.prompt = "> "
            self.intro = "Digite '?' ou 'help' para a lista de comandos.\nOpções de busca: nome\ncpf"
        def do_set_flag(self, arg):
            """
                Seta as flags opcionais para as pesquisas
                name_in_sequence => flag se o nome digitado esta na sequencia correta (evita buscas por nomes parecidos)
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
                print("lol")
            
            print(self.flag_dict)
        def do_nome(self, arg):
            """
                Executa uma pesquisa de nome no nome selecionado
            """
            name = arg
            name_parts = name.split()
            if len(name_parts) > 1:
                full_name = " ".join(name_parts)
                args = [full_name] + list(self.flag_dict.values())
                print("Resultados do escavador:")
                print(escavador_scrapper(*args))
                print()
                print(modules.antifraudebrasil.antifraude_name_scrapper(full_name))
            else:
                print("Aviso: você dificilmente vai conseguir um resultado preciso de volta pesquisando apenas por um nome\n")
                print("Resultados do escavador:")
                print(escavador_scrapper(name))
                print()
                print(modules.antifraudebrasil.antifraude_name_scrapper(name))
        def do_exit(self, arg):
            """
                Exit(sai) do modulo atual, ou do console, caso nenhum módulo esteja selecionado.
                exit
            """
            return True
    Sozinho().cmdloop()
    

