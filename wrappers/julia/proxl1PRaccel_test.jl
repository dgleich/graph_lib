include("proxl1PRaccel.jl")
include("readSMAT.jl")
A=readSMAT("../../graph/Unknown.smat")
A=A+A';
d=vec(sum(A,1)')
ds=sqrt.(d)
dsinv=1./ds
ref_node=101
(not_converged,grad,p)=proxl1PRaccel(A,ref_node,d,ds,dsinv)
@show p
