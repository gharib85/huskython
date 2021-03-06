
from husky.hamiltonian.ElectronicSystem import Junction

from husky.transport.esqc import ESQCsolver
from husky.transport.negf import NEGFsolver

from husky.hamiltonian.model import tight_binding as tb

import matplotlib.pyplot as plt 
import numpy as np

import sys

############################################################################
# compute the transmission coefficient of a benzene tight-binding
# molecule between two electrodes. Each cell of each electrode contains here
# a single state.
############################################################################



# define the junction
system = Junction()

# add the molecule hamiltonian
system.add_central_matrix(h0=tb.cyclic_aromatic(N=6,e=0,a=-1.))

# add the electrodes
e0,vi,vmol = 0.,-2.5, 1.
system.add_electrode_matrix(h0 = np.array([e0]), hi = np.array([vi]),vmol = np.array([vmol,0,0,0,0,0]))
system.add_electrode_matrix(h0 = np.array([e0]), hi = np.array([vi]),vmol = np.array([0,0,vmol,0,0,0]))

# compute the band structure of the electrode
system.electrodes['0'].band_structure(nK = 250, nE=250, filename='bandstructure_0.png')

##########################################################
#				ESQC
##########################################################

# declare the esqc solver and the enrgy range
trans=ESQCsolver(system)
trans.set_energy_range(emin=-5,emax=5,nE=500)

# compute the transmission and plot it
te_esqc = trans.compute_transmission()


##########################################################
#				NEGF - WBL
##########################################################
trans=NEGFsolver(system)
trans.set_energy_range(emin=-5,emax=5,nE=500)


# set the wbl approx on and define the ldos of the elctrodes
trans.set_wide_band_limit(True)
trans.set_local_dos_electrode(0.4)

# compute the transport properties
te_negf_wbl = trans.compute_transmission()


##########################################################
#				NEGF - NO WBL
##########################################################
trans=NEGFsolver(system)
trans.set_energy_range(emin=-5,emax=5,nE=500)

# set the wbl approx OFF and define the 
# surface green function of the electrodes
trans.set_wide_band_limit(False)
trans.junction.precompute_electrodes_surface_green_function(np.linspace(-8,8,250),tol=1E-6,identical_electrodes=True)

# compute the surface green functions of the electrodes
te_negf = trans.compute_transmission()



##########################################################
#				Plot the results
##########################################################
plt.semilogy(trans.energies,te_esqc,linewidth=4,color='black',label='ESQC')
plt.semilogy(trans.energies,te_negf_wbl,linewidth=2,color='#DF1400',label='NEGF-WBL')
plt.semilogy(trans.energies,te_negf,linewidth=2,color='#64D2FF',label='NEGF')
plt.ylim([1E-6,2])
plt.legend()
plt.savefig('te.png')


