import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('./gammasky.mplstyle')
import numpy as np

import gammalib as gl

COUNTSFILENAME = "data/events_binned_healpix.fits"
EXPOSUREFILENAME = "data/exposure.fits"

def set_axis(ax):
    ax.set_xscale('log')
    ax.set_xlabel('E [MeV]')
    ax.set_xlim([2e2, 1e5])
    ax.set_yscale('log')
    ax.set_ylabel(r'$E_\gamma^2 J_\gamma$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
    ax.set_ylim([1e-3, 5e-2])

def plot_innergalaxy_mask():
    nside = gl.readNSide(COUNTSFILENAME)
    mask = gl.computeInnerGalaxyMask(nside)
    gl.plotMap(mask, "mask", "Inner Galaxy")
    plt.savefig("inner_galaxy_mask.pdf")

def plot_spectrum():
    E_down, E_up, E_size = gl.readEnergyBins(COUNTSFILENAME)
    E_center = np.sqrt(E_down * E_up)
    Delta_E = E_up - E_down

    nside = gl.readNSide(COUNTSFILENAME)
    pixelArea = gl.pixelSolidAngle(nside)

    sourcemask = gl.computeSourceMask(nside)
    mask = gl.computeInnerGalaxyMask(nside)
    
    countmaps = gl.readMaps(COUNTSFILENAME, E_size)

    assert(E_size == gl.readEnergyNumBins(EXPOSUREFILENAME))
    exposures = gl.readMaps(EXPOSUREFILENAME, E_size)

    flux, flux_relative_err = np.zeros(E_size), np.zeros(E_size)

    for i in range(E_size):
        counts = countmaps[i]
        exposure =  exposures[i]
        map = counts / pixelArea / exposure / Delta_E[i]
        flux[i] = gl.computeMeanMap(map, mask * sourcemask)
        flux_relative_err[i] = gl.computeStatisticalError(counts, mask * sourcemask)

    fig = plt.figure(figsize=(10.5,8))
    ax = fig.add_subplot(111)
    set_axis(ax)

    xerr_up = E_up - E_center
    xerr_do = E_center - E_down
    yerr = E_center**2.0 * flux * flux_relative_err

    gl.plotPoints(ax, E_center, E_center**2.0 * flux, [xerr_do, xerr_up], yerr, 'tab:red', 'PASS-8', 'o')

    ax.set_title('Inner Galaxy')
    plt.savefig('inner_galaxy_spectrum.pdf')

if __name__== "__main__":
    plot_innergalaxy_mask()
    plot_spectrum()
