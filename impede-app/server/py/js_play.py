
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
from sound_handler import SoundHandler as SH
from config import Config

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
            s = "Node(graph"
            if value:
                s += ", value=True"
            if fixed:
                s += ", fixed=True"
            if source:
                s += ", source=True"
            if output:
                s += ", output=True"
            s += ") at {0}"
            print(s.format(pt))
            pt2node[pt] = Node(graph, value=value, fixed=fixed,
                               source=source, output=output)
        return pt2node[pt]

    # Special nodes have priority on creation
    # TODO cleanup
    vin_ = None
    vout_ = None

    for [x, y] in grounds:
        pt = (x, y)
        get_node(pt, value=0, fixed=True, source=True)

    for [x, y, v] in v_srcs:
        pt = (x, y)
        get_node(pt, value=v, fixed=True, source=True)

    for [x, y] in v_ins:
        pt = (x, y)
        vin_ = get_node(pt, fixed=True, source=True)

    for [x, y] in v_outs:
        pt = (x, y)
        vout_ = get_node(pt, output=True)

    # Other components
    for [x, y] in opamps:
        pt_minus = (x - 2, y - 1)
        pt_plus = (x - 2, y + 1)
        pt_out = (x + 1, y)
        
        node_minus = get_node(pt_minus)
        node_plus = get_node(pt_plus)
        node_out = get_node(pt_out, source=True)
        
        s = "Opamp(graph, node_a={0}, node_b={1}, node_out={2})"
        print(s.format(pt_minus, pt_plus, pt_out))
        opamp = Opamp(graph, node_a=node_minus, node_b=node_plus,
                      node_out=node_out)

        graph.add_component(opamp)

    for [x1, y1, x2, y2] in wires:
        pt1 = (x1, y1)
        pt2 = (x2, y2)

        node1 = get_node(pt1)
        node2 = get_node(pt2)

        #s = "Edge(graph, {0}, {1})"
        #print(s.format(pt1, pt2))
        edge = Edge(graph, node1, node2)

        s = "Wire(graph, {0}, {1}, (edge))"
        print(s.format(pt1, pt2))
        wire = Wire(graph, node1, node2, edge)
        graph.add_component(wire)

    for [x, y, v] in resistors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)

        #s = "Edge(graph, {0}, {1})"
        #print(s.format(pt1, pt2))
        edge = Edge(graph, node1, node2)

        s = "Resistor(graph, {0}, {1}, (edge))"
        print(s.format(pt1, pt2))
        resistor = Resistor(graph, v, node1, node2, edge)

        graph.add_component(resistor)

    for [x, y, v] in capacitors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)

        #s = "Edge(graph, {0}, {1})"
        #print(s.format(pt1, pt2))
        edge = Edge(graph, node1, node2)

        s = "Capacitor(graph, {0}, {1}, (edge))"
        print(s.format(pt1, pt2))
        capacitor = Capacitor(graph, v, node1, node2, edge)

        graph.add_component(capacitor)

    for [x, y, v] in inductors:
        pt1 = (x - 1, y)
        pt2 = (x + 1, y)

        node1 = get_node(pt1)
        node2 = get_node(pt2)

        #s = "Edge(graph, {0}, {1})"
        #print(s.format(pt1, pt2))
        edge = Edge(graph, node1, node2)

        s = "Inductor(graph, {0}, {1}, (edge))"
        print(s.format(pt1, pt2))
        inductor = Inductor(graph, v, node1, node2, edge)

        graph.add_component(inductor)

    return Filter(graph, vin_, vout_)

def play(id_):
    client = MongoClient("mongodb://127.0.0.1:3001/meteor")
    db = client["meteor"]
    match = db["sessions"].find_one(id_)
    config = match["config"]

    # Build filter
    filter_ = make_filter(config)

    samples = None
    with open(Config.samples_dir + "samples.json", "r") as f:
        samples = json.loads(f.read())["samples"]
    sample_id = int(config["sample"])

    sample_fname = "../" + samples[sample_id][1]

    input_signal = SH.load(sample_fname, sampleperiod=Config.time_step, peak=1)
    output_signal = filter_.execute(input_signal)

    SH.save(output_signal, Config.output_dir + str(id_) + ".wav",
            bytespersample=2, peak=1)

    # Tell meteor it is done
    db["sessions"].update_one({ "_id" : id_ }, { "$set" : { "pydone": True }})
