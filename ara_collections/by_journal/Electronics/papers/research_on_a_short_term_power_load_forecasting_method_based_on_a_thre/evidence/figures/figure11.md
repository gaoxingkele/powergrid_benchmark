# Figure 11: Prediction results of different models in the Electrician's Cup dataset

- **Source**: Figure 11, Section 4, p13
- **Caption**: "The prediction results of different models in the Electrician's Cup dataset."
- **Screenshot**: figure11.png (page 13; upper plot on the page)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = Time (Hour, linear, 0–24), Y = Load (MW, linear, 16,000–36,000)

| Time (Hour) | Actual (MW) | Models (LSTM/CNN-LSTM/TCN/LSTM-CNN) |
|-------------|-------------|-------------------------------------|
| 1  | ≈22,800 | baselines slightly below (≈22,000) |
| 5  | ≈18,300 (morning trough) | all tightly clustered |
| 11 | ≈34,800 (late-morning peak) | closely tracked |
| 13 | ≈30,500 (midday dip) | closely tracked |
| 19 | ≈35,600 (evening peak) | closely tracked; LSTM slightly high |
| 24 | ≈26,800 | converge |

## Trend summary
Classic double-peak daily load: morning trough at hour≈5 (≈18,300 MW), late-morning peak at
hour≈11 (≈34,800 MW), midday dip at hour≈13, evening peak at hour≈19 (≈35,600 MW). All models track
the Actual curve closely; the three-channel LSTM-CNN (red) follows morning/evening transitions
accurately with the smallest visible deviation. Supports C01, C06 (E05); exact metrics in
evidence/tables/table5.md.
</content>
