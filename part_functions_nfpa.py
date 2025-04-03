import re

def split_part_number(part_number):
    pattern = r'^(F|SS)-(\d{4})([A-Z]\d{2})-(\d{2})([A-Z])(?:-(\d{1,3}))?(?:-((?:\dA\d{2}A|RT\d{2}A)))?$'

    match = re.match(pattern, part_number)
    groups = match.groups()
    part_number_new = part_number
    if not match:
        raise ValueError("Invalid round body part number format")

    return groups, part_number_new

def front_head_calc(bore,style):
    prefix = 'C6-'
    number = {'0563':'200','0750':'197-ASY','0875':'200','1062':'279-ASY','1250':'315-ASY',
              '1500':'384-ASY','1750':'404-ASY','2000':'514-ASY','2500':'544-ASY','3000':'200'}
    quantity = 1
    if bore in ('0563','0875','3000'):
        new_prefix = {'0563':'F056-','0875':'F087-','3000':'200-'}
        prefix = new_prefix[bore]
    if style in ('S01','S02'):
        number = {'0563':'220','0750':'195-ASY','0875':'220','1062':'280-ASY','1250':'314-ASY',
              '1500':'385-ASY','1750':'405-ASY','2000':'515-ASY'}
    elif style in ('N01','N02'):
        if bore == '1250':
            prefix = 'F125-'
        number = {'0563':'230','0750':'196-ASY','0875':'230','1062':'281-ASY','1250':'230',
              '1500':'386-ASY'}
    elif style == 'D05':
        number = {'0750':'198-ASY','1062':'282-ASY','1500':'387-ASY'}
    elif style == 'D06':
        new_prefix = {'0750': 'F075-', '1062': 'F106-', '1500': 'F150-'}
        prefix = new_prefix[bore]
        number = {'0750':'240','1062':'240','1500':'240'}
    elif style in ('DG1','DG2','DG4'):
        new_prefix = {'0750': 'G075-', '1062': 'G106-', '1500': 'G150-','2000':'G200'}
        prefix = new_prefix[bore]
        number = {'0750':'200','1062':'200','1500':'200'}
    front_head = prefix + number[bore]


    return front_head,quantity

def rear_cap(bore,style,options):
    prefix = 'C7'
    if style =='D01':
        number = {'0563':'100','0750':'197-ASY','0875':'100','1062':'282','1250':'328',
                  '1500':'384-ASY','1750':'404-ASY','2000':'514-ASY','2500':'544','3000':'100'}
    if style == 'D02':
        pass

def generate_bom(parsed_data):

    prefix, bore, style, stroke, fractional_stroke, options, extension = parsed_data

    front_head,front_head_qty = front_head_calc(bore,options)





    bom = {"front_head": {"part_number": front_head, "quantity": front_head_qty, "description": 'FRONT HEAD'}






           }

    return bom


