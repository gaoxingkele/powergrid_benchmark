# Short-term-Global-Horizontal-Irradiance-Forecasting-Using-Weather-Classified-Categorical-Boosting
## Abstract
Accurate short-term solar irradiance (SI) forecasting is crucial for renewable energy integration to ensure unit commitment and economic load dispatch. However, hourly SI prediction is very challenging due to atmospheric conditions and weather fluctuations. This study proposes a hybrid approach using weather classification and boosting algorithms for short-term global horizontal irradiance (GHI) forecasting. In data pre-processing steps,  we employ random forest for feature selection and K-means clustering for weather classification. The weather-based clustered data is used for the model training using categorical boosting (CatBoost). The proposed weather-classified categorical boosting (WC-CB) scheme is compared with benchmarks in literature like adaptive boosting (AdaBoost), bi-directional long short-term memory (BiLSTM) and gated recurrent unit (GRU) using datasets from two distinct geographical locations obtained from the National Solar Radiation Database (NSRDB). The results show that the proposed WC-CB hybrid approach has lower forecast errors compared to conventional CatBoost modelling. The error reduction of 16\% and 39\% in root mean square error and 6\% and 9\% in mean absolute error is recorded for the two datasets, respectively. These findings demonstrate the importance of weather classification in improving forecasting accuracy, which has potential implications for broader renewable energy applications.

# Getting Started
Follow the steps below to set up and run the code for short-term global horizontal irradiance forecasting.

## Prerequisites
Ensure you have the following software installed:<br>
- Python 3.10.9 or above<br>

Required libraries: <br>
 -  NumPy<br>
 -  Pandas<br>
 -  Scikit-learn<br>
 -  CatBoost<br>
 -  Matplotlib<br>
 -  Seaborn<br>
 -  TensorFlow<br>
 -  Keras<br>
 -  RandomForest<br>

# Running the Code
## Step 1: Data Preprocessing
Run k-mean_clustering.ipynb script to perform weather-based clustering.<br>
Run splitting_the_clustering_data.ipynb script to separate respective clusters.<br>

## Step 2: Model Training and Evaluation

Run the Bidirectional_LSTM.ipynb, GRU.ipynb, CatBoost.ipynb and adaboost.ipynb scripts from respective folders to train and evaluate the weather-classified CatBoost model against benchmark techniques.

## Step 3: Visualization
Run the bar_plot.ipynb, graph.ipynb and scatter_regression_plot.ipynb scripts to visualize the forecasting results and compare the model's performance.


Short-term-Global-Horizontal-Irradiance-Forecasting/ <br>
├── Datasets/                   # Folder for datasets <br>
├── Weather Calssification/     # Folder containing scripts for data preprocessing and clustering <br>
├── Simulation for/             # Folder containing scripts for model training and evaluation <br>
├── Graphicall illustration     # Folder containing scripts for result visualization <br>
├── README.md                   # Project README file <br>




## Reference
Please cite this work as:
"Ubaid Ahmed, Ahsan Raza Khan, Anzar Mahmood, Iqra Rafiq, Rami Ghannam, Ahmed Zoha,
Short-term global horizontal irradiance forecasting using weather-classified categorical boosting,
Applied Soft Computing,
2024,
111441,
ISSN 1568-4946,
https://doi.org/10.1016/j.asoc.2024.111441.
(https://www.sciencedirect.com/science/article/pii/S1568494624002151)"
