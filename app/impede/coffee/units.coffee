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
            when @Units.p then "p"
            when @Units.n then "n"
            when @Units.u then "u"
            when @Units.m then "m"
            when @Units.i then ""
            when @Units.K then "K"
            when @Units.M then "M"
            when @Units.G then "G"

    @toValue: (n, unit) -> n * unit
