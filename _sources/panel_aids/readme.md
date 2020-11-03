    app = __import__('typer').Typer()

    @app.command()
    def mortgage_calculator():
        from .mortgage_calculator import __main__
