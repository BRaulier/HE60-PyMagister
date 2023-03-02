#!/bin/sh

# -O0 is default (no optimiszation)
# -O1 or -O2 produce an executable that runs approximately as twice as fast and works ok
# -O3 and -Ofast cause errors

# -ffree-line-length-none prevents truncation of long text lines
# -finit-local-zero required as parts of the code assume variables are initialised to zero
OPTS="-O1 -ffree-line-length-none -finit-local-zero"

# build directory and relative path from build dir to target dir and installed m2xl relative location

if [ "`uname`" == "Darwin" ]; then
  BUILD_DIR=../build_osx/el_build
else 
  BUILD_DIR=../build_linux/el_build
fi

mkdir -p $BUILD_DIR

# in a normal installaton the backend directory is two directories up
if [ -d "../../backend" ]; then
  REL_TARG_DIR=../../../backend
else
  REL_TARG_DIR=../backend
  mkdir -p $BUILD_DIR"/"$REL_TARG_DIR
fi

cp spawnEL_stnd.sh $BUILD_DIR"/"$REL_TARG_DIR

# for gfortran remove the DLL_IMPORT command
sed -e "s|DLL_IMPORT :: info||g" ../common_code/admin_mod.f95 > ../common_code/admin_mod_var.f95

# for linux and osx convert backslash to forward slash in m2xl relative path
if [ "`uname`" == "Darwin" ]; then
  sed -e "s|\\\\frontend\\\\|/MacOS/|g" main_EcoLight.f95 > main_EcoLight_var.f95 
else
  sed -e "s|\\\\frontend\\\\|/frontend/|g" main_EcoLight.f95 > main_EcoLight_var.f95 
fi

cd $BUILD_DIR

rm -f *.o
rm -f *.mod

gfortran $OPTS -c ../../common_data_modules/heinfo.f95

# have to compile data module mod_DimensDefaults.f95 first, to define array dimensions, etc.
gfortran $OPTS -c ../../common_data_modules/mod_DimensDefaults.f95
# gfortran $OPTS -c ../../common_data_modules/mod_Config.f95

# compile the remaining common data modules; these depend only on mod_DimensDefaults
gfortran $OPTS -c ../../common_data_modules/mod*.f95

# user-written functions
gfortran $OPTS -c ../../user_routines/Chlz_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/Minz_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/So_biolum_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/a_CDOM_user_func_mod.f95

# misc common code routines used in the HydroLight routines
gfortran $OPTS -c ../../common_code/print_arrays_mod.f95

# modified version for linux and osx
gfortran $OPTS -c ../../common_code/admin_mod_var.f95

gfortran $OPTS -c ../../common_code/read_Iroot_mod.f95
gfortran $OPTS -c ../../common_code/define_grid_mod.f95
gfortran $OPTS -c ../../common_code/set_paths_mod.f95
gfortran $OPTS -c ../../common_code/data_RangeCheck_mod.f95
gfortran $OPTS -c ../../common_code/read_data_files_mod.f95
gfortran $OPTS -c ../../common_code/print_phase_function_info_mod.f95
gfortran $OPTS -c ../../common_code/interpolation_mod.f95
gfortran $OPTS -c ../../common_code/matrix_multiplication_mod.f95
gfortran $OPTS -c ../../common_code/Excel_mod.f95
gfortran $OPTS -c ../../common_code/R_bottom_mod.f95
gfortran $OPTS -c ../../common_code/bottom_BRDF_mod.f95
gfortran $OPTS -c ../../common_code/print_bottom_info_mod.f95
gfortran $OPTS -c ../../common_code/Color_mod.f95
gfortran $OPTS -c ../../common_code/Secchi_mod.f95
gfortran $OPTS -c ../../common_code/So_biolum_data_mod.f95
gfortran $OPTS -c ../../common_code/So_biolum_mod.f95
gfortran $OPTS -c ../../common_code/PAR_mod.f95
gfortran $OPTS -c ../../common_code/K_functions_mod.f95
gfortran $OPTS -c ../../common_code/H2O_scat_TS_mod.f95

# common code routines used by the standard IOP models
gfortran $OPTS -c ../../common_code/pureH2O_mod.f95
gfortran $OPTS -c ../../common_code/Chlz_data_mod.f95
gfortran $OPTS -c ../../common_code/Chl_conc_mod.f95
gfortran $OPTS -c ../../common_code/Minz_data_mod.f95
gfortran $OPTS -c ../../common_code/Min_conc_mod.f95
gfortran $OPTS -c ../../common_code/CDOMz_data_mod.f95
gfortran $OPTS -c ../../common_code/astar_mod.f95
gfortran $OPTS -c ../../common_code/bstar_mod.f95

# user-written concentration functions for use in IOP_UserData_mod.f95 (example functions as distributed)
gfortran $OPTS -c ../../user_routines/CompConc1_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc2_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc3_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc4_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc5_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc6_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc7_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc8_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc9_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/CompConc10_user_func_mod.f95
gfortran $OPTS -c ../../user_routines/Comp_conc_user_data_mod.f95
gfortran $OPTS -c ../../user_routines/Comp_conc_user_defined_mod.f95

# IOP routines
gfortran $OPTS -c ../../common_code/IOP_constant_mod.f95
gfortran $OPTS -c ../../common_code/IOP_classicCase1_mod.f95
gfortran $OPTS -c ../../common_code/IOP_newCase1_mod.f95

gfortran $OPTS -c ../../common_code/a_CDOM_mod.f95

gfortran $OPTS -c ../../common_code/IOP_genericCase2_mod.f95
gfortran $OPTS -c ../../common_code/IOP_newCase2_mod.f95
gfortran $OPTS -c ../../EcoLight_code/select_pf_bb_mod.f95
gfortran $OPTS -c ../../common_code/IOP_userData_mod.f95
gfortran $OPTS -c ../../user_routines/IOP_userDefined_mod.f95
gfortran $OPTS -c ../../common_code/generic_IOP_model_mod.f95

# sky models
gfortran $OPTS -c ../../common_code/sky_irrad_data_mod.f95
gfortran $OPTS -c ../../common_code/sun_angles_mod.f95
gfortran $OPTS -c ../../common_code/sky_radiance_models_mod.f95
gfortran $OPTS -c ../../common_code/RADTRANX_mod.f95
gfortran $OPTS -c ../../common_code/sky_radiance_data_file_mod.f95
gfortran $OPTS -c ../../common_code/generic_sky_models_mod.f95

gfortran $OPTS -c ../../common_code/get_DynamicZ_mod.f95
gfortran $OPTS -c ../../common_code/common_surface_mod.f95
gfortran $OPTS -c ../../common_code/beamc_functions_mod.f95
gfortran $OPTS -c ../../common_code/z_zeta_mod.f95
gfortran $OPTS -c ../../common_code/bbfraction_powerlaw_mod.f95
gfortran $OPTS -c ../../common_code/wave_redist_func_mod.f95
gfortran $OPTS -c ../../common_code/sources_mod.f95

# legacy F77 public code routines (these are F77 routines, not placed in Modules)
gfortran $OPTS -fno-automatic -std=legacy -c ../../common_code/public_*.f

# EcoLight core code modules in the order required by dependencies
gfortran $OPTS -c ../../EcoLight_code/initialize_printout_mod.f95
gfortran $OPTS -c ../../EcoLight_code/print_grid_mod.f95
gfortran $OPTS -c ../../HydroLight_code/quad_average_sky_mod.f95
gfortran $OPTS -c ../../EcoLight_code/band_average_sky_mod.f95
gfortran $OPTS -c ../../EcoLight_code/initialize_mod.f95
gfortran $OPTS -c ../../EcoLight_code/load_surface_mod.f95
gfortran $OPTS -c ../../EcoLight_code/rho_tau_mod.f95
gfortran $OPTS -c ../../EcoLight_code/infinite_bottom_mod.f95
gfortran $OPTS -c ../../HydroLight_code/quad_average_BRRF_mod.f95
gfortran $OPTS -c ../../EcoLight_code/bottom_bndcond_mod.f95

gfortran $OPTS -c ../../EcoLight_code/radiances_zeta_mod.f95
gfortran $OPTS -c ../../EcoLight_code/radiances_w_mod.f95
gfortran $OPTS -c ../../EcoLight_code/initialize_radiances_mod.f95

gfortran $OPTS -c ../../EcoLight_code/dRTSdzeta_mod.f95
gfortran $OPTS -c ../../EcoLight_code/Riccati_mod.f95

gfortran $OPTS -c ../../EcoLight_code/radiances_mod.f95
gfortran $OPTS -c ../../EcoLight_code/irradiances_mod.f95
gfortran $OPTS -c ../../EcoLight_code/print_radiances_mod.f95
gfortran $OPTS -c ../../EcoLight_code/write_Lfile_mod.f95
gfortran $OPTS -c ../../EcoLight_code/write_LEfile_mod.f95
gfortran $OPTS -c ../../EcoLight_code/write_Dfile_mod.f95
gfortran $OPTS -c ../../HydroLight_code/synthesize_radiances_mod.f95
gfortran $OPTS -c ../../common_code/radiance_analysis_mod.f95


# osx build

if [ "`uname`" == "Darwin" ]; then

  #gfortran $OPTS ../../EcoLight_code/main_EcoLight_var.f95 *.o $REL_TARG_DIR/heinfof.so -o $REL_TARG_DIR/EcoLight6
  gfortran $OPTS ../../EcoLight_code/main_EcoLight_var.f95 *.o -o $REL_TARG_DIR/EcoLight6

  # for production build on osx copy libraries and adjust path to library files
  # otherwise use whatever libraries the compiler found
  # can check with otool -L

  if [ "$1" == "USE_BUNDLED_LIB" ]; then
 
      cd $REL_TARG_DIR

      # no longer needed
      # install_name_tool -change heinfof.so @executable_path/heinfof.so EcoLight6

      mkdir -p lib

      # some of the following is duplicated in the HydroLight build script
      # but it means that either script can work as stand-alone

      # copy these even in a local build so if gfortran is ininstalled HE60 will still run
      
      cp /usr/local/gfortran/lib/libgcc_s.1.dylib lib/
      cp /usr/local/gfortran/lib/libgfortran.3.dylib lib/
      cp /usr/local/gfortran/lib/libquadmath.0.dylib lib/

      # update where to find these libraries in the executable
      
      install_name_tool -id @executable_path/lib/libgcc_s.1.dylib lib/libgcc_s.1.dylib
      install_name_tool -id @executable_path/lib/libgfortran.3.dylib lib/libgfortran.3.dylib
      install_name_tool -id @executable_path/lib/libquadmath.0.dylib lib/libquadmath.0.dylib

      install_name_tool -change /usr/local/gfortran/lib/libgcc_s.1.dylib @executable_path/lib/libgcc_s.1.dylib EcoLight6
      install_name_tool -change /usr/local/gfortran/lib/libgfortran.3.dylib @executable_path/lib/libgfortran.3.dylib EcoLight6 
      install_name_tool -change /usr/local/gfortran/lib/libquadmath.0.dylib @executable_path/lib/libquadmath.0.dylib EcoLight6 
      install_name_tool -change /usr/local/gfortran/lib/libquadmath.0.dylib @executable_path/lib/libquadmath.0.dylib lib/libgfortran.3.dylib 
      install_name_tool -change /usr/local/gfortran/lib/libgcc_s.1.dylib @executable_path/lib/libgcc_s.1.dylib lib/libgfortran.3.dylib 
      install_name_tool -change /usr/local/gfortran/lib/libgcc_s.1.dylib @executable_path/lib/libgcc_s.1.dylib lib/libquadmath.0.dylib

  fi
  
# linux build

else

  # in the production build the rpath option is set so the bundled gfortran library will be found under ../lib
  # the order of searching on ELF systems (most linuxes) is: LD_LIBRARY_PATH, -rpath (../lib), then the system (e.g. /usr/lib64)
  # when recompiling on a system with different gfortran installed we will instead use the installed version so rpath is not set
  # can check rpath with readelf -d

    # production build passes an argument to indicate to set the rpath to ../lib
    # all builds need an rpath entry for the executable directory as some Linuxes don't search there by default
  if [ "$1" == "USE_BUNDLED_LIB" ]; then
    # ln -sf $REL_TARG_DIR/heinfof.so
    # gfortran $OPTS -Wl,-rpath,'$ORIGIN:$ORIGIN/../lib' ../../EcoLight_code/main_EcoLight_var.f95 *.o heinfof.so -o $REL_TARG_DIR/EcoLight6
    gfortran $OPTS -Wl,-rpath,'$ORIGIN:$ORIGIN/../lib' ../../EcoLight_code/main_EcoLight_var.f95 *.o -o $REL_TARG_DIR/EcoLight6
  else
    # ln -sf $REL_TARG_DIR/heinfof.so
    # gfortran $OPTS -Wl,-rpath,'$ORIGIN' ../../EcoLight_code/main_EcoLight_var.f95 *.o heinfof.so -o $REL_TARG_DIR/EcoLight6
    gfortran $OPTS -Wl,-rpath,'$ORIGIN' ../../EcoLight_code/main_EcoLight_var.f95 *.o -o $REL_TARG_DIR/EcoLight6
  fi

fi
