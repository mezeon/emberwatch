import get_eph
import parse_eph
import calc_pos
from print_data_row import print_data_row

def main():

    # WAŻNE - WSPÓŁRZĘDNE GEOGRAFICZNE OBSERWATORA - DO EDYCJI (53.0144434, 18.4394129 - Toruń)
    lat = 52+13/60+56/3600
    lon = 21+30/3600

    get_eph.get_eph()
    parse_eph.parse_eph()
    calc_pos.calc_pos(lat, lon)

if __name__ == '__main__':
    main()