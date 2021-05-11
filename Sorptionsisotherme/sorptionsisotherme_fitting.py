from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import least_squares
import numpy as np

def appr(rF,b,c):
    w = c*(b-1)*np.array(rF/100)/(b-np.array(rF/100))
    return w

# def appr(rF,b):
#     wf1   = 274.175
#     w = wf1*(b-1)*np.array(rF/100)/(b-np.array(rF/100))
#     return w

#Reading datapoints
rF, mH2o = np.genfromtxt('Sorptionsisotherme_3DF.csv', delimiter=';',skip_header=1, unpack=True)
mH2o = mH2o/100*1833 #in [kg/m³]
mH2o_ad = mH2o[:21]
mH2o_de = mH2o[19:]
rF_ad = rF[:21]
rF_de = rF[19:]

#Approximation Feuchtespeicherung

b1_ad = 1.07034
#b2_ad = 1.10821
b1_de = 1.10251
#b2_de = 1.16850
wf1   = 274.175
#wf2   = 203.1886

w1_ad = wf1*(b1_ad-1)*np.array(rF_ad/100)/(b1_ad-np.array(rF_ad/100))
#w2_ad = wf2*(b2_ad-1)*np.array(rF_ad/100)/(b2_ad-np.array(rF_ad/100))
w1_de = wf1*(b1_de-1)*np.array(rF_de/100)/(b1_de-np.array(rF_de/100))
#w2_ad = wf2*(b2_de-1)*np.array(rF_de/100)/(b2_ad-np.array(rF_de/100))

#optimization of b with scipy
popt_ad, pcov_ad = curve_fit(appr, rF_ad,mH2o_ad,p0=[1.1,20])
popt_de, pcov_de = curve_fit(appr, rF_de,mH2o_de,p0=[1.1,20])
#poptExp, pcovExp = curve_fit(appr_exp, rF_ad,mH2o_ad,p0=[1.1,1.1])
#npFit = np.polyfit(rF_ad,mH2o_ad,2)
#npFitArray = npFit[0]*rF_ad**2+npFit[1]*rF_ad+npFit[2]


plt.figure()
plt.title("Feuchtespeicherfunktion 3DF")
plt.xlabel("relative Luftfeuchte [%]")
plt.ylabel("Wassermenge [M.%]")
plt.scatter(rF_ad,mH2o_ad,c="g",label="Adsorption und Desorption")
plt.scatter(rF_de,mH2o_de,c="g")
plt.plot(rF_ad,mH2o_ad,c="g")
plt.plot(rF_de,mH2o_de,c="g")

plt.plot(rF_ad, w1_ad,c='b', label="Approximation Adsorption und Desorption")
plt.plot(rF_de, w1_de,c='b')

#Plotting scipy opt results
print(popt_ad)
print(popt_de)
plt.plot(rF_ad,appr(rF_ad,*popt_ad),c="r",label="curve_fit_ad")
plt.plot(rF_de,appr(rF_de,*popt_de),c="r",label="curve_fit_de")
#plt.plot(rF_ad,appr_exp(rF_ad,*poptExp),c="y",label="curve_fit_exp")
#plt.plot(rF_ad,npFitArray,c="c",label="npPolyfit")
plt.legend()
plt.tight_layout()
plt.show()