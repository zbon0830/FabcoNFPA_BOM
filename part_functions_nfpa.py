import re, string
from faulthandler import cancel_dump_traceback_later
from selectors import SelectSelector
from fractions import Fraction
import option_code_dict
# Maps bore code to prefix
bore_code = {
    '15': 'N15-', '20': 'N20-', '25': 'N25-', '32': 'N32-',
    '40': 'N40-', '50': 'N50-', '60': 'N60-', '80': 'N80-'
}
bore_descriptor = {'15': '1-1/2" Bore','20':'2" Bore','25': '2-1/2" Bore','32':'3-1/4" Bore','40': '4" Bore',
                   '50':'5" Bore','60': '6" Bore','80':'8" Bore',}
mounting_descriptor = {'X0':'No Mount','F1':'Head Rectangular Flange','F2':'Cap Rectangular Flange','P1':'Fixed Clevis',
                       'P2':'Detachable Clevis','P3':'Fixed Eye','P4':'Detachable Eye','T6':'Head Trunnion','T7':'Cap Trunnion',
                       'T8':'Mid Trunnion','X1':'Extended Tie Rods Both Ends','X2':'Cap End Extended Tie Rods','X3':'Head End Extended Tie Rods',
                       'S1':'Angle Mount','S2':'Side Lug','S4':'Bottom Tapped, Flush Mount','E3':'Head Square Mount','E4':'Cap Square Mount','SN':'Sleeve Nut',
                       'SE':'Sleeve Nut & Bottom Tapped Mount','SF':'Sleeve Nut & Bottom Tapped Mount w/Out Spacer Plate'}
rod_style_descriptor = {'1': 'Style #1, Standard Male','2': 'Style #2, Optional Male','3': 'Style #3, Optional Female',
                        '6': 'Style #6, Oversize Rod, Standard Male','7': 'Style #7, Oversize Rod, Optional Male',
                        '8': 'Style #8, Oversize Rod, Optional Female'}
ports_descriptor = {'B':'1/8 NPT, Position #1','H':'1/8 NPT, Position #2','N':'1/8 NPT, Position #3','T':'1/8 NPT, Position #4',
                    'C':'1/4 NPT, Position #1','I':'1/4 NPT, Position #2','O':'1/4 NPT, Position #3','U':'1/4 NPT, Position #4',
                    'D':'3/8 NPT, Position #1','J':'3/8 NPT, Position #2','P':'3/8 NPT, Position #3','V':'3/8 NPT, Position #4',
                    'E':'1/2 NPT, Position #1','K':'1/2 NPT, Position #2','Q':'1/2 NPT, Position #3','W':'1/2 NPT, Position #4',
                    'F':'3/4 NPT, Position #1','L':'3/4 NPT, Position #2','R':'3/4 NPT, Position #3','X':'3/4 NPT, Position #4'}
cushion_descriptor = {'A':'No Cushions','B':'Head & Cap, Position #1','C':'Head & Cap, Position #2','D':'Head & Cap, Position #3','E':'Head & Cap, Position #4',
                      'Y':'Head & Cap, Fixed Cushion','F':'Head Only, Position #1','G':'Head Only, Position #2','H':'Head Only, Position #3','I':'Head Only, Position #4',
                      'W':'Head Only, Fixed Cushion','K':'Cap Only, Position #1','L':'Cap Only, Position #2','M':'Cap Only, Position #3','N':'Cap Only, Position #4',
                      'V':'Cap Only, Fixed Cushion'}

# Maps fractional stroke letters to decimal values
fractional_stroke_value = {
    'A': 0, 'B': 0.0625, 'C': 0.125, 'D': 0.1875, 'E': 0.250,
    'F': 0.3125, 'G': 0.375, 'H': 0.4375, 'I': 0.500, 'J': 0.5625,
    'K': 0.625, 'L': 0.6875, 'M': 0.750, 'N': 0.8125, 'O': 0.875, 'P': 0.9375
}

magnet_chart = {
    '15': 'PS-1.365X.093', '20': 'PS-1.865X.093', '25': 'PS-2.365X.093',
    '32': 'PS-3.115X.093', '40': 'PS-3.865X.093', '50': 'PS-4.980X.093',
    '60': 'PS-5.980X.093', '80': 'PS-7.980X.093'
}

# Standard C and A dimensions
c_dim = {'15': 0.375, '20': 0.375, '25': 0.375, '32': 0.500, '40': 0.500,
         '50': 0.500, '60': 0.625, '80': 0.625}
c_dim_oversize = {'15': 0.500, '20': 0.500, '25': 0.500, '32': 0.625, '40': 0.625,
                  '50': 0.625, '60': 0.750, '80': 0.750}
a_dim = {'15': 0.750, '20': 0.750, '25': 0.750, '32': 1.125, '40': 1.125,
         '50': 1.125, '60': 1.625, '80': 1.625}
a_dim_oversize = {'15': 1.125, '20': 1.125, '25': 1.125, '32': 1.625, '40': 1.625,
                  '50': 1.625, '60': 2.000, '80': 2.000}

port_position = {
    'B': '1', 'H': '2', 'N': '3', 'T': '4',
    'C': '1', 'I': '2', 'O': '3', 'U': '4',
    'D': '1', 'J': '2', 'P': '3', 'V': '4',
    'E': '1', 'K': '2', 'Q': '3', 'W': '4',
    'F': '1', 'L': '2', 'R': '3', 'X': '4'
}

cushion_position = {
    'B': '1', 'K': '1', 'C': '2', 'L': '2', 'D': '3', 'M': '3', 'E': '4', 'N': '4',
    'F': '1', 'G': '2', 'H': '3', 'J': '4'
}

male_rod_codes = {
    "BI","BJ","BM","BN","BO","BQ","BU","DM","DN","DO","DX","DY",
    "EF","EG","EH","EI","EJ","EM","EN","EO","EU","HA","HB","HC",
    "HD","HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA",
    "IB","IC","ID","IE","IF","LH","LI","LJ","LK","LL","LM","LN",
    "LO","LU","LX","LY","LZ","MC","MD","ME","MF","MG","MH","MI",
    "MJ","MK","MQ","PM","SL","SM","VB","VC","VD","VE","VF","VG",
    "VH","VI","VJ","VK","VM","WC","WM"
}

viton_codes = {
    "PD","PN","PU","PV","PX","PZ","LZ","MJ","LY","LO","LI","IH","IF","IE","IB","IA",
    "HX","HW","HR","HT","HS","HO","HP","HK","HG","HH","HC","HD","DV","DP","DJ","DH","DC","DQ",
    "BV","BQ","BU","BG","BJ","BD","AH","SQ","SO","SV","SY","VB","VC","VD","VE","VF","VG",
    "VH","VI","VJ","VK","VL","VM","VN","VO","VP","VQ","VR","VS","VT","VU","WE","WG","WH",
    "WN","WT","WU","WV","WW","WY"
}

double_rod_codes = {
    "DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO","DP","DQ",
    "DR","DS","DT","DU","DV","DW","DX","DY","DZ","ED","EE","EF","EG","EH","EI","EN","HE",
    "HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP","HQ","HR","HS","HT","HU","HV",
    "HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF","IG","IH","LG","ME","MI","MJ","PD",
    "PN","PR","PY","PZ","SP","VF","VG","VH","VI","VJ","VK","VU","WF","WH","WJ","WL","WN",
    "WT","WX","WY"
}

polypak_rod_codes = {
    "BP","EP","MP","PA","PB","PC","PD","PE","PE","PG","PH","PI","PM","PN","PQ","PR",
    "PS","PT","PU","PV","PW","PY","WB","WN","WO","WP","WQ","WU","WW","WX","WY","WZ"
}

polypak_piston_codes = {
    "PC","PF","PG","PN","PQ","PP","PV","PX","PZ","WB","WG","WH","WJ","WK","WN","WQ",
    "WW","WX"
}

metallic_scraper_codes = {
    "AH", "BD", "BE", "BG", "BI", "BJ", "BO", "BU", "BW", "DE", "DG", "DI", "DJ", "DL", "DQ",
    "DW","DZ","EE", "EG","EI","EJ","EK","EO","EW","HB","HD","HF","HH","HJ","HL","HN","HP","HR",
    "HT","HV","HW", "HX","HZ","IB","IF","ID","LA","LC","LE","LF","LG","LH","LI","LJ","LL","LO",
    "LX","LZ","MB","ME","MG","MI","MP","MS","PH","PI","PR","PW","SW","VB","VE","VF","VG","VI","VK",
    "VP","VT","WB","WC","WD","WE","WF","WG","WH","WJ","WK","WL","WM","WN","WO","WP","WQ","WR",
    "WS","WT","WU","WV","WW","WX","WY","WZ"
}

low_breakaway_codes = {
    "LB","BL","HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN",
    "HO", "HP","HQ","HR","HS","HT","HU","HV","HW","HX","HY","HZ","IA","IB","IC","ID","IE","IF",
    "IG","IH","LA","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO","LQ","LR",
    "LS","LU","LV","LW","LX","LY","LZ","SX","VL","VN","VO","VP","VQ","VT","WL"
}

silent_seal_codes = {
    "CE", "SB", "ED", "EE", "EG", "EH", "EI", "EJ", "EK", "EM", "EN", "EO", "EP", "ER", "ES", "ET",
    "EU", "EW", "EZ",
    "PR", "PY", "SB", "WI", "WZ"
}

tube_gasket_codes = {
    '15': '2-028G', '20': '2-032G', '25': '2-035G', '32': '2-041G', '40': '2-044G',
    '50': '2-048G', '60': '2-050G', '80': '2-265G'
}

wearband_codes = {
    '15': 'N15-PWB', '20': 'N20-PWB', '25': 'N25-PWB', '32': 'N32-PWB', '40': 'N40-PWB',
    '50': 'N50-PWB', '60': 'N60-PWB', '80': 'N80-PWB'
}

bumper_rear_codes = {
    "BB","BD","BE","BG","BI","BJ","BL","BM","BN","BO","BP","BQ","BS","BT","BU","BV","BW","CD",
    "DB","DG","DH","DI","DK","DL","DP","DQ","FB","HA","HB","HC","HD","HI","HJ","HK","HL","HM",
    "HN","HO","HP","HY","HZ","IA","IB","IC","ID","IE","IF","LB","LC","LD","LE","LU","LX","LY",
    "LZ","MF","MG","MH","MI","SJ","SK","SL","SQ","SX","VD","VH","VI","VJ","VK","VO","VP","VQ",
    "VT","WB"
}

bumper_front_codes = {
    "BB","BD","BE",'BF',"BG","BI","BJ","BL","BM","BN","BO","BP","BQ",
    "BS","BT","BU","BV","BW","DB","DF","DG","DH","DI","DK","DL",
    "DP","DQ","FB","HA","HB","HC","HD","HI","HJ","HK","HL","HM",
    "HN","HO","HP","HY","HZ","IA","IB","IC","ID","IE","IF","LC",
    "LD","LE","LU","LX","LY","LZ","MF","MG","MH","MI","SK","SL",
    "SP","SQ","VD","VH","VI","VJ","VK","VO","VP","VQ","VT","WB"
}

bumper_both_codes = {
    'BB','BD','BE','BG','BI','BJ','BL','BM','BN','BO','BP','BQ','BS','BT','BU','BV','BW',
    'DB','DG','DH','DI','DK','DL','DP','DQ','FB','HA','HB','HC','HD','HI','HJ','HK','HL',
    'HM','HN','HO','HP','HY','HZ','IA','IB','IC','ID','IE','IF','LC','LD','LE','LU','LX',
    'LY','LZ','MF','MG','MH','MI','SK','SL','SQ','VD','VH','VI','VJ','VK','VO','VP','VQ',
    'VT','WB','MB','PB','PG'
}

stainless_fastener_codes = {
    "AH","BE","BE","BG","BN","BO","BQ","BS","BT","CS","CU","DC","DD","DE","DK","DL",
    "DP","DQ","DT","DI","DZ","EF","EH","EU","EI","EJ","EK","ES","ET","EU","EZ","HA",
    "HB","HC","HD","HE","HF","HG","HH","HM","HN","HO","HP","HU","HV","HW","HX","IC",
    "ID","IE","IF","LA","LD","LE","LK","LL","LN","LO","LQ","LS","MC","ME","MH","MI",
    "MJ","MK","MS","PH","PI","PS","PT","RW","SM","SJ","SM","SO","SP","SQ","SS","ST",
    "SV","SU","SW","SX","SY","VC","VE","VG","VJ","VK","VL","VN","VQ","VT","VU","WC","WD",
    "WE","WR","EU","LS","PI","PS","SR","ST","VL","VN"
}

stainless_rod_codes = {
    "AH","BE","BG","BN","BO","BQ","BS","BU","CR","CU","DC","DD","DE",
    "DJ","DK","DL","DP","DQ","DS","DU","DZ","EE","EF","EH","EI","EJ",
    "EK","ER","ES","EZ","HA","HB","HC","HD","HE","HF","HG","HH","HM",
    "HN","HO","HP","HU","HV","HW","HX","IC","ID","IE","IF","LA","LD",
    "LE","LK","LL","LN","LO","LR","MC","MD","ME","MH","MI","MJ","MQ",
    "MS","PC","PE","PF","RW","SK","SL","SP","SQ","SS","SU","SV","SW",
    "SX","SY","VC","VE","VG","VJ","VK","VQ","VR","VT","VU","WC","WD",
    "WE","WR","EU","LS","PI","PS","SR","ST","VL","VN"
}


# -------------------------------
# Parsing and Calculation Functions
# -------------------------------

def split_part_number(part_number):
    part_number = part_number.upper()
    part_number = part_number.upper().replace("XO", "X0")
    part_number_new=part_number
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2})([A-Z])(\d)([A-Z])([A-Z])-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z](?:\d{2}[A-Z])?|\w{4,8}))?(?:-XI=(\d+\.\d{1,3}))?$"
    match = re.match(pattern, part_number)
    if not match:
        raise ValueError("Part number format is invalid")
    return match.groups(),part_number_new


def front_head_calc(bore, mounting, ports, cushions, rod_style):
    # Default quantity = 1
    port_code = {
        'B': 'B', 'H': 'B', 'N': 'B', 'T': 'B',
        'C': 'C', 'I': 'C', 'O': 'C', 'U': 'C',
        'D': 'D', 'J': 'D', 'P': 'D', 'V': 'D',
        'E': 'E', 'K': 'E', 'Q': 'E', 'W': 'E',
        'F': 'F', 'L': 'F', 'R': 'F', 'X': 'F'
    }
    front_cushion_code = {'A': 'A', 'B': 'F', 'F': 'F', 'C': 'G', 'G': 'G', 'D': 'H', 'H': 'H', 'E': 'J', 'J': 'J'}
    front_cushion_position = {'B': '1', 'F': '1', 'C': '2', 'G': '2', 'D': '3', 'H': '3', 'E': '4', 'J': '4'}
    front_cushion_result = front_cushion_code.get(cushions, 'A')
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
        if block_code.get(mounting, 'ERROR') in ('200', '205'):
            if int(port_position[ports]) == int(front_cushion_position[cushions]) + 1:
                front_cushion_result = 'J'
            elif int(front_cushion_position[cushions]) == int(port_position[ports]) + 1:
                front_cushion_result = 'G'
            elif abs(int(front_cushion_position[cushions]) - int(port_position[ports])) == 2:
                front_cushion_result = 'H'
        else:
            port_code = {
                'B': 'B', 'H': 'H', 'N': 'N', 'T': 'T',
                'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                'F': 'F', 'L': 'F', 'R': 'R', 'X': 'X'
            }
    else:
        if block_code.get(mounting, 'ERROR') not in ('200', '205'):
            port_code = {
                'B': 'B', 'H': 'B', 'N': 'N', 'T': 'T',
                'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                'F': 'F', 'L': 'F', 'R': 'R', 'X': 'X'
            }
    front_head = bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-' + port_code[ports] + front_cushion_result
    return front_head  # quantity defaults to 1


def rear_cover_calc(bore, mounting, ports, cushions, options, rod_style):
    port_code = {
        'B': 'B', 'H': 'B', 'N': 'B', 'T': 'B',
        'C': 'C', 'I': 'C', 'O': 'C', 'U': 'C',
        'D': 'D', 'J': 'D', 'P': 'D', 'V': 'D',
        'E': 'E', 'K': 'E', 'Q': 'E', 'W': 'E',
        'F': 'F', 'L': 'F', 'R': 'F', 'X': 'F'
    }
    cover_code = {
        'X0': '100', 'F1': '100', 'F2': '100', 'P1': '150', 'P2': '100', 'P3': '140',
        'S1': '205', 'P4': '100', 'T6': '100', 'T7': '120', 'T8': '100', 'X1': '100',
        'X2': '100', 'X3': '100', 'S2': '130', 'S4': '110', 'E3': '190', 'E4': '190',
        'SN': '160', 'SE': '170', 'SF': '170'
    }
    rear_cushion_code = {'A': 'A', 'B': 'K', 'K': 'K', 'C': 'L', 'L': 'L', 'D': 'M', 'M': 'M', 'E': 'N', 'N': 'N'}
    rear_cushion_position = {'B': '1', 'K': '1', 'C': '2', 'L': '2', 'D': '3', 'M': '3', 'E': '4', 'N': '4'}
    rear_cushion_result = rear_cushion_code.get(cushions, 'A')
    if rear_cushion_result != 'A':
        if cover_code.get(mounting, 'ERROR') in ('100', '105'):
            if int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1:
                rear_cushion_result = 'N'
            elif int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1:
                rear_cushion_result = 'L'
            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'
        elif cover_code.get(mounting, 'ERROR') in ('140', '150'):
            if (int(rear_cushion_position[cushions]) == int(port_position[ports]) + 1) and (port_position[ports] in ('2', '4')):
                rear_cushion_result = 'L'
            elif (int(port_position[ports]) == int(rear_cushion_position[cushions]) + 1) and (port_position[ports] in ('1', '3')):
                rear_cushion_result = 'N'
            elif abs(int(rear_cushion_position[cushions]) - int(port_position[ports])) == 2:
                rear_cushion_result = 'M'
    else:
        if cover_code.get(mounting, 'ERROR') not in ('200', '205'):
            port_code = {
                'B': 'B', 'H': 'B', 'N': 'N', 'T': 'T',
                'C': 'C', 'I': 'C', 'O': 'O', 'U': 'U',
                'D': 'D', 'J': 'J', 'P': 'P', 'V': 'V',
                'E': 'E', 'K': 'K', 'Q': 'Q', 'W': 'W',
                'F': 'F', 'L': 'F', 'R': 'R', 'X': 'X'
            }
    if options not in double_rod_codes:
        rear_cover = bore_code.get(bore, 'UNKNOWN') + cover_code.get(mounting, 'ERROR') + '-' + port_code[ports] + rear_cushion_result
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
        rear_cover = bore_code.get(bore, 'ERROR') + block_code.get(mounting, 'ERROR') + '-' + port_code[ports] + rear_cushion_result
    return rear_cover  # quantity defaults to 1


def piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension, options):
    if bore in ('15', '20', '25'):
        rod_prefix = 'N15'
    else:
        rod_prefix = 'N32'
    rod_code = {'1': '-30X', '2': '-35X', '3': '-40X', '6': '-10X', '7': '-15X', '8': '-20X'}
    # OBSOLETE RODif bore == '15' and cushions != 'A' and rod_style == '3':
        #rod_code = {'3': '-40CX'}
    if bore in ('32', '40', '50') and cushions != 'A' and rod_style in ('6', '7', '8'):
        rod_code = {'6': '-10CX', '7': '-15CX', '8': '-20CX'}
    elif bore in ('60', '80') and cushions != 'A':
        rod_prefix = 'N60'
        rod_code = {'1': '-30CX', '2': '-35CX', '3': '-40CX', '6': '-10CX', '7': '-15CX', '8': '-20CX'}
    if options in stainless_rod_codes:
        rod_prefix += 'SR'
    rod_adder = 0
    total_extension = 0
    if extension:
        whole_extension = int(extension[2:4])
        fractional_extension = fractional_stroke_value[extension[4]]
        if extension.startswith(('CD', 'RC', 'CR')):
            if rod_style in ('1', '2', '3'):
                total_extension = (whole_extension + fractional_extension - c_dim[bore])
            else:
                total_extension = (whole_extension + fractional_extension - c_dim_oversize[bore])
        elif extension.startswith(('AD', 'RA', 'AR')):
            if rod_style in ('1', '2', '3'):
                total_extension = (whole_extension + fractional_extension - a_dim[bore])
            else:
                total_extension = (whole_extension + fractional_extension - a_dim_oversize[bore])
        elif extension.startswith(('AC', 'RR')):
            whole_extension = int(extension[2:3]) + int(extension[5:7])
            fractional_extension = fractional_stroke_value[extension[4]] + fractional_stroke_value[extension[7]]
            if rod_style in ('1', '2', '3'):
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
    if options in bumper_front_codes or options in bumper_both_codes:
        rod_adder += 0.063
    rod_length = rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke] + total_extension
    if rod_style in ('1','2','6','7'):
        L1_dim = f'{(rod_length - a_dim[bore]):.3f}' if rod_style in ('1','2') else f'{(rod_length - a_dim_oversize[bore]):.3f}'
    else:
        L1_dim = None
    rod = f"{rod_prefix}{rod_code[rod_style]}{rod_length:.3f}"
    if extension:
        if extension.startswith(('AD', 'RA', 'AR', 'AC')):
            rod += '-AD' + extension[2:5]
    return rod,L1_dim  # quantity defaults to 1


def piston_head_calc(bore, rod_style, options):
    if rod_style in ('1', '2', '3'):
        piston_number = '70' if options == 'SB' else '60'
    else:
        piston_number = '75' if (options == 'SB' and bore != '15') else '65'
        if bore in ('60', '80'):
            piston_number = '70' if options == 'SB' else '60'
    if (options in bumper_front_codes or options in bumper_rear_codes or options in bumper_both_codes) and bore != '15':
        piston_number += '-BB'
    piston_head = f"{bore_code.get(bore, 'ERROR')}{piston_number}"
    return piston_head  # quantity defaults to 1


def rod_bushing_calc(bore, rod_style, options):
    quantity = 1
    bushing_number = '90'
    bushing_prefix = ''
    if bore in ('15', '20', '25'):
        if bore == '15' and rod_style in ('6', '7', '8'):
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
    rod_bushing = bushing_prefix + bushing_number
    if options in metallic_scraper_codes:
        rod_bushing += '-WS'
    if options in double_rod_codes:
        quantity = 2
    return rod_bushing, quantity


def tube_calc(bore, options, stroke, fractional_stroke):
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
        cylinder_length = 1.875
    if (options in bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes:
        cylinder_length += 0.063
    elif options in bumper_both_codes:
        cylinder_length += 0.125
    if int(stroke) >= 72:
        cylinder_length += 0.036
    elif int(stroke) >= 48:
        cylinder_length += 0.024
    elif int(stroke) >= 24:
        cylinder_length += 0.012
    cylinder_tube = f"{cylinder_prefix}{(cylinder_length + int(stroke) + fractional_stroke_value[fractional_stroke]):.3f}"
    return cylinder_tube  # quantity defaults to 1


def tie_rod_calc(bore, options, stroke, mounting, fractional_stroke, rod_style, xi_num):
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
        elif mounting == 'T8':
            tie_rod_adder = (-0.8 if rod_style in ('1', '2', '3') else -1.175) + float(xi_num)
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
            tie_rod_adder = (-0.625 if rod_style in ('1', '2', '3') else -1.1) + float(xi_num)
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
            tie_rod_adder = (-0.625 if rod_style in ('1', '2', '3') else -1.1) + float(xi_num)
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
            tie_rod_adder = (-1.05 if rod_style in ('1', '2', '3') else -1.300) + float(xi_num)
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
            tie_rod_adder = (-0.925 if rod_style in ('1', '2', '3') else -1.175) + float(xi_num)
    elif bore == '60':
        tie_rod_prefix = 'N50-7X'
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
            tie_rod_adder = (-1.175 if rod_style in ('1', '2', '3') else -1.425) + float(xi_num)
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
            tie_rod_adder = (-1.05 if rod_style in ('1', '2', '3') else -1.300) + float(xi_num)
    if options in double_rod_codes:
        tie_rod_adder += 0.5
    if (options in bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes and mounting != 'T8':
        tie_rod_adder += 0.063
    elif options in bumper_both_codes and mounting != 'T8':
        tie_rod_adder += 0.125
    if mounting == 'S1':
        quantity = 2
    tie_rod_length = tie_rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke]
    tie_rod = f"{tie_rod_prefix}{tie_rod_length:.3f}"
    if mounting == 'T8_2':  # Unique T8 second tie rod set calculation (WIP)
        if rod_style in ('1', '2', '3'):
            ZB_subtractor = {'15': 4.875, '20': 4.940, '25': 5.060, '32': 6.000, '40': 6.000, '50': 6.375, '60': 7.125,
                             '80': 7.375}
        else:
            ZB_subtractor = {'15': 5.250, '20': 5.315, '25': 5.440, '32': 6.250, '40': 6.250, '50': 6.625, '60': 7.375,
                             '80': 7.625}
        adder = 0
        if options in (bumper_front_codes or options in bumper_rear_codes) and options not in bumper_both_codes:
            adder += .063
        elif options in bumper_both_codes:
            adder += .125
        if options in double_rod_codes:
            adder += 0.5
        tie_rod = f"{tie_rod_prefix}{(ZB_subtractor[bore] + int(stroke) + fractional_stroke_value[fractional_stroke] - float(xi_num) - .05 + adder):.3f}"
    return tie_rod, quantity


def rod_seal_calc(bore, rod_style, options):
    quantity = 1
    if bore in ('15', '20', '25'):
        rod_seal = '666-208-35901' if rod_style in ('1', '2', '3') else '666-50100-35901'
        if options in viton_codes:
            rod_seal = '8404-0062V' if rod_style in ('1', '2', '3') else '8405-0100V'
        if options in polypak_rod_codes:
            rod_seal = '1250-0625' if rod_style in ('1', '2', '3') else '1560-1000'
            if options in viton_codes:
                rod_seal += 'V'
    elif bore in ('32', '40', '50'):
        rod_seal = '666-50100-35901' if rod_style in ('1', '2', '3') else '666-324-35901'
        if options in viton_codes:
            rod_seal = '8405-0100V' if rod_style in ('1', '2', '3') else 'C43-36'
        if options in polypak_rod_codes:
            rod_seal = '1560-1000' if rod_style in ('1', '2', '3') else '1870-1375'
            if options in viton_codes:
                rod_seal = '1560-1000V' if rod_style in ('1', '2') else '18701375V4208'
    elif bore in ('60', '80'):
        rod_seal = '666-324-35901' if rod_style in ('1', '2', '3') else '666-327-35901'
        if options in viton_codes:
            rod_seal = 'c43-36' if rod_style in ('1', '2', '3') else '8406-0175V'
        if options in polypak_rod_codes:
            rod_seal = '1870-1375'
            if options in viton_codes:
                rod_seal = '18701375V4208' if rod_style in ('1', '2') else 'ERROR, NOT ComPATIBLE'
    if options in double_rod_codes:
        quantity = 2
    return rod_seal, quantity


def piston_seal_calc(bore, rod_style, options):
    # Piston seal quantity is always 2.
    quantity = 2
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
        piston_seal = '8509-05437-4180'
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
    return piston_seal, quantity


def rod_wiper_calc(bore, rod_style, options):
    quantity = 1
    if bore in ('15', '20', '25'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-5/6-BN' if rod_style in ('1', '2', '3') else 'SG-3435-5/6-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-3' if rod_style in ('1', '2','3') else '940-9'
            if options in viton_codes:
                rod_wiper += 'V'
    elif bore in ('32', '40', '50'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3435-1-BN' if rod_style in ('1', '2','3') else 'SG-3436-1-3/8-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-9' if rod_style in ('1', '2','3') else '940-15'
            if options in viton_codes:
                rod_wiper += 'V'
    elif bore in ('60', '80'):
        if options in metallic_scraper_codes:
            rod_wiper = 'SG-3436-1-3/8-BN' if rod_style in ('1', '2','3') else 'SG-3435-1-3/4-BN'
            if options in viton_codes:
                rod_wiper = rod_wiper[:-2] + "V"
        else:
            rod_wiper = '940-15' if rod_style in ('1', '2','3') else 'D-1750U2145'
            if options in viton_codes:
                rod_wiper = 'D-1750VT90'
    if options in double_rod_codes:
        quantity = 2
    return rod_wiper, quantity


def bushing_seal_calc(bore, rod_style, options):
    bushing_seal = ''
    if bore in ('15', '20', '25'):
        bushing_seal = '2-122' if rod_style in ('1', '2', '3') else '2-222'
        if bore == '15' and rod_style in ('6', '7', '8'):
            bushing_seal = '2-125'
        if options in viton_codes:
            bushing_seal += 'V'
    elif bore in ('32', '40', '50'):
        bushing_seal = '2-222' if rod_style in ('1', '2', '3') else '2-227'
        if options in viton_codes:
            bushing_seal += 'V'
    elif bore in ('60', '80'):
        bushing_seal = '2-227' if rod_style in ('1', '2', '3') else '2-229'
        if options in viton_codes:
            bushing_seal += 'V'
    bushing_seal_qty = 2 if options in double_rod_codes else 1
    return bushing_seal, bushing_seal_qty


def rod_bearing_calc(bore, rod_style, options):
    quantity = 1
    if bore in ('15', '20', '25'):
        rod_bearing = '701-00010-024' if rod_style in ('1', '2', '3') else '701-112016-032'
    elif bore in ('32', '40', '50'):
        if bore == '32' and options in metallic_scraper_codes:
            rod_bearing = '701-112016-029' if rod_style in ('1', '2', '3') else '701-600022-039'
        else:
            rod_bearing = '701-112016-032' if rod_style in ('1', '2', '3') else '701-600022-039'

    elif bore in ('60', '80'):
        rod_bearing = '701-600022-039' if rod_style in ('1', '2', '3') else '701-00028-044'
    if options in double_rod_codes:
        quantity = 2
    return rod_bearing, quantity


def retaining_ring_calc(bore, options, rod_style):
    quantity = 1
    if bore in ('15', '20', '25'):
        if rod_style in ('1', '2', '3'):
            retaining_ring = 'N5008-131' if options not in stainless_fastener_codes else 'N5008-131SS'
        else:
            retaining_ring = 'N5008-175' if options not in stainless_fastener_codes else 'N5008-175SS'
    elif bore in ('32', '40', '50'):
        if rod_style in ('1', '2', '3'):
            retaining_ring = 'N5008-175' if options not in stainless_fastener_codes else 'N5008-175SS'
        else:
            retaining_ring = 'N5008-237PA' if options not in stainless_fastener_codes else 'N5008-237SS'
    elif bore in ('60', '80'):
        if rod_style in ('1', '2', '3'):
            retaining_ring = 'N5008-237PA' if options not in stainless_fastener_codes else 'N5008-237SS'
    if options in double_rod_codes:
        quantity = 2
    return retaining_ring, quantity


def bumper_calc(bore, options):
    quantity = 1
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
        elif bore in ('50', '60', '80'):
            bumper = 'MPS-371-66'
        if options in bumper_both_codes:
            quantity = 2
    else:
        bumper = None
    return bumper, quantity


def cushion_spud_calc(bore, rod_style, cushions, options):
    # Returns:
    # (rod_spud, rod_spud_qty, rear_spud, rear_spud_qty, cushioning_seal, cushioning_seal_qty, cushioning_seal_2, cushioning_seal_2_qty)
    rod_spud = None
    rear_spud = None
    cushioning_seal = None
    cushioning_seal_qty = 1
    cushioning_seal_2 = None
    cushioning_seal_2_qty = 0
    if cushions != 'A':
        if bore in ('15', '20', '25'):
            rod_spud = 'N15-300' if rod_style in ('1', '2', '3') else 'N15-310'
            rear_spud = 'N15-305' if rod_style in ('1', '2', '3') else 'N15-315'
            if cushions in ('F', 'G', 'H', 'J', 'W'):  # if the cushions are only in front, they must change if oversize rod
                cushioning_seal = 'V6-04.0020N4181A85' if rod_style in ('1', '2', '3') else 'V6-05.0032N4181A85'
            elif cushions in ('B', 'C', 'D', 'E',
                              'Y'):  # if cushions in both sides, use one of each if oversize                                              #otherwise, two of standard ones
                cushioning_seal = 'V6-04.0020N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal_qty = 2
                else:
                    cushioning_seal_qty = 1
                    cushioning_seal_2 = 'V6-05.0032N4181A85'
            elif cushions in ('K', 'L', 'M', 'N', 'V'):  # if cushions are only in rear, cushions never change
                cushioning_seal = 'V6-04.0020N4181A85'
        elif bore in ('32', '40', '50'):  # repeat everything from previous bore onwards
            rod_spud = 'N32-300' if rod_style in ('1', '2', '3') else 'N32-310'
            rear_spud = 'N32-305' if rod_style in ('1', '2', '3') else 'N32-315'
            if cushions in ('F', 'G', 'H', 'J', 'W'):
                cushioning_seal = 'V6-05.0032N4181A85' if rod_style in ('1', '2', '3') else 'V6-05.0038N4181A85'
                cushioning_seal_2 = None
            elif cushions in ('B', 'C', 'D', 'E', 'Y'):
                cushioning_seal = 'V6-05.0032N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal_qty = 2
                else:
                    cushioning_seal_qty = 1
                    cushioning_seal_2 = 'V6-05.0038N4181A85'
            elif cushions in ('K', 'L', 'M', 'N', 'V'):
                cushioning_seal = 'V6-05.0032N4181A85'
        elif bore in ('60', '80'):
            rod_spud = 'N60-300' if rod_style in ('1', '2', '3') else 'N60-310'
            rear_spud = 'N60-305' if rod_style in ('1', '2', '3') else 'N60-315'
            if cushions in ('F', 'G', 'H', 'J', 'W'):
                cushioning_seal = 'V6-05.0038N4181A85' if rod_style in ('1', '2', '3') else 'V6-05.0050N4181A85'
                cushioning_seal_2 = None
            elif cushions in ('B', 'C', 'D', 'E', 'Y'):
                cushioning_seal = 'V6-05.0038N4181A85'
                if rod_style in ('1', '2', '3'):
                    cushioning_seal_qty = 2
                else:
                    cushioning_seal_qty = 1
                    cushioning_seal_2 = 'V6-05.0050N4181A85'
            elif cushions in ('K', 'L', 'M', 'N', 'V'):
                cushioning_seal = 'V6-05.0038N4181A85'
    return rod_spud, 1, rear_spud, 1, cushioning_seal, cushioning_seal_qty, cushioning_seal_2, cushioning_seal_2_qty


def tierod_nut_calc(bore, options, mounting):
    if bore == '15':
        part = '1/4-28' if options not in stainless_fastener_codes else '1/4-28SS'
    elif bore in ('20', '25'):
        part = '5/16-24' if options not in stainless_fastener_codes else '5/16-24SS'
    elif bore in ('32', '40'):
        part = '3/8-24' if options not in stainless_fastener_codes else '3/8-24SS'
    elif bore in ('50', '60'):
        part = '1/2-20' if options not in stainless_fastener_codes else '1/2-20SS'
    elif bore == '80':
        part = '5/8-18' if options not in stainless_fastener_codes else '5/8-18SS'
    if mounting in ('P1', 'P2', 'P3', 'P4', 'F1', 'F2', 'E3', 'E4'):
        quantity = 4
    elif mounting in ('SN', 'SE', 'SF'):
        if bore == '15':
            part = 'FCQN-0150-SN'
        elif bore in ('20', '25'):
            part = 'FCQN-0200/250-SN'
        elif bore in ('32', '40'):
            part = 'FCQN-0325/400-SN'
        elif bore in ('50', '60'):
            part = 'N50-SN'
        elif bore == '80':
            part = 'N/A'
        quantity = 8 if options in double_rod_codes else 4
    else:
        quantity = 8
    return part, quantity


def retainer_plate_calc(bore, rod_style, mounting):
    retainer = None
    retainer_screw = None
    retainer_screw_qty = 1
    if bore != '80':
        if mounting in ('SN', 'SE'):
            retainer_screw_code = {
                '15': '8/32X1/2SHCS', '20': '10/32X1/2SHCS', '25': '10/32X1/2SHCS', '32': '1/4-28X3/4SHCS'
                , '40': '3/8-24X3/4SHCS', '50': '3/8-24X3/4SHCS', '60': '3/8-24X3/4SHCS'
            }
            retainer_screw = retainer_screw_code[bore]
            retainer_screw_qty = 2
        elif bore in ('15', '60', '80') and mounting not in ('SN', 'SE', 'X1', 'X3') and rod_style not in ('1', '2', '3'):
            retainer = bore_code[bore] + '340'
            retainer_screw_code = {'15': '', '60': '5/16-24X3/4SHCS-SS', '80': '5/16-24X7/8SHCS'}
            retainer_screw = retainer_screw_code[bore]
            retainer_screw_qty = 2
    return retainer, (retainer_screw, retainer_screw_qty)


def pivot_calc(bore, mounting, options):
    pivot_bushing = None
    pivot_bushing_qty = 1
    if mounting in ('P1', 'P3'):
        if bore in ('15', '20', '25'):
            pivot_bushing = '521-370' if mounting == 'P1' else 'CP8011-2'
            if mounting == 'P1':
                pivot_bushing_qty = 2
        elif bore in ('32', '40', '50'):
            pivot_bushing = 'AA083901'
            pivot_bushing_qty = 2
        elif bore in ('60', '80'):
            pivot_bushing = 'EP161812'
            pivot_bushing_qty = 2
    pivot_mount = None
    if mounting in ('P2', 'P4'):
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
    pivot_pin = None
    pivot_pin_qty = 1
    pivot_ring = None
    pivot_ring_qty = 1
    if mounting in ('P1', 'P2'):
        if bore in ('15', '20', '25'):
            pivot_pin = 'HP11-155' if options not in stainless_fastener_codes else 'N15-500SS'
            pivot_ring = 'N5100-50' if options not in stainless_fastener_codes else 'N5100-50SS'
            pivot_ring_qty = 2
        elif bore in ('32', '40', '50'):
            pivot_pin = 'HP30-155' if options not in stainless_fastener_codes else 'N32-750SS'
            pivot_ring = 'N5100-75' if options not in stainless_fastener_codes else 'N5100-75SS'
            pivot_ring_qty = 2
        elif bore in ('60', '80'):
            pivot_pin = 'HP60-155' if options not in stainless_fastener_codes else 'N60-100SS'
            pivot_ring = 'N5100-100' if options not in stainless_fastener_codes else 'N5100-100SS'
            pivot_ring_qty = 2
    return (pivot_bushing, pivot_bushing_qty), pivot_mount, (pivot_pin, pivot_pin_qty), (pivot_ring, pivot_ring_qty)


def piston_bolt_calc(bore, options, rod_style, cushions):
    piston_bolt = ''
    if options not in double_rod_codes:
        if bore in ('15','20','25','30'):
            if rod_style in ('1', '2', '3'):
                piston_bolt = 'M8X1.25X40SHCS' if cushions == 'A' else 'M8X1.25X50SHCS'
            else:
                piston_bolt = '1/2-20X1-3/4SHCS' if cushions == 'A' else '1/2-20X2-1/2SHCS'
        elif bore in ('32', '40'):
            if rod_style in ('1', '2', '3'):
                piston_bolt = 'M14X2.0X50SHCS' if cushions == 'A' else 'M14X2.0X60SHCS'
            else:
                piston_bolt = '3/4-16X2SHCS' if cushions == 'A' else '3/4-16X3SHCS'
        elif bore == '50':
            if rod_style in ('1', '2', '3'):
                piston_bolt = 'M14X2.0X50SHCS' if cushions == 'A' else 'M14X2.0X60SHCS'
            else:
                piston_bolt = '3/4-16X2-1/4SHCS' if cushions == 'A' else '3/4-16X3SHCS'
        elif bore in ('60', '80'):
            if rod_style in ('1', '2', '3'):
                piston_bolt = '3/4-16X2-1/4SHCS' if cushions == 'A' else '3/4-16X3SHCS'
            else:
                piston_bolt = '3/4-16X2-1/2SHCS' if cushions == 'A' else '3/4-16X3SHCS'
    else:
        piston_bolt = None
    return piston_bolt  # quantity defaults to 1


def accessory_calc(bore, options, mounting, rod_style):
    male_rod = None
    # angle_mount: return as tuple (part, quantity)
    angle_mount = None
    angle_mount_qty = 1
    angle_mount_2 = None
    spacer_plate = None
    trunnion_pin = None
    trunnion_pin_qty = 1
    trunnion_screw = None
    mid_trunnion = None
    flange = None
    if options in male_rod_codes:
        if bore in ('15', '20', '25'):
            male_rod = '7/16-20X1-1/2SS' if rod_style in ('1', '2', '3') else '3/4-16X2-1/2SS'
        elif bore in ('32', '40', '50'):
            male_rod = '3/4-16X2-1/2SS' if rod_style in ('1', '2', '3') else '1-14X3SS'
        elif bore in ('60', '80'):
            male_rod = '1-14X3SS' if rod_style in ('1', '2', '3') else 'UNAVAILABLE'
    if mounting == 'S1':
        angle_mount_code = {
            '15': 'LB-FCQN-0150', '20': 'LB-FCQN-0200', '25': 'LB-FCQN-0250', '32': 'LB-FCQN-0325',
            '40': 'LB-FCQN-0400', '50': 'N50-400', '60': 'N60-400', '80': 'N80-400'
        }
        if rod_style in ('6', '7', '8'):
            angle_mount = angle_mount_code[bore]
            angle_mount_qty = 1
            angle_mount_2 = bore_code[bore] + '405'
        else:
            angle_mount = angle_mount_code[bore]
            angle_mount_qty = 2
        if bore != '80' and options not in double_rod_codes:
            spacer_plate = bore_code[bore] + '385'
    if mounting in ('T6', 'T7', 'T8'):
        if bore not in ('60', '80'):
            trunnion_pin = 'N15-325'
            trunnion_pin_qty = 2
            trunnion_screw = '5/8-18X2SHCS'
        else:
            trunnion_pin = 'N60-325'
            trunnion_pin_qty = 2
            trunnion_screw = '7/16-20X1SHCS'
        if mounting == 'T8':
            mid_trunnion = bore_code[bore] + '330'
    if mounting in ('F1', 'F2'):
        flange = bore_code[bore] + ('350' if rod_style in ('1', '2', '3') else '355')
    if mounting in ('SN', 'SE'):
        spacer_plate = bore_code[bore] + ('375' if rod_style in ('1', '2', '3') else '376')
    if mounting in ('X1', 'X3'):
        spacer_plate = bore_code[bore] + ('380' if rod_style in ('1', '2', '3') else '381')
    return male_rod, (angle_mount, angle_mount_qty), angle_mount_2, spacer_plate, (trunnion_pin, trunnion_pin_qty), trunnion_screw, mid_trunnion, flange


def generate_bom(parsed_data):
    """
    Given the parsed NFPA part number data, calculates all BOM parts and returns
    a dictionary where each part is represented as a dictionary with separate
    keys for 'part_number' and 'quantity'.
    """

    (bore, mounting, stroke, fractional_stroke, rod_style,
     ports, cushions, options, magnet, extension, xi_num) = parsed_data

    if mounting == 'T6' and (cushions in ('C', 'G', 'E', 'J') or port_position[ports] in ('2', '4')):
        raise ValueError("Error: Mounting 'T6' is Incompatible With Cushions or Ports on Head at Positions 2 or 4.")
    if mounting == 'S4' and cushions != 'A' and (cushion_position[cushions] == '3' or port_position[ports] == '3'):
        raise ValueError("Error: Mounting 'S4' is Incompatible with Cushions or Ports at Position 3.")
    if rod_style not in ('3','8') and options in male_rod_codes:
        raise ValueError("Error: Male Rod Stud Only Available on Style 3 and 8 Rods.")
    if mounting == 'T8' and not xi_num:
        raise ValueError("Error: Mid Trunnion Mount Must Have XI Dimension in Part Number.")
    if extension and extension.startswith(('RA','RC','RR','AR','CR')) and options not in double_rod_codes:
        raise ValueError("Error: Double-Rod Option is Not Present With Double-Rod Extension")
    if rod_style in ('6','7','8') and bore =='15' and cushions != 'A':
        raise ValueError('Error: Cushions Not Available With 1-1/2" Bore Oversize Rod.')
    if options not in option_code_dict.option_descriptor:
        raise ValueError('Contact Engineering to Add Option Code.')
    extension_type = {'AD': 'Rod Thread on Head End Total “A” Dim = ', 'CD': 'Shaft on Head End Total “C” Dim = ',
                      'AC': 'Head End Total “A” & “C” Dims Combined ',
                      'RA': 'Rod Thread on Cap End Double Rod Total "A" Dim = ',
                      'RC': 'Shaft on Cap End Double Rod Total "C" Dim = ',
                      'RR': 'Cap End Double Rod Total "A & C" Dims Combined = ',
                      'AR': 'Rod Thread on Head End Total "A" & Rod Thread on Cap End Total "A" Dims Combined = ',
                      'CR': 'Shaft on Head End Total "C" & Shaft on Cap End Total "C" Dims Combined = '}
    if extension:
        if extension.startswith(('AC','RR','AR','CR')):
            extension_1 = f'{str(int(extension[2:4]))}-{Fraction(fractional_stroke_value[extension[4]])}"' if \
                            extension[4] != 'A' else f'{str(int(extension[2:4]))}"'
            extension_2 = f'{str(int(extension[5:7]))}-{Fraction(fractional_stroke_value[extension[7]])}"' if \
                            extension[7] != 'A' else f'{str(int(extension[5:7]))}"'
            extension_length = f'{extension_1} and {extension_2}'
        else:
            extension_length = f'{str(int(extension[2:4]))}-{Fraction(fractional_stroke_value[extension[4]])}"' if \
                                extension[4] != 'A' else f'{str(int(extension[2:4]))}"'
        extension_descriptor = extension_type[extension[0:2]] + extension_length
    else:
        extension_descriptor = None



    magnet_descriptor = '(N) No Magnet' if magnet != 'E' else '(E) Magnet'
    front_head = front_head_calc(bore, mounting, ports, cushions, rod_style)
    rear_cover = rear_cover_calc(bore, mounting, ports, cushions, options, rod_style)
    rod,L1_dim = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension, options)
    rod_2 = None  # Will be calculated for double rods if applicable.
    piston_head = piston_head_calc(bore, rod_style, options)
    rod_bushing, rod_bushing_qty = rod_bushing_calc(bore, rod_style, options)
    cylinder_tube = tube_calc(bore, options, stroke, fractional_stroke)
    tie_rod, tie_rod_qty = tie_rod_calc(bore, options, stroke, mounting, fractional_stroke, rod_style, xi_num)
    tie_rod_2,tie_rod_2_qty = None,None  # If needed
    rod_seal, rod_seal_qty = rod_seal_calc(bore, rod_style, options)
    piston_seal, piston_seal_qty = piston_seal_calc(bore, rod_style, options)
    rod_wiper, rod_wiper_qty = rod_wiper_calc(bore, rod_style, options)
    tube_gasket = tube_gasket_codes[bore]
    tube_gasket_qty = 2
    bushing_seal, bushing_seal_qty = bushing_seal_calc(bore, rod_style, options)
    wearband = wearband_codes[bore]
    rod_bearing, rod_bearing_qty = rod_bearing_calc(bore, rod_style, options)
    magnet_number = magnet_chart[bore] if magnet == 'E' else None
    magnet_number_qty = 2 if magnet == 'E' else 1
    retaining_ring, retaining_ring_qty = retaining_ring_calc(bore, options, rod_style)
    bumper, bumper_qty = bumper_calc(bore, options)
    tierod_nut, tierod_nut_qty = tierod_nut_calc(bore, options, mounting)
    retainer, (retainer_screw, retainer_screw_qty) = retainer_plate_calc(bore, rod_style, mounting)
    piston_bolt = piston_bolt_calc(bore, options, rod_style, cushions)
    (pivot_bushing, pivot_bushing_qty), pivot_mount, (pivot_pin, pivot_pin_qty), (pivot_ring, pivot_ring_qty) = pivot_calc(bore, mounting, options)
    (rod_spud, rod_spud_qty, rear_spud, rear_spud_qty,
     cushioning_seal, cushioning_seal_qty, cushioning_seal_2, cushioning_seal_2_qty) = cushion_spud_calc(bore, rod_style, cushions, options)
    (male_rod, (angle_mount, angle_mount_qty), angle_mount_2, spacer_plate, (trunnion_pin, trunnion_pin_qty), trunnion_screw,
     mid_trunnion, flange) = accessory_calc(bore, options, mounting, rod_style)

    if mounting == 'T8': #recalls the tie rod calculation with new parameters to fit mid-trunnion (WIP)
        tie_rod, tie_rod_qty = tie_rod_calc(bore, options, '0', mounting, 'A', rod_style, xi_num)
        tie_rod_2_qty = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style,xi_num)
        if extension: #RA01A01A
            if extension.startswith(('CR','CD')):
                if rod_style in ('1','2','3'):
                    tie_rod, tie_rod_qty = tie_rod_calc(bore, options, '0', mounting, 'A', rod_style, float(xi_num) -
                                           (int(extension[2:4]) + fractional_stroke_value[extension[4]]-c_dim[bore]))
                    tie_rod_2,tie_rod_2_qty = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style, float(xi_num) -
                                           (int(extension[2:4])+fractional_stroke_value[extension[4]]-c_dim[bore]))
                elif rod_style in ('6','7','8'):
                    tie_rod, tie_rod_qty = tie_rod_calc(bore, options, '0', mounting, 'A', rod_style, float(xi_num) -
                                           (int(extension[2:4]) + fractional_stroke_value[extension[4]]-c_dim_oversize[bore]))
                    tie_rod_2,tie_rod_2_qty = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style, float(xi_num) -
                                           (int(extension[2:4])+fractional_stroke_value[extension[4]]-c_dim_oversize[bore]))
            elif extension.startswith(('CR','CD')):
                if rod_style in ('1','2','3'):
                    tie_rod, tie_rod_qty = tie_rod_calc(bore, options, '0', mounting, 'A', rod_style, float(xi_num) -
                                           (int(extension[5:7]) + fractional_stroke_value[extension[7]]-c_dim[bore]))
                    tie_rod_2,tie_rod_2_qty = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style, float(xi_num) -
                                           (int(extension[5:7])+fractional_stroke_value[extension[7]]-c_dim[bore]))
                elif rod_style in ('6','7','8'):
                    tie_rod, tie_rod_qty = tie_rod_calc(bore, options, '0', mounting, 'A', rod_style, float(xi_num) -
                                           (int(extension[5:7]) + fractional_stroke_value[extension[7]]-c_dim_oversize[bore]))
                    tie_rod_2,tie_rod_2_qty = tie_rod_calc(bore, options, stroke, 'T8_2', fractional_stroke, rod_style, float(xi_num) -
                                           (int(extension[5:7])+fractional_stroke_value[extension[7]]-c_dim_oversize[bore]))

    if cushions != 'A': #if cushions are present, adds needle assembles and seals
        needle_seal = ''
        needle_seal_qty = 1
        adjustable_cushion_qty = 1
        adjustable_cushion = '708386' if bore in ('15','20','25') else '708392'
        if options in viton_codes:
            needle_seal = '600-100F75' if bore in ('15','20','25') else '1000-100F75'
        if cushions in ('B','C','D','E'):
            adjustable_cushion_qty = 2
            if options in viton_codes:
                needle_seal_qty = 2

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
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
                elif extension.startswith(('CR','AR')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, extension[0:2]+extension[5:8], options)
                elif extension.startswith(('AD','RA')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
                elif extension.startswith(('AC','RR')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, cushions, stroke, fractional_stroke, None, options)
            else:
                if extension.startswith(('CD','RC')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
                elif extension.startswith(('CR','AR')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, extension[0:2]+extension[5:8], options)
                elif extension.startswith(('AD','RA')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
                elif extension.startswith(('AC','RR')):
                    rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, None, options)
        elif not extension:
            if cushions in ('B', 'C', 'D', 'E'):
                rod += '  (2)'  # if double rod with no extension and cushions on both ends, use same rod
            else:
                rod_2,L1_dim_2 = piston_rod_calc(bore, rod_style, 'A', stroke, fractional_stroke, extension, options)

    bom = {
        "bore_descriptor":bore_descriptor[bore], "mounting_descriptor": mounting_descriptor[mounting],
        "whole_stroke":f'{int(stroke)}"', "fractional_stroke_identifier": f'{Fraction(fractional_stroke_value[fractional_stroke])}"',
        "rod_style_descriptor":rod_style_descriptor[rod_style],"ports_descriptor":ports_descriptor[ports],
        "cushion_descriptor": cushion_descriptor[cushions], "option_descriptor":option_code_dict.option_descriptor[options],
        "option_addition":option_code_dict.option_addition[options], "extension_descriptor": extension_descriptor,
        "magnet_descriptor":magnet_descriptor,
        "front_head": {"part_number": front_head, "quantity": 1, "description": 'FRONT HEAD'},
        "rear_cover": {"part_number": rear_cover, "quantity": 1, "description": 'REAR CAP'},
        "rod": {"part_number": rod, "quantity": 1, "description": 'PISTON ROD',"L1_dim":f'(L1={L1_dim})' if rod_style in ('1','2','6','7') else None},
        "rod_2": {"part_number": rod_2, "quantity": 1, "description": 'PISTON ROD', "L1_dim":f'(L1={L1_dim})'if rod_style in ('1','2','6','7') and rod_2 else None} if rod_2 else None,
        "piston_head": {"part_number": piston_head, "quantity": 1, "description": 'PISTON'},
        "rod_bushing": {"part_number": rod_bushing, "quantity": rod_bushing_qty, "description": 'BUSHING'},
        "cylinder_tube": {"part_number": cylinder_tube, "quantity": 1, "description": 'CYLINDER TUBE'},
        "tie_rod": {"part_number": tie_rod, "quantity": tie_rod_qty, "description": 'TIE ROD'},
        "tie_rod_2": {"part_number": tie_rod_2, "quantity": tie_rod_qty, "description": 'TIE ROD'},
        "rod_seal": {"part_number": rod_seal, "quantity": rod_seal_qty, "description": 'ROD SEAL'},
        "piston_seal": {"part_number": piston_seal, "quantity": piston_seal_qty, "description": 'PISTON SEAL'},
        "rod_wiper": {"part_number": rod_wiper, "quantity": rod_wiper_qty, "description": 'ROD WIPER'},
        "tube_gasket": {"part_number": tube_gasket, "quantity": tube_gasket_qty, "description": 'TUBE GASKET'},
        "bushing_seal": {"part_number": bushing_seal, "quantity": bushing_seal_qty, "description": 'BUSHING SEAL'},
        "wearband": {"part_number": wearband, "quantity": 1, "description": 'NFPA WEARBAND'},
        "rod_bearing": {"part_number": rod_bearing, "quantity": rod_bearing_qty, "description": 'BEARING'},
        "magnet_number": {"part_number": magnet_number, "quantity": magnet_number_qty, "description": 'MAGNETIC RING'} if magnet_number else None,
        "retaining_ring": {"part_number": retaining_ring, "quantity": retaining_ring_qty, "description": 'LOCK RING'},
        "bumper": {"part_number": bumper, "quantity": bumper_qty, "description": 'RUBBER BUMPER'} if bumper else None,
        "tierod_nut": {"part_number": tierod_nut, "quantity": tierod_nut_qty, "description": 'NUT HEX'},
        "piston_bolt": {"part_number": piston_bolt, "quantity": 1, "description": 'SOCKET HEAD CAP SCREW'},
        "pivot_bushing": {"part_number": pivot_bushing, "quantity": pivot_bushing_qty, "description": 'PIVOT BUSHING'} if pivot_bushing else None,
        "pivot_mount": {"part_number": pivot_mount, "quantity": 1, "description": 'PIVOT MOUNT PLATE'} if pivot_mount else None,
        "pivot_pin": {"part_number": pivot_pin, "quantity": pivot_pin_qty, "description": 'PIVOT PIN'} if pivot_pin else None,
        "pivot_ring": {"part_number": pivot_ring, "quantity": pivot_ring_qty, "description": 'RETAINING RING'} if pivot_ring else None,
        "rod_spud": {"part_number": rod_spud, "quantity": rod_spud_qty, "description": 'CUSHION SPUD'} if rod_spud else None,
        "adjustable_cushion": {"part_number": adjustable_cushion, "quantity": adjustable_cushion_qty, "description": 'CUSHION NEEDLE ASSEMBLY'} if adjustable_cushion else None,
        "needle_seal": {"part_number": needle_seal, "quantity": needle_seal_qty, "description": "ORING"} if needle_seal else None,
        "rear_spud": {"part_number": rear_spud, "quantity": rear_spud_qty, "description": 'CUSHION SPUD'} if rear_spud else None,
        "cushioning_seal": {"part_number": cushioning_seal, "quantity": cushioning_seal_qty, "description": 'CUSHIONING SEAL'} if cushioning_seal else None,
        "cushioning_seal_2": {"part_number": cushioning_seal_2, "quantity": cushioning_seal_2_qty, "description": 'CUSHIONING SEAL'} if cushioning_seal_2 else None,
        "male_rod": {"part_number": male_rod, "quantity": 1, "description": 'THREADED ROD STUD'} if male_rod else None,
        "angle_mount": {"part_number": angle_mount, "quantity": angle_mount_qty, "description": 'ANGLE MOUNT'},  # Returned as tuple from accessory_calc
        "angle_mount_2": {"part_number": angle_mount_2, "quantity": 1, "description": 'ANGLE MOUNT'} if angle_mount_2 else None,
        "spacer_plate": {"part_number": spacer_plate, "quantity": 1, "description": 'SPACER PLATE'} if spacer_plate else None,
        "trunnion_pin": {"part_number": trunnion_pin, "quantity": trunnion_pin_qty,"description": 'TRUNNION PIN'} if trunnion_pin else None,
        "trunnion_screw": {"part_number": trunnion_screw, "quantity": 2, "description": 'SOCKET HEAD CAP SCREW'} if trunnion_screw else None,
        "mid_trunnion": {"part_number": mid_trunnion, "quantity": 1, "description": 'MID TRUNNION MOUNT'} if mid_trunnion else None,
        "flange": {"part_number": flange, "quantity": 1, "description": 'MOUNTING FLANGE'} if flange else None,
        "retainer": {"part_number": retainer, "quantity": 1, "description": 'BUSHING RETAINER'} if retainer else None,
        "retainer_screw": {"part_number": retainer_screw, "quantity": retainer_screw_qty,"description": 'SOCKET HEAD CAP SCREW'} if retainer_screw else None
    }
    return bom
