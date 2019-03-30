'''
bias random walk generator
'''

import argparse
import numpy as np
import networkx as nx
import Walk

def parse_args():
	'''
	Parses the random walk generator arguments.
	'''
	parser = argparse.ArgumentParser(description="Run bias random walk generator.")

	parser.add_argument('--input', nargs='?', default='data/graph.dat',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='data/walks',
	                    help='Prefix name of walks path')

	parser.add_argument('--maxT', type=int, default=128,
	                    help='maxT. Default is 128.')

	parser.add_argument('--minT', type=int, default=1,
	                    help='minT. Default is 1.')

	parser.add_argument('--p', type=float, default=1,
	                    help='Return hyperparameter. Default is 1.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--p_stop', type=float, default=0.15,
	                    help='Stop walking hyperparameter. Default is 0.15.')

	parser.add_argument('--mode', type=str, default='hits',
	                    help='Metrics of centrality. Default is hits.')

	parser.add_argument('--bipartite', dest='bipartite', action='store_true',
	                    help='Boolean specifying (non-)bipartite. Default is non-bipartite.')

	parser.add_argument('--nonbipartite', dest='nonbipartite', action='store_false')

	parser.set_defaults(bipartite=False)

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')

	parser.add_argument('--unweighted', dest='unweighted', action='store_false')

	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)


	return parser.parse_args()

def load_graph_from_file():
	'''
	Reads the input network in networkx.
	'''
	if args.directed:
		if args.weighted:
			G = nx.read_edgelist(args.input, nodetype=str, data=(('weight',float),), create_using=nx.DiGraph())
		else:
			G = nx.read_edgelist(args.input, nodetype=str, create_using=nx.DiGraph())
			for edge in G.edges():
				G[edge[0]][edge[1]]['weight'] = 1
	else:
		if args.weighted:
			G = nx.read_edgelist(args.input, nodetype=str, data=(('weight',float),), create_using=nx.Graph())
		else:
			G = nx.read_edgelist(args.input, nodetype=str, create_using=nx.Graph())
			for edge in G.edges():
				G[edge[0]][edge[1]]['weight'] = 1
		G = G.to_directed()
	return G		

def load_bigraph_from_file():
	'''
	Reads the input bipartite network in networkx.
	'''
	if args.directed:
		if args.weighted:
			G = nx.read_edgelist(args.input, nodetype=str, data=(('weight',float),), create_using=nx.DiGraph())
		else:
			G = nx.read_edgelist(args.input, nodetype=str, create_using=nx.DiGraph())
			for edge in G.edges():
				G[edge[0]][edge[1]]['weight'] = 1
	else:
		if args.weighted:
			G = nx.read_edgelist(args.input, nodetype=str, data=(('weight',float),), create_using=nx.Graph())
		else:
			G = nx.read_edgelist(args.input, nodetype=str, create_using=nx.Graph())
			for edge in G.edges():
				G[edge[0]][edge[1]]['weight'] = 1
		G = G.to_directed()
	A = nx.adjacency_matrix(G)
	AT = A.transpose()
	AU = A.dot(AT)
	AV = AT.dot(A)

	GU = nx.Graph(AU).to_directed()
	GV = nx.Graph(AV).to_directed()


	return GU, GV

# def learn_embeddings(walks):
# 	'''
# 	Learn embeddings by optimizing the Skipgram objective using SGD.
# 	'''
# 	walks = [map(str, walk) for walk in walks]
# 	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
# 	model.save_word2vec_format(args.output)
	
# 	return

def main(args):
	'''
	Get walks for graph.
	'''
	if not args.bipartite:
		nx_G = load_graph_from_file()
		G = Walk.Graph(nx_G, args.directed, args.p, args.q, args.p_stop, args.maxT, args.minT)
		G.preprocess_transition_probs()
		G.calculate_centrality()
		walks = G.simulate_walks()
		with open(args.output+".dat", 'w', encoding='utf-8') as fr:
			for walk in walks:
				fr.write(" ".join(walk)+"\n")

	else:
		GU, GV = load_bigraph_from_file()
		for (nx_G, t) in [(GU,"u"), (GV,"i")]:
			print(nx_G,t)
			G = Walk.Graph(nx_G, args.directed, args.p, args.q, args.p_stop, args.maxT, args.minT)
			G.preprocess_transition_probs()
			walks = G.simulate_walks()
			with open(args.output+"_"+t+".dat", 'w', encoding='utf-8') as fr:
				for walk in walks:
					fr.write(" ".join(walk)+"\n")			

if __name__ == "__main__":
	args = parse_args()
	main(args)