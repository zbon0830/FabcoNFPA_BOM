from functools import total_ordering

from flask import Flask, render_template, request
import re

app = Flask(__name__)
bore_code = {'15':'N15','20':'N20','25':'N25','32':'N32',
                 '40':'N40','50':'N50','60':'N60','80':'N80'}
fractional_stroke_value = {'A': 0,'B':.0625,'C':.125,'D':.1875,'E':.250,'F':.3125,'G':.375,'H':.4375,
                     'I':.500,'J':.5625,'K':.625,'L':.6875,'M':.750,'N':.8125,'O':.875,'P':.9375}

def split_part_number(part_number):
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2})([A-Z])(\d)([A-Z])([A-Z])-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z]))?$"
    match = re.match(pattern, part_number)

    if not match:
        raise ValueError("Part number format is invalid")

    return match.groups()

def front_head_calc(bore, mounting, ports, cushions, rod_style):
    if rod_style in ('6', '7', '8'):
        block_code = {'X0':'205','F1':'205','F2':'205','P1':'205','P2':'205','P3':'205','S1':'205',
                      'P4':'205','T6':'225','T7':'205','T8':'205','X1':'205','X2':'205','X3':'205',
                      'S2':'235','S4':'215','E3':'295','E4':'295','SN':'265','SE':'275', 'SF':'285'}
    else:
        block_code = {'X0':'200','F1':'200','F2':'200','P1':'200','P2':'200','P3':'200','S1':'200',
                      'P4':'200','T6':'220','T7':'200','T8':'200','X1':'200','X2':'200','X3':'200',
                      'S2':'230','S4':'210','E3':'290','E4':'290','SN':'260','SE':'270', 'SF':'280'}

    front_cushion_code = {'B':'F','F':'F','C':'G','G':'G','D':'H','H':'H','E':'J','J':'J'}

    front_head = (bore_code.get(bore, 'UNKNOWN') + '-' + block_code.get(mounting, 'ERROR') + '-' 
                  + ports + front_cushion_code.get(cushions, 'A'))
    return front_head

def rear_cover_calc(bore, mounting, ports, cushions, options, front_head):
    cover_code = {'X0':'100','F1':'100','F2':'100','P1':'150','P2':'100','P3':'140','S1':'205',
                  'P4':'100','T6':'100','T7':'120','T8':'100','X1':'100','X2':'100','X3':'100',
                  'S2':'130','S4':'110','E3':'190','E4':'190','SN':'160','SE':'170','SF':'170'}

    rear_cushion_code = {'B':'K','K':'K','C':'L','L':'L','D':'M','M':'M','E':'N','N':'N'}

    if options != 'DR':
        rear_cover = (bore_code.get(bore, 'UNKNOWN') + '-' + cover_code.get(mounting, 'ERROR') + '-'
                      + ports + rear_cushion_code.get(cushions, 'A'))
    else:
        rear_cover = front_head

    return rear_cover

def piston_rod_calc(bore,rod_style,stroke,fractional_stroke,extension):
    if bore in ('15','20','25'):
        rod_prefix = 'N15'
    else:
        rod_prefix = 'N32'
    rod_code = {'1':'-30X','2':'-35X','3':'-40X','6':'-10X','7':'-15X','8':'-20X'}
    rod_adder = 0
    total_extension = 0
    if extension and extension.startswith('CD'):
        whole_extension = int(extension[2:4])
        fractional_extension = fractional_stroke_value[extension[4]]
        total_extension = (whole_extension+fractional_extension-.5)
    if bore in ('15','20','25'):
        if rod_style in ('1','2'):
            rod_adder = 3.375
        elif rod_style == 3:
            rod_adder = 3.375
        elif rod_style in ('6','7'):
            rod_adder = 3.375
        elif rod_style == 8:
            rod_adder = 3.375
    elif bore in ('32','40','50'):
        if rod_style in ('1', '2'):
            rod_adder = 3.375
        elif rod_style == 3:
            rod_adder = 3.375
        elif rod_style in ('6', '7'):
            rod_adder = 3.375
        elif rod_style == 8:
            rod_adder = 3.375
    elif bore in ('60','80'):
        if rod_style in ('1', '2'):
            rod_adder = 3.375
        elif rod_style == 3:
            rod_adder = 3.375
        elif rod_style in ('6', '7'):
            rod_adder = 3.375
        elif rod_style == 8:
            rod_adder = 3.375
    rod_length = rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke] + total_extension
    rod = f"{rod_prefix}{rod_code[rod_style]}{round(rod_adder+int(stroke)+total_extension, 3)}"
    return rod

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            part_number = request.form['part_number'].upper()
            part_number = part_number.replace('XO','X0')
            (bore, mounting, stroke, fractional_stroke, rod_style,
             ports, cushions, options, magnet, extension) = split_part_number(part_number)
            front_head = front_head_calc(bore, mounting, ports, cushions, rod_style)
            rear_cover = rear_cover_calc(bore, mounting, ports, cushions, options, front_head)
            rod = piston_rod_calc(bore,rod_style,stroke,fractional_stroke,extension)
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
