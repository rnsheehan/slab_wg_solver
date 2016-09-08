#ifndef ATTACH_H
#define ATTACH_H

#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include <sstream>

#include <cmath>
#include <vector>

// Constants
static const bool TE=1;
static const bool TM=0;
static const bool Ex=1; // Ex propagation is equivalent to TE mode E^{x} polarisation => TM followed by TE
static const bool Ey=0; // Ey propagation is equivalent to TM mode E^{y} polarisation => TE followed by TM

static const double EPS=(3.0e-12);

static const double p=(atan(1.0));
static const double Two_PI=(8.0*p);
static const double PI=(4.0*p);
static const double PI_2=(2.0*p);
static const double PI_3=((4.0/3.0)*p);
static const double PI_4=(p);
static const double PI_5=((4.0/5.0)*p);
static const double PI_6=((2.0/3.0)*p);

static const double SPEED_OF_LIGHT=(3.0e14); // Speed of light in microns per second
static const double EPSILON=(8.85e-18); // Permittivity of free space in Farads per micron
static const double MU=(12.566e-13); // Permeability of free space in Henrys per micron
static const double ETA=sqrt(MU/EPSILON); // Impedance of free space

static const std::string dottxt=".txt";

#include "Templates.h"
#include "Useful.h"
#include "Slab_Solver.h"
#include "Examples.h"

#endif