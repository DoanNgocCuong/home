### **Cluster Analysis: Summary**

#### **What is Cluster Analysis?**

- **Cluster:** A group of data objects that are:
    - **Similar (related)** within the same group.
    - **Dissimilar (unrelated)** to objects in other groups.
- **Cluster Analysis (Clustering):** The process of grouping data objects based on their characteristics, identifying patterns, and forming clusters of similar data.

#### **Key Features:**

- **Unsupervised Learning:**
    
    - No predefined labels or classes; the algorithm learns patterns from data observations.
    - Different from supervised learning, where labeled examples are provided.
- **Applications:**
    
    - **As a stand-alone tool:** To understand data distribution and explore patterns.
    - **As preprocessing:** To prepare data for regression, classification, or other tasks.

---

#### **Applications of Cluster Analysis:**

1. **Data Reduction:**
    
    - Reducing the complexity of data by grouping similar objects.
2. **Summarization:**
    
    - Preprocessing for techniques like regression, PCA (Principal Component Analysis), classification, or association rule mining.
3. **Compression:**
    
    - Used in image processing (e.g., vector quantization).
4. **Hypothesis Generation & Testing:**
    
    - Identifying patterns for building or testing hypotheses.
5. **Prediction Based on Groups:**
    
    - Making predictions using identified clusters.
6. **Finding K-Nearest Neighbors:**
    
    - Efficiently locating nearest neighbors using clusters.
7. **Localized Search:**
    
    - Limiting search to specific clusters to increase speed.
8. **Outlier Detection:**
    
    - Identifying data points far from any cluster, marking them as potential anomalies.

---

### **Why Use Cluster Analysis?**

- To **understand patterns** in data.
- To **simplify and preprocess** data for other algorithms.
- To **detect anomalies** and **group data efficiently**.

Cluster analysis is a versatile tool used in a variety of fields like market segmentation, image compression, anomaly detection, and exploratory data analysis.



### **Detailed Steps to Develop a Clustering Task**

|**Step**|**Description**|**Examples/Notes**|
|---|---|---|
|**1. Feature Selection**|Select the most relevant features (attributes) for the clustering task to ensure meaningful groupings and reduce noise. Redundant or irrelevant features should be removed.|- **Example:** In customer segmentation, select features like age, income, and spending habits; remove irrelevant features like customer ID.|
|**2. Proximity Measure**|Define a measure to compute the similarity (or dissimilarity) between two feature vectors. The choice of proximity measure depends on the type of data (numerical, categorical, or mixed).|- **Common Measures:** - Euclidean Distance (for numerical data) - Manhattan Distance - Cosine Similarity (for text) - Jaccard Index (for binary data) - Dynamic Time Warping (for time-series data).|
|**3. Clustering Criterion**|Specify the criterion to evaluate the quality of clusters. This could be a **cost function** (to minimize within-cluster distance) or a set of rules for defining clusters.|- **Example:** - For K-Means: Minimize the sum of squared distances (inertia) between points and cluster centroids. - For DBSCAN: Define density-based criteria such as the minimum number of points in a neighborhood.|
|**4. Clustering Algorithms**|Select the clustering algorithm that best fits the data and task characteristics. The algorithm's choice depends on factors like data type, size, and expected number of clusters.|- **Examples of Algorithms:** - K-Means: For compact, spherical clusters. - Hierarchical Clustering: To capture nested or hierarchical relationships. - DBSCAN: For data with arbitrary-shaped clusters or noise. - Gaussian Mixture Models (GMM): For overlapping clusters.|
|**5. Validation of Results**|Validate the quality of the clustering results using statistical tests, visualizations, or metrics. Ensure that the clustering output makes sense and achieves the task’s objectives.|- **Methods for Validation:** - Internal Validation: Metrics like Silhouette Score, Dunn Index. - External Validation: Compare clusters with ground truth using Adjusted Rand Index. - Visualize: Use scatter plots, dendrograms, or t-SNE for insights.|
|**6. Interpretation of Results**|Analyze the clusters to understand their significance, identify patterns, and extract actionable insights. This step connects the clustering output to real-world meaning.|- **Example:** In customer segmentation, interpret each cluster as a group of customers with similar behaviors (e.g., high spenders, budget-conscious buyers).|
|**7. Integration with Applications**|Apply the clustering results in practical applications or as preprocessing for other machine learning tasks. Use clusters to enhance decision-making or optimize systems.|- **Example Applications:** - Market Segmentation: Target marketing campaigns for specific customer groups. - Image Compression: Reduce image size using clustering (e.g., vector quantization). - Anomaly Detection: Identify outliers based on clustering distance.|

---

### **Key Notes:**

- **Iterative Process:** Clustering is often an iterative process. Features, algorithms, or proximity measures might need to be refined based on validation results.
- **Choice of Algorithm:** The choice heavily depends on **domain knowledge** and **data characteristics** (e.g., K-Means works well for spherical clusters but fails for complex shapes like in DBSCAN scenarios).
- **Scalability:** For large datasets, computational efficiency is critical, so scalable clustering methods (e.g., MiniBatch K-Means) might be required.



---

### **Cách đo lường chất lượng của clustering**

#### **1. Phép đo tương đồng/khác biệt:**

- **Tương đồng thường được biểu diễn qua các hàm khoảng cách d(i,j)d(i, j):**
    - Tùy vào loại dữ liệu mà sử dụng hàm khoảng cách phù hợp:
        - **Dữ liệu dạng số (Interval-Scaled):** Khoảng cách Euclid, Manhattan.
        - **Dữ liệu nhị phân (Boolean):** Hamming.
        - **Dữ liệu phân loại (Categorical):** Matching coefficient.
        - **Dữ liệu thứ tự (Ordinal):** Rank correlation.
    - Có thể gán trọng số cho các biến để phản ánh mức độ quan trọng của chúng trong bài toán.

#### **2. Hàm đánh giá chất lượng cụm (Quality Function):**

- Một hàm riêng để đo lường mức độ tốt của clustering.
    - **Ví dụ các chỉ số đo lường:**
        - **Silhouette Score:** Đo mức độ gần của một điểm với cụm của nó so với các cụm khác.
        - **Dunn Index:** Tỷ lệ giữa khoảng cách nhỏ nhất giữa các cụm và khoảng cách lớn nhất trong cùng một cụm.
        - **Davies-Bouldin Index:** Đo mức độ tương đồng trung bình của mỗi cụm với cụm gần nhất.
    - Tuy nhiên, việc đánh giá thường phụ thuộc vào ngữ cảnh và mục đích của bài toán.

---

### **Thách thức khi đánh giá chất lượng clustering**

1. **Tính chủ quan:**
    - Thế nào là "tương đồng đủ" hay "cụm đủ tốt" thường là đánh giá mang tính chủ quan và phụ thuộc vào bài toán cụ thể.
2. **Không có thước đo chung:**
    - Không có một tiêu chuẩn chung vì mỗi loại dữ liệu và ứng dụng lại cần cách đánh giá riêng.

---

### **Kết luận**

- **Clustering tốt** cần tạo ra cụm dữ liệu rõ ràng, liên quan trong cụm và khác biệt giữa các cụm.
- Chất lượng clustering phụ thuộc vào:
    - Phép đo tương đồng/khác biệt.
    - Cách triển khai thuật toán.
    - Hiểu biết ngữ cảnh và mục tiêu bài toán.
- Việc đo lường chất lượng cụm thường đòi hỏi sự kết hợp giữa kiến thức thuật toán và hiểu biết chuyên môn về dữ liệu.

### **Considerations for Cluster Analysis**

|**Aspect**|**Description**|**Examples**|
|---|---|---|
|**Partitioning Criteria**|Defines how clusters are formed:||
||- **Single Level:** Flat clusters, no hierarchy (e.g., K-Means).||
||- **Hierarchical Partitioning:** Multi-level grouping, suitable for nested relationships (e.g., Hierarchical Clustering).||
|**Separation of Clusters**|Defines exclusivity of cluster membership:||
||- **Exclusive:** Each object belongs to only one cluster (e.g., customers in regions).||
||- **Non-Exclusive:** Objects can belong to multiple clusters (e.g., documents in multiple topics).||
|**Similarity Measure**|Defines how similarity or distance between objects is calculated:||
||- **Distance-Based:** Euclidean, Manhattan, or vector distances.||
||- **Connectivity-Based:** Density or contiguity-based measures (e.g., in DBSCAN).||
|**Clustering Space**|Defines the dimensionality of the clustering process:||
||- **Full Space:** Used for low-dimensional data.||
||- **Subspaces:** Suitable for high-dimensional data where only subsets of dimensions are relevant.||

---

### **Requirements and Challenges in Cluster Analysis**

|**Challenge/Requirement**|**Description**|
|---|---|
|**Scalability**|Clustering must handle full datasets efficiently, not just subsets or samples.|
|**Support for Various Data Types**|Algorithms should work with diverse attribute types (e.g., numerical, binary, categorical, ordinal, and mixed data).|
|**Constraint-Based Clustering**|Allow users to specify constraints or domain knowledge for better cluster definitions.|
|**Interpretability and Usability**|Clusters should be easy to interpret and useful for decision-making.|
|**Discovery of Arbitrary Shapes**|The algorithm should find clusters with arbitrary shapes, not just spherical clusters.|
|**Dealing with Noise**|Handle noisy and outlier data effectively.|
|**Incremental Clustering**|Support updates to clusters as new data arrives or input order changes.|
|**High Dimensionality**|Handle high-dimensional data, often through dimensionality reduction or subspace clustering.|

---

### **Major Clustering Approaches**

| **Approach**               | **Description**                                                                                               | **Typical Methods**           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Partitioning Approach**  | Divides data into non-overlapping clusters and optimizes a criterion like minimizing within-cluster variance. | K-Means, K-Medoids, CLARANS   |
| **Hierarchical Approach**  | Creates a tree-like structure (dendrogram) by progressively merging or splitting clusters.                    | Diana, Agnes, BIRCH, CAMELEON |
| **Density-Based Approach** | Identifies clusters based on regions of high density, allowing detection of arbitrary shapes.                 | DBSCAN, OPTICS, DenClue       |
| **Grid-Based Approach**    | Divides data space into grids and forms clusters based on grid densities.                                     | STING, WaveCluster, CLIQUE    |

---

### **Key Notes:**

- The choice of **clustering approach** and **criteria** depends on the dataset, application, and computational resources.
- Clustering is iterative and often requires validation and refinement to ensure useful and interpretable results.


### **So sánh chi tiết các phương pháp Clustering**

|**Phương pháp**|**Mô tả**|**Các thuật toán tiêu biểu**|**Ưu điểm**|**Nhược điểm**|
|---|---|---|---|---|
|**Partitioning Approach**|Chia dữ liệu thành các cụm không chồng lấn, tối ưu một tiêu chí (ví dụ: giảm thiểu khoảng cách trong cụm).|K-Means, K-Medoids, CLARANS|- Nhanh và đơn giản.- Hiệu quả với dữ liệu nhỏ hoặc cụm có hình dạng đơn giản (spherical).|- Yêu cầu số cụm trước (k).- Không hiệu quả với cụm phức tạp hoặc dữ liệu nhiễu.- Nhạy cảm với giá trị ban đầu.|
|**Hierarchical Approach**|Xây dựng cấu trúc cây (dendrogram) bằng cách hợp nhất hoặc tách dần các cụm dựa trên tiêu chí nào đó.|Diana, Agnes, BIRCH, CAMELEON|- Không cần số cụm trước.- Có thể phân tích cụm ở nhiều cấp độ (hierarchical).|- Tốn thời gian với dữ liệu lớn.- Khó điều chỉnh sau khi đã chia cụm.|
|**Density-Based Approach**|Phát hiện cụm dựa trên mật độ điểm dữ liệu; phù hợp với các cụm có hình dạng bất kỳ.|DBSCAN, OPTICS, DenClue|- Tìm được cụm với hình dạng phức tạp.- Xử lý tốt dữ liệu nhiễu.- Không cần số cụm trước.|- Hiệu suất giảm với dữ liệu có mật độ không đồng đều.- Cần chọn tham số như ε và MinPts cẩn thận.|
|**Grid-Based Approach**|Chia không gian dữ liệu thành các lưới nhỏ, sau đó gom cụm dựa trên mật độ của các lưới.|STING, WaveCluster, CLIQUE|- Tốc độ nhanh với dữ liệu lớn.- Phù hợp với không gian đa cấp độ.|- Kém hiệu quả nếu cụm không đồng nhất hoặc kích thước lưới không phù hợp.|
|**Model-Based Approach**|Giả định mỗi cụm có một mô hình riêng, sau đó tối ưu để tìm cụm tốt nhất dựa trên mô hình.|EM (Expectation Maximization), SOM, COBWEB|- Mô hình linh hoạt hơn (hỗ trợ cụm hình elip, phức tạp).- Tích hợp thống kê.|- Tốn thời gian hơn do phải tối ưu mô hình.- Nhạy cảm với giá trị ban đầu và giả định mô hình.|
|**Frequent Pattern-Based**|Tìm cụm dựa trên các mẫu xuất hiện thường xuyên trong dữ liệu.|p-Cluster|- Tìm được các mối quan hệ mạnh mẽ giữa các đối tượng.|- Chỉ phù hợp với dữ liệu có cấu trúc đặc biệt (mẫu lặp lại).|
|**User-Guided/Constraint-Based**|Sử dụng các ràng buộc do người dùng chỉ định hoặc dựa vào đặc thù của ứng dụng.|COD (Clustering with Obstacles), Constrained Clustering|- Tận dụng kiến thức chuyên môn để cải thiện chất lượng cụm.- Linh hoạt với các ứng dụng cụ thể.|- Phụ thuộc vào ràng buộc của người dùng.- Khó áp dụng với dữ liệu không có nhiều thông tin bổ sung.|
|**Link-Based Clustering**|Dựa trên các liên kết giữa các đối tượng để tạo cụm, thường dùng trong mạng xã hội hoặc dữ liệu đồ thị.|SimRank, LinkClus|- Phù hợp với dữ liệu liên kết (như mạng xã hội, đồ thị).- Xử lý dữ liệu phi cấu trúc tốt.|- Yêu cầu dữ liệu có liên kết rõ ràng.- Hiệu quả giảm với đồ thị lớn và phức tạp.|

---

### **Chi tiết từng phương pháp:**

#### **1. Partitioning Approach (Phân hoạch dữ liệu):**

- **Ưu điểm:** Đơn giản, dễ triển khai, hiệu quả với cụm dạng cầu (spherical).
- **Nhược điểm:** Nhạy cảm với nhiễu, không xử lý tốt cụm phi tuyến, yêu cầu biết số cụm trước.

#### **2. Hierarchical Approach (Phân cấp dữ liệu):**

- **Ưu điểm:** Cung cấp phân cụm ở nhiều cấp độ, không yêu cầu số cụm trước.
- **Nhược điểm:** Tốn tài nguyên, không hiệu quả với dữ liệu lớn.

#### **3. Density-Based Approach (Dựa trên mật độ):**

- **Ưu điểm:** Tìm cụm có hình dạng bất kỳ, phát hiện nhiễu tốt.
- **Nhược điểm:** Hiệu quả phụ thuộc vào tham số ε (bán kính cụm) và MinPts (số điểm tối thiểu).

#### **4. Grid-Based Approach (Dựa trên lưới):**

- **Ưu điểm:** Tốc độ cao, hiệu quả với dữ liệu lớn.
- **Nhược điểm:** Khó khăn với cụm phức tạp, phụ thuộc vào kích thước lưới.

#### **5. Model-Based Approach (Dựa trên mô hình):**

- **Ưu điểm:** Linh hoạt, hỗ trợ các cụm phức tạp hơn.
- **Nhược điểm:** Chậm hơn, yêu cầu giả định mô hình chính xác.

#### **6. Frequent Pattern-Based (Dựa trên mẫu thường xuyên):**

- **Ưu điểm:** Tìm các mối quan hệ mạnh mẽ, hữu ích với dữ liệu lặp lại.
- **Nhược điểm:** Hạn chế với dữ liệu không có mẫu lặp đặc trưng.

#### **7. User-Guided/Constraint-Based (Ràng buộc người dùng):**

- **Ưu điểm:** Linh hoạt, tận dụng kiến thức chuyên môn.
- **Nhược điểm:** Phụ thuộc vào thông tin ràng buộc.

#### **8. Link-Based Clustering (Dựa trên liên kết):**

- **Ưu điểm:** Hiệu quả với dữ liệu liên kết (mạng xã hội, đồ thị).
- **Nhược điểm:** Phức tạp khi áp dụng trên dữ liệu đồ thị lớn.

---

### **Tóm gọn:**

- **Phương pháp nào nên chọn?** Tùy vào loại dữ liệu:
    - **Dữ liệu nhỏ, dễ xử lý:** Partitioning (K-Means).
    - **Cụm phức tạp, có nhiễu:** Density-Based (DBSCAN).
    - **Quan hệ thứ bậc hoặc nhiều cấp độ:** Hierarchical (Diana, BIRCH).
    - **Mạng xã hội, đồ thị:** Link-Based (SimRank, LinkClus).
- **Hạn chế:** Tất cả phương pháp đều có nhược điểm riêng, nên lựa chọn phụ thuộc vào đặc điểm dữ liệu và ứng dụng cụ thể.

![[Pasted image 20241127113028.png]]