# a ManimCE animation or two from GPTP 2024

## Setup

I tend to work in VScode with Jupyter. In case that's mysterious or weird, here's how I set it up:

1. I used python3; no idea if you need to do so
2. create a [`venv` virtual environment in the folder](https://docs.python.org/3/library/venv.html) and activate it (you can do this in the `TERMINAL` tab of VScode)
3. activate the `venv` either with the Python environments plugin in VScode, or manually on the CLI (`source venv/bin/activate`)
4. [install Manim](https://docs.manim.community/en/stable/installation.html) I installed it in the `venv` directly, despite having it in my system as well; just make sure it can be invoked from within your project. Be sure you have access to the dependencies as well (`pango` `pkg-config` `scipy`)
5. install `matplotlib` and `seaborn`
6. To use [Jupyter notebooks in VSCode](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) you need to do a local `pip install ipykernel`, as of this writing

I just worked through that again in this fresh repo, and the `.ipynb` file worked for me.