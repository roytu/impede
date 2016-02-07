
""" Run for main test. """

from sound_handler import SoundHandler as SH
from config import Config
from filter_library import make_mxr_distortion_filter

if __name__ == "__main__":
    #filename = Config.samples_dir + "clean_guitar.wav"
    filename = Config.samples_dir + "stratocaster.wav"

    mxr_filter = make_mxr_distortion_filter()
    input_signal = SH.load(filename, sampleperiod=Config.time_step, peak=1)
    output_signal = mxr_filter.execute(input_signal)
    #amp_filter = NoninvertingOpAmpFilter.make(100, 100)
    #input_signal = Signal.sine(1, 440, 1, 0)
    #output_signal = amp_filter.execute(input_signal)
    mxr_filter.plot_probes()

    #output_signal = amp_filter.execute(input_signal)
    print("Playing input...")
    SH.play(input_signal, bytespersample=2, peak=1)
    print("Playing output...")
    SH.play(output_signal, bytespersample=2, peak=1)
    SH.save(output_signal, Config.output_dir + "stratocasterout.wav", bytespersample=2, peak=1)
