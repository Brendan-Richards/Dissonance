import FindSpectra as fSpec
import FindDissonanceCurves as FDC
import FileStuff as fs
import matplotlib.pyplot as plt
import detect_peaks as dp
import os

xyz = fSpec.findSpectra()

abc = FDC.findCurves()

# def plotPairs():
#     vals1 = fs.getDissonanceVals('Alto Sax_01')
#     vals2 = fs.getDissonanceVals('Piano Mono_01')
#
#     plt.plot(vals1, vals2)
#     plt.xlabel("Alto Sax Dissonance")
#     plt.ylabel("Accordion Dissonance")
#     plt.show()
#
# plotPairs()

sdfs = FDC.test()






def doOne(fileName):
    freqs, amps = fSpec.findOneSpectrum(fileName)
    FDC.findOneCurve(freqs, amps, fileName)

# a = doOne('Harpsichord_01.wav')

def testSmoothing():
    freqs, amps = fs.getAmpsAndFreqs('Piano Mono_01.wav')
    # amps = fs.getSmoothed('smoothed_data_harpsichord2')
    low = 9900
    high = 240000
    maxima = dp.detect_peaks(amps, mph=0.05, mpd=7000, show=False, valley=False, low=low, high=high)
    peakAmps = []
    peakFreqs = []
    for x in maxima:
        peakAmps.append(amps[x])
        peakFreqs.append(freqs[x])
        print(freqs[x])
    for i in range(len(maxima)):
        plt.axvline(x=freqs[maxima[i]], color='r')
    print(len(maxima))
    plt.plot(freqs, amps)
    plt.show()
    FDC.findOneCurve(peakFreqs, peakAmps, 'Piano Mono_01.wav')


# testSmoothing()