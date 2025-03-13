from functools import total_ordering
import part_functions
from flask import Flask, render_template, request
import re

from part_functions import cushion_position, port_position, rod_bushing_calc, tie_rod_calc, double_rod_codes

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            part_number = request.form['part_number'].upper()
            part_number = part_number.replace('XO','X0')

            (bore, mounting, stroke, fractional_stroke, rod_style, #split part number into sections to evaluate
             ports, cushions, options, magnet, extension) = part_functions.split_part_number(part_number)

            if mounting == 'T6' and (cushions in ('C', 'G', 'E', 'J') or port_position[ports] in ('2','4')):
                return render_template('index.html',
                       error="Error: Mounting 'T6' is incompatible with head cushions or port at positions 1 & 2.")
            if mounting == 'S4' and (cushion_position[cushions]=='3' or port_position[ports]=='3'):
                return render_template('index.html',
                       error="Error: Mounting 'S4' is incompatible with cushions or ports at position 3.")
            front_head = part_functions.front_head_calc(bore, mounting, ports, cushions, rod_style)
            rear_cover = part_functions.rear_cover_calc(bore, mounting, ports, cushions, options, rod_style)
            rod = part_functions.piston_rod_calc(bore,rod_style,stroke,fractional_stroke,extension, options)
            rod_2 = None
            piston_head = part_functions.piston_head_calc(bore,rod_style,options)
            rod_bushing = part_functions.rod_bushing_calc(bore,rod_style,options)
            cylinder_tube = part_functions.tube_calc(bore,options,stroke)
            tie_rod= part_functions.tie_rod_calc(bore,options,stroke,mounting)
            tie_rod_2 = None
            rod_seal = part_functions.rod_seal_calc(bore,rod_style,options)
            piston_seal = part_functions.piston_seal_calc(bore,rod_style,options)
            if mounting == 'S1':
                adder = {'15':.65,'20':.625,'25':.65,'32':1,'40':1.1,'50':1,'60':1.15, '80':.5}
                tie_rod_2 = part_functions.tie_rod_calc(bore,options,int(stroke)+adder[bore],mounting)
            if options in double_rod_codes:
                if extension and extension.startswith('CD'):
                    rod_2 = part_functions.piston_rod_calc(bore,rod_style,stroke,fractional_stroke,None, options)
                elif not extension:
                    rod +='  '+'(2)'
            return render_template('result.html', part_number=part_number, bore=bore, mounting=mounting,
                                   stroke=stroke, fractional_stroke=fractional_stroke,
                                   rod_style=rod_style, ports=ports, cushions=cushions,
                                   options=options,magnet=magnet,extension=extension, front_head=front_head,
                                   rear_cover=rear_cover, rod=rod, rod_2=rod_2, piston_head=piston_head,
                                   rod_bushing=rod_bushing, cylinder_tube=cylinder_tube, tie_rod=tie_rod,
                                   tie_rod_2=tie_rod_2, rod_seal=rod_seal, piston_seal=piston_seal)
        except ValueError as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
