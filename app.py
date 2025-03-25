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

        try:
            parsed_data,part_number_new = pf.split_part_number(part_number)
            # generate_bom internally calls functions that check these conditions
            bom = pf.generate_bom(parsed_data)
        except ValueError as e:
            error = str(e)
            return render_template('index.html', error=error)

        # Depending on the series, unpack the parsed_data accordingly
        if series == 'Round Body':
            prefix,bore,style,stroke,options,extension = parsed_data
            return render_template(template,
                                   part_number=part_number,
                                   part_number_new=part_number_new,
                                   prefix=prefix,
                                   bore=bore,
                                   style=style,
                                   stroke=stroke,
                                   options=options,
                                   extension=extension,
                                   **bom)
        else:
            # For NFPA series, for example
            bore, mounting, stroke, fractional_stroke, rod_style, ports, cushions, options, magnet, extension, xi_num = parsed_data
            return render_template(template,
                                   part_number=part_number,
                                   part_number_new=part_number_new,
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
