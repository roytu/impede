
""" Module that takes in a circuit ID and an input sound, and creates a
    WAV file in the circuit's directory representing the output. """

import argparse

def get_input_signal(cid):
    """ Get the input signal from the circuit ID.

    Args:
        cid: circuit ID (integer)

    Returns:
        Signal object
    """
    # TODO
    pass

def get_filter(cid):
    """ Get the Filter object from the circuit ID.

    Args:
        cid: circuit ID (integer)

    Returns:
        Filter object
    """
    # TODO
    pass

def make_wave(cid):
    """ Save an output wav file in the circuit's directory, using the input
    wave in the document.

    Args:
        cid: circuit ID (integer)
    """
    input_signal = get_input_signal(cid)
    filt = get_filter(cid)
    output_signal = filt.execute(input_signal)

    # Note: This auto-normalizes by default
    SH.save(output_signal, "output.wav", bytespersample=2, peak=max(output_signal))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make some sounds.")
    parser.add_argument("cid", type=int, help="circuit ID")

    args = parser.parse_args()
    make_wave(args.cid, args.input_wav)
