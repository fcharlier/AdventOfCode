#!/usr/bin/python

on = {}


def parse(dump):
    """docstring for parse"""
    all_processes = set()
    all_children = set()
    procs = {}
    with open(dump) as lines:
        for line in lines:
            line = line.strip()
            elements = line.split()
            name = elements[0]
            weight = int(elements[1][1:-1])
            children = []
            if len(elements) > 3:
                children = [elt.replace(',', '') for elt in elements[3:]]

            all_processes.add(name)

            for child in children:
                all_processes.add(child)
                all_children.add(child)

            procs[name] = {
                'weight': weight,
                'children': children
            }
            # print name, '--'.join(children)

    bottom = (all_processes - all_children).pop()
    print "Bottom process is: %s" % bottom

    compute_weight(procs, bottom)


def compute_weight(procs, process, level=0):
    children_weight = 0
    for child in procs[process]['children']:
        compute_weight(procs, child, level + 1)
        children_weight += procs[child]['total_weight']
    procs[process]['total_weight'] = procs[process]['weight'] + children_weight
    procs[process]['childW'] = children_weight
    if len(procs[process]['children']):
        procs[process]['avg'] = children_weight / len(procs[process]['children'])
        for child in procs[process]['children']:
            if procs[child]['total_weight'] != procs[process]['avg']:
                print "Proc: %s (%d) -> Child: %s (w:%d, tot:%d, child:%d" % (process, procs[process]['total_weight'], child, procs[child]['weight'], procs[child]['total_weight'], procs[process]['childW'])
    # print ' '*2*level, '> ', process, ' : ', procs[process]['total_weight']


parse('adv2017-7.input')
