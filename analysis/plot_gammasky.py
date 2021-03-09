import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('./gammasky.mplstyle')
import numpy as np
import gammalib as gl

def set_axis(ax):
    ax.set_xscale('log')
    ax.set_xlabel('E [MeV]')
    ax.set_xlim([2e2, 1e5])
    ax.set_yscale('log')
    ax.set_ylabel(r'$E_\gamma^2 J_\gamma$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
    ax.set_ylim([1e-3, 5e-2])

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

filenameCounts = "data/events_binned_healpix.fits"
filenameExposure = "data/exposure.fits"

E_down, E_up, E_size = gl.readEnergyBins(filenameCounts)
E_center = np.sqrt(E_down * E_up)
Delta_E = E_up - E_down

nside = gl.readNSide(filenameCounts)
pixelArea = gl.pixelSolidAngle(nside)

sourcemask = gl.computeSourceMask(nside)
mask = gl.computeInnerGalaxyMask(nside)

#gl.plotMap(mask, "mask", "Inner Galaxy")
#plt.savefig("InnerGalaxy.png")

countmaps = gl.readMaps(filenameCounts, E_size)

assert(E_size == gl.readEnergyNumBins(filenameExposure))
exposures = gl.readMaps(filenameExposure, E_size)

flux = np.zeros(E_size)
flux_err = np.zeros(E_size)

for i in range(E_size):
    counts = countmaps[i]
    exposure =  exposures[i]
    map = counts / pixelArea / exposure / Delta_E[i]
    flux[i] = computeMeanMap(map, mask * sourcemask)
    flux_relative_err[i] = computeStatisticalError(counts, mask * sourcemask)

print (flux_relative_err)

fig = plt.figure(figsize=(10.5,8))
ax = fig.add_subplot(111)
set_axis(ax)

xerr_up = E_up - E_center
xerr_do = E_center - E_down

yerr =  E_center**2.0 * flux * flux_relative_err

gl.plotPoints(ax, E_center, E_center**2.0 * flux, [xerr_do, xerr_up], yerr, 'tab:red', 'PASS-8', 'o')

ax.set_title('Inner Galaxy')

plt.savefig('innergalaxy_spectrum.pdf')
