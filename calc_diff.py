import os
import pygal
from pygal.style import Style
from difflib import SequenceMatcher
totals = []


#os.chdir('/Users/christopheryoung/PycharmProjects/netmanchris-scriptsonly/Events/ETSS June
# 2016/DevOps Networking Model/Generate_Spine_Leaf_Configs/Configs')
#listdir = os.listdir()
#os.chdir(os.listdir())
listdir = os.listdir()

configs = []
for i in listdir:
    if 'cfg' in i:
        configs.append(i)

#configs = ['5930-2.cfg','7904-1.cfg', '7904-2.cfg']

text1 = open(configs[0]).read()

for config in configs:
    config_content = open(config).read()
    metric = SequenceMatcher(None, text1, config_content)
    totals.append(metric.ratio())
    print (config, " stability metric: ", metric.ratio())


print ("\n Network Stability Metric: ", sum(totals)/len(totals))
print (" Network Fragility Metric: ", 1 - sum(totals)/len(totals))

custom_style = Style(colors=('Green', 'Red'))
pie_chart = pygal.Pie(style=custom_style)
pie_chart.title = 'Network Stability'
pie_chart.add('Network Stability Metric', sum(totals)/len(totals))
pie_chart.add('Network Fragility Metric', 1 - sum(totals)/len(totals))
pie_chart.render_to_file('piechart.svg')

