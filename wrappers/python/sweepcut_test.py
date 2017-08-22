from sweepcut import sweepcut
from list_to_CSR import list_to_CSR
import numpy as np

(m,n,ai,aj,a) = list_to_CSR("../../graph/minnesota.smat")

f = open("../../graph/minnesota_ids.smat")
data = f.read()
data = data.split()
nids = int(data[0])
ids = []
for i in range(nids):
    ids += [int(data[i + 1])]
f.close()

values=[]
flag = 1
(actual_length,bestclus)=sweepcut(n,ai,aj,a,ids,nids,values,flag)
print actual_length,bestclus
