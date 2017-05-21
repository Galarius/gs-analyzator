import sys, getopt
import wave
import numpy as np

import gs_plotter as plt
from gs_indicators import *

# based on: https://github.com/mgeier/python-audio/blob/master/audio-files/utility.py
def pcm_2_float(sig, dtype='float32'):
    """
    Convert PCM signal to floating point with a range from -1 to 1.
    :param sig: Input array, must have (signed) integral type.
    :param dtype: Desired (floating point) data type.
    :return: Normalized floating point data.
    """
    sig = np.asarray(sig)
    if sig.dtype.kind != 'i':
        raise TypeError("'sig' must be an array of signed integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be floating point type")
    return sig.astype(dtype) / dtype.type(np.iinfo(sig.dtype).max)

def float_2_pcm(sig, dtype='int16'):
    """
    Convert floating point signal with a range from -1 to 1 to PCM.
    :param sig: Input array, must have floating point type.
    :param dtype: Desired (integer) data type. [optional]
    :return: integer data.
    """
    sig = np.asarray(sig)
    if sig.dtype.kind != 'f':
        raise TypeError("'sig' must be a float array")
    dtype = np.dtype(dtype)
    if dtype.kind != 'i':
        raise TypeError("'dtype' must be signed integer type")
    return (sig * np.iinfo(dtype).max).astype(dtype)

def audio_decode(in_data, channels, dtype=np.float32):
    result = np.fromstring(in_data, dtype=dtype)
    if dtype == np.float32:
        result = float_2_pcm(result, np.int16)
    chunk_length = len(result) / channels
    output = np.reshape(result, (chunk_length, channels))
    l, r = np.copy(output[:, 0]), np.copy(output[:, 1])
    return l, r

def audio_encode(samples, dtype=np.float32):
    if dtype == np.float32:
        l = pcm_2_float(samples[0], np.float32)
        r = pcm_2_float(samples[1], np.float32)
    else:
        l, r, = samples
    interleaved = np.array([l, r]).flatten('F')
    out_data = interleaved.astype(dtype).tostring()
    return out_data


def main(argv):
    input_container_original = ''
    input_container_modified = ''
    opts, args = getopt.getopt(argv, "o:m:", ["ofile=", "mfile="])

    if not len(opts):
        input_container_original = 'wav/orig_in.wav'
        input_container_modified = 'wav/modified_in.wav'
        #sys.exit(1)

    for opt, arg in opts:
        if opt in ['-o', '--ofile']:
            input_container_original = arg
        if opt in ['-m', '--mfile']:
            input_container_modified = arg

    # read original
    original_wave_file = wave.open(input_container_original, 'rb')
    o_in_data = original_wave_file.readframes(original_wave_file.getnframes())
    o_left, o_right = audio_decode(o_in_data, original_wave_file.getnchannels(), np.int16)
    # read modified
    modified_wave_file = wave.open(input_container_modified, 'rb')
    m_in_data = modified_wave_file.readframes(modified_wave_file.getnframes())
    m_left, m_right = audio_decode(m_in_data, modified_wave_file.getnchannels(), np.int16)

    # # write original
    # o_processed_data = audio_encode((o_left, o_right), np.int16)
    # original_wave_file_out = wave.open("wav/orig_out.wav", 'wb')
    # original_wave_file_out.setnchannels(original_wave_file.getnchannels())
    # original_wave_file_out.setsampwidth(original_wave_file.getsampwidth())
    # original_wave_file_out.setframerate(original_wave_file.getframerate())
    # original_wave_file_out.writeframes(o_processed_data)
    # original_wave_file_out.close()
    # # write modified
    # m_processed_data = audio_encode((m_left, m_right), np.int16)
    # modified_wave_file_out = wave.open("wav/modified_out.wav", 'wb')
    # modified_wave_file_out.setnchannels(modified_wave_file.getnchannels())
    # modified_wave_file_out.setsampwidth(modified_wave_file.getsampwidth())
    # modified_wave_file_out.setframerate(modified_wave_file.getframerate())
    # modified_wave_file_out.writeframes(m_processed_data)
    # modified_wave_file_out.close()


    original_wave_file.close()
    modified_wave_file.close()

    print "MD  {0}".format(MD(o_right, m_right))
    print "AD {0}".format(AD(o_right, m_right))
    print "NAD {0}".format(NAD(o_right, m_right))
    print "MSE {0}".format(MSE(o_right, m_right))
    print "NMSE {0}".format(NMSE(o_right, m_right))
    print "Lp  {0}".format(LpNorm(o_right, m_right, 2))
    print "SNR {0}".format(SNR(o_right, m_right))
    print "PSNR {0}".format(PSNR(o_right, m_right))
    print "AF  {0}".format(AF(o_right, m_right))
    print "NC  {0} (original: {1})".format(NC(o_right, m_right), NC(o_right, o_right))
    print "CQ  {0} (original: {1})".format(CQ(o_right, m_right), CQ(o_right, o_right))
    print "SC  {0}".format(SC(o_right, m_right))

    #print all(o_right, m_right)

    plt.save_plots(o_right, m_right)
    plt.save_plots(o_right, m_right, True)

    print "Done!"

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)