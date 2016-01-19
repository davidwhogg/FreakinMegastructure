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
time, flux, ferr, quality = [], [], [], []
for lc in lcs:
    with lc.open() as f:
        # The lightcurve data are in the first FITS HDU.
        hdu_data = f[1].data
        time.append(hdu_data["time"])
        flux.append(hdu_data["sap_flux"])
        ferr.append(hdu_data["sap_flux_err"])
        quality.append(hdu_data["sap_quality"])

plt.clf()
plt.plot(time, flux, "k.", alpha=0.25)
plt.savefig("foo.png")
