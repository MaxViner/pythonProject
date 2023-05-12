import math

n=8
ygl=[104.75,105.16,108.75,112.08,92.66,92.41,88.83,91.58,109.33,98.5]

ygR=[]
for i in range(0, ygl.length):
    ygR.add(ygl[i]* 180/math.pi)

R=[46, 50, 54, 52, 58, 52, 46, 40, 34, 26]

kurs=274.2
kursR=180/math.pi*kurs

Yg_dif_kur=[]
for i in range(0,n):
    Yg_dif_kur.add(ygR[i]-kursR)

CosYdC=[]
SynYdC=[]
for i in range(0,n):
    CosYdC[i]=math.cos(Yg_dif_kur)
    SynYdC[i]=math.sin((Yg_dif_kur))

