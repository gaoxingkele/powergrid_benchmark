# Figure 6: Full connection process

- **Source**: Figure 6, Section 2.2, p7
- **Caption**: "Full connection process."
- **Screenshot**: figure6.png (page 7; diagram in upper-middle of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two small 2×2 feature blocks (values `[[3,4],[2,5]]` and `[[1,3],[1,4]]`) flattened into a single 8-element column vector `[3,4,2,5,1,3,1,4]` feeding a "Fully Connected Layer".
- **Connections**: Feature maps → flatten → column vector → fully connected layer.
- **Annotations**: Label "Fully Connected Layer".
- **What it conveys**: The FC layer flattens/integrates pooled feature maps into a vector; its computation is $y(x)=f(w\cdot x+b)$ (Eq. 7).
</content>
