from scipy import fftpack
import sounddevice as sd
import numpy as np
import time

import queue

q = queue.Queue()

SAMPLE_RATE = 44100

duration = 10
sd.default.samplerate = SAMPLE_RATE



def spectral_properties(y: np.ndarray, fs: int) -> dict:
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    spec = np.abs(spec)
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    sd = np.sqrt(np.sum(amp * ((freq - mean) ** 2)))
    amp_cumsum = np.cumsum(amp)
    median = freq[len(amp_cumsum[amp_cumsum <= 0.5]) + 1]
    mode = freq[amp.argmax()]
    Q25 = freq[len(amp_cumsum[amp_cumsum <= 0.25]) + 1]
    Q75 = freq[len(amp_cumsum[amp_cumsum <= 0.75]) + 1]
    IQR = Q75 - Q25
    z = amp - amp.mean()
    w = amp.std()
    skew = ((z ** 3).sum() / (len(spec) - 1)) / w ** 3
    kurt = ((z ** 4).sum() / (len(spec) - 1)) / w ** 4

    result_d = {
        'mean': mean,
        'sd': sd,
        'median': median,
        'mode': mode,
        'Q25': Q25,
        'Q75': Q75,
        'IQR': IQR,
        'skew': skew,
        'kurt': kurt
    }

    return result_d


def print_sound(indata, outdata, frames, time):

    data = indata
    
    volume_norm = np.linalg.norm(data)*10

    


    start_point = 0#int(SAMPLE_RATE * start_time / 1000)
    end_point = data.size#int(SAMPLE_RATE * end_time / 1000)
    #length = (end_time - start_time) / 1000
    counter = 0
    for i in range(start_point, end_point):
        if data[i] < 0 and data[i+1] > 0:
            counter += 1
    print(counter/10)

    #print(volume_norm)

    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(w.size)
    #print(freqs.min(), freqs.max())
        # (-0.5, 0.499975)

        # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * SAMPLE_RATE)

    

    #print(freq_in_hertz)
        #freq_norm = freq_in_hertz/10
    #print(str(freq_in_hertz) + "HZ")
        #print("|" * int(freq_norm))
        #print(indata)
        #print("|" * int(volume_norm))

    


    

stream = sd.InputStream(callback=print_sound, channels=1)
with stream:
    while 1:
        time.sleep(1)
        pass

input()
    
