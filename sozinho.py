if __name__ == "__main__":
    import main
    from core.banner import banner
    from time import sleep
    from rich.console import Console
    from rich.align import Align
    console = Console()
    print(banner())
    sleep(0.5)
    #todo transformar isso em dinamico xxdxd
    console.print(Align.center("Digite '?' ou 'help' para a lista de comandos.\nOpções de busca:\n", vertical="middle"))
    console.print(Align.center("Nome", vertical="middle"))
    main.sozinho()