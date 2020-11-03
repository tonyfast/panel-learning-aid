with __import__("tingle").Markdown():
    from . import readme

__import__('typer').run(readme.main)
