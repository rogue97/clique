import os
from typing import List
from matplotlib import pyplot as plt
from numpy import zeros
import copy
import sys
import random
import networkx as nx
from datetime import datetime

graph_pics_dir = "images_mut_1"

# Predefined files for testing
# index 0
graph_1 = "graphs"+os.sep+"[c125-9] 125 6963.txt"
# index 1
graph_2 = "graphs"+os.sep+"[brock200_4] 200 13089.txt"
# index 2
graph_3 = "graphs"+os.sep+"[gen400_p0-9_55] 400 71820.txt"
# index 3
graph_4 = "graphs"+os.sep+"[p_hat300-3] 300 33390.txt"
# index 4
graph_5 = "graphs"+os.sep+"[DSJC1000-5] 1000 499652.txt"

# to be loaded in process_data from selected file
NUMBER_NODES = 0
NUMBER_EDGES = 0

POPULATION = 10             # size of the population
LOCAL_IMPROVEMENT = 10      # number of local improvements
MUTATIONS = 1 	            # How many vertices to remove randomly in the mutate() function
UNIQUE_ITERATIONS = 100	    # Used by local_improvement() to prevent a stall for very small cliques
SHUFFLE_TOLERANCE = 10      # Generate a fresh population after a stall
DEFAULT_TOTAL_ITERATIONS = 500 # number of generations to run the algorithm

class Node:
   def __init__(self, value = 0):
      self.value = value
      self.degree = 0
      self.edges = []

   def add_edge(self, v):
      self.edges.append(v)

class SortedListNode:
   def __init__(self, node = None, reach = None):
      self.node = -1 if node is None else node
      self.reach = 0 if reach is None else reach

class Graph:
   def __init__(self):
      self.nodes = {}
      for i in range(0, NUMBER_NODES+1):
         self.nodes[i] = None
      self.aMatrix = zeros((NUMBER_NODES, NUMBER_NODES))
      self.sortedNodes = []
    
   def add_edge(self, sv, ev):
      self.aMatrix[sv][ev] = 1
      self.aMatrix[ev][sv] = 1
      
      node = self.nodes[sv]
      if(node == None):
         node = Node(sv)
         node.add_edge(ev)
         node.degree += 1
         self.nodes[sv] = [node] 
         self.sortedNodes.append(node)
      else:
         (Node)(self.nodes[sv]).add_edge(ev)
         (Node)(self.nodes[sv]).degree += 1
         
      node = self.nodes[ev]
      if(node == None):
         node = Node(ev)
         node.add_edge(sv)
         node.degree += 1
         self.nodes[ev] = [node] 
         self.sortedNodes.append(node)
      else:
         (Node)(self.nodes[ev]).add_edge(sv)
         (Node)(self.nodes[ev]).degree += 1
   
   def sortList(self):
      self.sortedNodes.sort(key= lambda  x: x.degree, reverse=True)
   
   def visualize(self, clique: list, filepath:str=None, filename:str =None):
      global NUMBER_NODES
      # Node names start at 1
      print ("\rFound clique with "+str(len(clique)) + " nodes :\n"+str(clique)+"\n")
      G = nx.Graph()
      visual = []
      for i in range(0, NUMBER_NODES):
         for j in range(i+1, NUMBER_NODES):
            if self.aMatrix[i][j] == 1:
               visual.append([i+1,j+1])
               G.add_edge(i+1,j+1)

      clique_edges = []
      for i in range(0, len(clique)):
         for j in range(i+1, len(clique)):
            clique_edges.append([clique[i]+1, clique[j]+1])

      pos = nx.circular_layout(G)  # positions for all nodes
      nx.draw_networkx_nodes(G, pos, nodelist=[i for i in range(1, NUMBER_NODES+1)], node_size=[1 for _ in range(1, NUMBER_NODES+1)])
      nx.draw_networkx_edges(G, pos, edgelist=visual)
      nx.draw_networkx_edges(G, pos, edgelist=clique_edges, edge_color="tab:blue", label="Clique")
      try:
         if filepath is not None:
            plt.title(filename + "\nnodes in the clique "+str(len(clique)))
            plt.savefig(filepath)
            # plt.show()
      except:
         pass
      plt.clf()

# A global instance of the Graph class used througout the code
graph :Graph = None

class Clique:
   def __init__(self, firstVertex = None):
      self.clique = [] # int
      self.pa = [] #int
      self.mapPA = {} #int
      self.mapClique = {} # int

      if firstVertex != None:
         self.clique.append(firstVertex)
         for i in range(0, NUMBER_NODES):
            if i == firstVertex:
               continue
            else:
               if graph.aMatrix[i][firstVertex] == 1:
                  self.pa.append(i)
                  self.mapPA[i] = True

   def add_vertex(self, vertex:int):
      global graph

      if(self.contains_in_clique(vertex)):
         return

      self.clique.append(vertex)

      self.erase_from_pa(vertex)
      erased_nodes = [] #int
      for i in range(0, len(self.pa)):
         pavertex = self.pa[i]
         if graph.aMatrix[pavertex][vertex] == 0:
            erased_nodes.append(pavertex)
      
      for i in range(0, len(erased_nodes)):
         self.erase_from_pa(erased_nodes[i])

   def remove_vertex(self, vertex:int):
      if not self.contains_in_clique(vertex):
         return
      
      self.erase_from_pa(vertex)
      for i in range(0, NUMBER_NODES):
         if self.contains_in_clique(i):
            continue
         else:
            flag = True
            for n in range(0, len(self.clique)):
               ver = self.clique[n]
               if graph.aMatrix[i][ver] == 0:
                  flag = False
                  break
            
            if flag:
               if not self.contains_in_clique(i):
                  self.pa.append(i)

   
   def erase_from_pa(self, vertex):
      del self.mapPA[vertex]
      flag = False
      toRemove = None
      for ver in self.pa:
         if ver == vertex:
            flag = True
            toRemove = ver
            break

      if flag and toRemove is not None:
         self.pa.remove(toRemove)

   
   def contains_in_pa(self, vertex) -> bool:
      if vertex in self.mapPA.keys():
         return True
      
      return False 
         
   def erase_from_clique(self, vertex):
      del self.mapClique[vertex]
      flag = False
      toRemove = None
      for ver in self.clique:
         if ver == vertex:
            flag = True
            toRemove = ver
            break
      
      if flag and toRemove is not None:
         self.clique.remove(toRemove)

   def contains_in_clique(self, vertex) -> bool:
      if vertex in self.mapClique.keys():
         return True
      return False
      
   def compute_sorted_list(self) -> List[SortedListNode]:
      sortedList = []
      for i in range(0, len(self.pa)):
         node1 = self.pa[i]
         reach = 0
         for j in range(0, len(self.pa)):
            if i == j:
               continue 
            node2 = self.pa[j]
            if graph.aMatrix[node1][node2] == 1:
               reach += 1
         n = SortedListNode(node1, reach)
         sortedList.append(n)
      sortedList.sort(key= lambda  x: x.reach, reverse=True)
      return sortedList

   def clone(self):
      cpa = copy.deepcopy(self.pa)
      cclique = copy.deepcopy(self.clique)
      cMapPA = copy.deepcopy(self.mapPA)
      cMapClique = copy.deepcopy(self.mapClique)

      clone = Clique()
      clone.pa = cpa
      clone.clique = cclique
      clone.mapPA = cMapPA
      clone.mapClique = cMapClique
      return clone

def process_data(filename):
   global graph
   global NUMBER_NODES
   global NUMBER_EDGES
   try:
      with open(filename, 'r') as f:
         line = f.readline()
         while line[0] == 'c' or len(line) <= 1:
            line = f.readline()
         if line[0] == 'p':
            tok = line.split(' ')
            NUMBER_NODES = int(tok[2])
            NUMBER_EDGES = int(tok[3])

         graph = Graph()
         tmp = 0
         for _ in range(0, NUMBER_EDGES):
            line = f.readline()
            try:
               tok = line.split(' ')
               sv = int(tok[1]) -1
               ev = int(tok[2]) -1
               graph.add_edge(sv,ev)
            except:
               tmp+=1
         if tmp != 0:
            print(str(tmp),"Unexpected error reading edges:", sys.exc_info())

   except IOError as _:
      print("No file found")
   except:
      print("Unexpected error:", sys.exc_info())

# Print iterations progress from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '*', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def generate_random_population():
   
   population = []
   flags = [False] * NUMBER_NODES

   for i in range(0,POPULATION-1):
      rand = random.randint(0, NUMBER_NODES - 1)
      cntt = 0
      while (flags[rand]):
         cntt += 1
         if cntt> NUMBER_NODES:
            break
         rand = random.randint(0, NUMBER_NODES - 1)
      flags[rand] = True

      clique = Clique(rand)
      sortedList = clique.compute_sorted_list()
      cnt = 0
      while len(clique.pa) > 0:
         node = sortedList[cnt].node
         cnt += 1
         if clique.contains_in_pa(node):
            clique.add_vertex(node)
      population.append(clique)

   node = graph.sortedNodes[0].value
   clique = Clique(node)
   sortedList = clique.compute_sorted_list()
   count = 0
   while len(clique.pa) > 0:
      node = sortedList[count].node
      count += 1
      if clique.contains_in_pa(node):
         clique.add_vertex(node)
   population.append(clique)
   return population

def greedy_crossover(c1: Clique, c2: Clique):
   flags = [False] * NUMBER_NODES
   vec = []

   for i in range(0, len(c1.clique)):
      vertex = c1.clique[i]
      if not flags[vertex]:
         vec.append(vertex)
         flags[vertex] = True

   for i in range(0, len(c2.clique)):
      vertex = c2.clique[i]
      if not flags[vertex]:
         vec.append(vertex)
         flags[vertex] = True

   sortedList = []

   for i in range(0, len(vec)):
      node1 = vec[i]
      reach = 0
      for j in range (0, len(vec)):
         if i == j:
            continue
         node2 = vec[j]
         if(graph.aMatrix[node1][node2] == 1):
            reach += 1

      sNode = SortedListNode(node1, reach)
      sortedList.append(sNode)

   sortedList.sort(key= lambda x: x.reach, reverse=True)
   firstVertex = sortedList[0].node
   clique = Clique(firstVertex)
   count = 1

   while count < len(sortedList):
      node = sortedList[count].node
      if clique.contains_in_pa(node):
         clique.add_vertex(node)
      count += 1

   while len(clique.pa) > 0:
      node = clique.pa[0]
      clique.add_vertex(node)

   return clique

def intersection_crossover(c1: Clique, c2: Clique):
   intersect = []
   flags = [False] * NUMBER_NODES

   for i in range(0, len(c2.clique)):
      vertex = c2.clique[i]
      flags[vertex] = True

   for i in range(0, len(c1.clique)):
      ver1 = c1.clique[i]
      if flags[ver1]:
         intersect.append(ver1)

   if len(intersect) == 0:
      return greedy_crossover(c1, c2)

   vertex = intersect[0]
   clique = Clique(vertex)
   for i in range(1,len(intersect)):
      vertex = intersect[i]
      if(clique.contains_in_pa(vertex)):
         clique.add_vertex(vertex)

   if len(clique.pa) > 0:
      sortedList = clique.compute_sorted_list()
      cnt = 0
      while len(clique.pa) > 0:
         node = sortedList[cnt].node
         cnt += 1
         if clique.contains_in_pa(node):
            clique.add_vertex(node)

   return clique

def random_selection(population):
   parents = []
   rand1 = random.randint(0, POPULATION - 1)
   rand2 = random.randint(0, POPULATION - 1)
   while rand1 == rand2:
      rand1 = random.randint(0, POPULATION - 1)
      rand2 = random.randint(0, POPULATION - 1)

   p1 = copy.deepcopy(population[rand1])
   p2 = copy.deepcopy(population[rand2])
   parents.append(p1)
   parents.append(p2)
   return parents

def local_improvement(clique: Clique):
   gBest = clique.clone()
   for i in range(0, LOCAL_IMPROVEMENT):
      rand1 = random.randint(0, len(clique.clique) - 1)
      rand2 = random.randint(0, len(clique.clique) - 1)
      count = 0

      while rand1==rand2:
         count += 1
         if count > UNIQUE_ITERATIONS:
            break
         rand1 = random.randint(0, len(clique.clique) - 1)
         rand2 = random.randint(0, len(clique.clique) - 1)

      vertex1 = clique.clique[rand1]
      vertex2 = clique.clique[rand2]
      clique.remove_vertex(vertex1)
      clique.remove_vertex(vertex2)
      sortedList = clique.compute_sorted_list()
      count = 0

      while len(clique.pa) > 0:
         node = sortedList[count].node
         count += 1
         if node >= NUMBER_NODES:
            print("***Node greater: ", node, "***")
            exit(0)

         if clique.contains_in_pa(node):
            clique.add_vertex(node)

      if len(gBest.clique) < len(clique.clique):
         gBest = clique.clone()

   clique = gBest


def mutate(clique: Clique):
   flags = [False] * NUMBER_NODES

   for _ in range(0, MUTATIONS):
      rand = random.randint(0, len(clique.clique) - 1)
      count = 0
      while flags[rand]:
         rand = random.randint(0, len(clique.clique) - 1)
         count += 1
         if count > UNIQUE_ITERATIONS:
            break

      flags[rand] = True
      vertex = clique.clique[rand]
      clique.remove_vertex(vertex)

   rand = random.random()
   if rand < 0.5:
      sortedList = clique.compute_sorted_list()
      cnt = 0
      while len(clique.pa) > 0:
         node = sortedList[cnt].node
         cnt += 1
         if clique.contains_in_pa(node):
            clique.add_vertex(node)
   else:
      while len(clique.pa) > 0:
         rand = random.randint(0, len(clique.pa) - 1)
         vertex = clique.pa[rand]
         clique.add_vertex(vertex)

def genetski(filepath: str, iterations) -> Clique:

   process_data(filepath)
   iters = int(iterations)

   graph.sortList()
   print("\nGenerating initial population...")
   population = generate_random_population()
   population.sort(key= lambda x: len(x.clique), reverse=True)

   gBest :Clique = population[0].clone()
   prevBest = len(gBest.clique)
   cnt = 0
   for i in range(0, iters):
      if prevBest == len(gBest.clique):
         cnt += 1
         if cnt > SHUFFLE_TOLERANCE:
            population = generate_random_population()
            random.seed(datetime.now().microsecond)
            cnt = 0
      else:
         prevBest = len(gBest.clique)
         cnt = 0

      newPopulation = []
      population.sort(key= lambda x: len(x.clique), reverse=True)

      localBest = population[0]
      if len(gBest.clique) < len(localBest.clique):
         gBest = localBest.clone()

      local_improvement(gBest)
      newPopulation.append(gBest)

      for i in range(0, POPULATION - 1):
         parents = random_selection(population)
         offspring = intersection_crossover(parents[0], parents[1])
         local_improvement(offspring)
         if len(offspring.clique) <= len(parents[0].clique) or len(offspring.clique) <= len(parents[1].clique):
            mutate(offspring)

         newPopulation.append(offspring)

      population = newPopulation

   filename = filepath.split(os.sep)[-1][:-4]+"_total_iters_"+str(iterations)+".png"
   pic_filepath = os.path.join(os.getcwd(), graph_pics_dir, filename)
   graph.visualize(gBest.clique, pic_filepath, filename)

   return gBest

def gen_for_all_files(file_no):
   global DEFAULT_TOTAL_ITERATIONS
   files = [graph_1, graph_2, graph_3, graph_4, graph_5]
   if file_no is None:
      for filename in files:
         current_file = os.path.join(os.getcwd(), filename)
         print("--------------------------","Started working on: "+ current_file, sep='\n')
         genetski(current_file, DEFAULT_TOTAL_ITERATIONS) 

   else:
      if file_no > len(files):
         print("There are only", len(files), files)
         exit(0)

      current_file = os.path.join(os.getcwd(), files[file_no])
      print("--------------------------","Started working on: "+ current_file, sep='\n')
      genetski(current_file, DEFAULT_TOTAL_ITERATIONS) 


if __name__ == '__main__':

   random.seed(datetime.now().microsecond)
   total_args = len(sys.argv)
   if total_args <= 2:
      gen_for_all_files(None if total_args != 2 else int(sys.argv[1]))
   else:
      if total_args < 3:
         print("\nSet filename and iterations as argument\n\n")
         exit(0)

      iterations = int(sys.argv[2])
      
      gBest = genetski(sys.argv[1], iterations)

      print("\nVertices in the Clique:\n")
      for i in range(0, len(gBest.clique)):
         print(gBest.clique[i] + 1," ")
      print("\n\n")