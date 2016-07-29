
""" Run for main test. """

from sound_handler import SoundHandler as SH
from config import Config
from filter_library import make_mxr_distortion_filter
from common_filters import LowPassFilter, NoninvertingOpAmpFilter
from signals import Signal

def noninverting_op_amp_test():
    amp_filter = NoninvertingOpAmpFilter.make(100, 100)
    input_signal = Signal.sine(0.1, 440, 1, 0)
    output_signal = amp_filter.execute(input_signal)
    amp_filter.plot_probes()

def lpf_test():
    lpf_filter = LowPassFilter.make(100, 100)
    input_signal = Signal.sine(0.1, 440, 1, 0)
    output_signal = lpf_filter.execute(input_signal)
    lpf_filter.plot_probes()

def stratocaster_test():
    #filename = Config.samples_dir + "clean_guitar.wav"
    filename = Config.samples_dir + "stratocaster.wav"

    mxr_filter = make_mxr_distortion_filter()
    input_signal = SH.load(filename, sampleperiod=Config.time_step, peak=1)
    output_signal = mxr_filter.execute(input_signal)

    print("Playing input...")
    SH.play(input_signal, bytespersample=2, peak=1)
    print("Playing output...")
    SH.play(output_signal, bytespersample=2, peak=1)

    SH.save(output_signal, Config.output_dir + "stratocasterout.wav", bytespersample=2, peak=1)

if __name__ == "__main__":
    noninverting_op_amp_test()
    #lpf_test()
    #stratocaster_test()
