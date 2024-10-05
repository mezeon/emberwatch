from PIL import Image
from math import log10

D = [1/4, 1/2, 1]
m = 1

h1 = 50
h2 = 150
h1w = 49
h2w = 60
s1w = 5
s2w = 50
v = 150
S = 100

ai1 = (19.187855, 0.000651, 0.389277, 4.821348, 1.215673, 0.483192)
ai2 = (1.156578, 0.027966, 0.013358, -0.046318, 0.025448, -0.008525)
ai3 = (-11.530798, -0.000930, 0.030359, 0.778747, -0.030386, 0.111023)

im = []
for i in range(m):
    im.append(Image.open('image_data/' + str(i) + '.png').convert('HSV'))

count = 0

L = 0
for i in range(m):
    for x in range(im[i].width):
        for y in range(im[i].height):
            (H, S, V) = im[i].getpixel((x, y))

            if not (H < h1 or H > h2):
                if not((h1w < H and H < h2w) and (s1w < S and S < s2w) and (V > v)):
                    count += 1

    P = 1 - count/(im[i].height*im[i].width)
    W = im[i].width

    A = []
    for j in range(6):
        A.append(ai1[j] + ai2[j]*(W/D[i]) + ai3[j]*log10(W/D[i]))
    
    print(P, A)
    f = (1-P)*P**(1/A[0])+(1-P**(1/A[1]))*(1-P)**(1/A[2])/(1/A[3]+A[4]*P**A[5])

    L += 2*f

L /= m

print('LAI = ' + str(round(L,2)))