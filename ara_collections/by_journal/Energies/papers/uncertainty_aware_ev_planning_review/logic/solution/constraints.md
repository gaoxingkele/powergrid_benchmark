# Constraints: Boundary Conditions, Assumptions, and Known Limitations

## Boundary Conditions of the Review

1. **Scope Boundary:** The review focuses on distribution networks (not transmission or generation) and EV charging infrastructure planning with renewable energy integration. It does not cover standalone EV charging without RES or RES without EV charging.

2. **Temporal Boundary:** The survey covers literature published primarily through early 2026, with the review accepted in February 2026. Emerging technologies beyond this cutoff are not included.

3. **Geographic Boundary:** While international in scope, the review draws disproportionately from studies conducted in China, India, the United States, and Europe, reflecting the publication distribution in this research domain.

4. **Methodological Boundary:** The review covers both forecasting methods and planning algorithms but does not provide experimental validation or implementation of any proposed framework — it is a synthesis of existing work.

5. **Technology Boundary:** The review focuses on grid-connected EVCS with RES (primarily PV and wind). It covers but does not deeply explore Vehicle-to-Grid (V2G) bidirectional power flow, wireless charging, or dynamic charging (in-motion) technologies.

## Assumptions

1. The reviewed literature is representative of the broader field of EVCS-RES planning research.
2. Classification categories (learning-based vs. non-learning-based; deterministic vs. stochastic) are sufficient to capture the methodological landscape.
3. The quantitative metrics (MAE, RMSE, MAPE, R²) used across studies are comparable despite differences in datasets and evaluation protocols.
4. EV penetration will continue to increase, making planning problems more critical.
5. RES capacity will continue to grow, increasing the urgency of joint planning.

## Known Limitations (acknowledged in the review)

1. **Data scarcity:** "Limited publicly available data" and the "unpredictable, stochastic nature of EV charging behavior" constrain the development and validation of forecasting models. (Section 2.1.1)

2. **Simplistic modeling practices:** "Most of the work has modeled EV load demand and PV generation in a simplistic and deterministic manner, whereas both should be treated stochastically" (Section 4).

3. **Missing environmental and reliability focus:** "Limited attention has been given to environmental impacts and long-term reliability. Moreover, comprehensive investigations that integrate technical, economic, environmental, and reliability impacts... are still lacking" (Section 4).

4. **Separation of forecasting from planning:** "Future research should employ ensemble learning or deep learning for EV and RES demand prediction, incorporate probabilistic forecasting outputs into optimization models, and quantify forecast error effect using sensitivity or scenario analysis rather than utilizing forecasting as a preprocessing step" (Section 4).

5. **Static optimization models:** "The majority of the current research uses static or one-period optimization models" rather than multi-stage stochastic planning frameworks (Section 4).

6. **Limited policy and market integration:** "Present research on EVCS and RES integration focuses on both technical and economic optimization, with very little attention paid to commercial models and policy frameworks" (Section 4).

7. **Computational complexity of advanced methods:** "Although advanced learning-based models such as LSTM, GRU, GNN, Transformer, and hybrid architectures provide superior forecasting accuracy, their practical implementation is constrained by high computational requirements, large data dependency, scalability limitations, and reduced interpretability" (Section 2.1.2 Summary).
