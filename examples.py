from matplotlib import *
from pylab import *
from scipy.optimize import curve_fit
import sclip

#this is a function we want to fit
def func(x,a,b):
	return a*x+b

#this function does the fitting. The arguments here are all mandatory, but you don't actually have to use the ye. Use mask as shown here!
def fit(x,y,ye,mask):
	popt,pcov = curve_fit(func,x[mask],y[mask],p0=[1,0])
	return func(x,popt[0],popt[1])

#generate some data:
x=np.array([0,1,2,3,4,5,6,7,8,9])
y=np.array([0,1.1,2.3,1,3.9,4.8,15,7.2,8.1,9.1])
ye=np.array([0,0,0,1.4,0,0,0,0,0,0])

#fit with sclip:
f,steps,mask=sclip.sclip(x,y,fit,5,ye,sl=2,su=2,min_data=2,grow=0)

fig=figure(0)

#plot data points
errorbar(x,y,ye,fmt='o')

#plot the final fit
plot(x,f,'r-')

#plot rejected points
plot(x[np.invert(mask)],y[np.invert(mask)],'rx',ms=15)

#plot intermediate steps:
for y in steps:
	plot(x,y,'b-', alpha=0.3)

show()