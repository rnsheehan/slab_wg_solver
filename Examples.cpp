#ifndef ATTACH_H
#include "Attach.h"
#endif

void examples::slab_wg_test()
{
	// Example to illustrate the use of the slab wg solver

	// define parameters
	double width = 2.0; 
	double wavelength = 1.55; 
	double core = 3.38; 
	double sub = 3.17; 
	double clad = 3.17; 

	// Declarate slab_wg object
	slab_wg the_slab(width, wavelength, core, sub, clad); 

	std::string null_string = ""; 

	//the_slab.calculate_all_neffs(null_string); 

	the_slab.calculate_all_modes(50, 10, null_string); 

	/*the_slab.clearbeta(TE); 

	the_slab.clearbeta(TM);*/

	std::cout<<"\n"; 
}