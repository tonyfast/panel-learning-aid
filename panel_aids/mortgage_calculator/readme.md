    def main():
        from .mortgage_calculator import layout
        __import__("panel").serve(layout)