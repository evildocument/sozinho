if __name__ == "__main__":
    import main
    from core.banner import banner
    from time import sleep
    from rich.console import Console
    from rich.align import Align
    console = Console()
    console.print(Align.center(banner(), vertical="middle"))
    sleep(0.5)
    # TODO: transformar isso em dinamico xxdxd
    console.print(Align.center("Digite '?' ou 'help' para a lista de comandos.\nOpções de busca:\n", vertical="middle"))
    console.print(Align.center("• [bold green]Nome[/]\n• [bold green]CPF[/]", vertical="middle"))
    main.sozinho()