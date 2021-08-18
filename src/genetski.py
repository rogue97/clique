from numpy import zeros
import copy
import sys
import random

# ucitava se iz fajla u processData
NUMBER_NODES = None
NUMBER_EDGES = None
    
POPULATION = 10             # size of the population
LOCAL_IMPROVEMENT = 10      # number of local improvements
GENERATIONS = 10000         # number of generations to run the algorithm
MUTATIONS = 1 	            # How many vertices to remove randomly in the mutate() function
UNIQUE_ITERATIONS = 100	    # Used by localImprovement() to prevent a stall for very small cliques
SHUFFLE_TOLERANCE = 10      # Generate a fresh population after a stall


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

# DescendingNode -> sortiranje nodova po degree

# DescendingSortedListNode -> sortiranje nodova po reach

class Graph:
   def __init__(self):
      # lista Node-ova
      self.nodes = {}
      for i in range(0, NUMBER_NODES+1):
         self.nodes[i] = None
      self.aMatrix = zeros((NUMBER_NODES, NUMBER_NODES))
      self.sortedNodes = []

    # detruktor za nodes i aMatrix...
    
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
      # za sortiranje objekata ove klase?
      pass

# A global instance of the Graph class used througout the code
graph :Graph = None

class Clique:
   def __init__(self, firstVertex = None):
      global graph

      self.clique = [] # int
      self.pa = [] #int
      self.mapPA = {} # int bool less<int> videti za sta sluzi less<int>
      self.mapClique = {} # int bool less<int> videti za sta sluzi less<int>
      
      # cuvanje mesta za niz od NUMBER_NODES elemenata za clique i pa
      # TODO: dorada  ?[None] * NUMBER_NODES?
      self.clique.append(firstVertex)

      for i in range(0, NUMBER_NODES):
         if i == firstVertex:
            continue
         else:
            if graph.aMatrix[i][firstVertex] == 1:
               self.pa.append(i)


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
      for ver in self.pa: # da li je ovde bitno koji je iterator, i da li je on sortiran???
         if ver == vertex:
            flag = True
            toRemove = ver
            break

      if flag and toRemove is not None:
         self.pa.remove(toRemove)

   
   def contains_in_pa(self, vertex) -> bool:
      if vertex not in self.mapPA.keys():
         return
      
      return self.mapPA[vertex] # znaci ono jeste mapa int, bool ostaje samo da se vidi sta je less!
         
   #TODO ovo i slicno moze sve da se skrati cini mi se? postoji jednostavniji zapis u py
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
         return False
      return self.mapClique[vertex]
      
   def compute_sorted_list(self) -> list: #vector<SortedListNode>
      global graph

      sortedList = []
      for i in range(0, len(self.pa)):
         node1 = self.pa[i]
         reach = 0
         for j in range(0, len(self.pa)):
            if i == j:
               continue # refaktorisati ovo da bude efikasnije
            node2 = self.pa[j]
            if graph.aMatrix[node1][node2] == 1:
               reach += 1
         n = SortedListNode(node1, reach)
         sortedList.append(n)
         # TODO dorada
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

# def generate_random_number  nepotrebno
# def generate_double_random_number  nepotrebno

def process_data(filename):
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
         for i in range(0, NUMBER_EDGES):
            line = f.readline()
            tok = line.split(' ')
            sv = int(tok[1]) -1
            ev = int(tok[2]) -1
            graph.add_edge(sv,ev)

   except IOError as e:
      print("No file found")
   except:
      print("Unexpected error:", sys.exc_info()[0])


def generate_random_population():
   print("\nGenerating population...")

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

   node = graph.sortedNodes[0]
   clique = Clique(node)
   sortedList = clique.compute_sorted_list()
   count = 0
   while len(clique.pa) > 0:
      node = sortedList[0].node
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
      rand1 = random.randint(0, POPULATION - 1)
      rand2 = random.randint(0, POPULATION - 1)
      count = 0

      while rand1==rand2:
         count += 1
         if count > UNIQUE_ITERATIONS:
            break
         rand1 = random.randint(0, POPULATION - 1)
         rand2 = random.randint(0, POPULATION - 1)

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
