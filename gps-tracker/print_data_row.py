def print_data_row(scheme, data):
    for i in range(len(data)):
        current_data = str(data[i])
        current_scheme = scheme[i]
        current_scheme -= len(current_data)
        current_scheme /= 2
        if current_scheme%1 == 0:
            current_data = ' '*int(current_scheme) + current_data + ' '*int(current_scheme)
        else:
            current_data = ' '+ ' '*int(current_scheme) + current_data + ' '*int(current_scheme)
        print(current_data, end='')
    print()