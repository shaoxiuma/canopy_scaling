#!/usr/bin/env python
"""
Plot GPP
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pandas as pd
import datetime as dt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (22.02.2016)"
__email__   = "mdekauwe@gmail.com"

def main():

    fname = "outputs/twoleaf_AMB.csv"
    dfta = pd.read_csv(fname)

    fname = "outputs/mate_AMB.csv"
    dfma = pd.read_csv(fname)


    golden_mean = 0.6180339887498949
    width = 9
    height = width * golden_mean
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(hspace=0.1)
    fig.subplots_adjust(wspace=0.2)
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['font.size'] = 11
    plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['xtick.labelsize'] = 11
    plt.rcParams['ytick.labelsize'] = 11

    ax1 = fig.add_subplot(111)



    ax1.plot(dfma["apar"], dfma["gpp"], ls=" ", marker="o", lw=1.5,
             color="green",label="MATE-AMB")
    ax1.plot(dfta["apar"], dfta["gpp"], ls=" ", marker="o", lw=1.5,
             color="blue", label="2Leaf-AMB")
    ax1.legend(numpoints=1, loc="best")

    ax1.set_ylabel("GPP (g C m$^{-2}$ d$^{-1}$)")
    ax1.set_xlabel("aPAR (MJ m$^{-2}$ d$^{-1}$)")


    fig.savefig("crap.pdf", bbox_inches='tight', pad_inches=0.1)

def date_converter(*args):
    return dt.datetime.strptime(str(int(float(args[0]))) + " " +\
                                str(int(float(args[1]))), '%Y %j')

if __name__ == "__main__":

    main()
