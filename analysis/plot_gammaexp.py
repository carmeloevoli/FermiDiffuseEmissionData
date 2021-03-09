import matplotlib.pyplot as plt
import numpy as np

import gammalib as gl

filename = "data/exposure.fits"

nbins = gl.readEnergyNumBins(filename)
expmaps = gl.readMaps(filename, nbins)

E_down, E_up, E_size = gl.readEnergyBins("data/events_binned_healpix.fits")
E_center = np.sqrt(E_down * E_up)

for i in range(nbins):
    map = np.array(expmaps[i])
    str_E = "{:.1f}".format(E_center[i] / 1e3)
    gl.plotMap(map, "exposure", "FERMI-LAT - E = " + str_E + " GeV")
    plt.savefig('exposure_' + str_E + '.png')
