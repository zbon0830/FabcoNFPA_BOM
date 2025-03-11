from flask import Flask, render_template, request
import re

app = Flask(__name__)

def split_part_number(part_number):
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2}A)(\d)([A-Z]{2})-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z]))?$"
    match = re.match(pattern, part_number)

    if not match:
        return None

    return match.groups()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        part_number = request.form['part_number']
        parsed_data = split_part_number(part_number)

        if parsed_data:
            bore, mounting, stroke, rod_style, port_cush, options, magnet, option_extension = parsed_data
            return render_template('result.html', bore=bore, mounting=mounting, stroke=stroke,
                                   rod_style=rod_style, port_cush=port_cush, options=options,
                                   magnet=magnet, option_extension=option_extension)
        else:
            return render_template('index.html', error="Invalid part number format")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
