import FileStuff as fs
import matplotlib.pyplot as plt


def findSpectra():
    wavFiles = fs.getWavFiles()
    cutoff = .2
    ignore = 400

    for i in range(len(wavFiles)):
        freqs, amps = fs.getAmpsAndFreqs(wavFiles[i])

        # make spectrum plot
        peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], cutoff, ignore, False)

        ans = input("Change cutoff? (y/n)")

        while True:
            while ans != 'y' and ans != 'n':
                ans = input("Try again, Change cutoff? (y/n)")
            if ans == 'y':
                cutoff = float(input("new cutoff: "))
                ans2 = input("change ignore? (y,n)")
                if ans2 == 'y':
                    ignore = float(input("new ignore: "))
                peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], cutoff, ignore, False)
                ans = input("Change cutoff? (y/n)")
            elif ans == 'n':
                ans2 = input("change ignore? (y,n)")
                if ans2 == 'y':
                    ignore = float(input("new ignore: "))
                    peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], cutoff, ignore, False)
                    ans = input("Change cutoff? (y/n)")
                    continue
                peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], cutoff, ignore, True)
                break

        fs.saveSpectra(peakFreqs, peakAmps, "partials/peak_freqs_" + wavFiles[i][:len(wavFiles[i])-4], "partials/peak_amps_" + wavFiles[i][:len(wavFiles[i])-4])



def plotMaxima(freqs, amps, filename, cutoff, ignore, save):
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
    peakFreqs, peakAmps = findPeaksAlternate(freqs, amps, cutoff, ignore)
    # plot vertical lines for local maxima
    for i in range(len(peakFreqs)):
        plt.axvline(x=peakFreqs[i], color='r')
        plt.text(peakFreqs[i] - 80, .8, 'f = ' + str(peakFreqs[i]), rotation=90)
    plt.axhline(y=cutoff, color='g')

    if not(save):
        plt.show()
    else:
        plt.savefig(fs.myPath + "spectrum_plots_with_maxima/" + filename[:len(filename)-4] + ".png")
    plt.close()
    return peakFreqs, peakAmps


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
        global zeroCount
        global start
        global end
        if temp[j] > 0:
            zeroCount = 0
            if start is None:
                start = j
        elif temp[j] == 0 and start is not None:
            if zeroCount >= maxZeros:
                end = j
                peakWidth = freqs[end] - freqs[start]
                print("width of peak: " + str(peakWidth))
                if freqs[start] > ignore:
                    guy = amps[start:end]
                    guy2 = freqs[start:end]
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

    cutoff = .2
    ignore = 400

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

