from matplotlib import *
from pylab import *
from scipy.optimize import curve_fit
import sclip
import itertools
from mpl_toolkits.mplot3d import Axes3D

################################################## 2D example ##############################################

#this is a function we want to fit
def func(x,a,b):
	return a*x+b

#this function does the fitting. The arguments here are all mandatory, but you don't actually have to use the ye. Use mask as shown here!
def myfit(p,ye,mask):
	x=p[0]
	y=p[1]
	popt,pcov = curve_fit(func,x[mask],y[mask],p0=[1,0])
	return func(x,popt[0],popt[1])

#generate some data:
x=np.array([0,1,2,3,4,5,6,7,8,9])
y=np.array([0,1.1,2.3,1,3.9,4.8,15,7.2,8.1,9.1])
ye=np.array([0,0,0,1.4,0,0,0,0,0,0])

#fit with sclip:
f,steps,mask=sclip.sclip((x,y),myfit,5,ye,sl=2,su=2,min_data=2,grow=0)

fig=figure('2D example')

#plot data points
errorbar(x,y,ye,fmt='o')

#plot the final fit
plot(x,f,'r-')

#plot rejected points
plot(x[np.invert(mask)],y[np.invert(mask)],'rx',ms=15)

#plot intermediate steps:
for y in steps:
	plot(x,y,'b-', alpha=0.3)

############################################# 3D example #########################################

#generate some data:
p=np.array([[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],[1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4],[0.7,0.8,0.6,1.1,0.8,2.9,0.8,1.1,1,1,1.2,1.4,2,2.2,2.3,2.6]])

#a function that fits a 2D polynomial
def polyfit2d(x, y, z, order=3):
	ncols = (order + 1)**2
	G = np.zeros((x.size, ncols))
	ij = itertools.product(range(order+1), range(order+1))
	for k, (i,j) in enumerate(ij):
		G[:,k] = x**i * y**j
	m, _, _, _ = np.linalg.lstsq(G, z)
	return m

#a function that evaluates the polynomial
def polyval2d(x, y, m):
	order = int(np.sqrt(len(m))) - 1
	ij = itertools.product(range(order+1), range(order+1))
	z = np.zeros_like(x)

	for a, (i,j) in zip(m, ij):
		z = z+ a * x**i * y**j
	return z

#a wrapper that sclip can use.
def wrapper(p,ye,mask):
	m=polyfit2d(p[0][mask],p[1][mask],p[2][mask],order=2)
	return polyval2d(p[0],p[1],m)

#fit
f=sclip.sclip(p,wrapper,5,ye=[],sl=2)

#plot the results
fig = plt.figure('3D example')
ax = fig.add_subplot(111, projection='3d')
ax.plot(p[0],p[1],p[2],'ko',ms=10)
ax.plot_trisurf(p[0],p[1],f[0],alpha=0.4)

show()