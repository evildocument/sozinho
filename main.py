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
        def do_nome(self, arg):
            
        
        def do_exit(self, arg):
            """
                Exit(sai) do modulo atual, ou do console, caso nenhum módulo esteja selecionado.
                exit
            """
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
    

