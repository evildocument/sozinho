def sozinho():
    from modules.escavador import escavador_scrapper, escavador_exhibit
    import modules.tudosobretodos
    import modules.antifraudebrasil
    import argparse
    import cmd
    import inspect
    
    module_list = ["escavador", "antifraudebrasil"]
    module_dict = {"escavador": [escavador_scrapper, inspect.signature(escavador_scrapper)], 
                   "antifraudebrasil": [modules.antifraudebrasil.antifraude_cpf_scrapper, inspect.signature(modules.antifraudebrasil.antifraude_cpf_scrapper)]}
    class Sozinho(cmd.Cmd):
        def __init__(self):
            super().__init__()
            # modulo atual, atualiza a se usar <select>
            self.current_module = ""
            # checa se um modulo foi selecionado, destravando outras funcoes, 
            # como <set> e <show options/arguments>
            self.module_selected = False
            # carrega os argumentos do modulo
            self.module_options = ""
            # dicionario que armazena os valores para cada argumento da função principal de cada modulo
            self.module_args_dict = {}
            # descricao da funcao
            self.desc = ""
            # argumentos da funcao
            self.func = ""
            # prompt padrão e introdução padrão
            self.prompt = f"{self.current_module}> "
            self.intro = "Digite '?' ou 'help' para a lista de comandos.\nMódulos disponiveis: Escavador, antifraudebrasil (cpf)"
        def do_run (self, arg):
            """
                Serve para executar uma função, uma vez que os argumentos estejam saciados.
                modo de uso: run
                (sem argumentos)
            """
            valid_args = False
            if self.module_selected:
                signature = module_dict[self.current_module][1]
                for name, parameter in signature.parameters.items():
                    if parameter.default is inspect.Parameter.empty:
                        if self.module_args_dict.get(name) is None:
                            valid_args = False
                            # TODO
                            # exibir no <show arguments> qual funcao é obrigatoria
                            print(f"{name} é obrigatório. Use <show arguments>")
                            break
                        else:
                            valid_args = True
                if valid_args == True:
                    args = [self.module_args_dict.get(key) for key in self.module_options]
                    print(module_dict[self.current_module][0](*args))
                else:
                    pass
                        
                
                        
                    
        def do_show(self, arg):
            '''
                Show(mostra) modulos ou opções
                    show modules ->         lista de modulos
                    show arguments ->       lista de argumentos necessários e opcionais do modulo
                    show options ->         lista de argumentos selecionados por você
            '''
            if arg == "modules":
                print("Modulos disponiveis:\n")
                for modulo in module_list:
                    print(modulo)
            elif self.module_selected:
                if arg == "options":
                    if len(self.module_args_dict) >= 1:
                        for functions, arguments in self.module_args_dict.items():
                            print(f"{functions} -> {arguments}")
                    else:
                        print("Use <show arguments>")
                elif arg == "arguments":
                    print("set <função> <argumento(s)>")
                    print(self.func)
            else:
                print("Selecione um módulo.")
        def do_set(self, arg):
            """
                Serve para 
            """
            if self.module_selected:
                # divide o argumento em partes
                # set <funcão do modulo> <argumentos>
                parts = arg.split()
                if len(parts) > 1:
                    module_function = parts[0]
                    if module_function in self.module_options:
                        argument = " ".join(parts[1:])
                        if argument.lower() == "true":
                            self.module_args_dict[module_function] = True
                        elif argument.lower() == "false":
                            self.module_args_dict[module_function] = False
                        else:
                            self.module_args_dict[module_function] =  argument
                        
                    else:
                        print("Argumento não encontrado. Use show arguments.")
                else:
                    print("set <funcao> <argumentos>")
            else:
                print("Selecione um modulo primeiro! <show modules>")
        def do_select(self, modulo):
            """
            
            """
            '''
                Select(seleciona) um módulo para uso
            '''  
            if modulo in module_list:
                # reseta argumentos, define o modulo atual, indica o modulo atual no
                # prompt, indica que no momento um modulo está selecionado,
                # busca as opções desse modulo em especifico
                self.module_args_dict = {}
                self.current_module = modulo.lower()
                self.prompt = f"{self.current_module}> "
                self.module_selected = True
                self.module_options = list(module_dict[self.current_module.lower()][1].parameters.keys())
                doc = inspect.getdoc(module_dict[self.current_module.lower()][0])
                self.desc = doc.split("SEPARADOR")[0]
                self.func = doc.split("SEPARADOR")[1]
            else:
                print("Modulo inexistente!")
        
        def do_exit(self, arg):
            if len(self.current_module) > 0:
                self.current_module = ""
                self.module_selected = False
                self.module_options = ""
                self.module_args_dict = {}
                self.desc = ""
                self.func = ""
                self.prompt = f"{self.current_module}> "
            else:
                return True
    Sozinho().cmdloop()
    

