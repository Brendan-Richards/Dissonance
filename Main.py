import FindSpectra as fSpec
import FindDissonanceCurves as FDC
import FileStuff as fs
import matplotlib.pyplot as plt
import detect_peaks as dp

# xyz = fSpec.findSpectra()

# abc = FDC.findCurves()

def doOne(fileName):
    freqs, amps = fSpec.findOneSpectrum(fileName)
    # for i in range(len(freqs)):
    #     freqs[i] = (i+1)*440
    FDC.findOneCurve(freqs, amps, fileName)

# a = doOne('Harpsichord_01.wav')

def testSmoothing():
    freqs, amps = fs.getAmpsAndFreqs('Piano Mono_01.wav')
    #amps = fs.getSmoothed('smoothed_data_harpsichord2')
    maxima = dp.detect_peaks(amps, mph=0.05, mpd=7000, show=True, valley=False)
    for i in range(len(maxima)):
        if freqs[maxima[i]] > 10000:
            maxima = maxima[:i]
            break
    for i in range(len(maxima)):
        if freqs[maxima[i]] > 400:
            maxima = maxima[i:]
            break
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


testSmoothing()