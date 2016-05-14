class @DescArea
    instance = null
    constructor: ->
        if instance
            return instance
        else
            instance = this

        SA = window.StatArea()

        @x = SA.w
        @y = 0
        @w = $(window).width() - 30 - @x
        @h = $(window).height() - 10
        
        _svg = d3.select("body")
                  .append("svg")
                  .attr("width", @w)
                  .attr("height", @h)
                  .attr("style", "left: #{@x} px")

        @svg = _svg.append("g")
                   .attr("width", @w)
                   .attr("height", @h)

        @svg.append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", @w)
            .attr("height", @h)
            .style("fill", "white")

        @svg.on("mousemove", (e) ->
            Metastate = window.Metastate()
            Metastate.updateGhost(d3.mouse(this)[0], d3.mouse(this)[1])
        )

        @svg.on("click", (e) ->
            Metastate = window.Metastate()
            switch Metastate.selected
                when   Elements.RESISTOR
                     , Elements.CAPACITOR
                     , Elements.INDUCTOR
                     , Elements.OPAMP
                     , Elements.V_IN
                     , Elements.V_OUT
                     , Elements.V_SRC
                           Metastate.addElement(d3.mouse(this)[0],
                                                d3.mouse(this)[1],
                                                Metastate.getValue())
        )
