A=readSMAT('../../graph/minnesota.smat');
ids=readSeed('../../graph/minnesota_ids.smat');
num=2642;
fun_id=1;
values=[];
[actual_length,results]=sweepcut(A,ids,values,fun_id);
actual_length
results'