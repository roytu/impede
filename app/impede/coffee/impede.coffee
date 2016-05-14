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
        
        Elements = window.Elements
        
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
                  Metastate.updateGhost()
                when 67  # C
                  Metastate.selected = Elements.CAPACITOR
                  Metastate.updateGhost()
                when 76  # L
                  Metastate.selected = Elements.INDUCTOR
                  Metastate.updateGhost()
                when 48, 49, 50, 51, 52, 53, 54, 55, 56, 57  # Numbers 0 - 9
                  DA = window.DescArea()
                  Metastate.value_text += "#{e.keyCode - 48}"
                  Metastate.updateGhost()
                when 8  # Backspace
                  e.preventDefault()
                  DA = window.DescArea()
                  Metastate.value_text = Metastate.value_text.slice(0, -1)
                  Metastate.updateGhost()
        )
