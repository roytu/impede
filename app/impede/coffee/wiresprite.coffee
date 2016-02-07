class @WireSprite extends Sprite
    @constructSVG: (x1, y1, x2, y2) ->
        DA = window.DescArea()

        toDStr = (lst) ->
            d3.svg.line()
                  .x((d) -> return d.x)
                  .y((d) -> return d.y)
                  .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x1, "y" : y1 },
                    { "x" : x2, "y" : y2 }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("circle")
            .attr("cx", x1)
            .attr("cy", y1)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        svg
            .append("circle")
            .attr("cx", x2)
            .attr("cy", y2)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        return svg
