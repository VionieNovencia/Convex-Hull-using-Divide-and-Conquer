from hashlib import new
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn import datasets
import sys

class TailRecurseException(BaseException):
    def __init__(self,args,kwargs):
        self.args = args
        self.kwargs = kwargs
def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func

data = datasets.load_iris()
#create a dataframe
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)
print(df.shape)
df.head()

#visualisasi hasil convex Hull
#from scipy.spatial import ConvexHull
def Cari_titik_terjauh(x):
    result = [0,0]
    jarak_max = 0
    for i in range(0,len(x),1):
        for j in range(i+1,len(x),1):
            jarak1 = (x[i][0]-x[j][0])**2 + (x[i][1]-x[j][1])**2
            jarak = math.sqrt(jarak1)
            if(jarak>jarak_max):
                jarak_max = jarak
                result[0] = x[i]
                result[1] = x[j]
    return result

def bagi(x, garis):
    matrix = [[0,0,1],[0,0,1],[0,0,1]]
    garis = np.array(garis)
    ind1 = np.lexsort((garis[:,1],garis[:,0]))
    atas = []
    bawah = []
    for i in range(2):
        for j in range(2):
            matrix[i][j] = garis[ind1][i][j]
    for p in range(len(x)):
        matrix[2][0] = x[p][0]
        matrix[2][1] = x[p][1]
        det = np.linalg.det(matrix)
        if(det > 0):
            atas.append(x[p])
        elif(det<0):
            bawah.append(x[p])
    return atas,bawah

def titik_jauh_garis(garis,x):
    p1 = np.array(garis[0])
    p2 = np.array(garis[1])
    dmax = 0
    titik = [0,0]
    for i in range(len(x)):
        p3 = np.array(x[i])
        d = np.abs(np.cross(p2-p1,p1-p3)/np.linalg.norm(p2-p1))
        if (d>dmax):
            dmax = d
            titik = x[i]
    return titik

def Bagian_atas(garis, array, result):
    jarak_max = titik_jauh_garis(garis,array)
    result.append(jarak_max)
    garis = np.array(garis)
    ind1 = np.lexsort((garis[:,1],garis[:,0]))
    garis1 = [0,0]
    garis1[0] = garis[ind1][0]
    garis1[1] = jarak_max
    atas,bawah = bagi(array,garis1)
    stop1 = False
    if(stop1==False):
        if (atas == [] ):
            stop1 = True
        else:
            Bagian_atas(garis1,atas,result)
    stop2 = False
    garis2 = [0,0]
    garis2[0] = garis[ind1][1]
    garis2[1] = jarak_max
    atas,bawah = bagi(array,garis2)
    if(stop2 == False):
        if (atas == [] ):
            stop2 = False
        else:
            Bagian_atas(garis2,atas,result)

def Bagian_bawah(garis, array, result):
    jarak_max = titik_jauh_garis(garis,array)
    result.append(jarak_max)
    #print(result)
    garis = np.array(garis)
    ind1 = np.lexsort((garis[:,1],garis[:,0]))
    garis1 = [0,0]
    garis1[0] = garis[ind1][0]
    garis1[1] = jarak_max
    atas,bawah = bagi(array,garis1)
    #print(atas)
    stop1 = False
    if(stop1==False):
        if (bawah == [] ):
            stop1 = True
        else:
            Bagian_bawah(garis1,bawah,result)
    #print("________________________________")
    stop2 = False
    garis2 = [0,0]
    garis2[0] = garis[ind1][1]
    garis2[1] = jarak_max
    atas,bawah = bagi(array,garis2)
    if(stop2 == False):
        if (bawah == [] ):
            stop2 = False
        else:
            Bagian_bawah(garis2,bawah,result)

def sort_result(garis_awal,atas,bawah):
    result = []
    garis_awal = np.array(garis_awal)
    atas = np.array(atas)
    bawah = np.array(bawah)

    ind1 = np.lexsort((garis_awal[:,1],garis_awal[:,0]))
    ind2 = np.lexsort((atas[:,1],atas[:,0]))
    ind3 = np.lexsort((bawah[:,1],bawah[:,0]))

    result.append(garis_awal[ind1][0])
    for i in range(len(atas)):
        result.append(atas[ind2][i])
    result.append(garis_awal[ind1][1])
    for j in range(len(bawah),0,-1):
        result.append(bawah[ind3][j-1])
   
    return result

def optimized_result(garis_awal,result,array):
    garis_awal = np.array(garis_awal)
    ind1 = np.lexsort((garis_awal[:,1],garis_awal[:,0]))
    garis_awal = garis_awal[ind1]
    grs = [[0,0],[0,0]]
    grs[0] = garis_awal[0]
    grs[1] = result[1]
    i = 1
    while (grs[1][0] != garis_awal[1][0] and grs[1][1] != garis_awal[1][1] and i<len(result)):
        grs[1] = result[i]
        atas = []
        bawah = []
        atas,bawah = bagi(array,grs)
        print("grs",grs)
        print("atas",atas)
        print()
        print("bawah",bawah)
        if(atas == [] or bawah == []):
            grs[0] = result[i]
            i+=1
        else:
            del result[i]
    return result

plt.figure(figsize=(10,6))
colors = ['b','r','g']
plt.title ("Petal Width vs Petal Length")
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
for i in range(len(data.target_names)-1):
    bucket = df[df['Target']==i]
    bucket = bucket.iloc[:,[0,1]].values
    plt.scatter(bucket[:,0],bucket[:,1],label = data.target_names[i])
    garis_awal = Cari_titik_terjauh(bucket)
    atas,bawah = bagi(bucket,garis_awal)
    result_atas = []
    result_bawah = []
    Bagian_atas(garis_awal,atas,result_atas)
    Bagian_bawah(garis_awal,bawah,result_bawah)
    res = sort_result(garis_awal,result_atas,result_bawah)
    res = optimized_result(garis_awal,res,bucket)
    for j in range(len(res)):
        x_values = [res[j][0],res[j-1][0]]
        y_values = [res[j][1],res[j-1][1]]
        plt.plot(x_values,y_values,color = colors[i])
plt.legend()
plt.show()