import numpy as np
import wave
import matplotlib.pyplot as plt


def H_freqs(n, m, f0):
    f = []
    for nn in range(1, n+1):
        for mm in range(nn+1, m+1):
            f.append(f0*(1.0/(nn*nn) - 1.0/(mm*mm)))
    return np.array(f)


if __name__ == "__main__":

    sampleRate = 44100

    length = 10.0
    nsamps = int(length*sampleRate)

    timeSeries = np.empty(nsamps, dtype=np.int16)

    Amax = np.iinfo(np.int16).max
    t = np.linspace(0.0, length, num=nsamps, endpoint=False)

    A1 = 0.3

    timeSeriesF = np.zeros(nsamps)
    fs = H_freqs(5, 100, 440)
    print(fs.min(), fs.max())
    for f in fs:
        phi0 = np.random.random(1)
        timeSeriesF += np.sin(2*np.pi*(f*t+phi0))
    timeSeriesF *= A1/timeSeriesF.max()
    timeSeries[:] = Amax * timeSeriesF

    print(timeSeries.min(), timeSeries.max(), timeSeries.mean())

    f = wave.open('sound.wav', 'wb')
    nchannels = 1
    sampwidth = 2
    framerate = sampleRate
    nframes = nsamps
    comptype = "NONE"
    compname = 'none'
    params = (nchannels, sampwidth, framerate, nframes, comptype, compname)
    f.setparams(params)
    f.writeframes(np.getbuffer(timeSeries))
    f.close()
    print("sound.wav Saved")

    z = np.fft.rfft(timeSeriesF)
    spec = np.abs(z)
    nf = np.fft.rfftfreq(len(timeSeriesF), 1.0/sampleRate)
    phi = np.arctan2(z.imag, z.real)

    human = (nf > 15) & (nf < 20000)

    fig, ax = plt.subplots(3, 1, figsize=(12, 9))
    ax[0].plot(t, timeSeriesF)
    ax[1].plot(nf[human], spec[human])
    ax[2].plot(nf[human], phi[human])
    ax[1].set_xscale('log')
    ax[2].set_xscale('log')
    ax[0].set_xlabel('Time (seconds)')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[2].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Amplitude')
    ax[1].set_ylabel('Amplitude')
    ax[2].set_ylabel('Phase')
    fig.tight_layout()
    fig.savefig("sound.png")
