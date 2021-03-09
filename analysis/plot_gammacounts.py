import matplotlib.pyplot as plt
import numpy as np

import gammalib as gl

def plotCountMaps(filename):
    E_down, E_up, E_size = gl.readEnergyBins(filename)
    E_center = np.sqrt(E_down * E_up)

    countmaps = gl.readMaps(filename, E_size)

    for i in range(E_size):
        map = np.array(countmaps[i])
        str_E = "{:.1f}".format(E_center[i] / 1e3)
        gl.plotMap(map, "counts", "FERMI-LAT - E = " + str_E + " GeV")
        plt.savefig('countmap_' + str_E + '.png')

def plotSourceMask(filename):
    nside = gl.readNSide(filename)
    mask = gl.computeSourceMask(nside)

    gl.plotMap(mask, "mask", "source nside = " + str(nside))
    plt.savefig("source_mask.png")

def plotCountMapsNoSources(filename):
    E_down, E_up, E_size = gl.readEnergyBins(filename)
    E_center = np.sqrt(E_down * E_up)

    nside = gl.readNSide(filename)
    mask = gl.computeSourceMask(nside)
    
    countmaps = gl.readMaps(filename, E_size)

    for i in range(E_size):
        map = np.array(countmaps[i])
        map = map * mask
        str_E = "{:.1f}".format(E_center[i] / 1e3)
        gl.plotMap(map, "counts", "FERMI-LAT No Sources - E = " + str_E + " GeV")
        plt.savefig('countmap_nosources_' + str_E + '.png')

filename = "data/events_binned_healpix.fits"

plotCountMaps(filename)
plotSourceMask(filename)
plotCountMapsNoSources(filename)
