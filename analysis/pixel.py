import numpy as np

order = 8
nside = 2**order
npixels = 12 * nside * nside

print ('order : ', order, 'nside : ', nside, 'npixels : ', npixels)

pixelarea = 4. * np.pi / npixels

print ('pixel area : %6.2e rad^2' % pixelarea)

pixelarea = (180. / np.pi)**2.0 * pixelarea

print ('pixel area : %6.2f deg^2' % pixelarea)

pixelsize = np.sqrt(pixelarea)

print ('pixel res : %6.2f deg' % pixelsize)
