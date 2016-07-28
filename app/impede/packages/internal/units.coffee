class @Units
    p: Math.pow(10, -12)
    n: Math.pow(10, -9)
    u: Math.pow(10, -6)
    m: Math.pow(10, -3)
    i: 1
    K: Math.pow(10, 3)
    M: Math.pow(10, 6)
    G: Math.pow(10, 9)

    @toString: (unit) ->
        switch unit
            when Units::p then "p"
            when Units::n then "n"
            when Units::u then "u"
            when Units::m then "m"
            when Units::i then ""
            when Units::K then "K"
            when Units::M then "M"
            when Units::G then "G"

    @toValue: (n, unit) -> n * unit

    @pretty_resize: (v) ->
        if v == 0
            return [v, ""]

        unit = Math.pow(10, Math.floor(Math.log10(v) / 3) * 3)
        if unit < Units::p
            unit = Units::p
        else if unit > Units::G
            unit = Units::G

        return [v / unit, @toString(unit)]
