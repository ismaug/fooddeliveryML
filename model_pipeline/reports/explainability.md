# Explainability
_Insights from feature importance tools._
## Methods and setup
I explain the selected Linear model using two approaches. First, I compute **permutation importance on the test split**, which is model‑agnostic and exposes which inputs most affect predictions. Second, because the estimator is linear with one‑hot encoding, I inspect **standardized coefficients** to understand sign and magnitude in human terms. When needed, I corroborate with simple partial dependence for Distance and categorical offsets for Traffic and Weather.

## What drives the predictions
The story is consistent and intuitive. **Distance_km** is the dominant driver; predicted time increases almost linearly with distance. **Traffic_Level** contributes clear vertical offsets, with **Heavy > Moderate > Light** adding several minutes under congestion. **Weather** adds a smaller but statistically significant penalty, where **Rain/Storm > Clear**, which matches the ANOVA from EDA. **Preparation_Time_min** has a meaningful positive effect that carries kitchen delays into delivery time. **Courier_Experience_yrs** shows a small negative effect (more experience, slightly faster routes), while **Vehicle_Type** and **Time_of_Day** contribute little after controlling for stronger features.

## How I communicate this to Ops
Because the model is additive, I can return the contribution of each piece of the joruney alongside the ETA that attribute minutes to the main contributors, using the average distance as the baseline. For example: +6.1 min from **Distance 7.8 km**, +3.9 min for **Traffic = Heavy**, +1.8 min for **Weather = Rain**, and +1.2 min from **Preparation_Time = 15 min**. These simple deltas make the prediction transparent and actionable for agents and operations managers.

## Limitations and next steps
The baseline is linear in the features, so interactions as distance costs more minutes when traffic is heavy are not yet explicit. To capture that compounding effect my next steps would be to add **Distance×Traffic** and **Distance×Weather** features while keeping the same estimator, and to evaluate **quantile regression** for conservative ETAs in adverse conditions.

## Conclusion
Feature importance and coefficients tell the same story as the business: distance dominates, congestion and rain add predictable overhead, and kitchen prep time matters slightly. The alignment between explainability, EDA, and test performance supports using this linear model in production with confidence(5 minutes of variance is very little in my experience with food delivery platforms), while leaving a clear path for targeted improvements.
