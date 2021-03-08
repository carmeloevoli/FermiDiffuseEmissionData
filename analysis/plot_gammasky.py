import matplotlib.pyplot as plt
import healpy as hp
import astropy.io.fits as pyfits
import numpy as np

def pixelSolidAngle(mapNside):
    npixels = 12. * mapNside * mapNside
    return 4. * np.pi / npixels

def readEnergyBins(filename):
    with pyfits.open(filename) as hdulist:
        bins = np.array(list(hdulist[2].data))
        ordering = hdulist[1].header['ORDERING']
        nside = hdulist[1].header['NSIDE']
        nbins = hdulist[1].header['TFIELDS']
    print (ordering, nside, nbins, len(bins))
    E_down = np.array(bins[:,1]) / 1e3 # MeV
    E_up = np.array(bins[:,2]) / 1e3 # MeV
    return E_down, E_up, nbins

def readNSide(filename):
    with pyfits.open(filename) as hdulist:
        bins = np.array(list(hdulist[2].data))
        ordering = hdulist[1].header['ORDERING']
        nside = hdulist[1].header['NSIDE']
        nbins = hdulist[1].header['TFIELDS']
    print (ordering, nside, nbins, len(bins))
    return nside

def readEnergyNumBins(filename):
    with pyfits.open(filename) as hdulist:
        ordering = hdulist[1].header['ORDERING']
        nside = hdulist[1].header['NSIDE']
        nbins = hdulist[1].header['TFIELDS']
    print (ordering, nside, nbins)
    return nbins

def plotCountMap(filename, iE):
    E_down, E_up, E_size = readEnergyBins(filename)
    countmaps = hp.read_map(filename, field=range(E_size), dtype=np.float64, nest=False)
    E_center = np.sqrt(E_down[iE] * E_up[iE])
    map = np.array(countmaps[iE])
    min_map = max(0., np.min(map))
    max_map = np.max(map)
    str_E = "{:.1f}".format(E_center / 1e3)
    hp.mollview(map, min=min_map, max=max_map, cmap=plt.cm.rainbow, norm="hist", title="FERMI-LAT - E = " + str_E + " GeV", unit='counts')
    hp.graticule()
    plt.savefig('test_countmap_' + str_E + '.png')
    
def plotExposureMap(filename, iE):
    E_size = readEnergyNumBins(filename)
    expmaps = hp.read_map(filename, field=range(E_size), dtype=np.float64, nest=False)
    map = np.array(expmaps[iE])
    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title="exposure")
    plt.savefig('test_expmap.png')

def plotFluxMap(eventsFilename, exposureFilename, iE):
    E_down, E_up, E_size = readEnergyBins(eventsFilename)
    E_center = np.sqrt(E_down * E_up)
    delta_E = (E_up - E_down)
    
    nside = readNSide(eventsFilename)
    dOmega = pixelSolidAngle(nside)

    allCountMaps = hp.read_map(eventsFilename, field=range(E_size), dtype=np.float64, nest=False)
    countmap = np.array(allCountMaps[iE])

    assert(readEnergyNumBins(exposureFilename) == E_size)
    assert(readNSide(exposureFilename) == nside)
    
    allExposureMaps = hp.read_map(exposureFilename, field=range(E_size), dtype=np.float64, nest=False)
    exposure = np.array(allExposureMaps[iE])

    map = (countmap / exposure) / dOmega # counts cm-2 s-1 sr-1
    map = map / delta_E[iE] # counts cm-2 s-1 sr-1 MeV-1
    
    str_E = "{:.1f}".format(E_center[iE] / 1e3)
    str_unit = r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$ MeV$^{-1}$"
    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title=r"E = " + str_E + " GeV", unit=str_unit)
    plt.savefig('test_flux.png')

    return map

### MAiN ###

iE = 5

plotCountMap("weekly/events_binned_healpix.fits", iE)
#plotExposureMap("weekly/exposure.fits", iE)
#fluxmap = plotFluxMap("weekly/events_binned_healpix.fits", "weekly/exposure.fits", iE)
#computeIntegratedFlux(fluxmap, E)



