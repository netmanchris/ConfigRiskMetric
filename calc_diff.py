#!/usr/bin/env python

import os
import pygal
from pygal.style import Style
from difflib import Differ, SequenceMatcher

totals = []
keywords = { "BGP": 0.1, "OSPF": 0.2, "ISIS": 0.3, "EIGRP": 0.4, "RIP": 10.0} 
listdir = os.listdir()

configs = []
for i in listdir:
    if 'cfg' in i:
        configs.append(i)

text1 = open(configs[0]).read()
d1 = open(configs[0]).readlines()

for config in configs:
    config_content = open(config).read()
    metric = SequenceMatcher(None, text1, config_content)

    d = Differ()
    d2 = open(config).readlines()
    weight = 1.0
    diff = list(d.compare(d1, d2))
    print("found {} diffs".format(len(diff)))
    for l in diff:
        if not l.startswith(("+","-")):
            continue
        for k in keywords:
            if " {} ".format(k).lower() in l.lower():
                print("matched {} in {}".format(k, l))
                weight = weight + keywords[k]
    ratio = metric.ratio() / weight
    totals.append(ratio)
    print (config, " stability metric: ", ratio)


print ("\n Network Stability Metric: ", sum(totals)/len(totals))
print (" Network Fragility Metric: ", 1 - sum(totals)/len(totals))

custom_style = Style(colors=('Green', 'Red'))
pie_chart = pygal.Pie(style=custom_style)
pie_chart.title = 'Network Stability'
pie_chart.add('Network Stability Metric', sum(totals)/len(totals))
pie_chart.add('Network Fragility Metric', 1 - sum(totals)/len(totals))
pie_chart.render_to_file('piechart.svg')

