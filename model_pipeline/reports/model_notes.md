# Model Notes
_Modeling logic, metric choice, and tuning approach._
## Objective and metric
The goal is to predict **Delivery_Time_min** for per‑order ETAs. I optimize for **RMSE (minutes)** on a held‑out test set because it reflects the real penalty of minute‑level error; I also track **R²** and **MAE** to understand variance explained and typical absolute deviation.

## Data preparation and split
I kept the preprocessing identical to the EDA: I dropped non‑informative IDs, removed **6** extreme target outliers using Tukey’s IQR rule, imputed categoricals with the mode and `Courier_Experience_yrs` with the median, and encoded low‑cardinality categoricals via one‑hot. All of this lives inside a single scikit‑learn `Pipeline` with the estimator to avoid training/serving skew. I used a deterministic **80/20 split** that yielded **795** training rows and **199** test rows.

## Model comparison and selection
I trained five models behind the same preprocessor. **Linear Regression** generalized best with **Test R² = 0.8521** and **RMSE = 8.56**, and a small negative train→test gap (‑0.0699) that signals no overfit. **Ridge** essentially tied (Test R² = 0.8516, RMSE = 8.58) but did not beat Linear. Tree/boosting models fit the training data more tightly but underperformed on test: **Random Forest** (Test R² = 0.8085, RMSE = 9.74), **XGBoost** (0.8044, 9.85) with noticeable overfitting from Train R² = 0.9420, and **LightGBM** (0.8261, 9.28). Given these results, I selected **Linear Regression** for accuracy, robustness, and deployment simplicity.

## Metric and overfitting check
RMSE is the primary target because minute‑scale error is additive for ETAs, while MAE and R² provide complementary views of typical error and explanatory power. I use the **train→test gap** as a quick overfitting dial; Linear and Ridge show stable generalization, while tree/boosting variants show larger gaps despite tuning‑light defaults.

## Tuning approach and immediate next steps
This run establishes a solid baseline without heavy tuning. If I squeeze for a bit more headroom, I’ll grid **Ridge α** on {0.01, 0.1, 1, 10, 100} with CV and add simple interaction features such as **Distance×Traffic** and **Distance×Weather** to the linear family. If I revisit tree/boosting, I’ll constrain complexity (shallower depth, subsampling, early stopping) and enforce a monotone trend on **Distance**. For tail risk under adverse conditions, I would trial **quantile regression** to produce conservative ETAs when rain and heavy traffic coincide. For this exercise i tuned the boosted models manually, so changing values and checking the scores but i think a Grid Search could help with the boosted models.

## Conclusion
A lean linear model captures the core signal (distance, traffic, weather, prep time) and delivers the best test accuracy in this dataset mostly because the interaction of distance is so major that overshadows most other features. It is easy to explain, fast to serve, and provides a clean base for incremental improvements (feature interactions, quantile targets) without sacrificing robustness.
