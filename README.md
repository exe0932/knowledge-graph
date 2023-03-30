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
build_medicalgraph.py
```

## Build Vocab
saved vocabulary
```
dict
```

## Build Question classification
Construct feature words, question words, word filtering, and construct word classification
```
question_classifier.py
```

## Build Question parser
For different problems, search and process separately
```
question_parser.py
```

## Build Answer search
Connect the knowledge graph database and find answers for the specified nodes
```
answer_search.py
```

## Run the dialog system
This function is to run the retrieval dialog system, it can be used after running
```
chatbot_graph.py
```