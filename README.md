#FITTING WITH SIGMA CLIPPING
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

###Define a fitting function

###Run the clipping iterations
