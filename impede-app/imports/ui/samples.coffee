
# Module stores a directory of samples
# TODO load from samples.json

class @Samples
    sine = 0
    stratocaster = 1
    cleanguitar = 2

    @samples = [sine, stratocaster, cleanguitar]

    @getDir: (sample) ->
        switch sample
            when sine
                return "../../../../samples/sine.wav"
            when stratocaster
                return "../../../../samples/stratocaster.wav"
            when cleanguitar
                return "../../../../samples/cleanguitar.wav"

    @getName: (sample) ->
        switch sample
            when sine
                return "sine.wav"
            when stratocaster
                return "stratocaster.wav"
            when cleanguitar
                return "cleanguitar.wav"
