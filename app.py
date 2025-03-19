from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        series = request.form.get('series')
        part_number = request.form['part_number'].upper()

        if series == 'NFPA':
            import part_functions_nfpa as pf
            template = 'result_nfpa.html'
        elif series == 'Round Body':
            import part_functions_roundbody as pf
            template = 'result_roundbody.html'
        # etc. for other series

        parsed_data = pf.split_part_number(part_number)
        bom = pf.generate_bom(parsed_data)

        # If you want to pass the parsed_data individually:
        # For Round Body, maybe it's (prefix, size, stroke_code, suffix)
        if series == 'Round Body':
            prefix, size, stroke_code, suffix = parsed_data
            return render_template(template,
                                   part_number=part_number,
                                   prefix=prefix,
                                   size=size,
                                   stroke_code=stroke_code,
                                   suffix=suffix,
                                   bom=bom)
        else:
            # NFPA: maybe it's (bore, mounting, stroke, fractional_stroke, rod_style, ports, cushions, options, magnet, extension)
            bore, mounting, stroke, fractional_stroke, rod_style, ports, cushions, options, magnet, extension, xi_num = parsed_data
            return render_template(template,
                                   part_number=part_number,
                                   bore=bore,
                                   mounting=mounting,
                                   stroke=stroke,
                                   fractional_stroke=fractional_stroke,
                                   rod_style=rod_style,
                                   ports=ports,
                                   cushions=cushions,
                                   options=options,
                                   magnet=magnet,
                                   extension=extension,
                                   xi_num=xi_num,
                                   **bom)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
