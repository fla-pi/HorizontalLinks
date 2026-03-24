import pandas as pd
import csv
from itertools import combinations
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
from matplotlib import rc
import math
import sys
import pathlib
import os
if sys.platform == 'win32':
    path = pathlib.Path(r'C:\Program Files\Graphviz\bin')
    if path.is_dir() and str(path) not in os.environ['PATH']:
        os.environ['PATH'] += f';{path}'
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz
import igraph as ig
from operator import itemgetter
from collections import defaultdict

#list of cxns
nodi = ['avere','provare','sentire','essere_in','conversion_stative','conversion+si_stative','parasynthesis+si_stative','suffixation_stative','andare_in','farsi','prendere','conversion+si_inchoative','parasynthesis+si_inchoative','dare','fare','mettere','conversion_causative','parasynthesis','suffixation_causative']
nodi_lab = [r'$\it{avere}$ N',r'$\it{provare}$ N',r'$\it{sentire}$ N',r'$\it{essere}$ $\it{in}$ N',r'N$\it{-a/ire}$',r'N$\it{-a/irsi}$',r'$\it{in/ad-}$N$\it{-a/irsi}$',r'N$\it{-izzare}$',r'$\it{andare}$ $\it{in}$ N',r'$\it{farsi}$ N',r'$\it{prendere}$ N',r'N$\it{-a/irsi}$',r'$\it{in/ad-}$N$\it{-a/irsi}$',r'$\it{dare}$ N','$\it{fare}$ N','$\it{mettere}$ N','N$\it{-a/ire}$','$\it{in/ad-}$N$\it{-a/ire}$','N$\it{-izzare}$']

events = { 'statives' : ['avere','provare','sentire','essere_in','conversion_stative','conversion+si_stative','parasynthesis+si_stative','suffixation_stative'],
'inchoatives' : ['andare_in','farsi','prendere','conversion+si_inchoative','parasynthesis+si_inchoative'],
'causatives' : ['dare','fare','mettere','conversion_causative','parasynthesis','suffixation_causative']}

cxn_type = { 'LVC' : ['avere','provare','sentire','essere_in', 'andare_in','farsi','prendere', 'dare','fare','mettere'],
'SV' : ['conversion_stative','conversion+si_stative','parasynthesis+si_stative','suffixation_stative', 'conversion+si_inchoative','parasynthesis+si_inchoative', 'conversion_causative','parasynthesis','suffixation_causative']
}

cxn_type2 = { 'LVC' : ['avere','provare','sentire','essere_in', 'andare_in','farsi','prendere', 'dare','fare','mettere'],
'SV_si' : ['conversion+si_stative','parasynthesis+si_stative', 'conversion+si_inchoative','parasynthesis+si_inchoative'],
'SV' : ['conversion_stative', 'suffixation_stative', 'conversion_causative','parasynthesis','suffixation_causative']}


    
#frequency measures of cxn (for the size of the nodes)
df0 = pd.read_csv('2_schema_frequency_info.csv', sep = ";", encoding ="utf-8")
n_types = df0['n_types'].tolist()
n_tokens = df0['n_tokens'].tolist()
max_tokens = df0['max_n_tokens'].tolist()
avg_tokens = df0['avg_n_tokens'].tolist()
median_tokens = df0['median_n_tokens'].tolist()
freq_pmw = df0['freq_pmw'].tolist()

#################################################################################################

#choose frequency measure for node sizes
freq_measure = n_types

sizes = []
for i in freq_measure:
    sizes.append(abs(300*(math.log(i))))
cxn_lab = dict()
for i in range(len(nodi)):
    cxn_lab[nodi[i]] = nodi_lab[i]


#choose number of pairs threshold
threshold = 4

#choose color of synonymy and paradigmatic links
syn_link_col = 'purple'
par_link_col = 'black'


#choose style of synonymy and paradigmatic links
syn_link_st = '-'
par_link_st = '-'

#choose size links
large_par = 1.5
large_syn = 1.5
medium_par = 1
medium_syn = 1
small_par = 0.5
small_syn = 0.5

#choose node color of event types
stat_col = 'cyan'
inc_col = 'yellow'
caus_col = 'red'

stat = [stat_col,]*8
inc = [inc_col,]*5
caus = [caus_col,]*6
colori = stat+inc+caus

#choose shape of cxn nodes
shape_cxn = "o"



####################################################################################################

#read data
df = pd.read_csv("3_graph_synonymy.csv", sep = ";", encoding = "utf-8")
df2 = pd.read_csv('3_graph_paradigmatic.csv', sep = ";", encoding ="utf-8")
syn_pred1 = df['pred1'].tolist()
syn_pred2 = df['pred2'].tolist()
syn_n = df['n'].tolist()
par_pred1 = df2['pred1'].tolist()
par_pred2 = df2['pred2'].tolist()
par_n = df2['n'].tolist()

#synonymy links graph
syn = []
for i in range(len(syn_pred1)):
    if syn_n[i] >= threshold:
        syn.append((syn_pred1[i], syn_pred2[i], syn_n[i]))

G = nx.Graph()
G.add_nodes_from(nodi)
G.add_weighted_edges_from(syn)


#paradigmatic links graph
par = []
for i in range(len(par_pred1)):
    if par_n[i] >= threshold:
        par.append((par_pred1[i], par_pred2[i], par_n[i]))

H = nx.Graph()
H.add_nodes_from(nodi)
H.add_weighted_edges_from(par)
 

#compose the two graphs
R = nx.compose(G, H)
R.remove_nodes_from(list(nx.isolates(R)))

nodi_ = ['',]*len(R.nodes())
nodi_lab_ = ['',]*len(R.nodes())
sizes_ = ['',]*len(R.nodes())
colori_ = ['',]*len(R.nodes())


nodini = list(R.nodes()) 
for i in list(R.nodes()):
    ind = nodi.index(i)
    ind_2 = nodini.index(i)
    nodi_[ind_2] = nodi[ind]
    nodi_lab_[ind_2] = nodi_lab[ind]
    sizes_[ind_2] = sizes[ind]
    colori_[ind_2] = colori[ind]



nodi = nodi_
nodi_lab = nodi_lab_
sizes = sizes_
colori = colori_

cxn_lab = dict()
for i in range(len(nodi)):
    cxn_lab[nodi[i]] = nodi_lab[i]

# add attributes
for event_label, node_list in events.items():
    for node in node_list:
        if R.has_node(node):
            R.nodes[node]['event_type'] = event_label
for cxn_label, node_list in cxn_type.items():
    for node in node_list:
        if R.has_node(node):
            R.nodes[node]['cxn_type'] = cxn_label


#function for plotting the graphs
def plot(graph, nodi, sizes, shape_cxn, colori):
    #define appearance of link weight and type
    elarge = [(u, v) for (u, v, d) in graph.edges(data=True) if d['weight'] >= 15 ]
    elarge_syn = []
    elarge_par = []
    for (u,v) in elarge:
        tr = 0
        for (i, j, z) in syn:
            if (u,v) == (i,j):
                tr += 1
        if tr ==1:
            elarge_syn.append((u,v))
        else:
            elarge_par.append((u,v))

    emedium  = [(u, v) for (u, v, d) in graph.edges(data=True) if d['weight'] >= 10 and d['weight'] < 15]
    emedium_syn = []
    emedium_par = []
    for (u,v) in emedium:
        tr = 0
        for (i, j, z) in syn:
            if (u,v) == (i,j):
                tr += 1
        if tr ==1:
            emedium_syn.append((u,v))
        else:
            emedium_par.append((u,v))
    esmall = [(u, v) for (u, v, d) in graph.edges(data=True) if d['weight']  < 10]
    esmall_syn = []
    esmall_par = []
    for (u,v) in esmall:
        tr = 0
        for (i, j, z) in syn:
            if (u,v) == (i,j):
                tr += 1
        if tr ==1:
            esmall_syn.append((u,v))
        else:
            esmall_par.append((u,v))

        
        

        

        
    #algorithm spring_layout (keeps together frequrntly linked nodes, pulls apart unlinked ones)
    pos = nx.spring_layout(graph, weight = 'weight')



    #draw nodes
    nx.draw_networkx_nodes(graph, pos, nodelist= nodi, node_size = sizes, node_color = colori, node_shape = shape_cxn)
    if add_vert == True:
        nx.draw_networkx_nodes(graph, pos, nodelist= mother_nodes, node_size = s_2, node_color = c_2, node_shape = shape_mother)
    #draw edges
    nx.draw_networkx_edges(graph, pos, edgelist=elarge_syn, edge_color =syn_link_col, style = syn_link_st, width=large_syn)
    nx.draw_networkx_edges(graph, pos, edgelist=elarge_par, style = par_link_st, edge_color=par_link_col,  width=large_par)
    nx.draw_networkx_edges(graph, pos, edgelist=emedium_syn, edge_color = syn_link_col, style = syn_link_st, width=medium_syn)
    nx.draw_networkx_edges(graph, pos, edgelist=emedium_par, edge_color = par_link_col, style = par_link_st, width=medium_par)
    nx.draw_networkx_edges(graph, pos, edgelist=esmall_syn, edge_color =syn_link_col, style = syn_link_st, width=small_syn)
    nx.draw_networkx_edges(graph, pos, edgelist=esmall_par, style = par_link_st, edge_color = par_link_col, width=small_par)
    

    #add labels
    nx.draw_networkx_labels(graph, pos, labels = cxn_lab, font_size=10, font_color="black")

    stative = mpatches.Patch(color=stat_col, label='statives')
    inchoative = mpatches.Patch(color=inc_col, label='inchoatives')
    causative = mpatches.Patch(color=caus_col, label='causatives')

    plt.legend(handles = [stative, inchoative, causative], title = "Event types", loc = "lower right",  title_fontproperties={'weight':'bold'})

    #show plot
    plt.show()
 



#calculate and saves centrality measures
def centrality(graph):
    deg = graph.degree(weight = 'weight')
    for u,v,d in graph.edges(data=True):
        if 'weight' in d:
            if d['weight'] != 0:
                d['reciprocal'] = 1/d['weight']
    betw = nx.betweenness_centrality(graph, weight= 'reciprocal', normalized=False)
    clos = nx.closeness_centrality(graph, distance= 'reciprocal')
    print(deg)
    print(betw)
    print(clos)
    df = pd.DataFrame(deg, columns = ['pred','degree'])
    df.to_csv('degree_centrality.csv',encoding='utf-8')
    df1 = pd.DataFrame.from_dict(betw, orient = 'index', columns = ['betweenness'])
    df1.to_csv('betweenness_centrality.csv',encoding='utf-8')
    df2 = pd.DataFrame.from_dict(clos, orient = 'index', columns = ['closeness'])
    df2.to_csv('closeness_centrality.csv',encoding='utf-8')
    
# attribute assortativity (weighted) calculated according to assortnet R function
def attribute_weighted_assortativity(graph, attr):
    mixing = defaultdict(float)
    total_weight = 0.0

    for u, v, data in graph.edges(data=True):
        if attr in graph.nodes[u] and attr in graph.nodes[v]:
            attr_u = graph.nodes[u][attr]
            attr_v = graph.nodes[v][attr]
            weight = data.get("weight", 1.0)
            total_weight += weight
            mixing[(attr_u, attr_v)] += weight
            if attr_u != attr_v:
                mixing[(attr_v, attr_u)] += weight 


    labels = sorted(set(k for pair in mixing for k in pair))
    index = {label: i for i, label in enumerate(labels)}
    n = len(labels)
    E = np.zeros((n, n))

    for (i_lab, j_lab), weight in mixing.items():
        i, j = index[i_lab], index[j_lab]
        E[i, j] += weight

    E /= E.sum()

    a = E.sum(axis=1)
    b = E.sum(axis=0)

    trace = np.trace(E)
    product = np.dot(a, b)
    r = (trace - product) / (1 - product) if (1 - product) != 0 else np.nan

    return r


#find maximal cliques
def clique(graph):
    cls = []
    for i in nx.find_cliques(graph):
        igr = graph.subgraph(i)
        somma = 0 
        if len(i) > 1:
            for (u,v,d) in nx.to_edgelist(igr):
                somma += d['weight']
            cls.append((i,somma))
    cls =  sorted(cls,key=itemgetter(1))
    print('Cliques, ordered by weight')
    for c in cls:
        print(c)

#find articulation points
def critical_points(graph):
    h = ig.Graph.from_networkx(graph)
    for i in h.vs[h.articulation_points()]:
        print(i)

#calculates node diversity wrt to neighbors expressing different event types. The original diversity measure in igraph was denormalized
def diversity(graph, classification):
    cells = dict()
    for i in graph:
        nei = nx.all_neighbors(graph, i)
        stats = []
        caus = []
        inchs = []
        for j in nei:
            if j in classification['statives']:
                if i not in classification['statives']:
                    stats.append(j)
            elif j in classification['inchoatives']:
                if i not in classification['inchoatives']:
                    inchs.append(j)
            elif j in classification['causatives']:
                if i not in classification['causatives']:
                    caus.append(j)

        if len(stats) > 0:
            stats.append(i)
            stg = graph.subgraph(stats)
            stg = ig.Graph.from_networkx(stg)
            name = stg.vs.find('_nx_name' == i).index
            st_dv = stg.diversity(vertices = name, weights = 'weight')
            dg = math.log(stg.degree(name, "all" ))
            st_en = st_dv
        else:
            st_dv = 'NA'
            st_en = 'NA'

        if len(inchs) > 0:
            inchs.append(i)
            ing = graph.subgraph(inchs)

            ing = ig.Graph.from_networkx(ing)
            name = ing.vs.find('_nx_name' == i).index
            in_dv = ing.diversity(vertices = name, weights = 'weight')
            dg = math.log(ing.degree(name, "all" ))
            in_en = in_dv 
        else:
            in_dv = 'NA'
            in_en = 'NA'

        if len(caus) > 0:
            caus.append(i)
            cng = graph.subgraph(caus)
            cng = ig.Graph.from_networkx(cng)
            name = cng.vs.find('_nx_name' == i).index
            ca_dv = cng.diversity(vertices = name, weights = 'weight')
            dg = math.log(cng.degree(name, "all"))
            ca_en = ca_dv
        else:
            ca_dv = 'NA'
            ca_en = 'NA'
        cells[i] = (st_en, in_en, ca_en)
        print(i, stats, inchs, caus)
        print(st_dv, in_dv, ca_dv)
        print(st_en, in_en, ca_en)
    df4 = pd.DataFrame.from_dict(cells, orient='index', columns=['stative', 'inchoative', 'causative'])
    df4.to_csv('diversity.csv',encoding='utf-8')


def clustering(graph):
    avg_degree = sum(dict(R.degree()).values()) / R.number_of_nodes()
    strengths = dict(G.degree(weight='weight'))
    avg_strength = sum(strengths.values()) / len(strengths)

    stat_nodes = [n for n, d in graph.nodes(data=True) if d.get('event_type') == 'statives']
    inch_nodes = [n for n, d in graph.nodes(data=True) if d.get('event_type') == 'inchoatives']
    caus_nodes = [n for n, d in graph.nodes(data=True) if d.get('event_type') == 'causatives']

    gr_st = graph.subgraph(stat_nodes).copy()
    gr_inch = graph.subgraph(inch_nodes).copy()
    gr_caus = graph.subgraph(caus_nodes).copy()

    print('Properties of the Graph')
    print('--------------------------')
    print('number of nodes:', str(graph.number_of_nodes()))
    print('number of edges:', str(graph.number_of_edges()))
    print('average_degree_unweighted', str(avg_degree))
    print('average_degree_weighted', str(avg_strength))
    print('density:', str(nx.density(graph)))
    print('transitivity: ', str(nx.transitivity(graph)))
    print('average clustering_unweighted:', str(nx.average_clustering(graph)))
    print('average clustering_weighted:', str(nx.average_clustering(graph, weight = 'weight')))
    print('degree_assortativity:', str(nx.degree_assortativity_coefficient(graph, weight = 'weight')))
    print('attribute_assortativity (cxn_type):', str(nx.attribute_assortativity_coefficient(graph, 'cxn_type')))
    print('attribute_assortativity (event_type):', str(nx.attribute_assortativity_coefficient(graph, 'event_type')))
    print('attribute_assortativity_weighted (cxn_type):', str(attribute_weighted_assortativity(graph, 'cxn_type')))
    print('attribute_assortativity_weighted (event_type):', str(attribute_weighted_assortativity(graph, 'event_type')))
    print('attribute_assortativity - cxn_type for statives:', str(nx.attribute_assortativity_coefficient(gr_st, 'cxn_type')), ', inchoatives: ', str(nx.attribute_assortativity_coefficient(gr_inch, 'cxn_type')), ', and causatives:', str(nx.attribute_assortativity_coefficient(gr_caus, 'cxn_type')))
    print('attribute_assortativity_weighted - cxn_type for statives:', str(attribute_weighted_assortativity(gr_st, 'cxn_type')), ', inchoatives: ', str(attribute_weighted_assortativity(gr_inch, 'cxn_type')), ', and causatives:', str(attribute_weighted_assortativity(gr_caus, 'cxn_type')))
    

print(clustering(R))

#clustering metrics for synonymy and paradimatic subgraphs
s_graph = []
i_graph = []
c_graph = []
for i in G:
    if i in events['statives']:
        s_graph.append(i)
    elif i in events['inchoatives']:
        i_graph.append(i)
    elif i in events['causatives']:
        c_graph.append(i)
G_stative = G.subgraph(s_graph)
print('Statives subgraph')
print(clustering(G_stative))
G_inchoative = G.subgraph(i_graph)
print('Inchoatives subgraph')
print(clustering(G_inchoative))
G_causative = G.subgraph(c_graph)
print('Causatives subgraph')
print(clustering(G_causative))
print('Paradigmatic constrast subgraph')
print(clustering(H))


print(clique(R))
print(critical_points(R))
centrality(R)
diversity(R,events)

plot(R, nodi, sizes, shape_cxn, colori)

