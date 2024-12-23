- Nhóm 2: ... 
- Nhóm 3: Book Recommneder system : 
		- Dataset: User Data: 
		- Aim to provide user 2 types of ouput : 
			- Top-K Movie Recommendtions 
			- Rating 
	- RMSE: ...
	- Methods: BPR, LighGCN, 
	- mETRICS: RMSE, Precision @10, Recall @10 
		- LightGCN, 
	- Cold Start Problem: 
		- with LightGCN, EmerG - Item Specific Feature Inteactions for Cold-Start CTR Prediction KDD 2024. 
		- GNN process and predict the likelihood ? 
		- EmerG designed to predict Click-through Rate CTR. 
		- Which estimate the probability that a user .... 
- Result : 
				-  Cold, Warm-A, Warm-B, Warm-C 
Model: LightGCN,   P@10, R@10, P@10, R@10, ... 
	EmerG 
Results: inclusing : MF (baseline), BPR, NCF, DeepFM, FM, BiVAE, LightGCN, EmerG. 
---
