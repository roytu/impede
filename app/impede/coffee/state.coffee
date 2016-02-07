class State
    # A State (singleton) is the current information of the world
    instance = null
    constructor: (@config) ->
        if instance
            return instance
        else
            instance = this

    start: ->
        Metastate.updateSVGs()

@State = new State()
