import FindSpectra as fSpec
import FindDissonanceCurves as FDC

xyz = fSpec.findSpectra()

abc = FDC.findCurves()

def doOne(fileName):
    freqs, amps = fSpec.findOneSpectrum(fileName)
    # for i in range(len(freqs)):
    #     freqs[i] = (i+1)*440
    FDC.findOneCurve(freqs, amps, fileName)

# a = doOne('Alto Sax_01.wav')

