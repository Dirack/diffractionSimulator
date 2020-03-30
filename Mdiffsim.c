/* Version 1.0 - Generate diffraction simulated hyperbolas in the stacked section
 
Programer: Rodolfo A. C. Neves (Dirack) 14/03/2020

Email:  rodolfo_profissional@hotmail.com 

License: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt>. 

*/

#include <stdio.h>
#include <stdlib.h>
#include <rsf.h>
#include <math.h>
#include "ricker.h"

int main(int argc, char* argv[])
{

	float* pm0; // picked m0's in the stacked section
	float* pt0; // picked t0's in the stacked section
	float* v; // picked velocity for m0's and t0's
	float** stackedSection; // stacked section A(t0,m0)
	float aperture; // simulated hyperbolas aperture
	int nt0; // number of t0's in stacked section
	float dt0; // t0 axis sampling
	float ot0; // t0 axis origin
	int nm0; // number of m0's in stacked section
	float dm0; // m0 axis sampling
	float om0; // m0 axis origin
	bool verb; // verbose parameter
	int im0; // center hyperbola index
	int it0; // center hyperbola index
	float m0; // center hyperbola m0 coordinate
	float t0; // center hyperbola t0 coordinate
	int ntraces; // aperture in number of traces
	float m; // CMP coordinate of a hyperbola sample
	float t; // time coordinate of a hyperbola sample
	int it; // time index coordinate of a hyperbola sample
	int i; // loop counter
	int j; // loop counter
	int k; // loop counter
	int nv; // Number of diffraction hyperbolas velocities
	int npt0; // Number of picked t0's
	int npm0; // Number of picked m0's
	float* ricker; // Generated ricker waveleti
	float freq; // Max frequency of ricker wavelet

	/* RSF files I/O */
	sf_file in, out, v_file, pt0_file, pm0_file;

	/* RSF files axis */

	sf_init(argc,argv);

	in = sf_input("in");
	pt0_file = sf_input("t0");
	pm0_file = sf_input("m0");
	v_file = sf_input("v");
	out = sf_output("out");

	/* Read stacked section geometry */
	if(!sf_histint(in,"n1",&nt0)) sf_error("No n1= in input");
	if(!sf_histfloat(in,"o1",&ot0)) sf_error("No o1= in input");
	if(!sf_histfloat(in,"d1",&dt0)) sf_error("No d1= in input");
	if(!sf_histint(in,"n2",&nm0)) sf_error("No n2= in input");
	if(!sf_histfloat(in,"d2",&dm0)) sf_error("No d2= in input");
	if(!sf_histfloat(in,"o2",&om0)) sf_error("No o2= in input");

	/* Read auxiliary files geometry */
	if(!sf_histint(pt0_file,"n1",&npt0)) sf_error("No n1= in t0's file");
	if(!sf_histint(pm0_file,"n1",&npm0)) sf_error("No n1= in m0's file");
	if(!sf_histint(v_file,"n1",&nv)) sf_error("No n1= in v's file");
	
	/* Vectors should have the same dimension */
	if(!(npt0==npm0)) sf_error("Auxiliary files (t0,m0 and v) should have the same n1!");
	if(!(npm0==nv)) sf_error("Auxiliary files (t0,m0 and v) should have the same n1!");
	
	if(!sf_getbool("verb",&verb)) verb=0;
	/* 1: active mode; 0: quiet mode */

	if(!sf_getfloat("aperture",&aperture)) aperture=1;
	/* Diffraction hyperbolas aperture */

	if (!sf_getfloat("freq",&freq)) freq=0.2/dt0;
    	/* peak frequency for Ricker wavelet */

	if(verb){
		sf_warning("Active mode on!!!");
		sf_warning("Input file parameters: ");
		sf_warning("n1=%d d1=%f o1=%f",nt0,dt0,ot0);
		sf_warning("n2=%d d2=%f o2=%f",nm0,dm0,om0);
	}

	/* Read input files */
	stackedSection = sf_floatalloc2(nt0,nm0);
	sf_floatread(stackedSection[0],nt0*nm0,in);
	pt0 = sf_floatalloc(npt0);
	sf_floatread(pt0,npt0,pt0_file);
	pm0 = sf_floatalloc(npm0);
	sf_floatread(pm0,npm0,pm0_file);
	v = sf_floatalloc(nv);
	sf_floatread(v,nv,v_file);

	ricker = sf_floatalloc(20);
    	ricker_init(nt0*2,freq*dt0,2);
	ricker[11]=1;
	sf_freqfilt(20,ricker);

	aperture = aperture;
	ntraces = round(aperture/dm0);

	for(k=0;k<nv;k++){

		/* Calculate center hyperbola coordinates */
		im0 = round(pm0[k]/dm0);
		it0 = round(pt0[k]/dt0);
		m0 = im0*dm0+om0;
		t0 = it0*dt0+ot0;
		
		for(i=im0-ntraces;i<im0+ntraces;i++){

			m = (i*dm0)-m0;
			t = sqrt(t0*t0 + ((m*m)/(v[k]*v[k])));
			it = (int) round(t/dt0);

			for(j=-10;j<11;j++){
				stackedSection[i][it+j]+=ricker[j+10];
			}/* Loop over a time window */

		} /* loop over one diffraction hyperbola */

	} /* Loop over hyperbolas */

	sf_floatwrite(stackedSection[0],nt0*nm0,out);

}
