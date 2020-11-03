# Mortgage Calculator
This repo contains the code to run a mortgage calculator app using Panel.
To see a running version of this app, please visit (binder url here eventually).

## Install environment
You need conda installed to run this app.  Create the `panel` environment by running the following:
`conda env create -f environment.yml`

## Deploy App Locally
After having installed the environment, activate it with:
- `conda activate panel`  

Then start the app by running on the command line:
- `python -m mortgage_calculator`  

You can see the app by navigating to the url which will appear on the command line in a browser (IE 11 not supported).

## Run tests
To run the repo tests, run the following in the command line when in the repo root folder.  


    def main():
        from .mortgage_calculator import layout
        __import__("panel").serve(layout)