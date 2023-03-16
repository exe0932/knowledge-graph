# knowledge-graph
Construct knowledge graph with neo4j
##  Database
The private data of the hospital, here only provides the format, not the data
database
```
{ "就诊号" : "88888888", "科室名称" : "口腔科门诊", "患者名称" : "X", "医生工号" : "88888", "医疗付款方式" : "广州市职工医保", "主要诊断编码" : "K04.000",  "主要诊断名称" : "牙髓炎", "医生名称" : "X" }
```
## Build Graph 
Import data, create nodes, and input to the knowledge graph
```
build_medicalgraph_1.py
```