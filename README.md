# impede

![](/images/demo.png)

SPICE-like program to simulate stompbox circuits.  The circuit is reduced symbolically (with Sympy) and then processed on the input signal, producing an audio output signal.

WIP

Run with:

    meteor run
    
in the ``impede-app/`` directory.

Currently supports:
* Resistors
* Capacitors
* Inductors
* Diodes
* Op-amps (in feedback mode)
