#FITTIN' WITH SIGMA CLIPPIN'
Sometimes when fitting a function to data you just want to do a simple and fast rejection of outliers. This module allows you to use your favourite fitting procedure with the addition of an iterative sigma clipping or min/max rejection step. Fitting in any number of dimensions can be used, but errorbars can only be used in one of the dimensions.

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
def fit(p,ye,mask):
	x=p[0]
	y=p[1]
	popt,pcov = curve_fit(func,x[mask],y[mask],p0=[1,0])
	return func(x,popt[0],popt[1])
```
The input parameters are:
* `p` is the array of points. It must be at least two dimensional, where each row contains coordinates in one dimension.
* `ye` is the array of errors for the last line in the `p` array.
* `mask` is a binary mask, so only a subsample of the data can be fitted.

The output is only one array of the fitted function values at coordinates given in `p`.

###Run the clipping iterations

With the fitting function defined, you can run it with sigma clipping iterations by:
```python
fitted,int_steps,mask=sclip.sclip(p,fit,5,ye,sl=2)
```

The mandatory input parameters are:
* `p` is the array of points. It must be at least two dimensional, where each row contains coordinates in one dimension.
* `fit` is the name of the fitting function.
* `n` is the number of iterations. The number of performed iterations can be smaller, if convergence is reached or if minimum number of acceptable points is reached.

Other parameters are:
* `ye` array with errors for the last line in the `p` array.
* `sl` lower rejection limit in sigma units.
* `su` upper rejection limit in sigma units. If only one of the `sl` or `su` is given, the other one will be assumed to be the same.
* `min` is the number or fraction of rejected points below the fitted curve. A value less than 1 means fraction, 1 or more means number of points. Points furthest away from the curve will be rejected regardles their errors.
* `max` is the number or fraction of rejected points above the fitted curve. A value less than 1 means fraction, 1 or more means number of points. Points furthest away from the curve will be rejected regardles their errors. If only one of the `min` or `max` is given, the other one will be assumed to be the same.
* `min_data` is the minimal number of points that can remain unrejected. It is up to the user to provide the right value, as it depends on the fitted function.
* `global_mask` is a bool array of the same dimension as the input data. False values in the mask mark the points that should never be used in the fitting, but the final fit will be evaluated in them.
* `grow` is the number of nearby points to reject. If set to 1, for example, first point to the left and to the right of the rejected point will be rejected as well. This option can only be used for 2 dimensional data for now.
* `verbose` can be set to True or False. If True, a short summary will be printed after the last iteration.

Returned parameters are:
* Final values of the fitted function at coordinates given in `p`.
* An array of values of the fitted function at coordinates given in `p` after each iteration.
* The final mask. Accepted points have value True.

###Get fitted parameters
`sclip` returns the final mask, so you can run your fitting function on the optimal subsample. Get whatever you need from the fiting function this time. 
