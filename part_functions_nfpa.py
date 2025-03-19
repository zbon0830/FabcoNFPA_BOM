import re, string
from selectors import SelectSelector

#maps bore code to prefix
bore_code = {'15':'N15-','20':'N20-','25':'N25-','32':'N32-',
             '40':'N40-','50':'N50-','60':'N60-','80':'N80-'}

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
male_rod_codes = {"BI","BJ","BM","BN","BO","BQ","BU","DM","DN","DO","DX","DY",
            "EF","EG","EH","EI","EJ","EM","EN","EO","EU","HA","HB","HC",
            "HD","HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA",
            "IB","IC","ID","IE","IF","LH","LI","LJ","LK","LL","LM","LN",
            "LO","LU","LX","LY","LZ","MC","MD","ME","MF","MG","MH","MI",
            "MJ","MK","MQ","PM","SL","SM","VB","VC","VD","VE","VF","VG",
            "VH","VI","VJ","VK","VM","WC","WM"}

viton_codes = {"PD","PN","PU","PV","PX","PZ","LZ","MJ","LY","LO","LI","IH","IF","IE","IB","IA",
                "HX","HW","HR","HT","HS","HO","HP","HK","HG","HH","HC","HD","DV","DP","DJ","DH","DC","DQ",
                "BV","BQ","BU","BG","BJ","BD","AH","SQ","SO","SV","SY","VB","VC","VD","VE","VF","VG",
                "VH","VI","VJ","VK","VL","VM","VN","VO","VP","VQ","VR","VS","VT","VU","WE","WG","WH",
                "WN","WT","WU","WV","WW","WY"}

double_rod_codes = {"DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO","DP","DQ",
                    "DR","DS","DT","DU","DV","DW","DX","DY","DZ","ED","EE","EF","EG","EH","EI","EN","HE",
                    "HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP","HQ","HR","HS","HT","HU","HV",
                    "HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF","IG","IH","LG","ME","MI","MJ","PD",
                    "PN","PR","PY","PZ","SP","VF","VG","VH","VI","VJ","VK","VU","WF","WH","WJ","WL","WN",
                    "WT","WX","WY"}

polypak_rod_codes = {"BP","EP","MP","PA","PB","PC","PD","PE","PE","PG","PH","PI","PM","PN","PQ","PR",
                     "PS","PT","PU","PV","PW","PY","WB","WN","WO","WP","WQ","WU","WW","WX","WY","WZ"}

polypak_piston_codes = {"PC","PF","PG","PN","PQ","PP","PV","PX","PZ","WB","WG","WH","WJ","WK","WN","WQ",
                        "WW","WX"}

metallic_scraper_codes = {"AH", "BD", "BE", "BG", "BI", "BJ", "BO", "BU", "BW", "DE", "DG", "DI", "DJ", "DL", "DQ",
                         "DW","DZ","EE", "EG","EI","EJ","EK","EO","EW","HB","HD","HF","HH","HJ","HL","HN","HP","HR",
                         "HT","HV","HW", "HX","HZ","IB","IF","ID","LA","LC","LE","LF","LG","LH","LI","LJ","LL","LO",
                         "LX","LZ","ME","MG","MI","MP","MS","PH","PI","PR","PW","SW","VB","VE","VF","VG","VI","VK",
                         "VP","VT","WB","WC","WD","WE","WF","WG","WH","WJ","WK","WL","WM","WN","WO","WP","WQ","WR",
                         "WS","WT","WU","WV","WW","WX","WY","WZ"}

low_breakaway_codes = {"LB","BL","HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN",
                       "HO", "HP","HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF",
                       "IG","IH","LA","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO","LQ","LR",
                       "LS","LU","LV","LW","LX","LY","LZ","SX","VL","VN","VO","VP","VQ","VT","WL"}

silent_seal_codes = {"CE", "SB", "ED", "EE", "EG", "EH", "EI", "EJ", "EK", "EM", "EN", "EO", "EP", "ER", "ES", "ET",
                     "EU", "EW", "EZ",
                     "PR", "PY", "SB", "WI", "WZ"}

tube_gasket_codes = {'15':'2-028G','20':'2-032G','25':'2-035G','32':'2-041G','40':'2-044G',
                     '50':'2-048G','60':'2-050G','80':'2-265G'}

wearband_codes ={'15':'N15-PWB','20':'N20-PWB','25':'N25-PWB','32':'N32-PWB','40':'N40-PWB',
                 '50':'N50-PWB','60':'N60-PWB','80':'N80-PWB'}

bumper_rear_codes = {"BB","BD","BE","BG","BI","BJ","BL","BM","BN","BO","BP","BQ","BS","BT","BU","BV","BW","CD",
                     "DB","DG","DH","DI","DK","DL","DP","DQ","FB","HA","HB","HC","HD","HI","HJ","HK","HL","HM",
                     "HN","HO","HP","HY","HZ","IA","IB","IC","ID","IE","IF","LB","LC","LD","LE","LU","LX","LY",
                     "LZ","MF","MG","MH","MI","SJ","SK","SL","SQ","SX","VD","VH","VI","VJ","VK","VO","VP","VQ",
                     "VT","WB"}

bumper_front_codes = {"BB","BD","BE","BG","BI","BJ","BL","BM","BN","BO","BP","BQ",
                      "BS","BT","BU","BV","BW","DB","DF","DG","DH","DI","DK","DL",
                      "DP","DQ","FB","HA","HB","HC","HD","HI","HJ","HK","HL","HM",
                      "HN","HO","HP","HY","HZ","IA","IB","IC","ID","IE","IF","LC",
                      "LD","LE","LU","LX","LY","LZ","MF","MG","MH","MI","SK","SL",
                      "SP","SQ","VD","VH","VI","VJ","VK","VO","VP","VQ","VT","WB"}

bumper_both_codes = {'BB','BD','BE','BG','BI','BJ','BL','BM','BN','BO','BP','BQ','BS','BT','BU','BV','BW',
                    'DB','DG','DH','DI','DK','DL','DP','DQ','FB','HA','HB','HC','HD','HI','HJ','HK','HL',
                    'HM','HN','HO','HP','HY','HZ','IA','IB','IC','ID','IE','IF','LC','LD','LE','LU','LX',
                    'LY','LZ','MF','MG','MH','MI','SK','SL','SQ','VD','VH','VI','VJ','VK','VO','VP','VQ',
                    'VT','WB','MB','PB','PG'}

stainless_fastener_codes = {"AH","BE","BE","BG","BN","BO","BQ","BS","BT","CS","CU","DC","DD","DE","DK","DL",
                             "DP","DQ","DT","DI","DZ","EF","EH","EU","EI","EJ","EK","ES","ET","EU","EZ","HA",
                             "HB","HC","HD","HE","HF","HG","HH","HM","HN","HO","HP","HU","HV","HW","HX","IC",
                             "ID","IE","IF","LA","LD","LE","LK","LL","LN","LO","LQ","LS","MC","ME","MH","MI",
                             "MJ","MK","MS","PH","PI","PS","PT","RW","SM","SJ","SM","SO","SP","SQ","SS","ST",
                             "SV","SU","SW","SX","SY","VC","VE","VG","VJ","VK","VL","VN","VQ","VT"}

stainless_rod_codes = {"AH","BE","BG","BN","BO","BQ","BS","BU","CR","CU","DC","DD","DE",
                       "DJ","DK","DL","DP","DQ","DS","DU","DZ","EE","EF","EH","EI","EJ",
                       "EK","ER","ES","EZ","HA","HB","HC","HD","HE","HF","HG","HH","HM",
                       "HN","HO","HP","HU","HV","HW","HX","IC","ID","IE","IF","LA","LD",
                       "LE","LK","LL","LN","LO","LR","MC","MD","ME","MH","MI","MJ","MQ",
                       "MS","PC","PE","PF","RW","SK","SL","SP","SQ","SS","SU","SV","SW",
                       "SX","SY","VC","VE","VG","VJ","VK","VQ","VR","VT","VU","WC","WD",
                       "WE","WR","EU","LS","PI","PS","SR","ST","VL","VN"}

# --- Parsing and Calculation Functions ---
def split_part_number(part_number):
    """
    Parses a NFPA part number using a specific pattern.
    """
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2})([A-Z])(\d)([A-Z])([A-Z])-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z](?:\d{2}[A-Z])?))?(?:-XI=(\d+(?:\.\d{1,3})?))?$"
                  #bore    #mounting       #stroke   #rod  #port #cush    #options  #magnet          #extensions                             #XI NUM
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
    front_cushion_result = front_cushion_code.get(cushions, 'A') #gives cushion position
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

    if front_cushion_result != 'A': #if there are cushions, do the following
        if block_code[mounting] in ('200', '205'): #if it is a square and symmetrical head, we use the port at position #1 and
                                                   #rotate the cushion port respectively
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
        if block_code[mounting] not in ('200', '205'): #if the head is not symmetrical, we keep the default positions
            port_code = {'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                         'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                         'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                         'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                         'F': 'F', 'L': 'L', 'R': 'R', 'X': 'X'}
    front_head = (bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-' +
                  port_code[ports] + front_cushion_result) #combine our bore code, block code, and port / cush codes to
                                                           #get front head part number
    return front_head


def rear_cover_calc(bore, mounting, ports, cushions, options, rod_style): #all same as front head
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
        elif cover_code[mounting] in ('140', '150'): #special cases for pivot mounts
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
    if bore in ('15', '20', '25'): #for normal rods, 15, 20, and 25 bores use N15 prefix, others use N32
        rod_prefix = 'N15'
    else:
        rod_prefix = 'N32'
    rod_code = {'1': '-30X', '2': '-35X', '3': '-40X', '6': '-10X', '7': '-15X', '8': '-20X'}

    if bore == '15' and cushions != 'A' and rod_style == '3': #adds a cushion prefix (CX) to rods where it's applicable
        rod_code = {'3':'-40CX'}
    elif bore in ('32','40','50') and cushions != 'A' and rod_style in ('6','7','8'):
        rod_code = {'6':'-10CX','7':'-15CX','8':'-20CX'}
    elif bore in ('60','80') and cushions != 'A':
        rod_prefix = 'N32'
        rod_code = {'1':'-30CX','2':'-35CX','3':'-40CX','6':'-10CX','7':'-15CX','8':'-20CX'}
    if options in stainless_rod_codes:
        rod_prefix += 'SR'

    rod_adder = 0 #initialize variable for rod adder and extension
    total_extension = 0
    if extension:  #calculates the additional length and name change needed for all rod extension codes
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


    if bore in ('15', '20', '25'): #maps out rod adders, per NFPA length chart Excel sheet
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
    if options in bumper_front_codes or options in bumper_both_codes: #add .063 to rod if there are front bumpers
        rod_adder += .063
    rod = f"{rod_prefix}{rod_code[rod_style]}{(rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke] + total_extension):.3f}"
    if extension:
        if extension.startswith(('AD','RA','AR','AC')):
            rod += '-AD' + extension[2:5]
    return rod


def piston_head_calc(bore, rod_style, options):
    if rod_style in ('1', '2', '3'): #maps standard piston numbers and oversize variants, including "Silent Seal" (SB)
                                     #option when applicable
        piston_number = '70' if options == 'SB' else '60'
    else:
        piston_number = '75' if (options == 'SB' and bore != '15') else '65'
    if (options in bumper_front_codes or options in bumper_rear_codes or options in bumper_both_codes) and bore != '15':
        piston_number += '-BB'                  #add -BB to pistons above 1.5" bore if bumpers are present
    piston_head = f"{bore_code.get(bore, 'ERROR')}{piston_number}" #combine bore code and piston number
    return piston_head


def rod_bushing_calc(bore, rod_style, options):
    bushing_number = '90'  #set standard bushing number to 90 and only change when criteria is met
    bushing_prefix = ''
    if bore in ('15', '20', '25'):  #set proper prefix and number for oversize rod on each bore
        if bore == '15' and rod_style in ('6','7','8'):
            bushing_prefix = 'N15'
            bushing_number = '95'
        else:
            bushing_prefix = 'N15-' if rod_style in ('1', '2', '3') else 'N32-'
    elif bore in ('32', '40', '50'):
        bushing_prefix = 'N32-' if rod_style in ('1', '2', '3') else 'N60-'
    elif bore in ('60', '80'):
        bushing_prefix = 'N60-'
        if rod_style in ('6', '7', '8'):
            bushing_number = '95'
    rod_bushing = bushing_prefix + bushing_number  #combine bushing prefix and bushing number to get rod bushing p/n
    if options in metallic_scraper_codes:
        rod_bushing += '-WS'
    if options in double_rod_codes:  #if double rod, quantity of 2
        rod_bushing += ' ' + '(2)'
    return rod_bushing


def tube_calc(bore, options, stroke, fractional_stroke):
    cylinder_prefix = '' #initialize standard cylinder prefix and length
    cylinder_length = 0
    if bore == '15':      #adders from NFPA length chart Excel sheet
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
    if (options in bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes:
        cylinder_length += .063                 #add length for bumpers in rear, front, or both
    elif options in bumper_both_codes:
        cylinder_length += .125
    cylinder_tube = f"{cylinder_prefix}{(cylinder_length + int(stroke) + fractional_stroke_value[fractional_stroke]):.3f}"
                        #combine prefix and length for full cylinder number                      (.3f rounds to 3 decimals)
    return cylinder_tube


def tie_rod_calc(bore, options, stroke, mounting, fractional_stroke, rod_style,xi_num):
    quantity = 4                        #default tie rod quantity
    tie_rod_adder = 0                   #initialize tie rod length adder and prefix
    tie_rod_prefix = ''
    if bore == '15':      #adders per NFPA length chart Excel sheet
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
        elif mounting == 'T8':         #Unique T8 first tie rod set calculation (WIP)
            tie_rod_adder = -0.8 if rod_style in ('1','2','3') else -1.175
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -.625 if rod_style in ('1','2','3') else -1.1
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -0.625 if rod_style in ('1','2','3') else -1.1
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -1.05 if rod_style in ('1','2','3') else -1.300
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -0.925 if rod_style in ('1','2','3') else -1.175
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -1.175 if rod_style in ('1','2','3') else -1.425
            tie_rod_adder +=float(xi_num)
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
        elif mounting == 'T8':
            tie_rod_adder = -1.05 if rod_style in ('1','2','3') else -1.300
            tie_rod_adder +=float(xi_num)
    if options in double_rod_codes:
        tie_rod_adder += 0.5
    if options in (bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes and mounting != 'T8':
        tie_rod_adder += .063
    elif options in bumper_both_codes and mounting != 'T8':
        tie_rod_adder += .125
    if mounting in 'S1':
        quantity = 2
    tie_rod = f"{tie_rod_prefix}{(tie_rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke]):.3f}  ({quantity})"
                #combine prefix, length, and quantity to get tie rod part number

    if mounting == 'T8_2': #Unique T8 second tie rod set calculation (WIP)
        if rod_style in ('1', '2', '3'):
            ZB_subtractor = {'15':4.875,'20':4.940,'25':5.060,'32':6.000,'40':6.000,'50':6.375,'60':7.125,'80':7.375}
        else:
            ZB_subtractor = {'15':5.250,'20':5.315,'25':5.440,'32':6.250,'40':6.250,'50':6.625,'60':7.375,'80':7.625}
        adder = 0
        if options in (bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes:
            adder += .063
        elif options in bumper_both_codes:
            adder += .125
        if options in double_rod_codes:
            adder += 0.5
        tie_rod = f"{tie_rod_prefix}{(ZB_subtractor[bore]+int(stroke)+fractional_stroke_value[fractional_stroke]-float(xi_num)-.05+adder):.3f}  ({quantity})"

    return tie_rod


def rod_seal_calc(bore, rod_style, options):
    rod_seal = ''          #initialize rod seal
    if bore in ('15', '20', '25'):                #map out rod seal part numbers based on options, viton / polypak
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
        rod_seal += ' ' + '(2)'      #if double rod quantity 2
    return rod_seal


def piston_seal_calc(bore, rod_style, options):
    piston_seal = ''           #map out piston seal part numbers based on options, viton / polypak / silent seal bumper
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
    piston_seal += ' ' + '(2)'
    return piston_seal


def rod_wiper_calc(bore, rod_style, options):
    rod_wiper = '' #initialize rod wiper code
    if bore in ('15','20','25'):        #map out rod wiper based on rod size and if metallic rod scraper is selected
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-5/6-BN' if rod_style in ('1','2','3') else 'SG-3435-5/6-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-3' if rod_style in ('1','2','3') else '940-9'
            if options in viton_codes:
                rod_wiper += 'V'
    elif bore in ('32','40','50'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-1-BN' if rod_style in ('1','2','3') else 'SG-3436-1-3/8-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-9' if rod_style in ('1','2','3') else '940-15'
            if options in viton_codes:
                rod_wiper += 'V'
    elif bore in ('60','80'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3436-1-3/8-BN' if rod_style in ('1','2','3') else 'SG-3435-1-3/4-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-15' if rod_style in ('1','2','3') else 'D-1750U2145'
            if options in viton_codes:
                if rod_style in ('1','2','3'):
                    rod_wiper += 'V'
                else:
                    rod_wiper = 'D-1750VT90'
    if options in double_rod_codes:
        rod_wiper += ' ' + '(2)'        #if double rod quantity 2
    return rod_wiper


def bushing_seal_calc(bore,rod_style,options):
    bushing_seal =''                     #simple bushing initializing and mapping
    if bore in ('15','20','25'):
        bushing_seal = '2-122' if rod_style in ('1','2','3') else '2-222'
        if bore == '15' and rod_style in ('6','7','8'):
            bushing_seal = '2-125'
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
    rod_bearing = ''      #simple bearing initializing and mapping
    if bore in ('15','20','25'):
        rod_bearing = '701-00010-024' if rod_style in ('1','2','3') else '701-112016-032'
    elif bore in ('32','40','50'):
        rod_bearing = '701-112016-032' if rod_style in ('1', '2', '3') else '701-600022-039'
        if rod_style == '32' and options in metallic_scraper_codes and rod_style in ('1', '2', '3'):
            rod_bearing = '701-112016-029'
    elif bore in ('60','80'):
        rod_bearing = '701-600022-039' if rod_style in ('1', '2', '3') else '701-00028-044'
    if options in double_rod_codes:
        rod_bearing += ' ' + '(2)'    #if double rod, quantity 2
    return rod_bearing


def retaining_ring_calc(bore, options):
    retaining_ring = ''           #simple retaining ring initializing and mapping
    if bore in ('15','20','25'):
        retaining_ring = 'N5008-131' if options not in stainless_fastener_codes else 'N5008-131SS'
    elif bore in ('32','40','50'):
        retaining_ring = 'N5008-175' if options not in stainless_fastener_codes else 'N5008-175SS'
    elif bore in ('60','80'):
        retaining_ring = 'N5008-237PA' if options not in stainless_fastener_codes else 'N5008-237SS'
    if options in double_rod_codes:
        retaining_ring += ' ' + '(2)'    #if double rod, quantity 2
    return retaining_ring


def bumper_calc(bore,options):
    bumper = ''     #simple bumper initializing and mapping
    if options in bumper_both_codes or options in bumper_front_codes or options in bumper_rear_codes:
        if bore == '15':
            bumper = 'SO-17-600'
        elif bore == '20':
            bumper = '221-BR-1'
        elif bore == '25':
            bumper = '321-BR-1'
        elif bore == '32':
            bumper = '1221-BR'
        elif bore == '40':
            bumper = '1221-BR'
        elif bore in ('50','60','80'):
            bumper = 'MPS-371-66'
        if options in bumper_both_codes:
            bumper += ' ' + '(2)'
    else:
        bumper = None   #use None if no bumpers present (optional as an empty string ('') is None by default)
    return bumper


def cushion_spud_calc(bore,rod_style,cushions,options):
    rod_spud = ''      #initialize necessary variables / parts that will later be returned
    rear_spud = ''
    cushioning_seal = ''
    cushioning_seal_2 = ''
    if cushions != 'A':       #if there are cushions, this maps out rod cushion and rear cushion spuds
        if bore in ('15','20','25'):
            rod_spud = 'N15-300' if rod_style in ('1','2','3') else 'N15-310'
            rear_spud = 'N15-305' if rod_style in ('1','2','3') else 'N15-315'
            if cushions in ('F','G','H','J','W'):    #if the cushions are only in front, they must change if oversize rod
                cushioning_seal = 'V6-04.0020N4181A85' if rod_style in ('1','2','3') else 'V6-05.0032N4181A85'
                cushioning_seal_2 = None
            elif cushions in ('B','C','D','E','Y'):          #if cushions in both sides, use one of each if oversize
                                                             #otherwise, two of standard ones
                cushioning_seal = 'V6-04.0020N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal += ' ' + '(2)'
                    cushioning_seal_2 = None
                else:
                    cushioning_seal_2 = 'V6-05.0032N4181A85'
            elif cushions in ('K','L','M','N','V'): #if cushions are only in rear, cushions never change
                cushioning_seal = 'V6-04.0020N4181A85'
        elif bore in ('32','40','50'):        #repeat everything from previous bore onwards
            rod_spud = 'N32-300' if rod_style in ('1', '2', '3') else 'N32-310'
            rear_spud = 'N32-305' if rod_style in ('1', '2', '3') else 'N32-315'
            if cushions in ('F', 'G', 'H', 'J', 'W'):
                cushioning_seal = 'V6-05.0032N4181A85' if rod_style in ('1', '2', '3') else 'V6-05.0038N4181A85'
                cushioning_seal_2 = None
            elif cushions in ('B', 'C', 'D', 'E', 'Y'):
                cushioning_seal = 'V6-05.0032N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal += ' ' + '(2)'
                    cushioning_seal_2 = None
                else:
                    cushioning_seal_2 = 'V6-05.0038N4181A85'
            elif cushions in ('K', 'L', 'M', 'N', 'V'):
                cushioning_seal = 'V6-05.0032N4181A85'
        elif bore in ('60','80'):
            rod_spud = 'N60-300' if rod_style in ('1', '2', '3') else 'N60-310'
            rear_spud = 'N60-305' if rod_style in ('1', '2', '3') else 'N60-315'
            if cushions in ('F', 'G', 'H', 'J', 'W'):
                cushioning_seal = 'V6-05.0038N4181A85' if rod_style in ('1', '2', '3') else 'V6-05.0050N4181A85'
                cushioning_seal_2 = None
            elif cushions in ('B', 'C', 'D','E', 'Y'):
                cushioning_seal = 'V6-05.0038N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal += ' ' + '(2)'
                    cushioning_seal_2 = None
                else:
                    cushioning_seal_2 = 'V6-05.0050N4181A85'
            elif cushions in ('K', 'L', 'M', 'N', 'V'):
                cushioning_seal = 'V6-05.0038N4181A85'
        if options in double_rod_codes:
            rear_spud = None
            rod_spud += ' ' + '(2)'
    return rod_spud,rear_spud,cushioning_seal,cushioning_seal_2


def tierod_nut_calc(bore,options,mounting):
    tierod_nut = ''   #simple tie rod nut initialization and mapping based on if stainless or not
    if bore == '15':
        tierod_nut = '1/4-28' if options not in stainless_fastener_codes else '1/4-28SS'
    elif bore in ('20','25'):
        tierod_nut = '5/16-24' if options not in stainless_fastener_codes else '5/16-24SS'
    elif bore in ('32','40'):
        tierod_nut = '3/8-24' if options not in stainless_fastener_codes else '3/8-24SS'
    elif bore in ('50','60'):
        tierod_nut = '1/2-20' if options not in stainless_fastener_codes else '1/2-20SS'
    elif bore == '80':
        tierod_nut = '5/8-18' if options not in stainless_fastener_codes else '5/8-18SS'
    if mounting in ('P1','P2','P3','P4','F1','F2','E3','E4'):       #mapping out quantity
        tierod_nut += ' ' + '(4)'
    elif mounting in ('SN','SE','SF'):                             #mapping out different nuts for sleeve nut mounts
        if bore == '15':
            tierod_nut = 'FCQN-0150-SN'
        elif bore in ('20', '25'):
            tierod_nut = 'FCQN-0200/250-SN'
        elif bore in ('32', '40'):
            tierod_nut = 'FCQN-0325/400-SN'
        elif bore in ('50', '60'):
            tierod_nut = 'N50-SN'
        elif bore == '80':
            tierod_nut = 'N/A'
        if options in double_rod_codes:
            tierod_nut += ' ' + '(8)'
        else:
            tierod_nut += ' ' + '(4)'
    else:
        tierod_nut += ' ' + '(8)'
    return tierod_nut


def pivot_calc(bore,mounting, options):
    pivot_mount = None       #intialize all pivot related variables
    pivot_bushing = None
    pivot_pin = None
    pivot_ring = None
    if mounting in ('P1','P3'):   #map pivot bushings to respective mounts
        if bore in ('15','20','25'):
            pivot_bushing = '521-370 (2)' if mounting == 'P1' else 'CP8011-2'
        elif bore in ('32','40','50'):
            pivot_bushing = 'AA083901 (2)'
        elif bore in ('60','80'):
            pivot_bushing = 'EP161812 (2)'
    if mounting in ('P2','P4'):     #map detachable pivot mounts to their respective bores
        if bore == '15':
            pivot_mount = 'BMP2-15-T' if mounting == 'P2' else 'BMP4-15-T'
        elif bore == '20':
            pivot_mount = 'BMP2-2-T' if mounting == 'P2' else 'BMP4-2-T'
        elif bore == '25':
            pivot_mount = 'BMP2-25-T' if mounting == 'P2' else 'BMP4-25-T'
        elif bore == '32':
            pivot_mount = 'BMP2-32-T' if mounting == 'P2' else 'BMP4-32-T'
        elif bore == '40':
            pivot_mount = 'BMP2-4-T' if mounting == 'P2' else 'BMP4-4-T'
        elif bore == '50':
            pivot_mount = 'BMP2-5-T' if mounting == 'P2' else 'N50-MP4'
        elif bore == '60':
            pivot_mount = 'BMP2-6-T' if mounting == 'P2' else 'N60-MP4'
        elif bore == '80':
            pivot_mount = 'N80-MP2' if mounting == 'P2' else 'N80-MP4'
    if mounting in ('P1','P2'):    #map pivot bushings and lock rings for P1 and P3 to their respective bores
        if bore in ('15','20','25'):
            pivot_pin = 'HP11-155' if options not in stainless_fastener_codes else 'N15-500SS'
            pivot_ring = 'N5100-50 (2)' if options not in stainless_fastener_codes else 'N5100-50SS (2)'
        elif bore in ('32','40','50'):
            pivot_pin = 'HP30-155' if options not in stainless_fastener_codes else 'N32-750SS'
            pivot_ring = 'N5100-75 (2)' if options not in stainless_fastener_codes else 'N5100-75SS (2)'
        elif bore in ('60','80'):
            pivot_pin = 'HP60-155' if options not in stainless_fastener_codes else 'N60-100SS'
            pivot_ring = 'N5100-100 (2)' if options not in stainless_fastener_codes else 'N5100-100SS (2)'
    return pivot_bushing,pivot_mount,pivot_pin,pivot_ring  #return all values


def piston_bolt_calc(bore,options,rod_style,cushions):
    piston_bolt = ''            #intialize and map piston bolt for non-double rod cylinders
    threaded_stud = ''
    if options not in double_rod_codes:
        if bore in ('15','20','30'):
            if rod_style in ('1','2','3'):
                piston_bolt = 'M8X1.25X40SHCS' if cushions == 'A' else 'M8X1.25X50SHCS'
            else:
                piston_bolt = '1/2-20X1-3/4SHCS' if cushions == 'A' else '1/2-20X2-1/2SHCS'
        elif bore in ('32','40'):
            if rod_style in ('1','2','3'):
                piston_bolt = 'M14X2.0X50SHCS' if cushions == 'A' else 'M14X2.0X60SHCS'
            else:
                piston_bolt = '3/4-16X2SHCS' if cushions == 'A' else '3/4-16X3SHCS'
        elif bore == '50':
            if rod_style in ('1','2','3'):
                piston_bolt = 'M14X2.0X50SHCS' if cushions == 'A' else 'M14X2.0X60SHCS'
            else:
                piston_bolt = '3/4-16X2-1/4SHCS' if cushions == 'A' else '3/4-16X3SHCS'
        elif bore in ('60','80'):
            if rod_style in ('1','2','3'):
                piston_bolt = '3/4-16X2-1/4SHCS' if cushions == 'A' else '3/4-16X3SHCS'
            else:
                piston_bolt = '3/4-16X2-1/2SHCS' if cushions == 'A' else '3/4-16X3SHCS'
    else:
        piston_bolt = None

    return piston_bolt


def retainer_plate_calc(bore,rod_style,mounting):
    retainer = None
    retainer_screw = None   #intialize retainer and retainer screw variables
    if bore != '80':
        if mounting in ('SN','SE'):  #map socket head cap screws to their respective bore sizes
            retainer_screw_code = {'15':'8/32X1/2SHCS','20':'10/32X1/2SHCS','25':'10/32X1/2SHCS','32':'1/4-28X3/4SHCS',
                              '40':'3/8-24X3/4SHCS','50':'3/8-24X3/4SHCS','60':'3/8-24X3/4SHCS'}
            retainer_screw = retainer_screw_code[bore] + ' ' + '(2)'        #quantity 2
        elif bore in ('15','60','80') and mounting not in ('SN','SE','X1','X3') and rod_style not in ('1','2','3'):
                    #for other bushing retainers, which are only on 15, 60, and 80 bores, use the following
            retainer = bore_code[bore]+'340'
            retainer_screw_code = {'15':'','60':'5/16-24X3/4SHCS-SS','80':'5/16-24X7/8SHCS'}
            retainer_screw = retainer_screw_code[bore] + ' ' + '(2)'
    return retainer,retainer_screw


def accessory_calc(bore,options,mounting, rod_style):
    male_rod = None  #initiate all variables being used (you can put them in a line seperated by commas instead of line-by-line)
    angle_mount,angle_mount_2,spacer_plate = None,None,None
    trunnion_pin,trunnion_screw,mid_trunnion = None,None,None
    flange = None
    if options in male_rod_codes:  #if male rod code is found, map the threaded stud to its bore size
        if bore in ('15','20','25'):
            male_rod = '7/16-20X1-1/2SS' if rod_style in ('1','2','3') else '3/4-16X2-1/2SS'
        elif bore in ('32','40','50'):
            male_rod = '3/4-16X2-1/2SS' if rod_style in ('1','2','3') else '1-14X3SS'
        elif bore in ('60','80'):
            male_rod = '1-14X3SS' if rod_style in ('1','2','3') else 'UNAVAILABLE'

    if mounting == 'S1':  #map the sleeve-nut angle bracket to its bore size if applicable
        angle_mount_code = {'15':'LB-FCQN-0150','20':'LB-FCQN-0200','25':'LB-FCQN-0250','32':'LB-FCQN-0325',
                       '40':'LB-FCQN-0400','50':'N50-400','60':'N60-400','80':'N80-400'}
        if rod_style in ('6','7','8'):
            angle_mount = angle_mount_code[bore]
            angle_mount_2 = bore_code[bore]+'405'
        else:
            angle_mount = angle_mount_code[bore] + ' ' + '(2)'
        if bore != '80' and options not in double_rod_codes:
            spacer_plate = bore_code[bore] + '385'

    if mounting in ('T6','T7','T8'): #if trunnion mount is present, add trunnion pins and screws
        if bore in ('60','80'):
            trunnion_pin = 'N15-325 (2)'
            trunnion_screw = '5/8-18X2SHCS (2)'
        else:
            trunnion_pin = 'N60-325 (2)'
            trunnion_screw = '7/16-20X1SHCS (2)' if bore in ('15','20','25',) else '7/16-20X1-1/4SHCS (2)'
        if mounting == 'T8':
            mid_trunnion = bore_code[bore] + '330' #mid-trunnion mount part number made with bore code and always is '330'
    if mounting in ('F1','F2'):
        flange = bore_code[bore]+'350' if rod_style in ('1','2','3') else bore_code[bore] + '355'

    if mounting in ('SN', 'SE'): #map spacer plates for sleeve nut mounts and extended tie rods
        spacer_plate = bore_code[bore] + '375' if rod_style in ('1', '2', '3') else bore_code[bore] + '376'
    if mounting in ('X1', 'X3'):
        spacer_plate = bore_code[bore] + '380' if rod_style in ('1', '2', '3') else bore_code[bore] + '381'

    return male_rod,angle_mount,angle_mount_2,spacer_plate,trunnion_pin,trunnion_screw,mid_trunnion,flange


# --- New Function for Generating BOM ---
def generate_bom(parsed_data):
    """
    Given the parsed NFPA part number data, calculates all BOM parts
    and returns a dictionary with the resulting part codes.
    """
    (bore, mounting, stroke, fractional_stroke, rod_style,
     ports, cushions, options, magnet, extension, xi_num) = parsed_data

    # Validate compatibility conditions
    if mounting == 'T6' and (cushions in ('C', 'G', 'E', 'J') or port_position[ports] in ('2', '4')):
        raise ValueError("Error: Mounting 'T6' is incompatible with head cushions or port at positions 1 & 2.")
    if mounting == 'S4' and (cushion_position[cushions] == '3' or port_position[ports] == '3'):
        raise ValueError("Error: Mounting 'S4' is incompatible with cushions or ports at position 3.")
    if rod_style not in ('3','8') and options in male_rod_codes:
        raise ValueError("Error: Male rod stud only available on style 3 and 8 rods.")

    # Calculate BOM parts using the existing functions
    front_head = front_head_calc(bore, mounting, ports, cushions, rod_style)
    rear_cover = rear_cover_calc(bore, mounting, ports, cushions, options, rod_style)
    rod = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension, options)
    rod_2 = None  #None by default, will get filled later if double rod is found
    piston_head = piston_head_calc(bore, rod_style, options)
    rod_bushing = rod_bushing_calc(bore, rod_style, options)
    cylinder_tube = tube_calc(bore, options, stroke, fractional_stroke)
    tie_rod = tie_rod_calc(bore, options, stroke, mounting, fractional_stroke, rod_style,xi_num)
    tie_rod_2 = None   #None by default, will get filled later if angle mount or mid-trunnion is found
    rod_seal = rod_seal_calc(bore, rod_style, options)
    piston_seal = piston_seal_calc(bore, rod_style, options)
    rod_wiper = rod_wiper_calc(bore, rod_style, options)
    tube_gasket = tube_gasket_codes[bore] + ' ' + '(2)'  #calls tube gasket from dictionary with quantity 2
    bushing_seal = bushing_seal_calc(bore,rod_style,options)
    wearband = wearband_codes[bore]
    rod_bearing = rod_bearing_calc(bore, rod_style, options)
    magnet_number = magnet_chart[bore] + ' ' + '(2)' if magnet == 'E' else None  #calls magnet from dictionary if magnet is found
    retaining_ring = retaining_ring_calc(bore,options)
    bumper = bumper_calc(bore,options)
    tierod_nut = tierod_nut_calc(bore,options,mounting)
    piston_bolt = piston_bolt_calc(bore,options,rod_style,cushions)
    pivot_bushing,pivot_mount,pivot_pin,pivot_ring = pivot_calc(bore,mounting,options)
    rod_spud, rear_spud, cushioning_seal, cushioning_seal_2 = cushion_spud_calc(bore,rod_style,cushions,options)
    male_rod, angle_mount, angle_mount_2, spacer_plate, trunnion_pin, trunnion_screw, mid_trunnion,flange = accessory_calc(bore,options,mounting,rod_style)
    retainer,retainer_screw = retainer_plate_calc(bore,rod_style,mounting)


    if mounting == 'T8': #recalls the tie rod calculation with new parameters to fit mid trunnion (WIP)
        tie_rod = tie_rod_calc(bore, options, '0',mounting,'A',rod_style,xi_num)
        tie_rod_2 = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style,xi_num)

    if cushions != 'A': #if cushions are present, adds needle assembles and seals
        needle_seal = ''
        adjustable_cushion = '708386' if bore in ('15','20','25') else '708392'
        if options in viton_codes:
            needle_seal = '600-100F75' if bore in ('15','20','25') else '1000-100F75'
        if cushions in ('B','C','D','E'):
            adjustable_cushion += ' ' + '(2)'
            if options in viton_codes:
                needle_seal += ' ' + '(2)'
    else:
        adjustable_cushion = None
        needle_seal = None


    if mounting == 'S1': #if angle mount is present, recalculates 2 tie-rods with an adder
        if options not in double_rod_codes:
            adder = {'15':0.65,'20':0.625,'25':0.65,'32':1,'40':1.1,'50':1,'60':1.15,'80':0.5}
        else:
            adder = {'15':0.25,'20':0.25,'25':0.25,'32':0.4,'40':0.475,'50':0.4,'60':0.4,'80':0.5}
        tie_rod_2 = tie_rod_calc(bore, options, int(stroke) + adder[bore], mounting, fractional_stroke,rod_style,xi_num)


    if options in double_rod_codes: #makes sure only one CX rod gets used if there are only cushions on one side
                                    #also recalculates rod_2 for double rods based on their extension codes
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
            if cushions in ('B', 'C', 'D', 'E'):
                rod += '  (2)'  # if double rod with no extension and cushions on both ends, use same rod
            else:
                rod_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, extension, options)
                #if there are no cushions, make the rod a normal instead of CX

    # Return all BOM parts in a dictionary to be called by our results page
    return {
            "front_head":front_head,"rear_cover":rear_cover,"rod":rod,
            "rod_2":rod_2,"piston_head":piston_head,"rod_bushing":rod_bushing,
            "cylinder_tube":cylinder_tube,"tie_rod":tie_rod,"tie_rod_2":tie_rod_2,"rod_seal":rod_seal,
            "piston_seal":piston_seal,"rod_wiper":rod_wiper,"tube_gasket":tube_gasket,
            "bushing_seal":bushing_seal,"wearband":wearband,"rod_bearing":rod_bearing,
            "magnet_number":magnet_number,"retaining_ring":retaining_ring,"bumper":bumper,
            "tierod_nut":tierod_nut,"piston_bolt":piston_bolt,"adjustable_cushion": adjustable_cushion,
            "needle_seal": needle_seal, "pivot_bushing": pivot_bushing, "pivot_mount": pivot_mount,
            "pivot_pin": pivot_pin,"pivot_ring": pivot_ring, "rod_spud": rod_spud, "rear_spud": rear_spud,
            "cushioning_seal": cushioning_seal, "cushioning_seal_2": cushioning_seal_2, "male_rod": male_rod,
            "angle_mount": angle_mount, "angle_mount_2": angle_mount_2, "spacer_plate": spacer_plate, "trunnion_pin": trunnion_pin,
            "trunnion_screw": trunnion_screw, "mid_trunnion": mid_trunnion, "flange": flange, 'retainer':retainer,
            "retainer_screw":retainer_screw

            }
