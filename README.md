
# Breast Cancer Data Analysis and Machine Learning

An academic data science project exploring breast cancer data through exploratory data analysis, machine learning, statistical methods, and clinical trial data collection.

The project combines two complementary analyses:
1. Breast cancer diagnosis prediction using the Wisconsin Diagnostic Breast Cancer dataset.
2. Collection and analysis of breast cancer clinical trial records using Python and Scrapy.

## 1. Project Objectives

- Explore and visualize patterns in breast cancer datasets.
- Apply supervised and unsupervised machine learning methods.
- Compare classification models using appropriate evaluation metrics.
- Investigate regression, clustering, and dimensionality reduction.
- Collect and analyze publicly available clinical trial records.

## 2. Datasets

### Wisconsin Diagnostic Breast Cancer Dataset

The dataset contains 569 observations with numerical features describing characteristics of cell nuclei extracted from breast mass images.

The classification task is to distinguish between benign and malignant diagnoses.

Dataset file: `data/data.csv`

### Breast Cancer Clinical Trials

The second part of the project explores clinical trial information related to breast cancer.

A Python Scrapy project was used to collect 500 clinical trial records for further analysis.

The scraping implementation is available in the `scraping/` directory.

## 3. Methodology

### Exploratory Data Analysis

The analysis includes:
- Data inspection and quality checks
- Statistical summaries and visualizations
- Feature relationships and correlations
- Examination of class distributions

### Machine Learning

The project explores several techniques, including:

**Classification**
- Logistic Regression
- Random Forest Classifier
- Hyperparameter tuning using GridSearchCV

**Regression**
- Regression models for numerical feature prediction

**Unsupervised Learning**
- Clustering
- Principal Component Analysis (PCA)

### Model Evaluation

For breast cancer classification, the dataset was divided into training (80%) and testing (20%) subsets using a stratified split with `random_state=42`.

Classification performance was assessed using:
- Accuracy
- Precision
- Recall
- F1-score
- ROC AUC
- Confusion matrices

## 4. Classification Results

The Random Forest classifier achieved the following results on the held-out test set:

| Metric | Score |
|---|---:|
| Accuracy | 97.37% |
| Precision | 1.000 |
| Recall | 0.929 |
| F1-score | 0.963 |
| ROC AUC | 0.997 |

These results were obtained on a test set of 114 observations.

The project also compares Logistic Regression models and explores hyperparameter optimization.

## 5. Technologies

- Python
- pandas and NumPy
- scikit-learn
- Matplotlib
- Jupyter Notebook
- Scrapy

## 6. Repository Structure

```text
breast-cancer-ml-analysis/
├── data/
│   └── data.csv
├── notebooks/
│   ├── breast_cancer_ml_analysis.ipynb
│   └── breast_cancer_clinical_trials.ipynb
├── scraping/
│   ├── scrapy.cfg
│   ├── breast_trials.json
│   └── ctgov/
├── README.md
├── requirements.txt
└── .gitignore
```

## 7. Running the Project

The analysis is provided as Jupyter notebooks.

The breast cancer classification notebook uses the dataset stored in `data/data.csv`.

The clinical trials notebook was developed in Google Colab and contains Colab-specific commands. Its scraping implementation is also included separately in the `scraping/` directory.

Detailed environment setup and execution instructions will be finalized after local path and dependency checks.

## 8. Limitations

The Wisconsin dataset is relatively small, and results obtained on a single train/test split may not generalize to other populations or clinical settings.

The project is intended for educational and research purposes only. It is not a validated medical diagnostic system.

## 9. Author

**Nađa Tomović**

Undergraduate student in Informatics and Data Technologies, University of Maribor, Slovenia.

[GitHub](https://github.com/nadjatomovic) | [LinkedIn](https://www.linkedin.com/in/nadja-tomovic/)
