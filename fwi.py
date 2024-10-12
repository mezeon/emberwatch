from math import exp, log

# Based on Van Wagner, C.E.; Pickett, T.L. 1985. Equations and FORTRAN program for the Canadian Forest Fire Weather Index System. Canadian Forest
# Service, Ottawa, ON. Forestry Technical Report 33. 

# read input
'''n = int(input('Number of datasets: '))
T = []
H = []
W = []
R = []
month = []
day = []'''


'''daily = input('Do you want to include day of month in the results? [y/something else]: ')

if daily == 'y':
    print('Input your data in the following format: <month [1, 12]> <day> <temperature [*C]> <relative humidity [%]> <wind speed [km/h]> <rain [m]>')
else:
    print('Input your data in the following format: <month [1, 12]> <temperature [*C]> <relative humidity [%]> <wind speed [km/h]> <rain [m]>')'''

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

def FFMC(FO, H, R, T, W):

    Mo = (147.2*(101-FO))/(59.5+FO)

    if R > 0.5:
        Rf = R-0.5
        if Mo > 150:
            Mo = Mo+42.5*Rf*exp(-100.0/(251.0-Mo))*(1.0-exp(-6.93/Rf))+(0.0015*(Mo-150.0)**2)*Rf**0.5
        else:
            Mo = Mo+42.5*Rf*exp(-100.0/(251.0-Mo))*(1.0-exp(-6.93/Rf))

    if Mo > 250:
        Mo = 250

    Ed = 0.942*(H**0.679)+(11.0*exp((H-100.0)/10.0))+0.18*(21.1-T)*(1.0-1.0/exp(0.115*H))


    if Mo > Ed:
        Kd = (0.424*(1-(H/100)**1.7)+0.0694*W**0.5*(1-(H/100)**8))*0.581*exp(0.0365*T)
        M = Ed+(Mo-Ed)*10**(-Kd)
    else:
        Ew = 0.618*H**0.753+10*exp((H-100)/10)+0.18*(21.1-T)*(1-exp(-0.115*H))

        if Mo < Ew:
            K1 = 0.424*(1-((100-H)/100)**1.7)+0.0694*W**0.5*(1-((100-H)/100)**8)
            Kw = K1 * 0.581*exp(0.0365*T)
            M = Ew - (Ew - Mo)*10**(-Kw)

        if Ed >= Mo and Mo >= Ew:
            M = Mo

    F = 59.5*(250-M)/(147.2+M)

    return (round(F,1), M)


def DMC(PO, MONTH, H, R, T):

    if R > 1.5:
        Re = 0.92*R - 1.27
        Mo = 20 + exp(5.6348-PO/43.43)
        if PO <= 33:
            b = 100/(0.5+0.3*PO)
        elif PO <= 65:
            b = 14-1.3*log(PO)
        else:
            b = 6.2*log(PO)-17.2
        Mr = Mo + 1000*Re/(48.77+b*Re)
        Pr = 244.72-43.43*log(Mr-20)
        if Pr < 0:
            Pr = 0
        PO = Pr

    Les = (6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 9.0, 7.0, 6.0)
    Le = Les[MONTH - 1]

    if T < -1.1:
        T = -1.1

    K = 1.894*(T+1.1)*(100-H)*Le*10**(-6)
    P = PO + 100 * K

    return round(P,1)


def DC(DO, MONTH, R, T):

    if R > 2.8:
        Rd = 0.83*R - 1.27
        Qo = 800*exp(-DO/400)
        Qr = Qo + 3.937*Rd
        Dr = 400*log(800/Qr)
        if Dr < 0:
            Dr = 0
        DO = Dr

    Lfs = (-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6)
    Lf = Lfs[MONTH - 1]

    if T < -2.8:
        T = -2.8

    V = 0.36*(T+2.8) + Lf

    if V < 0:
        V = 0

    D = DO + 0.5*V

    return round(D, 1)

def ISI(W, M):
    fW = exp(0.05039*W)
    fF = 91.9*exp(-0.1386*M)*(1+(M**5.31)/(4.93*10**7))
    R = 0.208*fW*fF
    return round(R, 1)

def BUI(P, D):
    if P <= 0.4*D:
        U = 0.8*P*D/(P + 0.4*D)
    else:
        U = P - (1-0.8*D/(P+0.4*D))*(0.92+(0.0114*P)**1.7)
    
    return round(U, 1)

def FWI(U, R):
    if U <= 80:
        fD = 0.626*U**0.809+2
    else:
        fD = 1000/(25+108.64*exp(-0.023*U))
        
    B = 0.1*R*fD

    if B > 1:
        S = exp(2.72*(0.434*log(B))**0.647)
    else:
        S = B

    return round(S, 1)


'''for i in range(n):
    print(str(i) + ': ', end='')
    data = input()
    data = data.split(' ')
    month.append(int(data[0]))

    idx = None
    if daily == 'y':
        day.append(data[1])
        idx = 1
    else:
        idx = 0

    T.append(float(data[idx+1]))
    H.append(float(data[idx+2]))
    W.append(float(data[idx+3]))
    R.append(float(data[idx+4]))'''

# initial standard values
FO = 85 # yesterday's FFMC (Fine Fuel Moisture Code)
PO = 6.0 # yesterday's DMC (Duff Moisture Code)
DO = 15.0 # yesterdays DC (Drought Code)

# (70, 20, 828)

'''scheme = None
if daily == 'y':
    print('\n| month | - day - | - FFMC - | - DMC - | - DC - | - ISI - | - BUI - | - FWI - |')
    scheme = (8, 10, 11, 10, 9, 10, 10, 10)
else:
    print('\n| month | - FFMC - | - DMC - | - DC - | - ISI - | - BUI - | - FWI - |')
    scheme = (8, 11, 10, 9, 10, 10, 10)
'''
'''for i in range(n):
    F = FFMC(FO, H[i], R[i], T[i], W[i])
    M = F[1]
    P = DMC(PO, month[i], H[i], R[i], T[i])
    D = DC(DO, month[i], R[i], T[i])
    R_ = ISI(W[i], M)
    U = BUI(P, D)
    S = FWI(U, R_)

    if daily == 'y':
        print_data_row(scheme, (month[i], day[i], F[0], P, D, R_, U, S))
    else:
        print_data_row(scheme, (month[i], F[0], P, D, R_, U, S))

    FO = F[0]
    PO = P
    DO = D'''

def get_fwi(H, R, T, W, month): # humidity rain temperature wind month
    F = FFMC(FO, H, R, T, W)
    M = F[1]
    P = DMC(PO, month, H, R, T)
    D = DC(DO, month, R, T)
    R_ = ISI(W, M)
    U = BUI(P, D)
    S = FWI(U, R_)

    return S