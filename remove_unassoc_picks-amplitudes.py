#!/usr/bin/env python

"""
Python script to remove unassociated picks and amplitudes from SC3ML file
Stephen Hicks, Uni. Southampton, Oct. 2017
Usage: python remove_unassoc_picks-amplitudes.py infile > outfile
"""

from seiscomp3 import DataModel, IO
import sys

# Read in ep xml file
ar = IO.XMLArchive()
ar.open(sys.argv[1])
obj = ar.readObject()
ep = DataModel.EventParameters.Cast(obj)

# Make a list of arrival ID and magnitude IDss
arrivals = []
magnitudes = []
for i in range(0, ep.originCount()):
    for j in range(0, ep.origin(i).arrivalCount()):
        arrivals.append(ep.origin(i).arrival(j).pickID())
    for j in range(0, ep.origin(i).stationMagnitudeCount()):
        magnitudes.append(ep.origin(i).stationMagnitude(j).amplitudeID())

# Remove unassociated picks
i = 0
while i < ep.pickCount():
    if not ep.pick(i).publicID() in arrivals:
        ep.removePick(i)
    else:
        i += 1

# Remove unassociated amplitudes
i = 0
while i < ep.amplitudeCount():
    if not ep.amplitude(i).publicID() in magnitudes:
        ep.removeAmplitude(i)
    else:
        i += 1

# Write to xml file
ar = IO.XMLArchive()
ar.setFormattedOutput(True)
ar.create("-")
ar.writeObject(ep)
ar.close()
