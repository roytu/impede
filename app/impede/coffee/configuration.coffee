class @Configuration
    constructor: ->
        @wires = []
        @resistors = []
        @capacitors = []
        @inductors = []
        @opamps = []

    addWire: (x1, y1, x2, y2) ->
        if not contains(@wires, [x1, y1, x2, y2])
            @wires.push([x1, y1, x2, y2])

    toString: ->
        JSON.stringify([])

    fromString: (str) ->
        pr = JSON.parse(str)
        return
