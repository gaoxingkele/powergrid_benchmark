# Method

## Main Algorithm

`DSTAR-GRU`: Digital-twin Siamese Temporal Alignment and Retrieval GRU

## Innovation Handles

- Treats dispatch-state similarity as a supervised retrieval target.
- Connects a digital-twin state bank with dispatch optimization.
- Evaluates feasibility, curtailment, topology risk, and runtime together.

## Baseline Coverage

- DC OPF
- AC OPF
- GRU Direct
- LSTM Direct
- CNN-LSTM
- Grid2Op Rule
- PSO
- GA

## Ablation Coverage

- no_siamese_branch
- lstm_encoder
- no_retrieval_bank
- no_topology_features
- single_objective_layer
- small_reference_bank
