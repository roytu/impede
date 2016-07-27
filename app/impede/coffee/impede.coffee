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
        GroundSprite = window.GroundSprite
        VSrcSprite = window.VSrcSprite

        State = window.State
        
        # Start program
        Grid.initialize()

        # Unit handling
        use_unit = (u) ->
            v = parseFloat(Metastate.value_text)
            v /= Math.pow(10, Math.floor(Math.log10(v) / 3) * 3)
            v *= u
            Metastate.value_text = "#{v}"
            Metastate.updateGhost()

        # Keypresses
        $("body").keydown( (e) ->
            console.log(e.keyCode)
            switch e.keyCode
                when 38  # UP
                  Grid.zoomIn()
                  Grid.redraw()
                  Metastate.updateSVGs()
                when 40  # DOWN
                  Grid.zoomOut()
                  Grid.redraw()
                  Metastate.updateSVGs()
                when 68  # d
                  Metastate.selected = Elements.DELETOR
                  Metastate.updateGhost()
                when 82  # r
                  Metastate.selected = Elements.RESISTOR
                  Metastate.value_text = ""
                  Metastate.updateGhost()
                when 67  # c
                  Metastate.selected = Elements.CAPACITOR
                  Metastate.value_text = ""
                  Metastate.updateGhost()
                when 76  # l
                  Metastate.selected = Elements.INDUCTOR
                  Metastate.value_text = ""
                  Metastate.updateGhost()
                when 71  # g
                  Metastate.selected = Elements.GND
                  Metastate.updateGhost()
                when 86  # v
                  Metastate.selected = Elements.V_SRC
                  Metastate.value_text = ""
                  Metastate.updateGhost()
                when 73  # i / I
                  if e.shiftKey
                      Metastate.selected = Elements.V_IN
                      Metastate.updateGhost()
                  else
                    use_unit(Units::i)
                when 79  # o
                  Metastate.selected = Elements.V_OUT
                  Metastate.updateGhost()
                when 65  # a
                  Metastate.selected = Elements.OPAMP
                  Metastate.updateGhost()
                # UNITS
                when 80  # p
                  use_unit(Units::p)
                when 78  # n
                  use_unit(Units::n)
                when 85  # u
                  use_unit(Units::u)
                when 77  # m
                  if e.shiftKey
                      use_unit(Units::M)
                  else
                      use_unit(Units::m)
                when 75  # k
                  use_unit(Units::K)
                when 71  # g
                  use_unit(Units::G)
                when 48, 49, 50, 51, 52, 53, 54, 55, 56, 57  # Numbers 0 - 9
                  Metastate.value_text += "#{e.keyCode - 48}"
                  Metastate.updateGhost()
                when 190  # .
                  Metastate.value_text += "."
                  Metastate.updateGhost()
                when 8  # Backspace
                  e.preventDefault()
                  DA = window.DescArea()
                  Metastate.value_text = Metastate.value_text.slice(0, -1)
                  Metastate.updateGhost()
                when 87  # w
                  Metastate.first_mx = null
                  Metastate.first_my = null
                  Metastate.selected = Elements.WIRE
                  Metastate.updateGhost()
                when 27  # Esc
                  Metastate.first_mx = null
                  Metastate.first_my = null
                  Metastate.selected = null
        )
