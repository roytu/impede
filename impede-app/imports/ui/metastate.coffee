class @Metastate
    # A Metastate (singleton) handles all the information about the current user's
    # settings; i.e. currently selected element
    instance = null
    constructor: (@id) ->
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

        @sessions = new Meteor.Collection("sessions")
        Meteor.subscribe("sessions", {
            onReady: =>
                @config = new Configuration()
                if @id != null
                    match = @sessions.findOne(@id)
                    @config.fromString(JSON.stringify(match["config"]))
                    @updateSVGs()
        })
        
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
                    @_ghost = VSrcSprite.constructSVG.apply(this, Grid.snapToGrid(mx, my).concat(@value_text))
                when Elements.V_IN
                    VInSprite = window.VInSprite
                    @_ghost = VInSprite.constructSVG.apply(this, Grid.snapToGrid(mx, my))
                when Elements.V_OUT
                    VOutSprite = window.VOutSprite
                    @_ghost = VOutSprite.constructSVG.apply(this, Grid.snapToGrid(mx, my))
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
        [x, y] = Grid.getGridPosFloor(mx, my)
        [rx, ry] = Grid.getGridPos(mx, my)
        switch @selected
            when Elements.RESISTOR
                @config.resistors.push([x, y, v])
            when Elements.CAPACITOR
                @config.capacitors.push([x, y, v])
            when Elements.INDUCTOR
                @config.inductors.push([x, y, v])
            when Elements.GND
                @config.grounds.push([x, y])
            when Elements.V_SRC
                @config.v_srcs.push([rx, ry, v])
            when Elements.V_IN
                @config.v_ins.push([rx, ry])
            when Elements.V_OUT
                @config.v_outs.push([rx, ry])
            when Elements.OPAMP
                @config.opamps.push([x, y])
            when Elements.WIRE
                pos = Grid.getGridPos(@first_mx, @first_my)
                pos = pos.concat(Grid.getGridPos(mx, my))
                @config.wires.push(pos)
        @updateSVGs()

    removeElement: (mx, my) ->
        # Explicitly remove HTML by rounding
        mpos = Grid.getGridPosNoround(mx, my)
        pos = Grid.getGridPos(mx, my)

        # Delete wires
        arr = @config.wires
        if arr.length > 0
            for i in [0..arr.length-1]
                x = arr[i]

                # Check if mouse position is close enough to pos
                # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
                [x0, y0] = [mpos[0], mpos[1]]
                [x1, y1] = [x[0], x[1]]
                [x2, y2] = [x[2], x[3]]
                num = Math.abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
                den = Math.sqrt(Math.pow(y2 - y1, 2) + Math.pow(x2 - x1, 2))
                dist = num / den
                
                if dist < 0.5
                    arr.splice(i, 1)
                    @updateSVGs()
                    return

        # Delete normal elements
        elementArrays = [@config.resistors,
                         @config.capacitors,
                         @config.inductors,
                         @config.opamps,
                         @config.grounds,
                         @config.v_srcs,
                         @config.v_ins,
                         @config.v_outs]
        for arr in elementArrays
            if arr.length > 0
                for i in [0..arr.length - 1]
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
            @_svgs.push(ResistorSprite.constructSVG.apply(this, Grid.getDrawPos(x, y).concat(v)))
        for [x, y, v] in @config.capacitors
            @_svgs.push(CapacitorSprite.constructSVG.apply(this, Grid.getDrawPos(x, y).concat(v)))
        for [x, y, v] in @config.inductors
            @_svgs.push(InductorSprite.constructSVG.apply(this, Grid.getDrawPos(x, y).concat(v)))
        for [x, y] in @config.grounds
            @_svgs.push(GroundSprite.constructSVG.apply(this, Grid.getDrawPos(x, y)))
        for [x, y] in @config.v_ins
            @_svgs.push(VInSprite.constructSVG.apply(this, Grid.getDrawPos(x, y)))
        for [x, y] in @config.v_outs
            @_svgs.push(VOutSprite.constructSVG.apply(this, Grid.getDrawPos(x, y)))
        for [x, y] in @config.opamps
            @_svgs.push(OpampSprite.constructSVG.apply(this, Grid.getDrawPos(x, y)))
        for [x, y, v] in @config.v_srcs
            @_svgs.push(VSrcSprite.constructSVG.apply(this, Grid.getDrawPos(x, y).concat(v)))
        for [x1, y1, x2, y2] in @config.wires
            pos = Grid.getDrawPos(x1, y1).concat(Grid.getDrawPos(x2, y2))
            @_svgs.push(WireSprite.constructSVG.apply(this, pos))

    save: ->
        if @id == null
            @sessions.insert({ "config" : @config }, (err, id) =>
                @id = id
                FlowRouter.go("/:id", { "id": @id })
            )
        else
            if @sessions.find(@id).count == 0
                @sessions.insert(@id, { "config" : @config })
            else
                @sessions.update(@id, { "config" : @config })

    loadInput: ->
        # Allows the user to load a WAV file
        # TODO
        return

    load: (jsonStr) ->
        jsonStr ?= prompt("Paste your JSON!")
        if jsonStr?
            @updateSVGs()

    getValue: ->
        if @value_text == ""
            return 0
        else
            return Units.toValue(parseFloat(@value_text), @value_unit)
