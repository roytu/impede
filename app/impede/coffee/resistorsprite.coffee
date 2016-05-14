class @ResistorSprite extends Sprite
    @constructSVG: (x, y, v) ->
        DA = window.DescArea()

        toDStr = (lst) ->
            return d3.svg.line()
                    .x((d) -> return d.x)
                    .y((d) -> return d.y)
                    .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize()        , "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.75 , "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.625, "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.375, "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.125, "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.125, "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.375, "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.625, "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.75 , "y" : y                            },
                    { "x" : x + Grid.getTickSize()        , "y" : y                            }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("circle")
            .attr("cx", x - Grid.getTickSize())
            .attr("cy", y)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        svg
            .append("circle")
            .attr("cx", x + Grid.getTickSize())
            .attr("cy", y)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        svg.valueText = svg.append("text")
            .attr("x", x)
            .attr("y", y - Grid.getTickSize())
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .classed("text", true)
            .attr("shape-rendering", "crispEdges")
            .style("font-size", "16px")
        svg.updateText = (v) ->
            svg.valueText.text("#{v} Ω")
        svg.updateText(v)
        return svg
