import bcv_utilities as bcv
import ast
import os
from graphviz import Digraph, nohtml

empty_key = "_"
empty_child = "·"
pointer = " → "

class bplustree:
  def __init__(self, order, filename = ""):
    self.order = order
    self.pop_up_index = 2*((order - 1)//2) + 1
    self.height = 0
    self.root = [empty_child]
    self.iil = []
    self.nodenum = 0
    if filename != "":
      self.root = ast.literal_eval(bcv.rfcas(filename))
      self.calculate_height(self.root)

  def calculate_height(self, alist):
    for i in alist:
      if type(i) == list:
        self.height += 1
        self.calculate_height(i)
      elif not list in alist:
        break

  def is_leaf(self, node):
    return empty_child in node

  def is_full(self, node):
    return len(node) >= 2*self.order - 1

  def keys_in_node(self, node):
    keys_in_node = []
    for j in range(1, len(node), 2):
      keys_in_node.append(node[j])
    return keys_in_node

  def keys_in_tree(self, keylist, alist):
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        self.keys_in_tree(keylist, alist[i])
      elif alist[i] != empty_child and alist[i - 1] == empty_child:
        keylist.append(alist[i])

  def get_node_with_key(self, key, level, alist):
    if level != self.height:
      key_cache = self.keys_in_node(alist) + [key]
      key_cache.sort()
      return self.get_node_with_key(key, level + 1, alist[2*key_cache.index(key)])
    else:
      return alist

  def node_insert(self, key, node, adjnodes = (empty_child, empty_child)):
    push_index = len(node) - 1
    for i in range(1, len(node), 2):
      if key <= node[i]:
        push_index = i - 1
        break
    node.insert(push_index, key)
    node.insert(push_index, adjnodes[0])
    node[push_index + 2] = adjnodes[1]

  def split_node(self, node):
    j = 2 if self.is_leaf(node) else 0
    leftnode = node[:self.pop_up_index + j]
    rightnode = node[self.pop_up_index + 1:]
    return (leftnode, rightnode)

  def insert(self, key):
    if key not in self.iil:self.iil.append(key)
    ml = []
    self.keys_in_tree(ml, self.root)
    if key not in ml:
      self.inserthelp(key, 0, self.root, [empty_child])
            
  def inserthelp(self, key, level, node, node_above):
    if level != self.height:
      key_cache = self.keys_in_node(node) + [key]
      key_cache.sort()
      leafdata = self.inserthelp(key, level + 1, node[2*key_cache.index(key)], node)
    else:
      leafdata = (key, (empty_child, empty_child))
    if leafdata != False and leafdata != None:
      if not self.is_full(node):
        self.node_insert(leafdata[0], node)
        return False
      elif not self.is_full(node_above) and node_above != [empty_child]:
        self.node_insert(leafdata[0], node, leafdata[1])
        self.node_insert(node[self.pop_up_index], node_above, self.split_node(node))
        return False
      elif node_above == [empty_child]:
        self.node_insert(leafdata[0], node, leafdata[1])
        self.root = [empty_child]
        self.node_insert(node[self.pop_up_index], self.root, self.split_node(node))
        self.height += 1
        return False
      else:
        self.node_insert(leafdata[0], node, leafdata[1])
        return (node[self.pop_up_index], self.split_node(node))

  def delete(self, key):
    if key in self.iil: self.iil.remove(key)
    self.deletehelp(key, 0, False, self.root, [empty_child], [empty_child], [empty_child])

  def deletehelp(self, key, level, saw_key, node, node_above, left_node, right_node):
    if level != self.height:
      if key in self.keys_in_node(node):
        saw_key = True
      key_cache = self.keys_in_node(node) + [key]
      key_cache.sort()
      left = [empty_child]
      right = [empty_child]
      if key_cache.index(key) != 0:
        left = node[2*key_cache.index(key) - 2]
      if key_cache.index(key) != len(key_cache) - 1:
        right = node[2*key_cache.index(key) + 2]
      leafdata = self.deletehelp(key, level + 1, saw_key, node[2*key_cache.index(key)], node, left, right)
      if leafdata != False:
        if key in node:
          node[node.index(key)] = leafdata
      return leafdata
    else:
      leafdata = (key, (empty_child, empty_child))
    if key in node and self.is_leaf(node):
      if not saw_key and len(self.keys_in_node(node)) > (self.order)//2:
        j = node.index(key)
        del node[j + 1]
        del node[j]
        return False
      if saw_key and len(self.keys_in_node(node)) > (self.order)//2:
        j = node.index(key)
        del node[j + 1]
        del node[j]
        return self.keys_in_node(node)[-1]
      if len(self.keys_in_node(node)) <= (self.order)//2:
        check1 = not self.is_full(left_node) and self.is_leaf(node) and self.order == 4
        check2 = left_node != [empty_child] and right_node == [empty_child] and len(node_above) > 3
        templist = []
        self.keys_in_tree(templist, self.root)
        ijtr = max(templist)
        temp = self.get_node_with_key(ijtr, 0, self.root)
        check3 = key in temp
        if check1 and check2 and check3:
          j = node.index(key)
          del node[j + 1]
          del node[j]
          rem = node[1]
          del node_above[len(node_above) - 1]
          del node_above[len(node_above) - 1]
          self.node_insert(rem, left_node)
        else:
          self.height = 0
          self.root = [empty_child]
          for i in self.iil:
            self.insert(i)

  def printhelp(self, depth, stringlist, alist):
    stringlist[depth] += "["
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
          stringlist[depth] += empty_child
          self.printhelp(depth + 1, stringlist, alist[i])
      else:
        stringlist[depth] += str(alist[i])
    stringlist[depth] += "]"
    if depth == self.height:
      stringlist[depth] += pointer

  def prettyprint(self):
    stringlist = [""]*(self.height + 1)
    self.printhelp(0, stringlist, self.root)
    stringlist[-1] = str(stringlist[-1][:-len(pointer)])
    for i in stringlist:
      print(i)
    print()

  def export_tree(self, filename):
    file = open(filename, "w")
    file.write(str(self.root))
    file.close()

  def export_tree_html(self, filename):
    stringlist = [""]*(self.height + 1)
    self.printhelp(0, stringlist, self.root)
    stringlist[-1] = str(stringlist[-1][:-len(pointer)])
    newstring = ""
    for i in range(0, len(stringlist)):
      newstring += stringlist[i]
      if i < len(stringlist) - 1:
        newstring += "<br>\n    "
    baseplate = bcv.rfcas("baseplate.html")
    finaloutput = ""
    for i in range(0, len(baseplate)):
      if baseplate[i] == "@":
        finaloutput = baseplate[:i] + newstring + baseplate[i+1:]
        break
    finaloutput = finaloutput.replace(empty_child, "&middot")
    finaloutput = finaloutput.replace(pointer, " &#8594 ")
    file = open(filename, "w", encoding="utf-8")
    file.write(finaloutput)
    file.close()
    
  def graphviznodemaker(self, g, alist):
    contents = ""
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        contents += "<f" + str(i) + "> " + "●"
        self.graphviznodemaker(g, alist[i])
        self.nodenum += 1
      elif alist[i] == empty_child:
        contents += "<f" + str(i) + "> " + "○"
      else:
        contents += "|<f" + str(i) + ">" +str(alist[i])+ " |"
    g.node("node"+str(self.nodenum), nohtml(contents))
    for i in range(0, len(alist)):
      if type(alist[i]) != list and alist[i] != empty_child:
        alist[i] = self.nodenum
    
  def graphvizedgemaker(self, g, alist):
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        g.edge("node" + str(alist[1]) + ":f" + str(i), "node" + str(alist[i][1]) + ":f0")
        self.graphvizedgemaker(g, alist[i])
        
  def graphvizit(self, filename, operation):
    graph = Digraph('g', filename='bplustree.gv', node_attr={'shape': 'record', 'height': '.1'}, format='png', )
    graph.attr(label=operation)
    graph.attr(labelloc="t")
    newtree = dcnl(self.root)
    self.graphviznodemaker(graph, newtree)
    self.graphvizedgemaker(graph, newtree)
    self.nodenum = 0
    graph.render(filename, "output")
    os.remove("output\\" + filename)
      
def dcnl(data):
  out = []
  for el in data:
    if isinstance(el, list):
      out.append(dcnl(el))
    else:
      out.append(el)
  return out