# Model Development Notes

## Modeling Approach

### Algorithm Selection
Tested five algorithms to identify optimal performance:
- Linear Regression (baseline)
- Ridge Regression (regularized linear)
- Random Forest (ensemble)
- XGBoost (gradient boosting)
- LightGBM (gradient boosting)

**Result**: Linear models achieved best generalization performance (85.2% test R²).

### Data Preprocessing
- **Missing values**: Mode imputation for categoricals, median for numerical
- **Outliers**: Removed 6 extreme delivery times using IQR method (99.4% data retained)
- **Feature engineering**: 
  - Distance categories (Small/Medium/Large)
  - Rush hour indicator (Morning/Evening)
- **Encoding**: One-hot encoding for categorical variables

### Train/Test Split
- 80/20 split (795 train, 199 test samples)
- Random state=42 for reproducibility
- No stratification due to continuous target

## Metric Selection

### Primary Metric: R² Score
Chosen because:
- Interpretable as percentage of variance explained
- Standard regression metric for model comparison
- Business stakeholders understand "85% accuracy"

### Secondary Metrics
- **RMSE**: Penalizes large errors (delivery delays)
- **MAE**: Average absolute error in minutes
- **MAPE**: Percentage error for relative performance

*[Add metric comparison table from results here]*

## Hyperparameter Tuning

### Grid Search Strategy
- 5-fold cross-validation for robust parameter selection
- Focused on preventing overfitting given small dataset
- Parameters tested:

**XGBoost**:
- n_estimators: [50, 100, 200]
- learning_rate: [0.1, 0.2] 
- max_depth: [3, 5, 10]
- subsample: [0.8, 1.0]

**LightGBM**:
- Similar grid plus num_leaves: [31, 50, 100]

### Best Parameters Found
*[Add best parameters from GridSearchCV results]*

## Key Findings

### Linear Models Outperform Tree Methods
**Counter-intuitive result**: Linear Regression achieved 85.2% test R² vs XGBoost 80.4%.

**Reasons**:
1. Strong linear relationship between distance and delivery time (r=0.788)
2. Limited complex interactions in dataset
3. Small sample size (794 training examples) insufficient for stable tree learning
4. Feature engineering captured main non-linearities

### Overfitting Analysis
- **Linear models**: Negative overfitting (-7%) - better test than train performance
- **Tree models**: Positive overfitting (3-14%) - memorizing training patterns
- **Optimal regularization**: Ridge alpha=10.0 provided best bias-variance tradeoff

## Model Selection Rationale

**Chosen Model**: Linear Regression
- **Performance**: 85.2% test R²
- **Interpretability**: Clear coefficient interpretation for business
- **Generalization**: Strong performance on unseen data
- **Simplicity**: Easy deployment and maintenance
- **Robustness**: Stable predictions without hyperparameter sensitivity

*[Add learning curves and validation curves here]*