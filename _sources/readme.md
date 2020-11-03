# Panel Learning Aid

This repo contains a learning-aid notebook designed to get you up and running quickly with panel. 

## Running on Binder

The fastest way to access the learning aid notebook is by clicking the following link: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Quansight/panel-learning-aid/master?filepath=learning_aid.ipynb) which will launch the jupyterlab notebook in your browser.

## Running Locally

If you'd like to run this locally, clone the repository and follow the following steps:
- install the conda environment with `conda env create -f environment.yml`
- activate the environment with `conda activate panel`
- run the `learning_aid.ipynb` notebook with `jupyter notebook learning_aid.iypnb`


---

    def task_test():

test the `panel_aids` with `pytest`, settings are configured in `"pyproject.toml"`.

        return dict(actions=[["pytest"]])

    def task_book():

Build the docs using jupyter book.

            return dict(actions=[
                "jb build . --toc docs/_toc.yml --config docs/_config.yml"
            ], file_dep=['docs/_toc.yml', 'docs/_config.yml'], targets=['_build/html'])

    def task_pdf():

configure a pdf to build from the book task.

            object = task_book()
            object['actions'][0] += F"  --builder pdfhtml" 
            object['targets'][0] = object['targets'][0].replace('html', 'pdf')
            return object
