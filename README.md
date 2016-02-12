#FITTING WITH SIGMA CLIPPING
Sometimes when fitting a function to data you just want to do a simple and fast rejection of outliers. This module allows you to use your favourite fitting procedure with the addition of an iterative sigma clipping or min/max rejection step.

##Download

This software can be downloaded by cloning the git repository:

```bash
git clone https://github.com/sheliak/fit_sig_clip.git
```

A folder `fit_sig_clip` will be created

##Installation

A setup.py file is provided. The module can be installed in the usual way by running

```bash
cd fit_sig_clip
sudo python setup.py install 
```
This will make the `fit_sig_clip` module available system-wide.

##Usage

###Define a fitting function

###Run the clipping iterations
