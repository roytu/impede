class @Metastate
    # A Metastate (singleton) handles all the information about the current user's
    # settings; i.e. currently selected element
    instance = null
    constructor: (@config) ->
        if instance
            return instance
        else
            instance = this
        @selected = null
        @value_text = ""
        @value_unit = Units.i
        @_mx = 0
        @_my = 0
        @_ghost = null
        @_svgs = []

    initialize: ->
        DA = window.DescArea()
        @_ghost = DA.svg.append("svg")

    updateGhost: (mx=@_mx, my=@_my) ->
        if @_ghost?
            @_ghost.remove()

        if @selected?
            @_mx = mx
            @_my = my
            switch @selected
                when Elements.RESISTOR
                    ResistorSprite = window.ResistorSprite
                    @_ghost = ResistorSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my).concat(@value_text))
                when Elements.CAPACITOR
                    CapacitorSprite = window.CapacitorSprite
                    @_ghost = CapacitorSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my).concat(@value_text))
                when Elements.INDUCTOR
                    InductorSprite = window.InductorSprite
                    @_ghost = InductorSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my).concat(@value_text))

    addElement: (mx, my, v=0) ->
        switch @selected
            when Elements.RESISTOR
                @config.resistors.push([mx, my, v])

        @updateSVGs()

    removeElement: (mx, my) ->
        # Explicitly remove HTML by rounding
        Grid = window.Grid
        State = window.State

        mpos = Grid.getGridPosNoround(mx, my)

        arr = State.config.htmls
        for i in [0..arr.length]
            x = arr[i]
            if (Math.sqrt(Math.pow(x[0] - mpos[0], 2) + Math.pow(x[1] - mpos[1], 2)) < 1)
                arr.splice(i, 1)
                @updateSVGs()
                return

        pos = Grid.getGridPos(mx, my)

        elementArrays = [State.config.args,
                         State.config.results,
                         State.config.sources,
                         State.config.sinks,
                         State.config.hwalls,
                         State.config.vwalls]
        for j in [0..elementArrays.length]
            arr = elementArrays[j]
            for i in [0..arr.length]
                x = arr[i]
                if x[0] == pos[0] && x[1] == pos[1]
                    arr.splice(i, 1)
                    @updateSVGs()
                    return

    updateSVGs: ->
        @_svgs.forEach( (svg) ->
            svg.remove()
        )
        @_svgs = []
        # Redraw everything
        for [x, y, v] in @config.resistors
            @_svgs.push(ResistorSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y).concat(v)))

    load: (jsonStr) ->
        State = window.State

        jsonStr ?= prompt("Paste your JSON!")
        if jsonStr?
            State.stop()
            State.config.fromString(jsonStr)
            @updateSVGs()

    getValue: ->
        Units.toValue(parseFloat(@value_text), @value)
