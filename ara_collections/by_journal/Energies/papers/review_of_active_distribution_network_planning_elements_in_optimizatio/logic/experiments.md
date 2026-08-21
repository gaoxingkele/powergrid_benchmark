# Experiments

This section describes verification plans for the claims made by this review paper. Since this is a review article (no original experiments), experiments here refer to procedures to validate the review's claims about the literature landscape.

## E1: Literature coverage verification

**Purpose:** Verify that the reviewed references (104 primary sources) adequately represent the stated scope of ADN planning optimization elements and GenAI applications.

**Method:**
1. For each claim about taxonomy categories (planning horizons, objectives, decision variables, constraints, OPF formulations), enumerate the supporting references cited in the paper.
2. Perform a backward citation search: for each category, check whether the cited references indeed address the claimed element.
3. For GenAI categories (Table 10), verify that each referenced paper [63–101] belongs to the claimed model family and application domain.
4. Assess coverage by checking whether influential ADN planning review papers (e.g., [3], [9], [40], [41]) are included and properly cited.

**Success criteria:**
- At least 90% of cited references map correctly to claimed categories.
- All major GenAI model families identified in the literature (GAN, diffusion, VAE, flow, transformer) are represented by at least two independent citations.
- Key foundational reviews on ADN planning and uncertainty modeling are included.

**Related claims:** C1, C2, C3, C4, C5, C6

---

## E2: Taxonomy completeness and consistency

**Purpose:** Validate that the proposed taxonomies (planning horizons, objectives, decision variables, constraints, OPF formulations) are comprehensive and logically consistent.

**Method:**
1. Cross-reference the taxonomy categories against the content of all 104 reviewed papers to detect any missing categories.
2. For each category in the taxonomy (e.g., "economic objectives"), check for mutually exclusive subcategories (e.g., CAPEX/OPEX minimization vs. net profit maximization).
3. Compare the review's taxonomy with established classification schemes from prior authoritative reviews (e.g., [3], [9], [45]).
4. Assess whether any ADN planning element mentioned in the reviewed papers falls outside the proposed taxonomy.

**Success criteria:**
- No reviewed paper's ADN planning element falls outside the proposed taxonomy.
- Subcategories within each taxonomy dimension are mutually exclusive and collectively exhaustive.
- Consistency with prior review classification schemes exceeds 80%.

**Related claims:** C1, C2, C4

---

## E3: Generative AI application mapping validation

**Purpose:** Verify the mapping of GenAI model families to ADN planning applications as presented in Table 10 and Figure 10.

**Method:**
1. For each GenAI model family (GAN, diffusion, VAE, flow, transformer), retrieve all cited application papers [63–101].
2. For each application paper, independently classify the model type and application domain without referencing the paper's Table 10.
3. Compute inter-rater agreement between the paper's classification and independent classification.
4. Verify the Sankey diagram (Figure 10) flow widths by counting the number of references per model family per application area in the cited literature.

**Success criteria:**
- Classification agreement exceeds 85% between paper's Table 10 and independent re-classification.
- The relative prevalence indicated by flow widths in Figure 10 matches the reference count distribution across model families.
- Each application area (scenario generation, data augmentation, uncertainty modeling, etc.) has at least one concrete ADN planning use case from the literature.

**Related claims:** C3, C6

---

## E4: Evolution need identification reproducibility

**Purpose:** Verify that the review's identification of "evolution needs" (AC-OPF formulations, new asset modeling, uncertainty management) is supported by the reviewed literature.

**Method:**
1. Extract all passages from the reviewed papers that discuss limitations of traditional planning or requirements for evolution to active planning.
2. Categorize these passages according to the evolution needs dimensions identified in the review (AC-OPF, asset modeling, uncertainty, flexibility utilization, dynamic optimization).
3. Quantify the proportion of reviewed papers that advocate for each evolution need dimension.
4. Identify any evolution need discussed in the reviewed papers but not captured in the review's framework.

**Success criteria:**
- Each claimed evolution need dimension is mentioned in at least 20% of the reviewed papers.
- At most one evolution need discussed in the reviewed literature is not captured in the review's framework.
- The relative emphasis on different evolution needs in the review matches their prevalence in the cited literature.

**Related claims:** C1, C4, C5
