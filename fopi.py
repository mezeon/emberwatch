from math import exp, log

c_vod = {'a': 0.6, 'b': 3.1, 'v0': 0.6, 'f0': 5.5}
c_lai = {'a': 0.7, 'b': 9.8, 'v0': 0.7, 'f0': 12.6}

def get_fopi_vod(v, f):
    f = log(f)
    fopi = (exp((v-c_vod['v0'])/c_vod['a']))**4*(exp((f-c_vod['f0'])/c_vod['b']))**4
    return round(fopi*100,2)

def get_fopi_lai(v, f):
    f = log(f)
    fopi = (exp((v-c_lai['v0'])/c_lai['a']))**4*(exp((f-c_lai['f0'])/c_lai['b']))**4
    return round(fopi*10,2)