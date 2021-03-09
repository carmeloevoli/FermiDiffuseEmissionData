import matplotlib.pyplot as plt
import healpy as hp
import astropy.io.fits as pyfits
import numpy as np

def plotExposureMap(filename, iE):
    E_size = readEnergyNumBins(filename)
    expmaps = hp.read_map(filename, field=range(E_size), dtype=np.float64, nest=False)
    map = np.array(expmaps[iE])
    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title="exposure")
    plt.savefig('test_expmap.png')

#def plotFluxMap(eventsFilename, exposureFilename, iE):
#    E_down, E_up, E_size = readEnergyBins(eventsFilename)
#    E_center = np.sqrt(E_down * E_up)
#    delta_E = (E_up - E_down)
#    
#    nside = readNSide(eventsFilename)
#    dOmega = pixelSolidAngle(nside)
#
#    allCountMaps = hp.read_map(eventsFilename, field=range(E_size), dtype=np.float64, nest=False)
#    countmap = np.array(allCountMaps[iE])
#
#    assert(readEnergyNumBins(exposureFilename) == E_size)
#    assert(readNSide(exposureFilename) == nside)
#    
#    allExposureMaps = hp.read_map(exposureFilename, field=range(E_size), dtype=np.float64, nest=False)
#    exposure = np.array(allExposureMaps[iE])
#
#    map = (countmap / exposure) / dOmega # counts cm-2 s-1 sr-1
#    map = map / delta_E[iE] # counts cm-2 s-1 sr-1 MeV-1
#    
#    str_E = "{:.1f}".format(E_center[iE] / 1e3)
#    str_unit = r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$ MeV$^{-1}$"
#    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title=r"E = " + str_E + " GeV", unit=str_unit)
#    plt.savefig('test_flux.png')
#
#    return map
#
#### MAiN ###
#
#E_down, E_up, E_size = readEnergyBins("weekly/events_binned_healpix.fits")
#
#for iE in range(E_size):
#    plotCountMap("weekly/events_binned_healpix.fits", iE)
#    E_center = np.sqrt(E_down[iE] * E_up[iE]) / 1e3
#    print ("%9.2f" % E_center)

#plotExposureMap("weekly/exposure.fits", iE)
#fluxmap = plotFluxMap("weekly/events_binned_healpix.fits", "weekly/exposure.fits", iE)
#computeIntegratedFlux(fluxmap, E)



