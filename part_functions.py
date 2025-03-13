import re, string

bore_code = {'15':'N15-','20':'N20-','25':'N25-','32':'N32-',
                 '40':'N40-','50':'N50-','60':'N60-','80':'N80-'}

fractional_stroke_value = {'A': 0,'B':.0625,'C':.125,'D':.1875,'E':.250,'F':.3125,'G':.375,'H':.4375,
                           'I':.500,'J':.5625,'K':.625,'L':.6875,'M':.750,'N':.8125,'O':.875,'P':.9375}

port_position = {'B':'1','H':'2','N':'3','T':'4',
                 'C':'1','I':'2','O':'3','U':'4',
                 'D':'1','J':'2','P':'3','V':'4',
                 'E':'1','K':'2','Q':'3','W':'4',
                 'F':'1','L':'2','R':'3','X':'4'}

cushion_position = {'B':'1','K':'1','C':'2','L':'2','D':'3','M':'3','E': '4','N':'4',
                    'F':'1','G':'2','H':'3','J':'4'}

viton_codes = ["PD","PN","PU","PV","PX","PZ","LZ","MJ","LY","LO","LI","IH","IF","IE","IB","IA",
               "HX","HW","HR","HT","HS","HO","HP","HK","HG","HH","HC","HD","DV","DP","DJ","DH","DC",
               "BV","BQ","BU","BG","BJ","BD","AH","SQ","SO","SV","SY","VB","VC","VD","VE","VF","VG",
               "VH","VI","VJ","VK","VL","VM","VN","VO","VP","VQ","VR","VS","VT","VU","WE","WG","WH",
               "WN","WT","WU","WV","WW","WY"]

double_rod_codes = ["DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO","DP","DQ","DR",
                    "DS","DT","DU","DV","DW","DX","DY","DZ","ED","EE","EF","EG","EH","EI","EN","HE","HF",
                    "HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP","HQ","HR","HS","HT","HU","HV","HW",
                    "HX","HY","HZ","IA","IB","IC","ID","IE","IF","IG","IH","LG","ME","MI","MJ","PD","PN",
                    "PR","PY","PZ","SP","VF","VG","VH","VI","VJ","VK","VU","WF","WH","WJ","WL","WN","WT","WX","WY"]

polypak_rod_codes = ["BP","EP","MP","PA","PB","PC","PD","PE","PE","PG","PH","PI","PM","PN","PQ","PR","PS","PT",
                     "PU","PV","PW","PY","WB","WN","WO","WP","WQ","WU","WW","WX","WY","WZ"]

polypak_piston_codes = ["PC","PF","PG","PN","PQ","PP","PV","PX","PZ","WB","WG","WH","WJ","WK","WN","WQ","WW","WX"]

metallic_scraper_codes =["AH","BD","BE","BG","BI","BJ","BO","BU","BW","DE","DG","DI","DJ","DL","DQ","DW","DZ","EE",
                         "EG","EI","EJ","EK","EO","EW","HB","HD","HF","HH","HJ","HL","HN","HP","HR","HT","HV","HW",
                         "HX","HZ","IB","IF","ID","LA","LC","LE","LF","LG","LH","LI","LJ","LL","LO","LX","LZ","ME",
                         "MG","MI","MP","MS","PH","PI","PR","PW","SW","VB","VE","VF","VG","VI","VK","VP","VT","WB",
                         "WC","WD","WE","WF","WG","WH","WJ","WK","WL","WM","WN","WO","WP","WQ","WR","WS","WT","WU",
                         "WV","WW","WX","WY","WZ"]

low_breakaway_codes = ["LB","BL","HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP",
                       "HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF","IG","IH",
                       "LA","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO","LQ","LR","LS","LU",
                       "LV","LW","LX","LY","LZ","SX","VL","VN","VO","VP","VQ","VT","WL"]

silent_seal_codes=["CE","SB","ED","EE","EG","EH","EI","EJ","EK","EM","EN","EO","EP","ER","ES","ET","EU","EW","EZ",
                   "PR","PY","SB","WI","WZ"]
def split_part_number(part_number):
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2})([A-Z])(\d)([A-Z])([A-Z])-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z]))?$"
    match = re.match(pattern, part_number)

    if not match:
        raise ValueError("Part number format is invalid")

    return match.groups()

def front_head_calc(bore, mounting, ports, cushions, rod_style):
    port_code={'B':'B','H':'B','N':'B','T':'B', #port will be at position 1 in p/n
               'C':'C','I':'C','O':'C','U':'C',
               'D':'D','J':'D','P':'D','V':'D',
               'E':'E','K':'E','Q':'E','W':'E',
                'F':'F','L':'F','R':'F','X':'F'}
    front_cushion_code = {'A':'A','B':'F','F':'F','C':'G','G':'G','D':'H','H':'H','E':'J','J':'J'}
    front_cushion_position = {'B':'1','F':'1','C':'2','G':'2','D':'3','H':'3','E':'4','J':'4'}
    front_cushion_result = front_cushion_code[cushions]  # initialize standard cushion result
    if rod_style in ('6', '7', '8'):
        block_code = {'X0':'205','F1':'205','F2':'205','P1':'205','P2':'205','P3':'205',
                      'S1':'205','P4':'205','T6':'225','T7':'205','T8':'205','X1':'205',
                      'X2':'205','X3':'205','S2':'235','S4':'215','E3':'295','E4':'295',
                      'SN':'265','SE':'275', 'SF':'285'}

    else:
        block_code = {'X0':'200','F1':'200','F2':'200','P1':'200','P2':'200','P3':'200',
                      'S1':'200','P4':'200','T6':'220','T7':'200','T8':'200','X1':'200',
                      'X2':'200','X3':'200','S2':'230','S4':'210','E3':'290','E4':'290',
                      'SN':'260','SE':'270','SF':'280'}

    if cushions != 'A': #yes cushions
        if block_code[mounting] in ('200','205'):
            if int(port_position[ports]) == int(front_cushion_position[cushions])+1:
                front_cushion_result = 'J' #cushion will be position 4

            elif int(front_cushion_position[cushions]) == int(port_position[ports])+1:
                front_cushion_result = 'G'  #cushion will be position 2 in p/n

            elif abs(int(front_cushion_position[cushions])-int(port_position[ports])) == 2:
                front_cushion_result = 'H' #cushion will be position 3 in p/n

        else:
            port_code = {'B':'B','H':'H','N':'N','T':'T',  #cushion and ports stay respective value
                         'C':'C','I':'I','O':'O','U':'U',
                         'D':'D','J':'J','P':'P','V':'V',
                         'E':'E','K':'K','Q':'Q','W':'W',
                         'F':'F','L':'L','R':'R','X':'X'}
    else: #no cushions
        if block_code[mounting] not in ('200','205'):  # for normal 200 blockhead
            port_code = {'B':'B','H':'H','N':'N','T':'T',
                         'C':'C','I':'I','O':'O','U':'U',
                         'D':'D','J':'J','P':'P','V':'V',
                         'E':'E','K':'K','Q':'Q','W':'W',
                         'F':'F','L':'L','R':'R','X':'X'}
    front_head = (bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-'
                  + port_code[ports] + front_cushion_result)
    return front_head


def rear_cover_calc(bore, mounting, ports, cushions, options, rod_style):
    port_code = {'B':'B','H':'B','N':'B','T':'B',  # port will be at position 1 in p/n
                 'C':'C','I':'C','O':'C','U':'C',
                 'D':'D','J':'D','P':'D','V':'D',
                 'E':'E','K':'E','Q':'E','W':'E',
                 'F':'F','L':'F','R':'F','X':'F'}
    cover_code = {'X0':'100','F1':'100','F2':'100','P1':'150','P2':'100','P3':'140',
                  'S1':'205','P4':'100','T6':'100','T7':'120','T8':'100','X1':'100',
                  'X2':'100','X3':'100','S2':'130','S4':'110','E3':'190','E4':'190',
                  'SN':'160','SE':'170','SF':'170'}
    rear_cushion_code = {'A':'A','B':'K','K':'K','C':'L','L':'L','D': 'M', 'M': 'M', 'E':'N','N':'N'}
    rear_cushion_position = {'B':'1','K':'1','C':'2','L':'2','D':'3','M':'3','E': '4','N':'4'}
    rear_cushion_result = rear_cushion_code[cushions]
    if cushions != 'A':  # yes cushions
        if cover_code[mounting] in ('100', '105'):
            if int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1:
                rear_cushion_result = 'N'  # cushion will be position 4

            elif int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1:
                rear_cushion_result = 'L'  # cushion will be position 2 in p/n

            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'  # cushion will be position 3 in p/n #YES CUSHIONS

        elif cover_code[mounting] in ('140','150'):
            if (int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1) and (int(port_position[ports]) in ('2','4')):
                rear_cushion_result = 'L' # cushion will be position 2 in p/n

            elif (int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1) and (int(port_position[ports]) in ('1','3')):
                rear_cushion_result = 'N' # cushion will be position 2 in p/n

            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'  # cushion will be position 3 in p/n
        else:
            port_code = {'B':'B','H':'H','N':'N','T':'T',  #cushion and ports stay respective value
                         'C':'C','I':'I','O':'O','U':'U',
                         'D':'D','J':'J','P':'P','V':'V',
                         'E':'E','K':'K','Q':'Q','W':'W',
                         'F':'F','L':'L','R':'R','X':'X'}
    else:  # no cushions
        if cover_code[mounting] not in ('200', '205'):  # for normal 200 blockhead
            port_code = {'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                         'C': 'C', 'I': 'I', 'O': 'O', 'U': 'U',
                         'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                         'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                         'F': 'F', 'L': 'L', 'R': 'R', 'X': 'X'}
    if options not in double_rod_codes:
        rear_cover = (bore_code.get(bore, 'UNKNOWN') + cover_code.get(mounting, 'ERROR') + '-'
                     + port_code[ports] + rear_cushion_result)
    else:
        if rod_style in ('6', '7', '8'):
            block_code = {'X0': '205', 'F1': '205', 'F2': '205', 'P1': '205', 'P2': '205', 'P3': '205',
                          'S1': '205', 'P4': '205', 'T6': '225', 'T7': '205', 'T8': '205', 'X1': '205',
                          'X2': '205', 'X3': '205', 'S2': '235', 'S4': '215', 'E3': '295', 'E4': '295',
                          'SN': '265', 'SE': '275', 'SF': '285'}
        else:
            block_code = {'X0': '200', 'F1': '200', 'F2': '200', 'P1': '200', 'P2': '200', 'P3': '200',
                          'S1': '200', 'P4': '200', 'T6': '220', 'T7': '200', 'T8': '200', 'X1': '200',
                          'X2': '200', 'X3': '200', 'S2': '230', 'S4': '210', 'E3': '290', 'E4': '290',
                          'SN': '260', 'SE': '270', 'SF': '280'}
        rear_cover = (bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-'
                      + port_code[ports] + rear_cushion_result)
    return rear_cover

def piston_rod_calc(bore,rod_style,stroke,fractional_stroke,extension,options):
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
        elif rod_style == '3':
            rod_adder = 2.625
        elif rod_style in ('6','7'):
            rod_adder = 4.125
        elif rod_style == '8':
            rod_adder = 3.000
    elif bore in ('32','40','50'):
        if rod_style in ('1', '2'):
            rod_adder = 4.375
        elif rod_style == '3':
            rod_adder = 3.250
        elif rod_style in ('6', '7'):
            rod_adder = 5.125
        elif rod_style == '8':
            rod_adder = 3.500
    elif bore in ('60','80'):
        if rod_style in ('1', '2'):
            rod_adder = 5.375
        elif rod_style == '3':
            rod_adder = 3.750
        elif rod_style in ('6', '7'):
            rod_adder = 6.000
        elif rod_style == '8':
            rod_adder = 4.000
    if options in ('BF','BB'):
        rod_adder += .063
    rod = f"{rod_prefix}{rod_code[rod_style]}{(rod_adder+int(stroke)+total_extension):.3f}"
    return rod

def piston_head_calc(bore,rod_style,options):
    if rod_style in ('1','2','3'):
        if options == 'SB':
            piston_number = '70'
        else:
            piston_number = '60'
    else:
        if options == 'SB' and bore != '15':
            piston_number = '75'
        else:
            piston_number = '65'
    if options in ('BB','BF','BR') and bore != '15':
        piston_number += '-BB'
    piston_head = f"{bore_code.get(bore, 'ERROR')}{piston_number}"
    return piston_head

def rod_bushing_calc(bore, rod_style, options):
    bushing_number = '90'
    bushing_prefix = ''
    if bore in ('15','20','25'):
        if rod_style in ('1','2','3'):
            bushing_prefix = 'N15-'
        else:
            bushing_prefix = 'N32-'
    elif bore in ('32','40','50'):
        if rod_style in ('1','2','3'):
            bushing_prefix = 'N32-'
        else:
            bushing_prefix = 'N60-'
    elif bore in ('60','80'):
            bushing_prefix = 'N60-'
            if rod_style in ('6','7','8'):
                bushing_number = '95'
    rod_bushing = bushing_prefix + bushing_number
    if options in double_rod_codes:
        rod_bushing += ' ' + '(2)'
    return rod_bushing

def tube_calc(bore,options,stroke):
    cylinder_prefix = ''
    cylinder_length = 0
    if bore == '15':
        cylinder_prefix = 'HAT175X'
        cylinder_length = 1.375
    elif bore == '20':
        cylinder_prefix = 'HAT225X'
        cylinder_length = 1.375
    elif bore == '25':
        cylinder_prefix = 'HAT275X'
        cylinder_length = 1.500
    elif bore == '32':
        cylinder_prefix = 'N32X'
        cylinder_length = 1.500
    elif bore == '40':
        cylinder_prefix = 'N40X'
        cylinder_length = 1.500
    elif bore == '50':
        cylinder_prefix = 'N50X'
        cylinder_length = 1.750
    elif bore == '60':
        cylinder_prefix = 'HAT625X'
        cylinder_length = 1.750
    elif bore == '80':
        cylinder_prefix = 'HAT837X'
        cylinder_length = 1.750
    if options == 'BB':
        cylinder_length += .125
    elif options in ('BR','BF'):
        cylinder_length += .063
    cylinder_tube = f"{cylinder_prefix}{(cylinder_length+int(stroke)):.3f}"
    return cylinder_tube

def tie_rod_calc(bore,options,stroke,mounting):
    quantity = 4
    tie_rod_adder = 0
    tie_rod_prefix = ''
    if bore == '15':
        tie_rod_prefix = 'FCQN15-7X'
        if mounting in ('X0','F1','F2','S2','S4','T6','T7','S1'):
            tie_rod_adder = 4.150
        elif mounting in ('P1','P3'):
            tie_rod_adder = 3.450
        elif mounting in ('P2','P4'):
            tie_rod_adder = 4.250
        elif mounting == 'X1':
            tie_rod_prefix = 'N15-7WFRX'
            tie_rod_adder = 6.000
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN15-7WFX'
            tie_rod_adder = 4.900
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN15-7WFX'
            tie_rod_adder = 5.250
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 2.700
    elif bore == '20':
        tie_rod_prefix = 'FCQN20-7X'
        if mounting in ('X0','F1','F2','S2','S4','T6','T7','S1','P2','P4'):
            tie_rod_adder = 4.250
        elif mounting in ('P1','P3'):
            tie_rod_adder = 3.550
        elif mounting == 'X1':
            tie_rod_prefix = 'N20-7WFRX'
            tie_rod_adder = 6.250
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN20-7WFX'
            tie_rod_adder = 5.100
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN20-7WFX'
            tie_rod_adder = 5.500
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 2.700
    elif bore == '25':
        tie_rod_prefix = 'FCQN25-7X'
        if mounting in ('X0','F1','F2','S2','S4','T6','T7','S1','P2','P4'):
            tie_rod_adder = 4.400
        elif mounting in ('P1','P3'):
            tie_rod_adder = 3.700
        elif mounting == 'X1':
            tie_rod_prefix = 'N20-7WFRX'
            tie_rod_adder = 6.375
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN25-7WFX'
            tie_rod_adder = 5.200
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN25-7WFX'
            tie_rod_adder = 5.600
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 2.825
    elif bore in ('32','40'):
        tie_rod_prefix = 'FCQN32-7X'
        if mounting in ('X0','S2','S4','T6','T7','S1'):
            tie_rod_adder = 5.000
        elif mounting in ('F1','F2','P2','P4'):
            tie_rod_adder = 5.250
        elif mounting in ('P1','P3'):
            tie_rod_adder = 4.150
        elif mounting == 'X1':
            tie_rod_prefix = 'N32-7WFRX'
            tie_rod_adder = 7.625
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN32-7WFX'
            tie_rod_adder = 6.000
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN32-7WFX'
            tie_rod_adder = 6.625
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 3.000
    elif bore == '50':
        tie_rod_prefix = 'N50-7X'
        if mounting in ('X0','S2','S4','T6','T7','S1'):
            tie_rod_adder = 5.500
        elif mounting in ('F1','F2','P2','P4'):
            tie_rod_adder = 5.600
        elif mounting in ('P1','P3'):
            tie_rod_adder = 4.750
        elif mounting == 'X1':
            tie_rod_prefix = 'N50-7WFRX'
            tie_rod_adder = 8.750
        elif mounting == 'X2':
            tie_rod_prefix = 'N50-7WFX'
            tie_rod_adder = 6.850
        elif mounting == 'X3':
            tie_rod_prefix = 'N50-7WFX'
            tie_rod_adder = 7.500
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 3.250
    elif bore == '60':
        tie_rod_prefix = 'N60-7X'
        if mounting in ('X0','S2','S4','T6','T7','S1'):
            tie_rod_adder = 6.000
        elif mounting in ('F1','F2','P2','P4'):
            tie_rod_adder = 6.250
        elif mounting in ('P1','P3'):
            tie_rod_adder = 5.000
        elif mounting == 'X1':
            tie_rod_prefix = 'N60-7WFRX'
            tie_rod_adder = 9.400
        elif mounting == 'X2':
            tie_rod_prefix = 'N60-7WFX'
            tie_rod_adder = 7.350
        elif mounting == 'X3':
            tie_rod_prefix = 'N60-7WFX'
            tie_rod_adder = 8.100
        elif mounting in ("SN","SE","SF"):
            tie_rod_adder = 3.650
    elif bore == '80':
        tie_rod_prefix = 'N80-7X'
        if mounting in ('X0', 'S2', 'S4', 'T6', 'T7', 'S1','P2','P4'):
            tie_rod_adder = 6.500
        elif mounting == 'E3':
            tie_rod_adder = 5.000
        elif mounting in ('E4','P1','P3'):
            tie_rod_adder = 5.500
        elif mounting == 'X1':
            tie_rod_prefix = 'N80-7WFRX'
            tie_rod_adder = 9.750
        elif mounting in ('X2','X3'):
            tie_rod_prefix = 'N80-7WFX'
            tie_rod_adder = 8.125
    if mounting == 'S1':
        quantity = 2
    tie_rod = f"{tie_rod_prefix}{(tie_rod_adder+int(stroke)):.3f}  ({quantity})"
    return tie_rod
def rod_seal_calc(bore, rod_style, options):
    rod_seal = ''
    if bore in ('15','20','25'):
        if rod_style in ('1', '2', '3'):
            rod_seal = '666-208-35901'
        else:
            rod_seal = '666-50100-35901'
        if options in viton_codes:
            rod_seal = '8404-0062V' if rod_style in ('1', '2', '3') else '8405-0100V'
        if options in polypak_rod_codes:
            rod_seal = '1250-0625' if rod_style in ('1', '2', '3') else '1560-1000'
            if options in viton_codes:
                rod_seal += 'V'
    if bore in ('32','40','50'):
        if rod_style in ('1','2','3'):
            rod_seal = '666-50100-35901'
        else:
            rod_seal = '666-321-35901'
        if options in viton_codes:
            rod_seal = '8405-0100V' if rod_style in ('1', '2', '3') else 'C43-36'
        if options in polypak_rod_codes:
            rod_seal = '1560-1000' if rod_style in ('1', '2', '3') else '1870-1375'
            if options in viton_codes:
                rod_seal = '1560-1000V' if rod_style in ('1', '2', '3') else '18701375V4208'
    if bore in ('60','80'):
        if rod_style in ('1','2','3'):
            rod_seal = '666-324-35901'
        else:
            rod_seal = '666-327-35901'
        if options in viton_codes:
            rod_seal = 'c43-36' if rod_style in ('1', '2', '3') else '8406-0175V'
        if options in polypak_rod_codes:
            rod_seal = '1870-1375' if rod_style in ('1', '2', '3') else '1870-1375'
            if options in viton_codes:
                rod_seal = '18701375V4208' if rod_style in ('1', '2', '3') else 'ERROR, NOT COMPATIBLE'
    if options in double_rod_codes:
        rod_seal += ' ' + '(2)'
    return rod_seal
def piston_seal_calc(bore, rod_style, options):
    piston_seal = ''
    if bore == '15':
        piston_seal = '8505-01187-4180'
        if options in viton_codes:
            piston_seal = 'C43-59'
        if options in polypak_piston_codes:
            piston_seal = '1560-1187'
            if options in viton_codes:
                piston_seal = 'TBD'
        if options in low_breakaway_codes:
            piston_seal = '8405-0118'
            if options in viton_codes:
                piston_seal = '8405-0118V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP1500-312'
    elif bore == '20':
        piston_seal = '8506-01625-4180'
        if options in viton_codes:
            piston_seal = 'C43-68'
        if options in polypak_piston_codes:
            piston_seal = '1870-1625'
            if options in viton_codes:
                piston_seal = 'TBD'
        if options in low_breakaway_codes:
            piston_seal = '8406-0162'
            if options in viton_codes:
                piston_seal = '8406-0162V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP2000-312'
    elif bore == '25':
        piston_seal = '8506-02125-4180'
        if options in viton_codes:
            piston_seal = 'C43-70'
        if options in polypak_piston_codes:
            piston_seal = '1870-2125'
            if options in viton_codes:
                piston_seal = '1870-2125V'
        if options in low_breakaway_codes:
            piston_seal = '8406-0162'
            if options in viton_codes:
                piston_seal = '8406-0162V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP2500-375'
    elif bore == '32':
        piston_seal = '8507-02812-4180'
        if options in viton_codes:
            piston_seal = '8407-0281V'
        if options in polypak_piston_codes:
            piston_seal = '2180-2812'
            if options in viton_codes:
                piston_seal = 'TBD'
        if options in low_breakaway_codes:
            piston_seal = '8407-0281'
            if options in viton_codes:
                piston_seal = '8407-0281V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP3250-375'
    elif bore == '40':
        piston_seal = '8508-03500-4180'
        if options in viton_codes:
            piston_seal = '8408-0350V'
        if options in polypak_piston_codes:
            piston_seal = '2500-3500'
            if options in viton_codes:
                piston_seal = '2500-3500V'
        if options in low_breakaway_codes:
            piston_seal = '8408-0350'
            if options in viton_codes:
                piston_seal = '8408-0350V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP4000-375'
    elif bore == '50':
        piston_seal = '8508-04500-4180'
        if options in viton_codes:
            piston_seal = '8408-0450V'
        if options in polypak_piston_codes:
            piston_seal = '2500-4500'
            if options in viton_codes:
                piston_seal = '2500-4500V'
        if options in low_breakaway_codes:
            piston_seal = '8408-0450'
            if options in viton_codes:
                piston_seal = '8408-0450V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP5000-500'
    elif bore == '60':
        piston_seal = '8509-05437-4187'
        if options in viton_codes:
            piston_seal = '8409-0543V'
        if options in polypak_piston_codes:
            piston_seal = '2810-5437'
            if options in viton_codes:
                piston_seal = '2810-5437V'
        if options in low_breakaway_codes:
            piston_seal = '8409-0543'
            if options in viton_codes:
                piston_seal = '8409-0543V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP6000-500'
    elif bore == '80':
        piston_seal = '626-100737-3847'
        if options in viton_codes:
            piston_seal = '8410-0737V'
        if options in polypak_piston_codes:
            piston_seal = '3120-7375'
            if options in viton_codes:
                piston_seal = '3120-7375V'
        if options in low_breakaway_codes:
            piston_seal = '8410-0737'
            if options in viton_codes:
                piston_seal = '8410-0737V'
        if options in silent_seal_codes:
            piston_seal = '4283BMP8000-500'
    return piston_seal

