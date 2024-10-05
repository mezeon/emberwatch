from ftplib import FTP
from datetime import date
import gzip
from os import remove

def get_eph():

    today = date.today()
    ftp =  FTP('gssc.esa.int')
    ftp.login()
    ftp.cwd('gnss/data/daily/' + str(today.year) +'/brdc/')

    filename = 'brdc' + str(int(today.strftime('%j'))-1) + '0.24n.gz'

    with open(filename, 'wb') as file:
        ftp.retrbinary(f'RETR {filename}', file.write)
    ftp.quit()

    with gzip.open(filename, 'rb') as file:
        data = file.read()

    remove(filename)

    with open('data', 'w+') as file:
        file.write(str(data).replace('\\n', '\n')[2:-1])