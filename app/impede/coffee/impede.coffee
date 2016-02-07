root = exports ? this
root.init = ->
    if Meteor.isClient
        contains: (array, element) ->
            for i in [0..array.length]
                for j in [0..element.length]
                    if array[i][j] != element[j]
                        return false
                return true
            return false
        
        Elements =
            WIRE: 0
            RESISTOR: 1
            CAPACITOR: 2
            INDUCTOR: 3
            OPAMP: 4
            V_IN: 5
            V_OUT: 6
            V_SRC: 7
        
        SA = new window.StatArea()
        DA = new window.DescArea()
        
        Drawable = window.Drawable
        Grid = window.Grid
        Configuration = window.Configuration
        Metastate = new window.Metastate(new Configuration())
        Sprite = window.Sprite
        
        WireSprite = window.WireSprite
        WireGhostSprite = window.WireGhostSprite
        ResistorSprite = window.ResistorSprite
        InductorSprite = window.InductorSprite
        CapacitorSprite = window.CapacitorSprite

        State = window.State
        
        Grid.initialize()
        
        $("body").keydown( (e) ->
            switch e.keyCode
                when 38  # UP
                  Grid.zoomIn()
                  Grid.redraw()
                  Metastate.updateSVGs()
                when 40  # DOWN
                  Grid.zoomOut()
                  Grid.redraw()
                  Metastate.updateSVGs()
                when 82  # R
                  Metastate.selected = Elements.RESISTOR
                when 67  # C
                  Metastate.selected = Elements.CAPACITOR
                when 76  # L
                  Metastate.selected = Elements.INDUCTOR
        )
