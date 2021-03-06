#!/usr/bin/env python2.7

"""
Create a G'DAY met forcing file from the MAESPA-style met file

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (17.01.2017)"
__email__ = "mdekauwe@gmail.com"

import sys
import os
import csv
import math
import numpy as np
from datetime import date
import calendar
import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import datetime as dt


class CreateMetData(object):

    def __init__(self, site, fname):

        self.fname = fname
        self.site = site
        self.ovar_names = ['#year', 'doy', 'hod', 'rain', 'par', 'tair',
                           'tsoil', 'vpd', 'co2', 'ndep', 'nfix', 'wind', 'press']
        self.ounits = ['#--', '--', '--', 'mm/30min', 'umol/m2/s','degC',
                       'degC', 'kPa', 'ppm', 't/ha/30min', 't/ha/30min', 'm/s','kPa']
        self.lat = -999.9
        self.lon = -999.9

        # unit conversions
        self.SEC_TO_HFHR = 60.0 * 30.0 # sec/half hr
        self.PA_TO_KPA = 0.001
        self.J_TO_MJ = 1.0E-6
        self.K_to_C = 273.15
        self.G_M2_to_TONNES_HA = 0.01
        self.MM_S_TO_MM_HR = 3600.0
        self.SW_2_PAR = 2.3


    def main(self, ofname, scheme, co2_conc=None):

        df = pd.read_csv(self.fname, sep=" ")

        yr_sequence = np.unique(df.year)
        start_sim = yr_sequence[0]
        end_sim = yr_sequence[-1]

        try:
            ofp = open(ofname, 'wb')
            wr = csv.writer(ofp, delimiter=',', quoting=csv.QUOTE_NONE,
                            escapechar=None, dialect='excel')
            wr.writerow(['# %s 30 min met forcing' % (self.site)])
            wr.writerow(['# Data from %s-%s' % (start_sim, end_sim)])
            wr.writerow(['# Created by Martin De Kauwe: %s' % date.today()])
            wr.writerow([var for i, var in enumerate(self.ounits)])
            wr.writerow([var for i, var in enumerate(self.ovar_names)])

        except IOError:
            raise IOError('Could not write met file: "%s"' % ofname)


        for i in range(len(df)):
            if co2_conc is not None:
                co2 = co2_conc
            else:
                #co2 = df.co2[i]
                co2 = 390 * 1.3

            if df.vpd[i] < 0.05:
                vpd = 0.05
            else:
                vpd = df.vpd[i]
            wr.writerow([float(df.year[i]), float(df.doy[i]), float(df.hod[i]),\
                         df.rain[i],df.par[i], df.tair[i], df.tsoil[i], vpd,\
                         co2, -999.9, -999.9, df.wind[i],\
                         df.press[i]])

        ofp.close()


if __name__ == "__main__":

    fdir = "raw_data"
    fname = os.path.join(fdir, "gdayMet.dat")
    site = "EucFACE"

    scheme = "twoleaf"

    ofname = "%s_AMB.csv" % (scheme)
    C = CreateMetData(site, fname)
    C.main(ofname, scheme, co2_conc=390.0)

    ofname = "%s_ELE.csv" % (scheme)
    C.main(ofname, scheme, co2_conc=None)
