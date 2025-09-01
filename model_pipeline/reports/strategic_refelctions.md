# Strategic Reflections


## 1. Model Failure: Rainy Day Underestimation

**Scenario**: Your model consistently underestimates delivery time on rainy days.

### Question: Do you fix the model, the data, or the business expectations?

**My approach**
I think the answer is you need to address all 3 but you need to weight out what to do first. It's best to mantain an open and honest communication with the bussiness so i will bring up the defficency to them after a quick scan of our model so i can have all information. That would be my first step because is improbable that i would fix the model before it starts showing up in production.

After aligning with the bussines about our limitations then i would dive deeper in the data, it's the source of many problems and tends to be more complex to solve because it relays on many factors e.g. manual input, sensors, etc.

Finally i would check the model and the limitions this one particular could have handling this typo of seasonal features, rain varies in quantity(precipation) an we may have to do some feature engineering to help the model out to predict such a complex variable.

**Technical steps:**
- Root cause analysis of why rain impacts delivery time
- Data quality assessment for weather features
- Model architecture limitations
- Business context and stakeholder expectations

---

## 2. Model Transferability: Mumbai to São Paulo

**Scenario**: Your model performs well in Mumbai but needs deployment in São Paulo.

### Question: How do you ensure generalization across cities?

I would research and understand the differennces that could impact our model, an pinpoint where i need to generalize more. For example a typical feature that is hard to generalize is weather because if particular for the geographica area. There are two main approaches to this type of problems. Either i divide the feature or i combine it. Its going to depend of the type of data i have and the nature of the feature. So this is mostly resolved with good feature engineering from the start. In most cases we want our models to be applicable to mayority of cases. 

**Some concepts to not forget in this cases:**
- Distribution may shift
- Geographic, cultural, and infrastructural differences
- Validation strategies for new markets
- Gradual rollout so we can observe the behaviour

## 3. GenAI Disclosure

**Scenario**: Professional transparency about AI assistance in your development process.

### Question: What parts of this project used GenAI tools? How did you validate their output?

What I used GenAI for (high-level):
I used ChatGPT and Claude as a thinking partner to move faster on patterns I already know how to do. Concretely, it helped me:

Made a plan to do the whole assesment, dividing in smaller parts.

Validate my SQL query patterns, then I finalized and tested them in DuckDB.

Outline EDA steps and produce a concise EDA_report.md (I verified every number/figure against my notebook).

md templates for all reports.

Generate a minimal error-analysis notebook scaffold that loads my saved pipeline and writes metrics/figures.

Tighten the production plan into short, practical steps (API → container → managed cloud → basic monitoring).

Light editing/translation between English/Spanish for clarity and tone.

How I validated GenAI output:

Executed everything: I ran the notebook and pipeline to confirm metrics, plots, and saved artifacts match the code.

Reproducibility checks: fixed seeds; confirmed train/test metrics are stable across runs.

Data sanity: confirmed shapes, dtypes, missingness, and that transforms are fit on train only (no leakage).

EDA cross-checks: the strongest correlations (Distance, Traffic/Weather effects) match domain logic and ANOVA.

Explainability alignment: permutation importances/coefficients agree with expectations (Distance ≫ others).

Slice errors: verified that rainy + heavy-traffic underestimation is real in my held-out data.

SQL validation: ran every query, inspected results (top-K, aggregates, date filters), and corrected edge cases.

Code review: simplified prompts’ code, removed unnecessary bits, enforced my naming, structure, and style.

Ownership:
All final decisions, code, and results are mine. I treated GenAI suggestions as drafts/checklists, not ground truth, and kept anything only after verifying it worked with my data and matched business logic.

Disclosure notice:
This answer (and parts of the project documentation and scaffolding) were drafted with assistance from ChatGPT (GPT-5 Thinking) and Claus(Opus 4) and then reviewed, executed, and edited by me.
---

## 4. Your Signature Insight

**Scenario**: Showcase your unique analytical thinking and decision-making.

### Question: What's one non-obvious insight or decision you're proud of?

To calculate average delivery time per courier, I chose a one-month window—long enough to smooth out short-term volatility (like weather spikes or one-off delays), but not so long that it dilutes current operational realities. Shorter windows risk reacting to noise; longer ones risk anchoring decisions to outdated patterns. This balance ensures the metric reflects stable performance trends while staying operationally relevant for staffing, routing, and performance feedback

I used a baseline-controlled methodology that isolates the true impact of adverse delivery conditions by comparing them against optimal benchmarks for identical routes. This is very helpful for analysis and actionable insights.

I finally settled on a linear regression model that seems out of pocket but that in reality it does check out with our EDA, it's not that other factors do not interect in the delivery time is that the impact of the distance is so strong that it actually presents very close as a linear regression.
---
## 5. Production Deployment Strategy
**Scenario**: Move your prototype to a production-ready system. 
### Question: How would you deploy this model? What components would you need?
I’ll put the trained pipeline behind a tiny HTTP API. It will use the exact same preprocessing that’s inside the saved model, so there’s no mismatch. containerize it and run it on managed cloud compute with autoscaling(important to no have surprises in peak hours), health checks, and HTTPS. The service stays stateless and loads the model once at startup for speed.

It will also need a way to check is doing ok. Lets log each request and prediction, watch latency and error rate, and run a daily job that matches predictions to actual delivery times. From that, I’ll track RMSE/MAE and “ETA within ±5 min,” broken down by weather, traffic, and distance. And here get alerts if accuracy drops. 