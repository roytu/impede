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
        @value_unit = Units::i
        @_mx = 0
        @_my = 0
        @_ghost = null
        @_svgs = []
        @first_mx = null
        @first_my = null

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
                when Elements.GND
                    GroundSprite = window.GroundSprite
                    @_ghost = GroundSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my))
                when Elements.V_SRC
                    VSrcSprite = window.VSrcSprite
                    @_ghost = VSrcSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my).concat(@value_text))
                when Elements.V_IN
                    VInSprite = window.VInSprite
                    @_ghost = VInSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my))
                when Elements.V_OUT
                    VOutSprite = window.VOutSprite
                    @_ghost = VOutSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my))
                when Elements.OPAMP
                    OpampSprite = window.OpampSprite
                    @_ghost = OpampSprite.constructSVG.apply(this, Grid.snapToGridFloor(mx, my))
                when Elements.WIRE
                    WireSprite = window.WireSprite
                    if @first_mx != null
                        pos = Grid.snapToGrid(@first_mx, @first_my)
                        pos = pos.concat(Grid.snapToGrid(mx, my))
                        @_ghost = WireSprite.constructSVG.apply(this, pos)

    addElement: (mx, my, v=0) ->
        switch @selected
            when Elements.RESISTOR
                @config.resistors.push([mx, my, v])
            when Elements.CAPACITOR
                @config.capacitors.push([mx, my, v])
            when Elements.INDUCTOR
                @config.inductors.push([mx, my, v])
            when Elements.GND
                @config.grounds.push([mx, my])
            when Elements.V_SRC
                @config.v_srcs.push([mx, my, v])
            when Elements.V_IN
                @config.v_ins.push([mx, my])
            when Elements.V_OUT
                @config.v_outs.push([mx, my])
            when Elements.OPAMP
                @config.opamps.push([mx, my])
            when Elements.WIRE
                pos = Grid.snapToGrid(@first_mx, @first_my)
                pos = pos.concat(Grid.snapToGrid(mx, my))
                @config.wires.push(pos)
        @updateSVGs()

    removeElement: (mx, my) ->
        # Explicitly remove HTML by rounding
        # TODO fix this
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
        for [x, y, v] in @config.capacitors
            @_svgs.push(CapacitorSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y).concat(v)))
        for [x, y, v] in @config.inductors
            @_svgs.push(InductorSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y).concat(v)))
        for [x, y] in @config.grounds
            @_svgs.push(GroundSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y)))
        for [x, y] in @config.v_ins
            @_svgs.push(VInSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y)))
        for [x, y] in @config.v_outs
            @_svgs.push(VOutSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y)))
        for [x, y] in @config.opamps
            @_svgs.push(OpampSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y)))
        for [x, y, v] in @config.v_srcs
            @_svgs.push(VSrcSprite.constructSVG.apply(this, Grid.snapToGridFloor(x, y).concat(v)))
        for [x1, y1, x2, y2] in @config.wires
            pos = Grid.snapToGrid(x1, y1).concat(Grid.snapToGrid(x2, y2))
            @_svgs.push(WireSprite.constructSVG.apply(this, pos))

    load: (jsonStr) ->
        State = window.State

        jsonStr ?= prompt("Paste your JSON!")
        if jsonStr?
            State.stop()
            State.config.fromString(jsonStr)
            @updateSVGs()

    getValue: ->
        Units.toValue(parseFloat(@value_text), @value_unit)
