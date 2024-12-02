- movie: LightGCN, BPR, DeepFM, BiVAE, NCF, MF baseline 
- RMSE, Pricision@10, Recall@10, NDCG@10

3. Book: 
- Basé on Singular Value Decomposition SVD, 
- Books - User 10.3M - Item 4.4M - Rating 29.5M (Amazon Reviews Dataset). 
- 2 methods: Conllaoborative (SA SREC, SVD, Sli_Rec) + Content-base (NAML, NPA)
NPA (Neural Recommendation with Personalized Attiion), 
NAML (NeÂMl News Recommendation , ... )

Transfomer based method: SASREC, SSEPT (Collaborative filtering), ... 
Single Value SV: 


4. RAG: 
- model and identify the topic distribution for each research paper. 
- Inputt Abstracts list of artivel 
- b, Co-Author Network: Nodes each node represents an author , edge weight = average topic distributions of co-authored pper 

Apporch1: Topic Model-Based Search 
	- Topic Filtering: 500 most relevant pape based on
	- Embedding and Reranking: 
		- embedding represent absstract 
		- rerank 500
Approach2 : Author Network-Based Search 
1. Topic Filerting: Similar approach 1 => 50 most 
2. Expand Dataset : top 100 author related to above papper 
3. Embedding Reranks 
4. Final: Choose top 10 for the relationship 

Dataset: Kaggle: metadataa: id, submitter, authors, ... 
