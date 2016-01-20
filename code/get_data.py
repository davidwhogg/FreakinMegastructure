"""
This file is part of the FreakinMegastructure project.
Copyright 2016 David W. Hogg.
"""

import numpy as np
import pylab as plt
import kplr
client = kplr.API()
star = client.star(8462852)
lcs = star.get_light_curves()

# Loop over the datasets and read in the data.
time, flux, ivar, quality = [], [], [], []
for lc in lcs:
    with lc.open() as f:
        # The lightcurve data are in the first FITS HDU.
        hdu_data = f[1].data
        time = np.append(time, hdu_data["time"])
        thisflux = hdu_data["pdcsap_flux"]
        good = np.isfinite(thisflux)
        bad = np.logical_not(good)
        median = np.median(thisflux[good])
        thisflux /= median
        thisflux[bad] = 1.
        flux = np.append(flux, thisflux)
        thisferr = hdu_data["pdcsap_flux_err"] / median
        thisferr[bad] = np.Inf
        ivar = np.append(ivar, 1. / (thisferr * thisferr))
        quality.append(hdu_data["sap_quality"])

print(time.shape, flux.shape, ivar.shape, np.median(flux), np.median(ivar))

plt.clf()
plt.plot(time, flux, "k.", alpha=0.25)
plt.savefig("foo.png")
