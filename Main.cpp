#ifndef ATTACH_H
#include "Attach.h"
#endif

// sample call: Slab_WG_Slv w l nc ns ncl pwd

int main(int argc, char *argv[])
{
	try{
		
		if(argc >= 6){
			
			// List off the input parameters
			// Program needs 5 or more parameters to run, remember that the name of the program is also considered a parameter
			// argv[0] = program name
			// argv[1] = slab waveguide width
			// argv[2] = operating wavelength
			// argv[3] = core refractive index
			// argv[4] = substrate refractive index
			// argv[5] = cladding refractive index
			// argv[6] = name of present working directory

			std::cout<<argc-1<<" parameters were input into the program\n"; 
			for(int count = 1; count < argc; count++){
				std::cout<<"argv["<<count<<"] = "<<argv[count]<<"\n"; 
			}
			std::cout<<"\n";
			
			// Define input parameters

			int N = 201; // Number of points at which slab mode will be sampled
			double Lx = 3.0*atof( argv[1] ); // distance over which slab mode will be sampled

			double wg_width = atof( argv[1] ); // slab waveguide width
			double wavelength = atof( argv[2] ); // operating wavelength
			double n_core = atof( argv[3] ); // core refractive index
			double n_sub = atof( argv[4] ); // substrate refractive index
			double n_clad = atof( argv[5] ); // cladding refractive index

			std::string storage = argv[6]; // present working directory

			// Declarate slab waveguide object
			slab_wg the_slab(wg_width, wavelength, n_core, n_sub, n_clad); 

			the_slab.calculate_all_modes(N, Lx, storage); 
		}
		else{
			std::string reason = "Error: Slab_WG_Slv\n";
			reason += "Insufficient number of input arguments\n"; 

			throw std::invalid_argument(reason); 
		}

	}
	catch(std::invalid_argument &e){
		useful_funcs::exit_failure_output(e.what()); 
		exit(EXIT_FAILURE); 
	}

	/*std::cout<<"Press enter to close\n"; 
	std::cin.get();*/ 

	return 0; 
}