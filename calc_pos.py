from time import time
from datetime import datetime
from json import loads
from math import sqrt, sin, cos, asin, pi, degrees, radians, atan2
def get_epoch():
    now = datetime.now()
    return int(now.strftime('%w'))*86400 + time()%86400


'''def print_data_row(scheme, data):
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
    print()'''

#scheme = (6, 8, 8, 8)
data = dict()
#print('| PRN | - h - | - A - | - r - |')
def calc_pos(lat, lon):
    with open('eph') as file:
        ephs = file.read()

    ephs = loads(ephs)

    ro = 6356752.314245/sqrt(1-((1-6356752.314245**2/6378137.0**2)**2*cos(radians(lat))**2))
    mu = 3.986005e14
    for eph in ephs:
        e = ephs[eph]
        try: t = get_epoch() - e[11]
        except: continue
        a = e[10]**2
        n = sqrt(mu/a**3) + e[5]
        M = e[6] + n*t
        ec = e[8]

        E = M
        for i in range(100):
            E_new = M+ec*sin(E)   
            if abs(E_new - E) < 0.000001:
                break
            E = E_new
        
        u = atan2((sqrt(1-ec**2)*sin(E)),(cos(E)-ec)) + e[17]
        
        sin2u = sin(2*u)
        cos2u = cos(2*u)

        du = e[9]*sin2u + e[7]*cos2u
        dr = e[4]*sin2u + e[16]*cos2u
        di = e[14]*sin2u + e[12]*cos2u + e[19]*t
        
        u += du
        r = a*(1-ec*cos(E)) + dr
        i = e[15] + di

        zeta = r*cos(u)
        eta = r*sin(u)
        omega = e[13] + (e[18] - 7.2921151467e-5)*t - 7.2921151467e-5*e[11]

        x = zeta*cos(omega) - eta*cos(i)*sin(omega) - ro*sin(radians(lat))*cos(radians(lon))
        y = zeta*sin(omega) + eta*cos(i)*cos(omega) - ro*sin(radians(lat))*sin(radians(lon))
        z = eta*sin(i) - ro*cos(radians(lat))
        r_ = sqrt(x**2+y**2+z**2)
        
        phi = asin(z/r)
        lambda_ = atan2(y,x)
    
        #if lambda_ < 0: lambda_ += 2*pi

        H = (-radians(lon) + lambda_)

        h = asin(cos(H)*cos(phi)*cos(radians(lat))+sin(phi)*sin(radians(lat)))
        cos_A = -(sin(phi) - sin(h) * sin(radians(lat))) / (cos(h) * cos(radians(lat)))
        sin_A = cos(phi) * sin(H) / cos(h)
        A = atan2(sin_A, cos_A)
        if A < 0: 
            A += pi*2

        #print_data_row(scheme, (eph, round(degrees(phi),1), round(degrees(lambda_),1), round(r_/1000)))
        #print_data_row(scheme, (eph, round(degrees(h),1), round(degrees(A),1), round(r_/1000)))
        data.update({eph: {'h': round(degrees(h),1), 'A': round(degrees(A),1), 'r': round(r_/1000)}})
    return data