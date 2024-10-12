from os import remove

def parse_number(number):
    number = number.split('D')
    number[0] = float(number[0]) * 10**(int(number[1]))
    return number[0]

def parse_eph():

    with open('data', 'r') as file:
        data = file.read()
    remove('data')

    data = data[648:]
    data = [data[i:i+640] for i in range(0, len(data), 640)]

    eph_json = dict()
    for i in range(33):
        prn = int(data[i][0:3].replace(' ', ''))
        eph_json.update({str(prn): []})
        d = data[i][22:].replace('   ', '').replace('\n', '')
        d = [d[x:x+19] for x in range(0, len(d), 19)]
        for elem in d:
            eph_json[str(prn)].append(parse_number(elem))

    with open('eph', 'w+') as file:
        file.write(str(eph_json).replace("'", '"'))