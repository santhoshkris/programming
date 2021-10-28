from ipywidgets import widgets
from IPython.display import display

a = widgets.FloatText()
b = widgets.FloatSlider()

c = widgets.Button(description="Hello")

display(a,b,c)