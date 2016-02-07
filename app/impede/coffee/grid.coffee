class Grid extends Drawable
    # A Grid (singleton) is a type of Drawable that draws a grid
    instance = null
    constructor: ->
        if instance
            return instance
        else
            instance = this
        @tickCount = 26
        @minTickCount = 10
        @maxTickCount = 50
        @xAxisGrid = null
        @yAxisGrid = null
        @svgXLines = null
        @svgYLines = null

    initialize: ->
        DA = window.DescArea()

        scale = d3.scale.linear()
                  .domain([-1, 1])
                  .range([-1, 1])

        xAxis = d3.svg.axis()
                  .scale(scale)
                  .tickFormat("")
                  .orient("bottom")

        yAxis = d3.svg.axis()
                  .scale(scale)
                  .tickFormat("")
                  .orient("right")

        @xAxisGrid = xAxis
                   .tickSize(DA.h)
                   .tickValues(d3.range(0, DA.w, @getTickSize()))

        @yAxisGrid = yAxis
            .tickSize(DA.w)
            .tickValues(d3.range(0, DA.h, @getTickSize()))

        @svgXLines = DA.svg.append("g")
                           .classed("grid", true)
                           .call(@xAxisGrid)

        @svgYLines = DA.svg.append("g")
                           .classed("grid", true)
                           .call(@yAxisGrid)

    redraw: ->
        DA = window.DescArea()

        @xAxisGrid.tickValues(d3.range(0, DA.w, @getTickSize()))
        @yAxisGrid.tickValues(d3.range(0, DA.h, @getTickSize()))
        @svgXLines.call(@xAxisGrid)
        @svgYLines.call(@yAxisGrid)

    zoomIn: ->
        @tickCount-- if @tickCount > @minTickCount

    zoomIn: ->
        @tickCount++ if @tickCount < @maxTickCount

    getTickSize: ->
        # Return the size of grid squares (in pixels)
        DA = window.DescArea()
        Math.min(DA.w, DA.h) / @tickCount

    getDrawPos: (x, y) ->
        # Converts grid coordinates to drawable coordinates
        [x * @getTickSize(), y * @getTickSize()]

    getGridPos: (x, y) ->
        # Converts drawable coordinates to grid coordinates
        [Math.round(x / @getTickSize()), Math.round(y / @getTickSize())]

    getGridPosFloor: (x, y) ->
        # Converts drawable coordinates to grid coordinates (rounding down)
        [Math.floor(x / @getTickSize()), Math.floor(y / @getTickSize())]

    getGridPosNoround: (x, y) ->
        # Converts drawable coordinates to grid coordinates (without rounding)
        [x / @getTickSize(), y / @getTickSize()]

    snapToGrid: (x, y) ->
        @getDrawPos.apply(this, @getGridPos(x, y))

    snapToGridFloor: (x, y) ->
        @getDrawPos.apply(this, @getGridPosFloor(x, y))

@Grid = new Grid()
