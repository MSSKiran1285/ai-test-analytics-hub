# Phase 0 Plan – EDA & Baseline ML

## 1. Objective

Establish a minimal dataset and run initial exploratory data analysis (EDA) 
locally before setting up AWS infrastructure. This ensures clarity on the 
features, labels, and ML approach before implementing cloud components.

---

## 2. Dataset Inputs (Synthetic)

- `sample_test_cases.csv`  
- `sample_defects.csv`

---

## 3. EDA Goals

1. Understand dataset structure  
2. Join test cases and defect data  
3. Compute basic metrics:
   - Failure rate  
   - Defect count  
   - High-severity defect count  
4. Visualize trends:
   - Failures per module  
   - Defects per release  
   - High-risk test cases  
5. Define initial *naive risk score* (baseline)

---

## 4. ML Strategy (Phase 1 Preview)

**Label (y):**  
Binary classification:  
`high_risk = 1` if (failure_rate > 0.3 OR high_sev_defects > 0), else 0

**Features (X):**
- Execution_count  
- Failure_count  
- Past_failure_rate  
- Defect_count  
- High_sev_defects  
- Project (categorical)  
- Module (categorical)

Models planned:
- RandomForestClassifier  
- XGBoostClassifier  

Evaluation metrics:
- AUC  
- Precision/Recall  
- F1  
- Confusion Matrix  

---

## 5. Deliverables

- Updated EDA notebook (`01_eda_and_baseline.ipynb`)  
- Markdown summary of findings  
- ML-ready processed dataset in `data/processed/`  
