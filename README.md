#FITTIN' WITH SIGMA CLIPPIN'
Sometimes when fitting a function to data you just want to do a simple and fast rejection of outliers. This module allows you to use your favourite fitting procedure with the addition of an iterative sigma clipping or min/max rejection step.

##Download

This software can be downloaded by cloning the git repository:

```bash
git clone https://github.com/sheliak/sclip.git
```

A folder `sclip` will be created

##Installation

A setup.py file is provided. The module can be installed in the usual way by running

```bash
cd sclip
sudo python setup.py install 
```
This will make the `sclip` module available system-wide.

##Usage

See `examples.py` or keep reading.

###Define a fitting function

You can use any function for fitting data you want. Just write a small wraper around it, so the input and output will be managable by sclip. Example:

```python
def fit(x,y,ye,mask):
	popt,pcov = curve_fit(func,x[mask],y[mask],p0=[1,0])
	return func(x,popt[0],popt[1])
```
The input parameters are:
`x` and `y` are two arrays containing the coordinates of data points,
`ye` is the array of errors in the y coordinates.
`mask` is a binary mask, so only a subsample of the data can be fitted.

The output is only one array of the fitted function values at coordinates `x`.

###Run the clipping iterations

###Get fitted parameters
`sclip` returns the final mask, so you can run your fitting function on the optimal subsample. Get whatever you need from the fiting function this time. 


