from math import exp, log

model = int(input('Select model: 1 - VOD+BA, 2 - LAI+BA: '))

constants_models = ({'a': 0.6, 'b': 3.1, 'v0': 0.6, 'f0': 5.5}, {'a': 0.7, 'b': 9.8, 'v0': 0.7, 'f0': 12.6})
c = constants_models[model-1]

v = float(input('Enter v parameter (VOD or LAI): '))
f = float(input('Enter FWI: '))
f = log(f)

fopi = (exp((v-c['v0'])/c['a']))*(exp((f-c['f0'])/c['b']))

print('FOPI is', str(round(fopi*100, 1))+'%')