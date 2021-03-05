import matplotlib.pyplot as plt
import healpy as hp
import astropy.io.fits as pyfits
import numpy as np

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

def readEnergyNumBins(filename):
    with pyfits.open(filename) as hdulist:
        ordering = hdulist[1].header['ORDERING']
        nside = hdulist[1].header['NSIDE']
        nbins = hdulist[1].header['TFIELDS']
    print (ordering, nside, nbins)
    return nbins

def plotCountMap(filename):
    E_down, E_up, E_size = readEnergyBins(filename)
    countmaps = hp.read_map(filename, field=range(E_size), dtype=np.float64, nest=False)

    i = 5
    E = np.sqrt(E_down[i] * E_up[i])
    map = np.array(countmaps[i])
    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title="E = " + str(E / 1e3) + " GeV")
    plt.savefig('test_countmap.png')

def plotExposureMap(filename):
    E_size = readEnergyNumBins(filename)
    expmaps = hp.read_map(filename, field=range(E_size), dtype=np.float64, nest=False)

    i = 2
    map = np.array(expmaps[i])
    hp.mollview(map, min=np.min(map), max=np.max(map), cmap=plt.cm.rainbow, norm="hist", title="exposure")
    plt.savefig('test_expmap.png')

### MAiN ###
plotCountMap("weekly/events_binned_healpix.fits")
plotExposureMap("weekly/exposure.fits")
