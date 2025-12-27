# Brain Tumor Analysis

Machine learning analysis of brain tumor mutations using the TCGA GBM-LGG dataset.

## About

This project analyzes brain tumor mutation data from The Cancer Genome Atlas (TCGA), focusing on Glioblastoma Multiforme (GBM) and Lower Grade Glioma (LGG) cases.

## Project Structure

```
├── data/                   # Dataset
├── notebooks/              # Jupyter notebooks
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the notebook:
```bash
jupyter notebook notebooks/BrainTumor.ipynb
```

## Dependencies

- pandas
- numpy
- matplotlib
- scikit-learn
- seaborn

## Dataset

TCGA_GBM_LGG_Mutations_all.csv contains:
- Patient demographics
- Mutation data
- Clinical features

---

*For educational and research purposes only.*
