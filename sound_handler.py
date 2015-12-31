
""" Module containing methods to handle sounds. """

from pyaudio import PyAudio
import wave, struct

class SoundHandler(object):
    """ Static class with methods to input / output / play sounds """

    __temp = ".temp.wav"
    """ Filename for temporary wave files """

    @staticmethod
    def play(samples, framerate=44100, bytespersample=1, peak=1):
        """ Play a vector as a sound.

        Code stolen shamelessly from:
            http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python

        Args:
            samples : vector of floats
            framerate : samples per second
            bytespersample : bytes per sample
            peak : value corresponding to the largest magnitude
        """
        SoundHandler.save(samples, SoundHandler.__temp, framerate, bytespersample, peak)

        chunk = 1024

        f = wave.open(SoundHandler.__temp, "rb")
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        data = f.readframes(chunk)

        while data != '':
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    @staticmethod
    def save(samples, filename, framerate=44100, bytespersample=1, peak=1):
        """ Save samples as a WAV file.

        Args:
            samples : vector of floats
            filename : string
            framerate : samples per second
            bytespersample : bytes per sample
            peak : value corresponding to the largest magnitude
        """
        wav_writer = wave.open(filename, "wb")
        wav_writer.setnchannels(1)  # Mono
        wav_writer.setsampwidth(bytespersample)  # Number of bytes per sample
        wav_writer.setframerate(framerate)  # Sample rate
        def sample_to_byte(s):
            s = int((float(s) / peak) * 128) + 128
            return chr(abs(s))
        data = "".join([sample_to_byte(s) for s in samples])
        wav_writer.writeframes(data)
        wav_writer.close()
    @staticmethod
    def load(filename, peak=1):
        """ Load WAV file as samples.

        Only reads mono, little-endian files.

        Args:
            samples : vector of floats
            filename : string
            peak : value corresponding to the largest magnitude

        Returns:
            samples (as list of floats)
        """
        wav_reader = wave.open(filename, "rb")
        bytespersample = wav_reader.getsampwidth()
        length = wav_reader.getnframes()
        if bytespersample == 2:
            bytefmt = "<h"
        elif bytespersample == 1:
            bytefmt = "<b"
        else:
            print("WARNING: Unsupported bytespersample")
        def frame_to_sample(f):
            sample = float(struct.unpack(bytefmt, f)[0])
            # Renormalize
            sample /= 2 ** ((bytespersample * 8) - 1)
            sample *= peak
            return sample
        samples = []
        for _ in range(length):
            frame = wav_reader.readframes(1)
            sample = frame_to_sample(frame)
            samples.append(sample)
        wav_reader.close()
        return samples
