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
	float v; // velocity for hyperbolas in m0's and t0's
	float** stackedSection; // stacked section A(t0,m0)
	float** diffractionSection; // diffraction section A(t0,m0)
	float aperture; // simulated hyperbolas aperture (km)
	int nt0; // number of t0's in stacked section
	float dt0; // t0 axis sampling
	float ot0; // t0 axis origin
	int nm0; // number of m0's in stacked section
	float dm0; // m0 axis sampling
	float om0; // m0 axis origin
	bool verb; // verbose parameter
	int im0; // center hyperbola index
	int ntraces; // aperture in number of traces
	float m; // CMP coordinate of a hyperbola sample
	float t; // time coordinate of a hyperbola sample
	int it; // time index coordinate of a hyperbola sample
	int i; // loop counter over a trace aperture to build one hyperbola
	int j; // loop counter over a time window in a trace
	int k; // loop counter number of hyperbolas for a given reflector
	int npt0; // Number of picked t0's
	int npm0; // Number of picked m0's
	float* ricker; // Generated ricker wavelet
	float freq; // Max frequency of ricker wavelet
	int rickerCenter; // Center sample of the ricker wavelet (max amplitude)

	/* RSF files I/O */
	sf_file in, out, pt0_file, pm0_file, diff_file;

	/* RSF files axis */

	sf_init(argc,argv);

	in = sf_input("in");
	pt0_file = sf_input("t0");
	pm0_file = sf_input("m0");
	out = sf_output("out");
	diff_file = sf_output("diff");

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
	
	/* Vectors should have the same dimension */
	if(!(npt0==npm0)) sf_error("Auxiliary files t0 and m0 should have the same n1!");
	
	if(!sf_getbool("verb",&verb)) verb=0;
	/* 1: active mode; 0: quiet mode */

	if(!sf_getfloat("aperture",&aperture)) aperture=1;
	/* Diffraction hyperbolas aperture (Km) */

	if (!sf_getfloat("freq",&freq)) freq=0.2/dt0;
    	/* peak frequency for Ricker wavelet (Hz) */

	if(!sf_getfloat("v",&v)) sf_error("No v= hyperbolas velocity!");
	/* Hyperbolas velocity (Km/s)*/
	
	/* half medium velocity for diffraction */
	v=v/2;

	if(verb){
		sf_warning("Active mode on!!!");
		sf_warning("Input file parameters: ");
		sf_warning("n1=%d d1=%f o1=%f",nt0,dt0,ot0);
		sf_warning("n2=%d d2=%f o2=%f",nm0,dm0,om0);
	}

	/* Read input files */
	stackedSection = sf_floatalloc2(nt0,nm0);
	diffractionSection = sf_floatalloc2(nt0,nm0);
	sf_floatread(stackedSection[0],nt0*nm0,in);
	pt0 = sf_floatalloc(npt0);
	sf_floatread(pt0,npt0,pt0_file);
	pm0 = sf_floatalloc(npm0);
	sf_floatread(pm0,npm0,pm0_file);

	/* Ricker wavelet trace */
	ricker = sf_floatalloc(nt0);
    	ricker_init(nt0*2,freq*dt0,2);
	rickerCenter = (int) round(nt0/2);
	ricker[rickerCenter] = 0.5;
	sf_freqfilt(nt0,ricker);

	ntraces = round(aperture/dm0);

	for(k=0;k<npt0;k++){

		/* Calculate center hyperbola coordinates */
		im0 = round(pm0[k]/dm0);
	
		for(i=im0-ntraces;i<im0+ntraces;i++){
			m = (i*dm0)-pm0[k];
			t = sqrt((pt0[k]*pt0[k]) + ((m*m)/(v*v)));
			it = (int) round(t/dt0);

			/* Jump to next iteration if its outside of the section */
			if(it >= nt0 || i >= nm0 || i < 0) continue;

			for(j=-20;j<21;j++){
				diffractionSection[i][j+it]+=ricker[j+rickerCenter];
				stackedSection[i][j+it]+=ricker[j+rickerCenter];
			}/* Loop over a time window */

		} /* loop over one diffraction hyperbola */

	} /* Loop over hyperbolas */

	sf_floatwrite(stackedSection[0],nt0*nm0,out);
	sf_floatwrite(diffractionSection[0],nt0*nm0,diff_file);
}
