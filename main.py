import bplustree as bp
import bcv_utilities as bcv

# START TEST 1 ---------------------------------------

buildlist = [12, 35, 3, 20, 85, 22, 5, 10, 1, 18, 11, 55, 99, 36, 47]
sequence = [("D", 85), ("D", 84), ("D", 18), ("I", 19), ("D", 5), ("D", 47), ("D", 99), ("I", 11)]

mytree = bp.bplustree(4)
for i in buildlist:
  mytree.insert(i)
print("Original tree:")
mytree.prettyprint()
mytree.graphvizit("mytree0", "Original tree")

for i in range(0, len(sequence)):
  if sequence[i][0] == "D":
    if sequence[i][1] in mytree.iil:
      print("Deleting key value", sequence[i][1])
      mytree.delete(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "After deleting key value " + str(sequence[i][1]))
    else:
      print("Key with value", sequence[i][1], "is not in the tree! No change made.")
      mytree.delete(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "Key with value " + str(sequence[i][1]) + " is not in the tree! No change made.")
  elif sequence[i][0] == "I":
    if sequence[i][1] not in mytree.iil:
      print("Inserting key value", sequence[i][1])
      mytree.insert(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "After inserting key value " + str(sequence[i][1]))
    else:
      print("Key with value", sequence[i][1], "is already in the tree! No change made.")
      mytree.insert(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "Key with value " + str(sequence[i][1]) + " is already in the tree! No change made.")

# END TEST 1 ----------------------------------------