init = (id=null) =>
    DA = new window.DescArea()
    Metastate = new window.Metastate(id)
    
    # Start program
    Grid.initialize()
    DA.initialize()
    
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
              DA.addMessage("Selected deletor")
            when 82  # r
              Metastate.selected = Elements.RESISTOR
              Metastate.value_text = ""
              Metastate.updateGhost()
              DA.addMessage("Selected resistor")
            when 67  # c
              Metastate.selected = Elements.CAPACITOR
              Metastate.value_text = ""
              Metastate.updateGhost()
              DA.addMessage("Selected capacitor")
            when 76  # l
              if e.shiftKey
                  Metastate.selected = Elements.INDUCTOR
                  Metastate.value_text = ""
                  Metastate.updateGhost()
                  DA.addMessage("Selected inductor")
              else
                  Metastate.loadInput()
            when 71  # g
              Metastate.selected = Elements.GND
              Metastate.updateGhost()
              DA.addMessage("Selected ground reference")
            when 86  # v
              Metastate.selected = Elements.V_SRC
              Metastate.value_text = ""
              Metastate.updateGhost()
              DA.addMessage("Selected voltage source")
            when 73  # i / I
              if e.shiftKey
                  Metastate.selected = Elements.V_IN
                  Metastate.updateGhost()
                  DA.addMessage("Selected voltage input")
              else
                use_unit(Units::i)
                DA.addMessage("Unit identity")
            when 79  # o
              Metastate.selected = Elements.V_OUT
              Metastate.updateGhost()
              DA.addMessage("Selected voltage output")
            when 65  # a
              Metastate.selected = Elements.OPAMP
              Metastate.updateGhost()
              DA.addMessage("Selected op amp")
            # UNITS
            when 80  # p
              use_unit(Units::p)
              DA.addMessage("Unit pico")
            when 78  # n
              use_unit(Units::n)
              DA.addMessage("Unit nano")
            when 85  # u
              use_unit(Units::u)
              DA.addMessage("Unit micro")
            when 77  # m
              if e.shiftKey
                  use_unit(Units::M)
                  DA.addMessage("Unit mega")
              else
                  use_unit(Units::m)
                  DA.addMessage("Unit milli")
            when 75  # k
              use_unit(Units::K)
              DA.addMessage("Unit kilo")
            when 71  # g
              use_unit(Units::G)
              DA.addMessage("Unit giga")
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
              DA.addMessage("Selected wire")
            when 27  # Esc
              Metastate.first_mx = null
              Metastate.first_my = null
              Metastate.selected = null
              Metastate.updateGhost()
              DA.addMessage("Cancelled")
            when 83  # s
              Metastate.save()
              DA.addMessage("Saved")
    )

FlowRouter.route('/', {
    name: '',
    action: (params) =>
        init()
})

FlowRouter.route('/:id', {
    name: '',
    action: (params) =>
        id = params.id
        init(id)
})
