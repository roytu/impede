
# Configuration.coffee
#
# Structure that holds information about the state of the field
# Also has functions that support serialization

class @Configuration
    constructor: ->
        @wires = []
        @resistors = []
        @capacitors = []
        @inductors = []
        @opamps = []
        @grounds = []
        @v_srcs = []
        @v_ins = []
        @v_outs = []

        @sample = null

    addWire: (x1, y1, x2, y2) ->
        if not contains(@wires, [x1, y1, x2, y2]) and (x1 != x2 and y1 != y2)
            @wires.push([x1, y1, x2, y2])

    toString: ->
        JSON.stringify({
            wires: @wires,
            resistors: @resistors,
            capacitors: @capacitors,
            inductors: @inductors,
            opamps: @opamps,
            grounds: @grounds,
            v_srcs: @v_srcs,
            v_ins: @v_ins,
            v_outs: @v_outs
        })

    fromString: (str) ->
        pr = JSON.parse(str)
        @wires = pr["wires"]
        @resistors = pr["resistors"]
        @capacitors = pr["capacitors"]
        @inductors = pr["inductors"]
        @opamps = pr["opamps"]
        @grounds = pr["grounds"]
        @v_srcs = pr["v_srcs"]
        @v_ins = pr["v_ins"]
        @v_outs = pr["v_outs"]

        @sample = pr["sample"]
