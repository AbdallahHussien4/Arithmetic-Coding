import numpy as np 
import cv2
import math


#get the image directory and block size from the user
image = input("Enter image directory : ") 
ex ='.'+ input("Enter image Extention (jpg,png,..) : ") 
image2=image+ex
BS = int(input("Enter Block Size :"))
dat = input("Enter Data Type (float16 ,float32,..) :")
Width = int(input("Enter the width of the image :"))
Height = int(input("Enter the height of the image :"))

# Load an color image in grayscale
img = cv2.imread(image2,0)

#Flatten the image into vector
arr=np.array(img)
FlattenImg=arr.flatten()         

#Handle the last few elements
if(len(FlattenImg)%BS==0):
    EncSize=len(FlattenImg)/BS
    b=1
else:
    b=0
    EncSize=int(len(FlattenImg)/BS)+1   
    for i in range(BS-len(FlattenImg)%BS):
        FlattenImg= np.append(FlattenImg, 300)

#Calculate the probability of each grayscale
Prob={}
Proba=[]
for item in FlattenImg:
    if(item in Prob):
       Prob[item] +=1
    else:
       Prob[item]=1
i=0       
for item in Prob:
    Prob[item]/=len(FlattenImg)
    Proba=np.append(Proba,Prob[item]) 
    i+=1   

#Construct Range dictionary
Range=Proba
for i in range(1,len(Range)):
    Range[i]+=Range[i-1]
Ranges=Prob
i=0
Range = Range.astype(dat) 
for item in Ranges:
    Ranges[item]=Range[i]
    i+=1
 
#Decimal to Binary Converter
def decimal2binary(num):
    t="0."
    while num > 0:
        if num<0.5:
            t+='0'
            num*=2
        if num >= 0.5:
            t+='1'
            num= 2*num -1
    return float(t) 

#Encoding
Enc =np.array([])
TempData = np.array([])
TempProb = np.array([])
for i in range(0,len(FlattenImg),BS):
    TempData= FlattenImg[i:i+BS]
    oL = L = 0
    oH = H = 1
    for item in TempData:
        w = oH-oL
        i=np.where(Range==Ranges[item])[0][0]
        if i==0:
            L = oL 
        else:
            L = oL + w*Range[i-1]
        H = oL + w*Range[i]  
        oL = L
        oH = H
    t = (L+H)/2.0
   # t = decimal2binary(t)
    Enc=np.append(Enc,t)
Enc = Enc.astype(dat)    
np.save(image+str(BS)+'Enc',Enc)

#Decoding
Enc=np.load(image+str(BS)+'Enc.npy','r')
Dec = np.array([])
for item in Enc:
    TempData= item
    oL = L = 0
    oH = H = 1
    for i in range(BS):
        w = oH-oL
        for j in range(len(Range)):
            if TempData<=oL+w*Range[j]:
                for k in Ranges:
                    if Ranges[k]==Range[j]:
                        V=k
                        break        
                if V!=300:        
                    Dec=np.append(Dec,V)
                else:
                    break    
                if j==0:
                    L = oL 
                else:
                    L = oL + w*Range[j-1]
                H = oL + w*Range[j]  
                oL = L
                oH = H
                break
if(b==0):             
    for i in range(BS-(Width*Height)%BS):
        Dec=np.delete(Dec,-1)                
Dec=np.reshape(Dec, (Width, Height),order='F')
Dec=Dec.T  
     
#ٍSave the image .
cv2.imwrite(image+str(BS)+'Out'+ex, Dec)