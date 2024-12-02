LEARN FROM BEST PRACTICES AND MANY SUMMARY&PRACTICES OF PEOPLE 

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



-------------------------------------

Methods Semantic Analysis 
- mẹthod: Hỉeachical Graph Convolutions network HIER - GCN (bert encode the review sentence and gen re)
- Domain:Hotel, Resuatl, 
- 4 sentiment: none, pos, neg, neutral
- VNCorenlp, ... 
- Method 3; 

-----------------

Group 7: Film: 
Dataset: Netlfix 2006, 5600 ratings/users, 200 rating/1 films . 
User ID, Fil,, Date, Rading 

Trying to predict the ratings in the test set when given User ID, filmID, and dataset. 
(In other words: Given)

Method ; 

SVD : soimplest solutoion 

- A is the rating matrics, all missing values 
- A = U * Xích ma V_T 
- Either learn a function R'_ij directly 
Method: Time-aware rating predction from assumption that theré tesceits a shift in ủe preferrence s
Grading Boosting decision tree: 


--------------------------------
Group 8: Extract opinions about specific aspects, obtaining deeper and more details. 
3 Main subtassk: 
- MATE Multimodel Aspect Sentiment Classification MASC : MABSSC, MCBSC. 
	- mcbsc : USE , ....
- MASC Multimode 
- ASPE PEpect S Pairs

Method: Text : RNN< LSTM, Bert 
Image : Cnn, Resnet 
Cross model attention mechainis ,; Focus on inô, extract content form text or image, 

Fusion Techiniques : 
	-  Earrly fusion (Feature layer fusion) - Late fusion - Immedate ... 
Dataset;ViMACSA, ... 

Textual Data: Tokenize, Stemming Normalize remove stipss , Image : Normalize, Augmentation, .. 


3.3 Models: FCMF (main model, show in the papper, ) 
MIMN: Feature Extraction, Multimodel Memory Network, Multi, ... 
tomBERT?? 

-------------------

GROUP 8-
Machine learning: TF-IDF, Word Frequency, N-gram models, word couting 

- SVM for multi class finication : One-Rest  (1 class vs others classes)---- One vs One (classifier for every pair of classes : 20*19/2
)- Decision Tree, LSTM, Bi-LSTM
- Finetunging báes methofs: Finetuning the pretrained RoBERTa model (a new traing strategfy for the BERT MODEL). 

dATASET: 510.000 twết, each contain 1 emoji that servers as the classifi cation 

Metrics : Macro-averate F1 Score ??
