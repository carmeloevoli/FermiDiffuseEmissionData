import healpy as hp
import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt

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

def readMaps(filename, nbins, nest=False):
    maps = hp.read_map(filename, field=range(nbins), dtype=np.float64, nest=nest)
    return maps

def plotMap(map, unit, title):
    min_map = max(0., np.min(map))
    max_map = np.max(map)
    hp.mollview(map, min=min_map, max=max_map, cmap=plt.cm.rainbow, norm="hist", title=title, unit=unit)
    hp.graticule()

def computeNpixels(nside):
    return 12 * nside * nside
    
def computeSourceMask(nside, nest=False):
    npixels = computeNpixels(nside)
    catalog = "data/Catalog-4FGL_DR2.dat"
    sourceLon, sourceLat = np.loadtxt(catalog, skiprows=0, usecols=(1,2), unpack=True)  #Column 1 is the Galactic longitude (l) and 2 is the latitude (b)
    sourceMask = np.ones(npixels)
    nsources = len(sourceLon)
    pixx = hp.pixelfunc.ang2pix(nside=nside, theta=sourceLon, phi=sourceLat, lonlat=True, nest=nest)
    sourceMask[pixx] = 0.
    return sourceMask

def computeInnerGalaxyMask(nside, nest=False):
    npixels = computeNpixels(nside)
    mask = np.zeros(npixels)
    for i in range(npixels):
        theta, phi = hp.pixelfunc.pix2ang(nside, i, lonlat=True)
        if (abs(theta) < 80. or abs(theta) > 280.) and abs(phi) < 8.:
            mask[i] = 1.0
    return mask

def plotPoints(ax, x, y, xerr, yerr, color, label, fmt):
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt=fmt, markersize=7, elinewidth=2, capsize=4, capthick=2,
                markeredgecolor=color, color=color, label=label, zorder=1)

def computeMeanMap(map, mask):
    counter = 0
    value = 0.
    for map_i, mask_i in zip(map, mask):
        if mask_i > 0.:
            value += map_i
            counter += 1
    return value / float(counter)

def computeStatisticalError(counts, mask):
    counter = 0
    value = 0.
    for counts_i, mask_i in zip(counts, mask):
        if mask_i > 0.:
            value += counts_i
            counter += 1
    return 3. * np.sqrt(value) / value
