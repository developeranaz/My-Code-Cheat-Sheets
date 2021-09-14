# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 23:19:51 2021

@author: kalas
"""
from pywebio.input import input, FLOAT
from pywebio.output import put_text

from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info




def main():
    """BMI Calculation
    Simple application for calculating Body Mass Index.
    
    """

    put_markdown("""# Body Mass Index
    
    [Body mass index](https://en.wikipedia.org/wiki/Body_mass_index) (BMI) is a measure of body fat based on height and weight that applies to adult men and women. 
    
    BMI Categories:
    
    | Category             | BMI           |
    | -------------------- | ------------- |
    | Severely underweight | BMI<14.9      |
    | Underweight          | 14.9≤BMI<18.4 |
    | Normal               | 18.4≤BMI<22.9 |
    | Overweight           | 22.9≤BMI<27.5 |
    | Moderately obese     | 27.5≤BMI<40   |
    | Severely obese       | BMI≥40        |
    
    ## BMI calculation
    The source code of this application is [here](https://github.com/wang0618/PyWebIO/blob/dev/demos/bmi.py)
    """, strip_indent=4)

    info = input_group('BMI calculation', [
        input("Your Height(cm)", name="height", type=FLOAT),
        input("Your Weight(kg)", name="weight", type=FLOAT),
    ])

    BMI = info['weight'] / (info['height'] / 100) ** 2

    top_status = [(14.9, 'Severely underweight'), (18.4, 'Underweight'),
                  (22.9, 'Normal'), (27.5, 'Overweight'),
                  (40.0, 'Moderately obese'), (float('inf'), 'Severely obese')]

    for top, status in top_status:
        if BMI <= top:
            put_markdown('Your BMI: `%.1f`, Category: `%s`' % (BMI, status))
            break
 

    
from pywebio.platform.flask import webio_view
from flask import Flask

app = Flask(__name__)

app.add_url_rule('/tool', 'webio_view', webio_view(main),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

app.run()
