
""" Module that takes a configuration and input signal from a JSON file
    and calculates the output signal, saving it as a JSON file.
"""

import sys
import json
from pymongo import MongoClient

from graph import Node, Edge, Graph
from resistor import Resistor
from capacitor import Capacitor
from diode import Diode
from opamp import Opamp
from wire import Wire
from units import Units
from filter import Filter

def make_filter(config):
    """ Returns a Filter object. """
    wires = config["wires"]
    resistors = config["resistors"]
    capacitors = config["capacitors"]
    inductors = config["inductors"]
    opamps = config["opamps"]
    grounds = config["grounds"]
    v_srcs = config["v_srcs"]
    v_ins = config["v_ins"]
    v_outs = config["v_outs"]

    pt2node = {}

    graph = Graph()

    def get_node(pt, value=0, fixed=False, source=False, output=False):
        if pt not in pt2node:
            pt2node[pt] = Node(graph, value=value, fixed=fixed,
                               source=source, output=output)
        return pt2node[pt]

    # Special nodes have priority on creation
    # TODO cleanup
    vsrcs_ = {}
    vin_ = None
    vout_ = None

    # All grounds are the same node
    for [x, y] in grounds:
        pt = (x, y)
        if 0 not in vsrcs_:
            node = get_node(pt, value=0, fixed=True, source=True)
            vsrcs_[0] = node
        else:
            node = get_node(pt)
            edge = Edge(graph, node, vsrcs_[0])
            wire = Wire(graph, node, vsrcs_[0], edge)
            graph.add_component(wire)

    for [x, y, v] in v_srcs:
        pt = (x, y)
        if v not in vsrcs_:
            node = get_node(pt, value=v, fixed=True, source=True)
            vsrcs_[v] = node
        else:
            node = get_node(pt)
            edge = Edge(graph, node, vsrcs_[v])
            wire = Wire(graph, node, vsrcs_[v], edge)
            graph.add_component(wire)

    for [x, y] in v_ins:
        pt = (x, y)
        if not vin_:
            node = get_node(pt, fixed=True, source=True)
            vin_ = node
        else:
            node = get_node(pt)
            edge = Edge(graph, node, vin_)
            wire = Wire(graph, node, vin_, edge)
            graph.add_component(wire)

    for [x, y] in v_outs:
        pt = (x, y)
        if not vout_:
            node = get_node(pt, output=True)
            vout_ = node
        else:
            node = get_node(pt)
            edge = Edge(graph, node, vout_)
            wire = Wire(graph, node, vout_, edge)
            graph.add_component(wire)

    # Other components
    for [x, y] in opamps:
        pt_minus = (x - 2, y - 1)
        pt_plus = (x - 2, y + 1)
        pt_out = (x + 1, y)
        
        node_minus = get_node(pt_minus)
        node_plus = get_node(pt_plus)
        node_out = get_node(pt_out, source=True)
        
        opamp = Opamp(graph, node_a=node_minus, node_b=node_plus,
                      node_out=node_out)
        graph.add_component(opamp)

    for [x1, y1, x2, y2] in wires:
        pt1 = (x1, y1)
        pt2 = (x2, y2)

        node1 = get_node(pt1)
        node2 = get_node(pt2)
        edge = Edge(graph, node1, node2)

        wire = Wire(graph, node1, node2, edge)
        graph.add_component(wire)

    for [x, y, v] in resistors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)
        edge = Edge(graph, node1, node2)

        resistor = Resistor(graph, v, node1, node2, edge)
        graph.add_component(resistor)

    for [x, y, v] in capacitors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)
        edge = Edge(graph, node1, node2)

        capacitor = Capacitor(graph, v, node1, node2, edge)
        graph.add_component(capacitor)

    for [x, y, v] in inductors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)
        edge = Edge(graph, node1, node2)

        inductors = Inductors(graph, v, node1, node2, edge)
        graph.add_component(inductors)

    return Filter(graph, vin_, vout_)

if __name__ == "__main__":
    id_ = sys.argv[1]

    client = MongoClient("mongodb://127.0.0.1:3001/meteor")
    db = client["meteor"]
    match = db["sessions"].find_one(id_)
    config = match["config"]

    # Build filter
    filter_ = make_filter(config)

    # Play?

