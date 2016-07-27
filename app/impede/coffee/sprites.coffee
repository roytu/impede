class @Sprite
    # A Sprite supports a constructSVG function that returns an SVG generator
    constructor: ->
    @constructSVG: ->

class @CapacitorSprite extends Sprite
    @constructSVG: (x, y, v) ->
        DA = window.DescArea()

        if v == ""
            v = 0
        else
            v = parseFloat(v)
        [v, us] = Units.pretty_resize(v)

        toDStr = (lst) ->
            return d3.svg.line()
                    .x((d) -> return d.x)
                    .y((d) -> return d.y)
                    .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize()      , "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.5, "y" : y                            }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 0.5, "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.5, "y" : y + Grid.getTickSize() * 0.5 }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x + Grid.getTickSize() * 0.5, "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.5, "y" : y + Grid.getTickSize() * 0.5 }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x + Grid.getTickSize() * 0.5, "y" : y                            },
                    { "x" : x + Grid.getTickSize()      , "y" : y                            }
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
            if v == ""
                v = "0"
            svg.valueText.text("#{v.toFixed(1)} #{us}F")
        svg.updateText(v)
        return svg

class @GroundSprite extends Sprite
    @constructSVG: (x, y) ->
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
                    { "x" : x, "y" : y },
                    { "x" : x, "y" : y + Grid.getTickSize() * 0.5 }
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 0.5, "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.5, "y" : y + Grid.getTickSize() * 0.5 },
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 0.375, "y" : y + Grid.getTickSize() * 0.625 },
                    { "x" : x + Grid.getTickSize() * 0.375, "y" : y + Grid.getTickSize() * 0.625 },
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 0.25, "y" : y + Grid.getTickSize() * 0.75 },
                    { "x" : x + Grid.getTickSize() * 0.25, "y" : y + Grid.getTickSize() * 0.75 },
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)

        svg
            .append("circle")
            .attr("cx", x)
            .attr("cy", y)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        return svg

class @VSrcSprite extends Sprite
    @constructSVG: (x, y, v) ->
        DA = window.DescArea()

        if v == ""
            v = 0
        else
            v = parseFloat(v)
        [v, us] = Units.pretty_resize(v)

        toDStr = (lst) ->
            d3.svg.line()
                  .x((d) -> return d.x)
                  .y((d) -> return d.y)
                  .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("circle")
            .attr("cx", x)
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
            if v == ""
                v = "0"
            svg.valueText.text("#{v.toFixed(1)} #{us}V")
        svg.updateText(v)
        return svg

class @VInSprite extends Sprite
    @constructSVG: (x, y) ->
        DA = window.DescArea()

        toDStr = (lst) ->
            d3.svg.line()
                  .x((d) -> return d.x)
                  .y((d) -> return d.y)
                  .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("circle")
            .attr("cx", x)
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
            .text("Vin")
        return svg

class @VOutSprite extends Sprite
    @constructSVG: (x, y) ->
        DA = window.DescArea()

        toDStr = (lst) ->
            d3.svg.line()
                  .x((d) -> return d.x)
                  .y((d) -> return d.y)
                  .interpolate("linear")(lst)
        svg = DA.svg.append("g")
        svg
            .append("circle")
            .attr("cx", x)
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
            .text("Vout")
        return svg

class @InductorSprite extends Sprite
    @constructSVG: (x, y, v) ->
        DA = window.DescArea()

        if v == ""
            v = 0
        else
            v = parseFloat(v)
        [v, us] = Units.pretty_resize(v)

        toDStr = (lst) ->
            return d3.svg.line()
                    .x((d) -> return d.x)
                    .y((d) -> return d.y)
                    .interpolate("cardinal")(lst)
        svg = DA.svg.append("g")
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize()        , "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.75 , "y" : y                            },

                    { "x" : x - Grid.getTickSize() * 0.5  , "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.375, "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.5  , "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.625, "y" : y                            },
                    { "x" : x - Grid.getTickSize() * 0.5  , "y" : y + Grid.getTickSize() * 0.5 },

                    { "x" : x                             , "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.125, "y" : y                            },
                    { "x" : x                             , "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x - Grid.getTickSize() * 0.125, "y" : y                            },
                    { "x" : x                             , "y" : y + Grid.getTickSize() * 0.5 },

                    { "x" : x + Grid.getTickSize() * 0.5  , "y" : y + Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.625, "y" : y                            },
                    { "x" : x + Grid.getTickSize() * 0.5  , "y" : y - Grid.getTickSize() * 0.5 },
                    { "x" : x + Grid.getTickSize() * 0.375, "y" : y                            },
                    { "x" : x + Grid.getTickSize() * 0.5  , "y" : y + Grid.getTickSize() * 0.5 },

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
            if v == ""
                v = "0"
            svg.valueText.text("#{v.toFixed(1)} #{us}H")
        svg.updateText(v)
        return svg

class @ResistorSprite extends Sprite
    @constructSVG: (x, y, v) ->
        DA = window.DescArea()

        if v == ""
            v = 0
        else
            v = parseFloat(v)
        [v, us] = Units.pretty_resize(v)

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
            if v == ""
                v = "0"
            svg.valueText.text("#{v.toFixed(1)} #{us}Ω")
        svg.updateText(v)
        return svg

class @OpampSprite extends Sprite
    @constructSVG: (x, y) ->
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
                    { "x" : x + Grid.getTickSize() * 0.5 , "y" : y},
                    { "x" : x - Grid.getTickSize() * 1.5 , "y" : y - Grid.getTickSize() * 1.5},
                    { "x" : x - Grid.getTickSize() * 1.5 , "y" : y + Grid.getTickSize() * 1.5},
                    { "x" : x + Grid.getTickSize() * 0.5 , "y" : y}
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 2 , "y" : y - Grid.getTickSize()},
                    { "x" : x - Grid.getTickSize() * 1.5 , "y" : y - Grid.getTickSize()},
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x - Grid.getTickSize() * 2 , "y" : y + Grid.getTickSize()},
                    { "x" : x - Grid.getTickSize() * 1.5 , "y" : y + Grid.getTickSize()},
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("path")
            .attr("d", toDStr([
                    { "x" : x + Grid.getTickSize() * 0.5 , "y" : y },
                    { "x" : x + Grid.getTickSize(), "y" : y },
                ]))
            .style("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
        svg
            .append("text")
            .attr("x", x - Grid.getTickSize())
            .attr("y", y - Grid.getTickSize() * 0.5)
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .classed("text", true)
            .attr("shape-rendering", "crispEdges")
            .style("font-size", "16px")
            .text("-")
        svg
            .append("text")
            .attr("x", x - Grid.getTickSize())
            .attr("y", y + Grid.getTickSize() * 0.5)
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .classed("text", true)
            .attr("shape-rendering", "crispEdges")
            .style("font-size", "16px")
            .text("+")
        svg
            .append("circle")
            .attr("cx", x + Grid.getTickSize())
            .attr("cy", y)
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        svg
            .append("circle")
            .attr("cx", x - Grid.getTickSize() * 2)
            .attr("cy", y - Grid.getTickSize())
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        svg
            .append("circle")
            .attr("cx", x - Grid.getTickSize() * 2)
            .attr("cy", y + Grid.getTickSize())
            .attr("r", Grid.getTickSize() * .125)
            .style("fill", "black")
            .attr("stroke", "black")
        return svg

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
