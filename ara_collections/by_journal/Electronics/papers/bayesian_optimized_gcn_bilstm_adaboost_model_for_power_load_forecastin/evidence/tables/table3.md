# Table 3 - Model structure parameters

**Source**: Table 3, §4.2 (page 13, middle of page)
**Caption**: "Model structure parameters."
**Screenshot**: table3.png
**Extraction type**: raw_table

| Types of Layer Structures | Input Dimension | Output Dimension |
|---------------------------|-----------------|------------------|
| Input layer | 24 × 8 | – |
| GCN layer | 24 × 8 | 24 × 128 |
| Dropout | 24 × 128 | 24 × 128 |
| BiLSTM layer | 24 × 128 | 1 × 512 |
| Output layer | 1 × 512 | 1 × 1 |

**Associated hyperparameters (§4.2 narrative)**: PyTorch; NVIDIA RTX 4060Ti GPU, 13th-Gen Intel Core i7,
32 GB RAM; Adam optimizer; initial learning rate 0.001; 1800 epochs; Dropout rate 0.2; AdaBoost
integration of the 1×512 feature into the next-hour forecast.
