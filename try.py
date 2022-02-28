import math
awal = [[7,7],[9,2],[1,4],[3,5],[6,5],[6,9],[9,9],[3,8],[6,2],[10,4],[11,7]]
print(awal)
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

def bagi(x,garis,atas,bawah,gradien):
    a = garis[1][1]-garis[0][1]
    b = garis[0][0]-garis[1][0]
    c = garis[0][1]*garis[1][0] - garis[0][0]*garis[1][1]
    
    for i in range(len(x)):
        d = a*x[i][0] + b*x[i][1] + c
        if(gradien>0 or a==0):
            if(d<0):
                 atas.append(x[i])
            elif(d>0):
                bawah.append(x[i])
        elif(gradien <0 or b==0):
            if(d<0):
                 bawah.append(x[i])
            elif(d>0):
                atas.append(x[i])


def jarak_titik_garis(x1,y1,a,b,c):
    res = abs((a*x1+b*y1+c))/(math.sqrt(a*a+b*b))
    return res

def jarak_terjauh(array, garis):
    if (len(array)==1):
        return array[0]
    else:
        a = garis[1][1]-garis[0][1]
        b = garis[0][0]-garis[1][0]
        c = garis[0][1]*garis[1][0] - garis[0][0]*garis[1][1]
        jarak_max = 0
        titik = [0,0]
        for i in range(len(array)):
            jarak = jarak_titik_garis(array[i][0],array[i][1],a,b,c)
            if(jarak > jarak_max):
                jarak_max = jarak
                titik = array[i]
        return titik
    

#gradien utama True = >   
def Bagian_atas(array, garis, result):
    #print()
    stop1 = False
    stop2 = False
    while(stop1 == False or stop2 == False):
        #print(result)

        garis1 = [0,0]
        while(stop1 == False):
            jarak_max = jarak_terjauh(array,garis)
            result.append(jarak_max)
            garis1[0] = garis[0]
            garis1[1] = jarak_max
            if(garis1[0][0] - garis1[1][0] == 0 or garis1[0][1]-garis1[1][1]==0):
                gradien1 = 0
            else:
                gradien1 = (garis1[0][1]-garis1[1][1]) / (garis1[0][0] - garis1[1][0])
            print("garis1,gradien1",garis1,gradien1)
            atas = []
            bawah = []
            bagi(array,garis1,atas,bawah,gradien1)
            print(atas)
            if (atas == []):
                stop1 = True
            else:
                array = []
                garis = []
                for i in range(len(atas)):
                    array.append(atas[i])
                for j in range(2):
                    garis.append(garis1[j]) 
                break
            print("________________________________")
    
        garis2 = [0,0]
        while(stop2==False):
            jarak_max = jarak_terjauh(array,garis)
            result.append(jarak_max)
            garis2[0] = garis[1]
            garis2[1] = jarak_max
            if(garis2[0][0] - garis2[1][0] == 0 or garis2[0][1]-garis2[1][1]==0):
                gradien2 = 0
            else:
                gradien2 = (garis2[0][1]-garis2[1][1]) / (garis2[0][0] - garis2[1][0])
            print("garis2,gradien2",garis2,gradien2)
            atas = []
            bawah = []
            bagi(array,garis2,atas,bawah,gradien2)
            print(atas)
            if (atas == []):
                stop2 = True
            else:
                array = []
                garis = []
                for i in range(len(atas)):
                    array.append(atas[i])
                for j in range(2):
                    garis.append(garis2[j]) 
                break

def Bagian_bawah(array, garis, result,count):
    #print()
    jarak_max = jarak_terjauh(array,garis)
    result.append(jarak_max)
    #print(result)
    count+=1
    print(count)

    garis1 = [0,0]
    garis1[0] = garis[0]
    garis1[1] = jarak_max
    try:
        gradien1 = (garis1[0][1]-garis1[1][1]) / (garis1[0][0] - garis1[1][0])
    except:
        gradien1 = 0
    #print("garis1,gradien1",garis1,gradien1)
    atas = []
    bawah = []
    bagi(array,garis1,atas,bawah,gradien1)
    #print(atas)
    stop1 = False
    if(stop1==False):
        if (atas == []):
            stop1 = True
        else:
            Bagian_bawah(atas,garis1,result,count)
    #print("________________________________")
    stop2 = False
    garis2 = [0,0]
    garis2[0] = garis[1]
    garis2[1] = jarak_max
    try: 
        gradien2 = (garis2[0][1]-garis2[1][1]) / (garis2[0][0] - garis2[1][0])
    except: 
        gradien2 = 0
    #print("garis2,gradien2",garis2,gradien2)
    atas = []
    bawah = []
    bagi(array,garis2,atas,bawah,gradien2)
    #print(atas)
    if(stop2 == False):
        if (atas == []):
            stop2 = False
        else:
            Bagian_bawah(atas,garis2,result,count)

def main(x):
    garis_awal = Cari_titik_terjauh(x)
    gradien = (garis_awal[0][1]-garis_awal[1][1]) / (garis_awal[0][0] - garis_awal[1][0])
    result = [0,0]
    result[0] = garis_awal[0]
    result[1] = garis_awal[1]
    result_atas = []
    result_bawah= []
    atas = []
    bawah = []
    count = 0
    bagi(x,garis_awal,atas,bawah,gradien)
    Bagian_atas(atas,garis_awal,result_atas)
    print("res",result_atas)
    Bagian_bawah(bawah,garis_awal,result_bawah,count)
    print(result_bawah)
    print(count)
main(awal)