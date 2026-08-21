# Figure 3 - Diagram of Cycle Cross

- **Source**: Figure 3, Section 3.3
- **Caption**: "Diagram of cycle cross."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: The diagram illustrates the cyclic crossover operation with two parent individuals (Parent 1, Parent 2) and two offspring (Offspring 1, Offspring 2)
- **Process**:
  1. A starting gene position is selected randomly in Parent 1
  2. The value at that position is copied to Offspring 1
  3. The same value is located in Parent 2; its position is found
  4. The gene at that position in Parent 2 is copied to Offspring 2
  5. The matching gene (identical value) in Parent 1 is located
  6. That gene is copied to Offspring 1
  7. Steps 3-6 repeat, forming a closed cycle, until the starting point is reached
  8. Remaining genes (not part of the cycle) are copied from Parent 1 to Offspring 2 and Parent 2 to Offspring 1
- **What it conveys**: Cyclic crossover preserves the relative order and co-occurrence of genes from parents by exchanging them along closed cycles, avoiding duplicate gene combinations and maintaining genetic structure.
