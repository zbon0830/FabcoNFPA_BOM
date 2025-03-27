import re, string
from faulthandler import cancel_dump_traceback_later
from selectors import SelectSelector
from fractions import Fraction
import option_code_dict
# Maps bore code to prefix
bore_descriptor = {'15': '1-1/2" Bore','20':'2" Bore','25': '2-1/2" Bore','32':'3-1/4" Bore','40': '4" Bore',
                   '50':'5" Bore','60': '6" Bore','80':'8" Bore'}

mounting_descriptor = {'X0':'No Mount','F1':'Head Rectangular Flange','F2':'Cap Rectangular Flange','P1':'Fixed Clevis',
                       'P2':'Detachable Clevis','P3':'Fixed Eye','P4':'Detachable Eye','T6':'Head Trunnion','T7':'Cap Trunnion',
                       'T8':'Mid Trunnion','X1':'Extended Tie Rods Both Ends','X2':'Cap End Extended Tie Rods','X3':'Head End Extended Tie Rods',
                       'S1':'Angle Mount','S2':'Side Lug','S4':'Bottom Tapped, Flush Mount','E3':'Head Square Mount','E4':'Cap Square Mount','SN':'Sleeve Nut',
                       'SE':'Sleeve Nut & Bottom Tapped Mount','SF':'Sleeve Nut & Bottom Tapped Mount w/Out Spacer Plate'}

bore_code = {'15':'FCQN15','20':'FCQN20','25':'FCQN25','32':'FCQN32','40':'FCQN40'}
# Maps fractional stroke letters to decimal values
fractional_stroke_value = {
    'A': 0, 'B': 0.0625, 'C': 0.125, 'D': 0.1875, 'E': 0.250,
    'F': 0.3125, 'G': 0.375, 'H': 0.4375, 'I': 0.500, 'J': 0.5625,
    'K': 0.625, 'L': 0.6875, 'M': 0.750, 'N': 0.8125, 'O': 0.875, 'P': 0.9375}

# Standard C and A dimensions
c_dim = {'15': 0.375, '20': 0.375, '25': 0.375, '32': 0.500, '40': 0.500,}
a_dim = {'15': 0.750, '20': 0.750, '25': 0.750, '32': 1.125, '40': 1.125,}
# -------------------------------
# Parsing and Calculation Functions
# -------------------------------

def split_part_number(part_number):
    part_number = part_number.upper()
    part_number = part_number.upper().replace("XO", "X0")
    part_number_new=part_number
    pattern = r"^FCQN-(11|21)-(\d{2})([A-Z]\d)-(\d{2})([A-P])(?:-([A-Z]{2}\d))?(?:-(MR))?(?:-(V))?(?:-(([A-Z]{2}\d{2}[A-P](?:\d{2}[A-P])?)))?$"
    match = re.match(pattern, part_number)
    if not match:
        raise ValueError("Part number format is invalid")
    return match.groups(),part_number_new


def body_calc(rod_type,bore):
    single_double = '1' if rod_type == '11' else '2'
    bore_prefix = {'15':'0150','20':'0200','25':'0250','32':'0325','40':'0400'}
    front_head = f"FCQN-{single_double}-{bore_prefix[bore]}-CP-M-NPT"
    return front_head

def piston_rod_calc(bore,rod_type,stroke,fractional_stroke,extension,thread_type):
    rod_prefix = ''
    rod_number = ''
    rod_adder = 0
    total_extension = 0
    if extension:
        whole_extension = int(extension[2:4])
        fractional_extension = fractional_stroke_value[extension[4]]
        if extension.startswith(('CD', 'RC', 'CR')):
                total_extension = (whole_extension + fractional_extension - c_dim[bore])
        elif extension.startswith(('AD', 'RA', 'AR')):
                total_extension = (whole_extension + fractional_extension - a_dim[bore])
        elif extension.startswith(('AC', 'RR')):
            whole_extension = int(extension[2:3]) + int(extension[5:7])
            fractional_extension = fractional_stroke_value[extension[4]] + fractional_stroke_value[extension[7]]
            total_extension = (whole_extension + fractional_extension - a_dim[bore] - c_dim[bore])
    if rod_type == '21':
        rod_prefix = '15'
    elif rod_type == '11':
        rod_prefix = '10'
    thread_map = {'CC2':'C2','FF4':'F4','KK3':'K3',None:''}
    rod = f"{bore_code}-{rod_prefix}{thread_map[thread_type]}{round((int(stroke) + fractional_stroke_value[fractional_stroke]+total_extension),3)}"
    if extension:
        if extension.startswith(('AD', 'RA', 'AR', 'AC')):
            rod_prefix = 'N15SR-' if bore in ('15','20','25') else 'N32SR-'
            if thread_type:
                if thread_type == 'CC2':
                    rod_number = '35X'
                elif thread_type == 'FF4':
                    rod = f"{bore_code}-{rod_prefix}{thread_map[thread_type]}{round((int(stroke) + fractional_stroke_value[fractional_stroke]+total_extension),3)}-{extension}"
                    return rod
            else:
                rod_number = '30X'
            if bore == '15':
                rod_adder = 3.495
            elif bore =='20':
                rod_adder = 3.515
            elif bore =='25':
                rod_adder =3.440
            elif bore == '32':
                rod_adder = 4.454
            elif bore == '40':
                rod_adder = 4.65
            rod = f'{rod_prefix}{rod_number}{rod_adder+int(stroke)+fractional_stroke_value[fractional_stroke]-a_dim[bore]}-AD{extension[2:5]}'
    return rod  # quantity defaults to 1


def tube_calc(bore,stroke,fractional_stroke):
    cylinder_tube = f"{bore_code[bore]}{round((int(stroke) + fractional_stroke_value[fractional_stroke]),3)}"
    return cylinder_tube  # quantity defaults to 1


def tie_rod_calc(rod_type,bore,stroke,mounting,fractional_stroke,):
    quantity = 4
    tie_rod_adder = 0
    tie_rod_prefix = '-7X'
    if bore == '15':
        if mounting in ('S4','F1','F2','P1','P2','S1'):
            tie_rod_prefix = 'FCQN15-7DRX' if rod_type == '21' else 'FCQN15-7X'
            tie_rod_adder = 2.625 if rod_type == '11' else 2.820
        elif mounting == 'T4':
            tie_rod_adder = 1.335 if rod_type == '11' else 1.335
            quantity = 8 if rod_type == '21' else 4
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN15-7WRX'
            tie_rod_adder = 4.125
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN15-7WFX' if rod_type == '11' else 'FCQN15-7WRX'
            tie_rod_adder = 4.500 if rod_type == '11' else 4.655
        elif mounting == 'T4_2':
            tie_rod_prefix = 'FCQN15-7TRX'
            tie_rod_adder = 1.187
            quantity = 4
    elif bore == '20':
        if mounting in ('S4','F1','F2','P1','P2','S1'):
            tie_rod_prefix = 'FCQN20-7DRX' if rod_type == '21' else 'FCQN20-7X'
            tie_rod_adder = 2.625 if rod_type == '11' else 2.820
        elif mounting == 'T4':
            tie_rod_prefix = 'FCQN20-7TFX'
            tie_rod_adder = 1.345 if rod_type == '11' else 1.335
            quantity = 8 if rod_type == '21' else 4
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN20-7WRX'
            tie_rod_adder = 4.250
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN20-7WFX' if rod_type == '11' else 'FCQN20-7DWFX'
            tie_rod_adder = 4.625 if rod_type == '11' else 4.820
        elif mounting == 'T4_2':
            tie_rod_prefix = 'FCQN20-7TRX'
            tie_rod_adder = 1.155
            quantity = 4
    elif bore == '25':
        if mounting in ('S4','F1','F2','P1','P2','S1'):
            tie_rod_prefix = 'FCQN25-7DRX' if rod_type == '21' else 'FCQN25-7X'
            tie_rod_adder = 2.750 if rod_type == '11' else 2.980
        elif mounting == 'T4':
            tie_rod_prefix = 'FCQN25-7TFX'
            tie_rod_adder = 1.425 if rod_type == '11' else 1.425
            quantity = 8 if rod_type == '21' else 4
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN25-7WRX'
            tie_rod_adder = 4.375
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN25-7WFX' if rod_type == '11' else 'FCQN25-7DWFX'
            tie_rod_adder = 4.625 if rod_type == '11' else 4.980
        elif mounting == 'T4_2':
            tie_rod_prefix = 'FCQN25-7TRX'
            tie_rod_adder = 1.200
            quantity = 4
    elif bore in ('32', '40'):
        if mounting in ('S4','F1','F2','P1','P2','S1'):
            tie_rod_prefix = 'FCQN32-7DRX' if rod_type == '21' else 'FCQN32-7X'
            tie_rod_adder = 3.000 if rod_type == '11' else 3.390
        elif mounting == 'T4':
            tie_rod_prefix = 'FCQN32-7TFX'
            tie_rod_adder = 1.640 if rod_type == '11' else 1.640
            quantity = 8 if rod_type == '21' else 4
        elif mounting == 'X2':
            tie_rod_prefix = 'FCQN32-7WRX'
            tie_rod_adder = 5.000
        elif mounting == 'X3':
            tie_rod_prefix = 'FCQN32-7WFX' if rod_type == '11' else 'FCQN32-7DWFX'
            tie_rod_adder = 5.625 if rod_type == '11' else 6.015
        elif mounting == 'T4_2':
            tie_rod_prefix = 'FCQN32-7TRX'
            tie_rod_adder = 1.235
            quantity = 4
    if mounting in ('T4','T4_2'):
        tie_rod_length = tie_rod_adder + ((int(stroke) + fractional_stroke_value[fractional_stroke])/2)
    else:
        tie_rod_length = tie_rod_adder + int(stroke) + fractional_stroke_value[fractional_stroke]
    tie_rod = f"{tie_rod_prefix}{tie_rod_length:.3f}"
    return tie_rod, quantity


def accessory_calc(bore, options, mounting, rod_style):
    return ''


def generate_bom(parsed_data):
    """
    Given the parsed NFPA part number data, calculates all BOM parts and returns
    a dictionary where each part is represented as a dictionary with separate
    keys for 'part_number' and 'quantity'.
    """

    (rod_type,bore,mounting,stroke,fractional_stroke,thread_type,male_rod,viton,extension) = parsed_data

    body = body_calc(rod_type,bore)
    rod = piston_rod_calc(bore,rod_type, stroke, fractional_stroke, extension, thread_type)
    rod_2 = None
    cylinder_tube = tube_calc(bore, stroke, fractional_stroke)
    tie_rod, tie_rod_qry = tie_rod_calc(rod_type, bore, stroke, mounting, fractional_stroke)
    tie_rod_2 = None
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


    bom = {
        "body": {"part_number":body, "quantity": 1, "description": 'FRONT HEAD'},
        "cylinder_tube": {"part_number": cylinder_tube, "quantity": 1, "description": 'CYLINDER TUBE'},
        "tie_rod": {"part_number":tie_rod, "quantity": tie_rod_qty, "description": 'TIE ROD'},
        "tie_rod_2": {"part_number": tie_rod_2, "quantity": tie_rod_qty, "description": 'TIE ROD'},
    }
    return bom
