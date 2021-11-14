from pyeplan import rousys, datsys, inosys

datsys = datsys('wat_inv')
datsys.data_extract()
datsys.kmeans_clust()

rousys = rousys('wat_inv')
rousys.min_spn_tre()

inosys = inosys('wat_inv', ref_bus = 260)
inosys.solve()

# invest: True/False indicates binary/continuous investment-related variables 
# commit: True/False indicates biniary/continuous commitment-related variables 
# network: True/False indicates including/excluding network-related constraints 
# phase: 3/1 indicates including a three/single phase model