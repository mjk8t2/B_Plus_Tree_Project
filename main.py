import bplustree as bp
import bcv_utilities as bcv
import random #just for testing purposes

# START TEST 1 ---------------------------------------

#insertlist = bcv.rcsvail("insertlist.csv")
#deletelist = bcv.rcsvail("deletelist.csv")
insertlist = random.sample(range(100, 1000), 60)
deletelist = random.sample(insertlist, 60)
#bcv.elacsv(insertlist, "insertlist.csv")
#bcv.elacsv(insertlist, "deletelist.csv")

tree1 = bp.bplustree(4)
for i in range(0, len(insertlist)):
  print("Inserting key value", insertlist[i])
  tree1.insert(insertlist[i])
  tree1.prettyprint()
tree1.export_tree_html("mytree.html")
for i in range(0, len(deletelist)):
  print("Deleting key value", deletelist[i])
  tree1.delete(deletelist[i])
  tree1.prettyprint()

# END TEST 1 ----------------------------------------
