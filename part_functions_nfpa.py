import re, string
#maps bore code to prefix
bore_code = {'15': 'N15-', '20': 'N20-', '25': 'N25-', '32': 'N32-',
             '40': 'N40-', '50': 'N50-', '60': 'N60-', '80': 'N80-'}

#maps fractional stroke letters to decimal values
fractional_stroke_value = {'A': 0, 'B': .0625, 'C': .125, 'D': .1875, 'E': .250, 'F': .3125, 'G': .375, 'H': .4375,
                           'I': .500, 'J': .5625, 'K': .625, 'L': .6875, 'M': .750, 'N': .8125, 'O': .875, 'P': .9375}
magnet_chart = {'15':'PS-1.365X.093','20':'PS-1.865X.093','25':'PS-2.365X.093','32':'PS-3.115X.093',
          '40':'PS-3.865X.093','50':'PS-4.980X.093','60':'PS-5.980X.093','80':'PS-7.980X.093'}
#dictionary of standard c and a dimensions
c_dim = {'15':.375,'20':.375,'25':.375,'32':.500,'40':.500,
                     '50':.500,'60':.625,'80':.625}

c_dim_oversize = {'15':.500,'20':.500,'25':.500,'32':.625,'40':.625,
                     '50':.625,'60':.750,'80':.750}

a_dim = {'15':.750,'20':.750,'25':.750,'32':1.125,'40':1.125,
         '50':1.125,'60':1.625,'80':1.625}

a_dim_oversize = {'15':1.125,'20':1.125,'25':1.125,'32':1.625,'40':1.625,
                  '50':1.625,'60':2.000,'80':2.000}

#maps port positions to port code
port_position = {'B':'1','H':'2','N':'3','T':'4',
                'C':'1','I':'2','O':'3','U':'4',
                'D':'1','J':'2','P':'3','V':'4',
                'E':'1','K':'2','Q':'3','W':'4',
                'F':'1','L':'2','R':'3','X':'4'}

#maps cushion position to cushion code
cushion_position = {'B':'1','K':'1','C':'2','L':'2','D':'3','M':'3','E':'4','N':'4',
                    'F':'1','G':'2','H':'3','J':'4'}

#lists of all codes with respective seals / features
viton_codes = ["PD","PN","PU","PV","PX","PZ","LZ","MJ","LY","LO","LI","IH","IF","IE","IB","IA",
                "HX","HW","HR","HT","HS","HO","HP","HK","HG","HH","HC","HD","DV","DP","DJ","DH","DC",
                "BV","BQ","BU","BG","BJ","BD","AH","SQ","SO","SV","SY","VB","VC","VD","VE","VF","VG",
                "VH","VI","VJ","VK","VL","VM","VN","VO","VP","VQ","VR","VS","VT","VU","WE","WG","WH",
                "WN","WT","WU","WV","WW","WY"]

double_rod_codes = ["DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO","DP","DQ",
                    "DR","DS","DT","DU","DV","DW","DX","DY","DZ","ED","EE","EF","EG","EH","EI","EN","HE",
                    "HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP","HQ","HR","HS","HT","HU","HV",
                    "HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF","IG","IH","LG","ME","MI","MJ","PD",
                    "PN","PR","PY","PZ","SP","VF","VG","VH","VI","VJ","VK","VU","WF","WH","WJ","WL","WN",
                    "WT","WX","WY"]

polypak_rod_codes = ["BP","EP","MP","PA","PB","PC","PD","PE","PE","PG","PH","PI","PM","PN","PQ","PR",
                     "PS","PT","PU","PV","PW","PY","WB","WN","WO","WP","WQ","WU","WW","WX","WY","WZ"]

polypak_piston_codes = ["PC","PF","PG","PN","PQ","PP","PV","PX","PZ","WB","WG","WH","WJ","WK","WN","WQ",
                        "WW","WX"]

metallic_scraper_codes = ["AH", "BD", "BE", "BG", "BI", "BJ", "BO", "BU", "BW", "DE", "DG", "DI", "DJ", "DL", "DQ",
                         "DW","DZ","EE", "EG","EI","EJ","EK","EO","EW","HB","HD","HF","HH","HJ","HL","HN","HP","HR",
                         "HT","HV","HW", "HX","HZ","IB","IF","ID","LA","LC","LE","LF","LG","LH","LI","LJ","LL","LO",
                         "LX","LZ","ME","MG","MI","MP","MS","PH","PI","PR","PW","SW","VB","VE","VF","VG","VI","VK",
                         "VP","VT","WB","WC","WD","WE","WF","WG","WH","WJ","WK","WL","WM","WN","WO","WP","WQ","WR",
                         "WS","WT","WU","WV","WW","WX","WY","WZ"]

low_breakaway_codes = ["LB","BL","HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN",
                       "HO", "HP",
                       "HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF",
                       "IG","IH",
                       "LA","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO","LQ","LR",
                       "LS","LU",
                       "LV","LW","LX","LY","LZ","SX","VL","VN","VO","VP","VQ","VT","WL"]

silent_seal_codes = ["CE", "SB", "ED", "EE", "EG", "EH", "EI", "EJ", "EK", "EM", "EN", "EO", "EP", "ER", "ES", "ET",
                     "EU", "EW", "EZ",
                     "PR", "PY", "SB", "WI", "WZ"]

tube_gasket_codes = {'15':'2-028G','20':'2-032G','25':'2-035G','32':'2-041G','40':'2-044G',
                     '50':'2-048G','60':'2-050G','80':'2-265G'}
wearband_codes ={'15':'N15-PWB','20':'N20-PWB','25':'N25-PWB','32':'N32-PWB','40':'N40-PWB',
                 '50':'N50-PWB','60':'N60-PWB','80':'N80-PWB'}
# --- Parsing and Calculation Functions ---

def split_part_number(part_number):
    """
    Parses a NFPA part number using a specific pattern.
    """
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2})([A-Z])(\d)([A-Z])([A-Z])-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z](?:\d{2}[A-Z])?))?$"
                  #bore    #mounting       #stroke   #rod  #port #cush    #options  #magnet       #extensions
    match = re.match(pattern, part_number)
    if not match:
        raise ValueError("Part number format is invalid")
    return match.groups()


def front_head_calc(bore, mounting, ports, cushions, rod_style):
    port_code = {'B': 'B', 'H': 'B', 'N': 'B', 'T': 'B',   #maps all ports to position 1 to use as base
                 'C': 'C', 'I': 'C', 'O': 'C', 'U': 'C',
                 'D': 'D', 'J': 'D', 'P': 'D', 'V': 'D',
                 'E': 'E', 'K': 'E', 'Q': 'E', 'W': 'E',
                 'F': 'F', 'L': 'F', 'R': 'F', 'X': 'F'}
    #maps head & cap cushion codes to head value
    front_cushion_code = {'A': 'A', 'B': 'F', 'F': 'F', 'C': 'G', 'G': 'G', 'D': 'H', 'H': 'H', 'E': 'J', 'J': 'J'}
    #maps head & cap cushion code to respective position
    front_cushion_position = {'B': '1', 'F': '1', 'C': '2', 'G': '2', 'D': '3', 'H': '3', 'E': '4', 'J': '4'}
    front_cushion_result = front_cushion_code.get(cushions, 'A') #creates a variable with necessarry
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
    if front_cushion_result != 'A':
        if block_code[mounting] in ('200', '205'):
            if int(port_position[ports]) == int(front_cushion_position[cushions]) + 1:
                front_cushion_result = 'J'
            elif int(front_cushion_position[cushions]) == int(port_position[ports]) + 1:
                front_cushion_result = 'G'
            elif abs(int(front_cushion_position[cushions]) - int(port_position[ports])) == 2:
                front_cushion_result = 'H'
        else:
            port_code = {'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                         'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                         'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                         'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                         'F': 'F', 'L': 'L', 'R': 'R', 'X': 'X'}
    else:
        if block_code[mounting] not in ('200', '205'):
            port_code = {'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                         'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                         'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                         'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                         'F': 'F', 'L': 'L', 'R': 'R', 'X': 'X'}
    front_head = (bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-' +
                  port_code[ports] + front_cushion_result)
    return front_head


def rear_cover_calc(bore, mounting, ports, cushions, options, rod_style):
    port_code = {'B': 'B', 'H': 'B', 'N': 'B', 'T': 'B',
                 'C': 'C', 'I': 'C', 'O': 'C', 'U': 'C',
                 'D': 'D', 'J': 'D', 'P': 'D', 'V': 'D',
                 'E': 'E', 'K': 'E', 'Q': 'E', 'W': 'E',
                 'F': 'F', 'L': 'F', 'R': 'F', 'X': 'F'}
    cover_code = {'X0': '100', 'F1': '100', 'F2': '100', 'P1': '150', 'P2': '100', 'P3': '140',
                  'S1': '205', 'P4': '100', 'T6': '100', 'T7': '120', 'T8': '100', 'X1': '100',
                  'X2': '100', 'X3': '100', 'S2': '130', 'S4': '110', 'E3': '190', 'E4': '190',
                  'SN': '160', 'SE': '170', 'SF': '170'}
    rear_cushion_code = {'A': 'A', 'B': 'K', 'K': 'K', 'C': 'L', 'L': 'L', 'D': 'M', 'M': 'M', 'E': 'N', 'N': 'N'}
    rear_cushion_position = {'B': '1', 'K': '1', 'C': '2', 'L': '2', 'D': '3', 'M': '3', 'E': '4', 'N': '4'}
    rear_cushion_result = rear_cushion_code.get(cushions, 'A')
    if rear_cushion_result != 'A':
        if cover_code[mounting] in ('100', '105'):
            if int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1:
                rear_cushion_result = 'N'
            elif int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1:
                rear_cushion_result = 'L'
            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'
        elif cover_code[mounting] in ('140', '150'):
            if (int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1) and (
                    port_position[ports] in ('2', '4')):
                rear_cushion_result = 'L'
            elif (int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1) and (
                    port_position[ports] in ('1', '3')):
                rear_cushion_result = 'N'
            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'
    else:
        if cover_code[mounting] not in ('200', '205'):
            port_code = {'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                         'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                         'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                         'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                         'F': 'F', 'L': 'L', 'R': 'R', 'X': 'X'}
    if options not in double_rod_codes:
        rear_cover = (bore_code.get(bore, 'UNKNOWN') + cover_code.get(mounting, 'ERROR') + '-' +
                      port_code[ports] + rear_cushion_result)
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
        rear_cover = (bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-' +
                      port_code[ports] + rear_cushion_result)
    return rear_cover


def piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension, options):
    if bore in ('15', '20', '25'):
        rod_prefix = 'N15'
    else:
        rod_prefix = 'N32'
    rod_code = {'1': '-30X', '2': '-35X', '3': '-40X', '6': '-10X', '7': '-15X', '8': '-20X'}

    if bore == '15' and cushions != 'A' and rod_style == '3':
        rod_code = {'3':'-40CX'}
    elif bore in ('32','40','50') and cushions != 'A' and rod_style in ('6','7','8'):
        rod_code = {'6':'-10CX','7':'-15CX','8':'-20CX'}
    elif bore in ('60','80') and cushions != 'A':
        rod_prefix = 'N32'
        rod_code = {'1':'-30CX','2':'-35CX','3':'-40CX','6':'-10CX','7':'-15CX','8':'-20CX'}

    rod_adder = 0
    total_extension = 0
    if extension:
        whole_extension = int(extension[2:4])
        fractional_extension = fractional_stroke_value[extension[4]]
        if extension.startswith(('CD','RC','CR')):
            if rod_style in ('1','2','3'):
                total_extension = (whole_extension + fractional_extension - c_dim[bore])
            else:
                total_extension = (whole_extension + fractional_extension - c_dim_oversize[bore])
        elif extension.startswith(('AD','RA','AR')):
            if rod_style in ('1', '2', '3'):
                total_extension = (whole_extension + fractional_extension - a_dim[bore])
            else:
                total_extension = (whole_extension + fractional_extension - a_dim_oversize[bore])
        elif extension.startswith(('AC','RR')):
            whole_extension = int(extension[2:3]) + int(extension[5:7])
            fractional_extension = fractional_stroke_value[extension[4]] + fractional_stroke_value[extension[7]]
            if rod_style in ('1','2','3'):
                total_extension = (whole_extension + fractional_extension - a_dim[bore] - c_dim[bore])
            else:
                total_extension = (whole_extension + fractional_extension - a_dim_oversize[bore] - c_dim_oversize[bore])


    if bore in ('15', '20', '25'):
        if rod_style in ('1', '2'):
            rod_adder = 3.375
        elif rod_style == '3':
            rod_adder = 2.625
        elif rod_style in ('6', '7'):
            rod_adder = 4.125
        elif rod_style == '8':
            rod_adder = 3.000
    elif bore in ('32', '40', '50'):
        if rod_style in ('1', '2'):
            rod_adder = 4.375
        elif rod_style == '3':
            rod_adder = 3.250
        elif rod_style in ('6', '7'):
            rod_adder = 5.125
        elif rod_style == '8':
            rod_adder = 3.500
    elif bore in ('60', '80'):
        if rod_style in ('1', '2'):
            rod_adder = 5.375
        elif rod_style == '3':
            rod_adder = 3.750
        elif rod_style in ('6', '7'):
            rod_adder = 6.000
        elif rod_style == '8':
            rod_adder = 4.000
    if options in ('BF', 'BB'):
        rod_adder += 0.063
    rod = f"{rod_prefix}{rod_code[rod_style]}{(rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke] + total_extension):.3f}"
    if extension:
        if extension.startswith(('AD','RA','AR','AC')):
            rod += '-AD' + extension[2:5]
    return rod


def piston_head_calc(bore, rod_style, options):
    if rod_style in ('1', '2', '3'):
        piston_number = '70' if options == 'SB' else '60'
    else:
        piston_number = '75' if (options == 'SB' and bore != '15') else '65'
    if options in ('BB', 'BF', 'BR') and bore != '15':
        piston_number += '-BB'
    piston_head = f"{bore_code.get(bore, 'ERROR')}{piston_number}"
    return piston_head


def rod_bushing_calc(bore, rod_style, options):
    bushing_number = '90'
    bushing_prefix = ''
    if bore in ('15', '20', '25'):
        bushing_prefix = 'N15-' if rod_style in ('1', '2', '3') else 'N32-'
    elif bore in ('32', '40', '50'):
        bushing_prefix = 'N32-' if rod_style in ('1', '2', '3') else 'N60-'
    elif bore in ('60', '80'):
        bushing_prefix = 'N60-'
        if rod_style in ('6', '7', '8'):
            bushing_number = '95'
    rod_bushing = bushing_prefix + bushing_number
    if options in double_rod_codes:
        rod_bushing += ' ' + '(2)'
    return rod_bushing


def tube_calc(bore, options, stroke):
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
        cylinder_length += 0.125
    elif options in ('BR', 'BF'):
        cylinder_length += 0.063
    cylinder_tube = f"{cylinder_prefix}{(cylinder_length + int(stroke)):.3f}"
    return cylinder_tube


def tie_rod_calc(bore, options, stroke, mounting):
    quantity = 4
    tie_rod_adder = 0
    tie_rod_prefix = ''
    if bore == '15':
        tie_rod_prefix = 'FCQN15-7X'
        if mounting in ('X0', 'F1', 'F2', 'S2', 'S4', 'T6', 'T7', 'S1'):
            tie_rod_adder = 4.150
        elif mounting in ('P1', 'P3'):
            tie_rod_adder = 3.450
        elif mounting in ('P2', 'P4'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 2.700
    elif bore == '20':
        tie_rod_prefix = 'FCQN20-7X'
        if mounting in ('X0', 'F1', 'F2', 'S2', 'S4', 'T6', 'T7', 'S1', 'P2', 'P4'):
            tie_rod_adder = 4.250
        elif mounting in ('P1', 'P3'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 2.700
    elif bore == '25':
        tie_rod_prefix = 'FCQN25-7X'
        if mounting in ('X0', 'F1', 'F2', 'S2', 'S4', 'T6', 'T7', 'S1', 'P2', 'P4'):
            tie_rod_adder = 4.400
        elif mounting in ('P1', 'P3'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 2.825
    elif bore in ('32', '40'):
        tie_rod_prefix = 'FCQN32-7X'
        if mounting in ('X0', 'S2', 'S4', 'T6', 'T7', 'S1'):
            tie_rod_adder = 5.000
        elif mounting in ('F1', 'F2', 'P2', 'P4'):
            tie_rod_adder = 5.250
        elif mounting in ('P1', 'P3'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 3.000
    elif bore == '50':
        tie_rod_prefix = 'N50-7X'
        if mounting in ('X0', 'S2', 'S4', 'T6', 'T7', 'S1'):
            tie_rod_adder = 5.500
        elif mounting in ('F1', 'F2', 'P2', 'P4'):
            tie_rod_adder = 5.600
        elif mounting in ('P1', 'P3'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 3.250
    elif bore == '60':
        tie_rod_prefix = 'N60-7X'
        if mounting in ('X0', 'S2', 'S4', 'T6', 'T7', 'S1'):
            tie_rod_adder = 6.000
        elif mounting in ('F1', 'F2', 'P2', 'P4'):
            tie_rod_adder = 6.250
        elif mounting in ('P1', 'P3'):
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
        elif mounting in ("SN", "SE", "SF"):
            tie_rod_adder = 3.650
    elif bore == '80':
        tie_rod_prefix = 'N80-7X'
        if mounting in ('X0', 'S2', 'S4', 'T6', 'T7', 'S1', 'P2', 'P4'):
            tie_rod_adder = 6.500
        elif mounting == 'E3':
            tie_rod_adder = 5.000
        elif mounting in ('E4', 'P1', 'P3'):
            tie_rod_adder = 5.500
        elif mounting == 'X1':
            tie_rod_prefix = 'N80-7WFRX'
            tie_rod_adder = 9.750
        elif mounting in ('X2', 'X3'):
            tie_rod_prefix = 'N80-7WFX'
            tie_rod_adder = 8.125
    if mounting == 'S1':
        quantity = 2
    tie_rod = f"{tie_rod_prefix}{(tie_rod_adder + int(stroke)):.3f}  ({quantity})"

    return tie_rod


def rod_seal_calc(bore, rod_style, options):
    rod_seal = ''
    if bore in ('15', '20', '25'):
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
    elif bore in ('32', '40', '50'):
        if rod_style in ('1', '2', '3'):
            rod_seal = '666-50100-35901'
        else:
            rod_seal = '666-321-35901'
        if options in viton_codes:
            rod_seal = '8405-0100V' if rod_style in ('1', '2', '3') else 'C43-36'
        if options in polypak_rod_codes:
            rod_seal = '1560-1000' if rod_style in ('1', '2', '3') else '1870-1375'
            if options in viton_codes:
                rod_seal = '1560-1000V' if rod_style in ('1', '2') else '18701375V4208'
    elif bore in ('60', '80'):
        if rod_style in ('1', '2', '3'):
            rod_seal = '666-324-35901'
        else:
            rod_seal = '666-327-35901'
        if options in viton_codes:
            rod_seal = 'c43-36' if rod_style in ('1', '2', '3') else '8406-0175V'
        if options in polypak_rod_codes:
            rod_seal = '1870-1375' if rod_style in ('1', '2', '3') else '1870-1375'
            if options in viton_codes:
                rod_seal = '18701375V4208' if rod_style in ('1', '2') else 'ERROR, NOT COMPATIBLE'
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


def rod_wiper_calc(bore, rod_style, options):
    rod_wiper = ''
    if bore in ('15','20','25'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-5/6-BN' if rod_style in ('1','2','3') else 'SG-3435-5/6-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
                return rod_wiper
        rod_wiper = '940-3' if rod_style in ('1','2','3') else '940-9'
        if options in viton_codes:
            rod_wiper += 'V'
    elif bore in ('32','40','50'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-1-BN' if rod_style in ('1','2','3') else 'SG-3436-1-3/8-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
                return rod_wiper
        rod_wiper = '940-9' if rod_style in ('1','2','3') else '940-15'
        if options in viton_codes:
            rod_wiper += 'V'
    elif bore in ('60','80'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3436-1-3/8-BN' if rod_style in ('1','2','3') else 'SG-3435-1-3/4-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
                return rod_wiper
        rod_wiper = '940-15' if rod_style in ('1','2','3') else 'D-1750U2145'
        if options in viton_codes:
            if rod_style in ('1','2','3'):
                rod_wiper += 'V'
            else:
                rod_wiper = 'D-1750VT90'
    if options in double_rod_codes:
        rod_wiper += ' ' + '(2)'
    return rod_wiper


def bushing_seal_calc(bore,rod_style,options):
    bushing_seal =''
    if bore in ('15','20','25'):
        bushing_seal = '2-122' if rod_style in ('1','2','3') else '2-222'
        if options in viton_codes:
            bushing_seal +='V'
    elif bore in ('32','40','50'):
        bushing_seal = '2-222' if rod_style in ('1', '2', '3') else '2-227'
        if options in viton_codes:
            bushing_seal += 'V'
    elif bore in ('60','80'):
        bushing_seal = '2-227' if rod_style in ('1', '2', '3') else '2-229'
        if options in viton_codes:
            bushing_seal += 'V'
    if options in double_rod_codes:
        bushing_seal += ' ' + '(2)'
    return bushing_seal


def rod_bearing_calc(bore, rod_style, options):
    rod_bearing = ''
    if bore in ('15','20','25'):
        rod_bearing = '701-00010-024' if rod_style in ('1','2','3') else '701-112016-032'
    elif bore in ('32','40','50'):
        rod_bearing = '701-112016-032' if rod_style in ('1', '2', '3') else '701-600022-039'
        if rod_style == '32' and options in metallic_scraper_codes and rod_style in ('1', '2', '3'):
            rod_bearing = '701-112016-029'
    elif bore in ('60','80'):
        rod_bearing = '701-600022-039' if rod_style in ('1', '2', '3') else '701-00028-044'
    return rod_bearing

# --- New Function for Generating BOM ---
def generate_bom(parsed_data):
    """
    Given the parsed NFPA part number data, calculates all BOM parts
    and returns a dictionary with the resulting part codes.
    """
    (bore, mounting, stroke, fractional_stroke, rod_style,
     ports, cushions, options, magnet, extension) = parsed_data

    # Validate compatibility conditions
    if mounting == 'T6' and (cushions in ('C', 'G', 'E', 'J') or port_position[ports] in ('2', '4')):
        raise ValueError("Error: Mounting 'T6' is incompatible with head cushions or port at positions 1 & 2.")
    if mounting == 'S4' and (cushion_position[cushions] == '3' or port_position[ports] == '3'):
        raise ValueError("Error: Mounting 'S4' is incompatible with cushions or ports at position 3.")

    # Calculate BOM parts using the existing functions
    front_head = front_head_calc(bore, mounting, ports, cushions, rod_style)
    rear_cover = rear_cover_calc(bore, mounting, ports, cushions, options, rod_style)
    rod = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension, options)
    rod_2 = None
    piston_head = piston_head_calc(bore, rod_style, options)
    rod_bushing = rod_bushing_calc(bore, rod_style, options)
    cylinder_tube = tube_calc(bore, options, stroke)
    tie_rod = tie_rod_calc(bore, options, stroke, mounting)
    tie_rod_2 = None
    rod_seal = rod_seal_calc(bore, rod_style, options)
    piston_seal = piston_seal_calc(bore, rod_style, options)
    rod_wiper = rod_wiper_calc(bore, rod_style, options)
    tube_gasket = tube_gasket_codes[bore]
    bushing_seal = bushing_seal_calc(bore,rod_style,options)
    wearband = wearband_codes[bore]
    rod_bearing = rod_bearing_calc(bore, rod_style, options)
    magnet_number = magnet_chart[bore] if magnet == 'E' else None

    if mounting == 'S1':
        adder = {'15': 0.65, '20': 0.625, '25': 0.65, '32': 1, '40': 1.1, '50': 1, '60': 1.15, '80': 0.5}
        tie_rod_2 = tie_rod_calc(bore, options, int(stroke) + adder[bore], mounting)
    if options in double_rod_codes:
        if extension:
            if cushions in ('B','C','D','E'):
                if extension.startswith(('CD','RC')):
                    rod_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
                elif extension.startswith(('CR','AR')):
                    rod_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension[0:2]+extension[5:8], options)
                elif extension.startswith(('AD','RA')):
                    rod_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
                elif extension.startswith(('AC','RR')):
                    rod_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
            else:
                if extension.startswith(('CD','RC')):
                    rod_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
                elif extension.startswith(('CR','AR')):
                    rod_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, extension[0:2]+extension[5:8], options)
                elif extension.startswith(('AD','RA')):
                    rod_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
                elif extension.startswith(('AC','RR')):
                    rod_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
        elif not extension:
            rod += '  (2)'

    # Return all BOM parts in a dictionary
    return {
        "front_head": front_head,
        "rear_cover": rear_cover,
        "rod": rod,
        "rod_2": rod_2,
        "piston_head": piston_head,
        "rod_bushing": rod_bushing,
        "cylinder_tube": cylinder_tube,
        "tie_rod": tie_rod,
        "tie_rod_2": tie_rod_2,
        "rod_seal": rod_seal,
        "piston_seal": piston_seal,
        "rod_wiper": rod_wiper,
        "tube_gasket": tube_gasket,
        "bushing_seal": bushing_seal,
        "wearband" : wearband,
        "rod_bearing" : rod_bearing,
        "magnet_number": magnet_number
    }
