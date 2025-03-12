from functools import total_ordering
import part_functions
from flask import Flask, render_template, request
import re
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            part_number = request.form['part_number'].upper()
            part_number = part_number.replace('XO','X0')
            (bore, mounting, stroke, fractional_stroke, rod_style,
             ports, cushions, options, magnet, extension) = part_functions.split_part_number(part_number)
            front_head = part_functions.front_head_calc(bore, mounting, ports, cushions, rod_style)
            rear_cover = part_functions.rear_cover_calc(bore, mounting, ports, cushions, options, front_head)
            rod = part_functions.piston_rod_calc(bore,rod_style,stroke,fractional_stroke,extension)
            return render_template('result.html', bore=bore, mounting=mounting,
                                   stroke=stroke, fractional_stroke=fractional_stroke,
                                   rod_style=rod_style, ports=ports, cushions=cushions,
                                   options=options,magnet=magnet,extension=extension, front_head=front_head,
                                   rear_cover=rear_cover, rod=rod)
        except ValueError as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
