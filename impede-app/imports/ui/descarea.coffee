class @DescArea
    instance = null
    constructor: ->
        if instance
            return instance
        else
            instance = this

        @msg = ""

        @x = 0
        @y = 0
        @w = $(window).width() - 30 - @x
        @h = $(window).height() - 10
        
        _svg = d3.select("body")
                  .append("svg")
                  .attr("position", "absolute")
                  .attr("width", @w)
                  .attr("height", @h)
                  .attr("style", "left: #{@x} px")

        @svg = _svg.append("g")
                   .attr("position", "absolute")
                   .attr("width", @w)
                   .attr("height", @h)

        @svg.append("rect")
            .attr("position", "absolute")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", @w)
            .attr("height", @h)
            .style("fill", "white")

        # Events
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
                     , Elements.GND
                     , Elements.V_IN
                     , Elements.V_OUT
                     , Elements.V_SRC
                           Metastate.addElement(d3.mouse(this)[0],
                                                d3.mouse(this)[1],
                                                Metastate.getValue())
                when Elements.WIRE
                    if Metastate.first_mx == null
                        # Pick first point
                        Metastate.first_mx = d3.mouse(this)[0]
                        Metastate.first_my = d3.mouse(this)[1]
                    else
                        # Draw wire
                        Metastate.addElement(d3.mouse(this)[0],
                                             d3.mouse(this)[1],
                                             Metastate.getValue())
                        Metastate.first_mx = null
                        Metastate.first_my = null
                when   Elements.DELETOR
                    Metastate.removeElement(d3.mouse(this)[0],
                                            d3.mouse(this)[1])
        )

    initialize: ->
        # Initialization of things after the grid
        # Messages
        bw = 200  # Box width
        bh = 20  # Box height per text
        bpad = 5  # Padding from right side of screen
        tmarg = 5  # Text offset
        
        @msgBox = @svg.append("rect")
            .attr("position", "absolute")
            .attr("x", @w - bw - bpad)
            .attr("y", @h - bh - bpad)
            .attr("width", bw)
            .attr("height", bh)
            .style("fill", "white")
            .style("stroke", "black")
            .style("opacity", 0)

        @msgText = @svg.append("text")
            .attr("x", @w - bw - bpad + tmarg)
            .attr("y", @h - bh - bpad + tmarg + 8)
            .attr("position", "absolute")
            .attr("width", bw)
            .attr("height", bh)
            .attr("font-size", "10px")
            .attr("font-family", "sans-serif")
            .attr("text-anchor", "left")

    addMessage: (msg) ->
        # TODO misnomer, actually replaces the message
        #
        # Add a string to the message box
        @msg = msg
        @msgText.text(msg)

        msgBox = @msgBox
        msgText = @msgText

        msgBox
            .style("opacity", 1)
            .transition()
            .duration(0)
        msgBox
            .style("opacity", 1)
            .transition()
            .delay(3000)
            .duration(200).style("opacity", 0)
        msgText
            .style("opacity", 1)
            .transition()
            .duration(0)
        msgText
            .style("opacity", 1)
            .transition()
            .delay(3000)
            .duration(200).style("opacity", 0)
