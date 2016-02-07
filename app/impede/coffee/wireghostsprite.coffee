class @WireGhostSprite extends Sprite
    @constructSVG: (x1, y1, x2, y2) ->
        DA = window.DescArea()
    
        svg = DA.svg.append("g")
        svg
            .append("circle")
            .attr("cx", x1)
            .attr("cy", y1)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        return svg
