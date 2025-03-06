import re
def split_part_number(part_number):
    pattern = r"^(\d{2})(P\d)-?(\d{2}A)(\d)([A-Z]{2})-?([A-Z]{2})([A-Z])$"
    match = re.match(pattern, part_number)

    if not match:
        raise ValueError("Part number format is invalid")

    return match.groups()

def cylinder_specs():
    print(f'Bore Size: {bore}')
    print(f'Mounting Style: {mounting}')
    print(f'Stroke: {stroke}')
    print(f'Rod Style: {rod_style}')
    print(f'Port and Cushion: {port_cush}')
    print(f'Option Code: {options}')
    print(f'Magnet: {magnet}')

def front_head_calc():
    front_head = []
    bore_code = {'15':'N15','20':'N20','25':'N25','32':'N32',
                 '40':'N40','50':'N50','60':'N60','80':'N80'}
    front_head.append(bore_code[bore])
    if rod_style == '6' or rod_style == '7' or rod_style == '8':
        block_code = {'XO': }
    else:
        block_code = {'XO': }
    front_head.append()

BOM_List=[]



part_number = input('Please enter NFPA part number: ')
bore, mounting, stroke, rod_style, port_cush, options, magnet = split_part_number(part_number) #identify components


