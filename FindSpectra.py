import FileStuff as fs
import matplotlib.pyplot as plt
import detect_peaks as dp
import GUI as g


def findSpectra():
    wavFiles = fs.getWavFiles()
    cutoff = .05
    mph = 0
    mpd = 3000
    low = 5000
    high = 240000

    params = [cutoff, mph, mpd, low, high, False]

    for i in range(len(wavFiles)):
        freqs, amps = fs.getAmpsAndFreqs(wavFiles[i])
        fs.saveData(freqs, amps, wavFiles[i])

        while True:
            # make spectrum plot
            peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], params)
            g.guiInit(params)
            if params[5]:
                params[5] = False
                fs.saveSpectra(peakFreqs, peakAmps, "partials/peak_freqs_" + wavFiles[i][:len(wavFiles[i]) - 4], "partials/peak_amps_" + wavFiles[i][:len(wavFiles[i]) - 4])
                break


def plotMaxima(freqs, amps, filename, params):
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 22
    fig_size[1] = 15
    plt.rcParams["figure.figsize"] = fig_size

    plt.title("Spectrum for: " + filename)
    plt.xlabel("Frequency[HZ]")
    plt.ylabel("Amplitude")
    plt.plot(freqs, amps)
    maxima = dp.detect_peaks(amps, mph=params[1], mpd=params[2], show=False, valley=False, cutoff=params[0], low=params[3], high=params[4])
    # maxima = fixPeaks(amps, result)
    peakAmps = []
    peakFreqs = []
    for x in maxima:
        a = amps[x]
        f = freqs[x]
        peakAmps.append(a)
        peakFreqs.append(f)
    # plot vertical lines for local maxima
    for i in range(len(peakFreqs)):
        plt.axvline(x=peakFreqs[i], color='r')
        plt.text(peakFreqs[i] - 80, .8, 'f = ' + str(peakFreqs[i]), rotation=90)
    plt.axhline(y=params[0], color='g')

    if not(params[5]):
        plt.show()
    else:
        plt.savefig(fs.myPath + "spectrum_plots_with_maxima/" + filename[:len(filename)-4] + ".png")
        params[5] = True
    plt.close()
    return peakFreqs, peakAmps

def fixPeaks(amps, result):
    width = 4800
    keep = []
    for i in range(len(result)):
        maxAmp = max(amps[result[i]-width:result[i]+width])
        keep.append(amps.index(maxAmp))
    return keep



# takes a list of amplitudes a and list of frequencies f
# attempts to find the peaks and corresponding amplitudes in the list of data
def findPeaks(freqs, amps, cutoff, ignore):
    width = 5000 # the number of array bins to use for one search
    maxZeros = 10 # once this many zeroes are seen in the array, we must be over the peak
    temp = list(amps)
    peakFreqs = []
    peakAmps = []

    for i in range(len(temp)):
        if temp[i] < cutoff:
            temp[i] = 0

    nextStart = 0
    for i in range(int(len(temp)/width)):
        start = None
        end = None
        zeroCount = 0
        for j in range(width):
            curr = j + i*width
            if curr < nextStart:
                continue
            if temp[curr] > 0:
                zeroCount = 0
                if start is None:
                    start = curr
            elif temp[curr] == 0 and start is not None:
                if zeroCount >= maxZeros:
                    end = curr
                    break
                else:
                    zeroCount += 1
        if start is not None and end is not None:
            peakWidth = freqs[end]-freqs[start]
            print("width of peak: " + str(peakWidth))
            if freqs[start] > ignore:
                guy = amps[start:end]
                guy2 = freqs[start:end]
                maxAmp = max(amps[start:end])
                maxFreqInd = amps[start:end].index(maxAmp)+start
                maxFreq = freqs[maxFreqInd]
                peakFreqs.append(maxFreq)
                peakAmps.append(maxAmp)
            nextStart = end

    return peakFreqs, peakAmps


def findPeaksAlternate(freqs, amps, cutoff, ignore):
    maxZeros = 50 # once this many zeroes are seen in the array, we must be over the peak
    temp = list(amps)
    peakFreqs = []
    peakAmps = []

    for i in range(len(temp)):
        if temp[i] < cutoff:
            temp[i] = 0

    zeroCount = 0
    end = None
    start = None

    for j in range(len(freqs)):
        # global zeroCount
        # global start
        # global end
        if temp[j] > 0:
            zeroCount = 0
            if start is None:
                start = j
        elif temp[j] == 0 and start is not None:
            if zeroCount >= maxZeros:
                end = j-zeroCount
                peakWidth = freqs[end] - freqs[start]
                print("width of peak: " + str(peakWidth))
                if freqs[start] > ignore:
                    guy = amps[start:end]
                    guy2 = freqs[start:end]

                    # myFile2 = open("C:/Users/Brendan/Desktop/440amps.csv", 'w')
                    # for x in guy:
                    #     myFile2.write(str(x) + ',\n')
                    # myFile2.close()
                    #
                    # myFile2 = open("C:/Users/Brendan/Desktop/440freqs.csv", 'w')
                    # for x in guy2:
                    #     myFile2.write(str(x) + ',\n')
                    # myFile2.close()
                    #
                    # break

                    maxAmp = max(amps[start:end])
                    maxFreqInd = amps[start:end].index(maxAmp) + start
                    maxFreq = freqs[maxFreqInd]
                    peakFreqs.append(maxFreq)
                    peakAmps.append(maxAmp)
                end = None
                start = None
            else:
                zeroCount += 1

    return peakFreqs, peakAmps


def findOneSpectrum(fileName):
    freqs, amps = fs.getAmpsAndFreqs(fileName)
    fs.saveData(freqs, amps, fileName)

    cutoff = .1
    ignore = 3000

    # make spectrum plot
    peakFreqs, peakAmps = plotMaxima(freqs, amps, fileName, cutoff, ignore, False)

    ans = input("Change cutoff? (y/n)")

    while True:
        while ans != 'y' and ans != 'n':
            ans = input("Try again, Change cutoff? (y/n)")
        if ans == 'y':
            cutoff = float(input("new cutoff: "))
            ans2 = input("change ignore? (y,n)")
            if ans2 == 'y':
                ignore = float(input("new ignore: "))
            peakFreqs, peakAmps = plotMaxima(freqs, amps, fileName, cutoff, ignore, False)
            ans = input("Change cutoff? (y/n)")
        elif ans == 'n':
            ans2 = input("change ignore? (y,n)")
            if ans2 == 'y':
                ignore = float(input("new ignore: "))
                peakFreqs, peakAmps = plotMaxima(freqs, amps, fileName, cutoff, ignore, False)
                ans = input("Change cutoff? (y/n)")
                continue
            peakFreqs, peakAmps = plotMaxima(freqs, amps, fileName, cutoff, ignore, True)
            break

    return peakFreqs, peakAmps

