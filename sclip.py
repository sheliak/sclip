import numpy as np

def sclip(p,fit,n,ye=[],sl=99999,su=99999,min=0,max=0,min_data=1,grow=0,global_mask=None,verbose=True):
	"""
	p: array of coordinate vectors. Last line in the array must be values that are fitted. The rest are coordinates.
	fit: name of the fitting function. It must have arguments x,y,ye,and mask and return an array of values of the fitted function at coordinates x
	n: number of iterations
	ye: array of errors for each point
	sl: lower limit in sigma units
	su: upper limit in sigma units
	min: number or fraction of rejected points below the fitted curve
	max: number or fraction of rejected points above the fitted curve
	min_data: minimal number of points that can still be used to make a constrained fit
	global_mask: if initial mask is given it will be used throughout the whole fitting process, but the final fit will be evaluated also in the masked points
	grow: number of points to reject around the rejected point.
	verbose: print the results or not
	"""

	nv,dim=np.shape(p)

	#if error vector is not given, assume errors are equal to 0:
	if ye==[]: ye=np.zeros(dim)
	#if a single number is given for y errors, assume it means the same error is for all points:
	if isinstance(ye, (int, long, float)): ye=np.ones(dim)*ye
	
	if global_mask==None: global_mask=np.ones(dim, dtype=bool)
	else: pass
	
	f_initial=fit(p,ye,global_mask)
	s_initial=np.std(p[-1]-f_initial)

	f=f_initial
	s=s_initial

	tmp_results=[]

	b_old=np.ones(dim, dtype=bool)

	for step in range(n):
		#check that only sigmas or only min/max are given:
		if (sl!=99999 or su!=99999) and (min!=0 or max!=0):
			raise RuntimeError('Sigmas and min/max are given. Only one can be used.')

		#if sigmas are given:
		if sl!=99999 or su!=99999:
			b=np.zeros(dim, dtype=bool)
			if sl>=99999 and su!=sl: sl=su#check if only one is given. In this case set the other to the same value
			if su>=99999 and sl!=su: su=sl

			good_values=np.where(((f-p[-1])<(sl*(s+ye))) & ((f-p[-1])>-(su*(s+ye))))#find points that pass the sigma test
			b[good_values]=True

		#if min/max are given
		if min!=0 or max!=0:
			b=np.ones(dim, dtype=bool)
			if min<1: min=dim*min#detect if min is in number of points or percentage
			if max<1: max=dim*max#detect if max is in number of points or percentage

			bad_values=np.concatenate(((p[-1]-f).argsort()[-int(max):], (p[-1]-f).argsort()[:int(min)]))
			b[bad_values]=False

		#check the grow parameter:
		if grow>=1 and nv==2:
			b_grown=np.ones(dim, dtype=bool)
			for ind,val in enumerate(b):
				if val==False:
					ind_l=ind-int(grow)
					ind_u=ind+int(grow)+1
					if ind_l<0: ind_l=0
					b_grown[ind_l:ind_u]=False

			b=b_grown

		tmp_results.append(f)

		#check that the minimal number of good points is not too low:
		if len(b[b])<min:
			step=step-1
			b=b_old
			break

		#check if the new b is the same as old one and break if yes:
		if np.array_equal(b,b_old):
			step=step-1
			break

		#fit again
		f=fit(p,ye,b&global_mask)
		s=np.std(p[-1][b]-f[b])
		b_old=b

	if verbose:
		print ''
		print 'FITTING RESULTS:'
		print 'Number of iterations requested:    ',n
		print 'Number of iterations performed:    ', step+1
		print 'Initial standard deviation:        ', s_initial
		print 'Final standard deviation:          ', s
		print 'Number of rejected points:         ',len(np.invert(b[np.invert(b)]))
		print ''
	
	return f,tmp_results,b
