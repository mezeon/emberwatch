from gps_tracker.get_eph import get_eph
from gps_tracker.parse_eph import parse_eph
from gps_tracker.calc_pos import calc_pos
from fwi import get_fwi
from lai import get_lai
from fopi import get_fopi_lai, get_fopi_vod
from math import sin, sqrt, log10, log, radians, exp

h0 = 1 # wysokość cansata nad ziemią w km

# sekcja informacji VOD
P0 = 4.7 # moc odbierana z góry
P = 0.5 # moc odbierana z dołu
PRN = '25' # PRN satelity GPS, którego sygnał odbieramy

# sekcja informacji FWI
hum = 10
rain = 0
temp = 30
wind = 10
month = 10

# sekcja informacji LAI
m = 3 # liczba zdjęć
D = (1, 2, 4) # wielkość liścia w px danego zdjęcia

# współrzędne geogarficzne obserwatora (53.0144434, 18.4394129 - Toruń)
lat = 53.0144434
lon = 18.4394129

def main():
    # poniższe dwa służą do pobrania i sparsowania efemeryd gps, cansat nie będzie tego robił, warto mu po prostu wrzucić do pamięci plik ./gps_tracker/eph
    #get_eph()
    #parse_eph()

    data = calc_pos(lat, lon)

    h = data[PRN]['h']
    Rr = h0/sin(radians(h))
    Rt = data[PRN]['r']

    T = sqrt((Rr + Rt)**2*P/(Rt**2*P0)) # przy założeniu, że promieniowanie całkowicie się od ziemi odbija
    vod = -log(T)*sin(radians(h))
    
    fwi = get_fwi(hum, rain, temp, wind, month)
    
    lai = get_lai(m, D) # WAŻNE - nie mam pojęcia, jak oni normalizują to LAI

    fopi_lai = get_fopi_lai(lai, fwi)
    fopi_vod = get_fopi_vod(vod, fwi)

    print(fopi_lai, fopi_vod)
    

if __name__ == '__main__':
    main()