import re
def split_part_number(part_number):
    pattern = r"^(\d{2})([A-Z0-9]{2})-?(\d{2}A)(\d)([A-Z]{2})-?([A-Z]{2})([A-Z])(?:-?([A-Z]{2}\d{2}[A-Z]))?$"
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
    if extension:
        print(f'Extension: {extension}')

def front_head_calc():
    bore_code = {'15':'N15','20':'N20','25':'N25','32':'N32',
                 '40':'N40','50':'N50','60':'N60','80':'N80'}
    front_head = bore_code[bore] + '-'
    if rod_style == '6' or rod_style == '7' or rod_style == '8':
        block_code = {'X0':'205','F1':'205','F2':'200' }
    else:
        block_code = {'X0':'200','F1':'200','F2':'200'}
    front_head += block_code.get(mounting, 'ERROR')
    return front_head

def print_BOM():
    print('\nMATERIAL LIST:')
    print(front_head_calc())

part_number = input('Please enter NFPA part number: ')
bore, mounting, stroke, rod_style, port_cush, options, magnet, extension = split_part_number(part_number)
cylinder_specs()
print_BOM()
