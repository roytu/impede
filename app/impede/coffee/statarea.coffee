class @StatArea
    instance = null
    constructor: ->
        if instance
            return instance
        else
            instance = this
        @x = 0
        @y = 0
        @w = $(".leftArea").width()
        @h = $(window).height()
        @padding = 10

        @div = d3.select(".leftArea")
                 .append("div")
                 .classed("statArea", true)
        @_text = @div.append("p")
                     .classed("text", true)
        @_text.html(["time: " + 0,
                     "running: " + false,
                     "continuous mode: " + "off"
                    ].join("<br>"))
    updateText: ->
        @_text.html(["time: #{State.time}",
                     "running: #{State.running}",
                     "continuous mode: #{State.continuousTime ? "on" : "off"}"
                     ].join("<br>"))
