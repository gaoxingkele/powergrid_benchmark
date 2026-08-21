# Caption drafts

> Protocol/method diagrams only. No unfrozen experimental result is represented.

## ma_sqlgrid_algorithm_framework_vector

Overall MA-SQLGrid framework and information boundary. The Query Analyst and Schema Cartographer structure the request, whereas the SQL Synthesizer only packages externally produced candidates. The Validation Engine records safe bounded read-only execution, and the Metamorphic-State Critic records complete constructed-state evidence. The deterministic adjudicator applies hard eligibility gates before the 10/5/5 effective evidence score, resolves ties by frozen candidate order, and abstains when no candidate is eligible. Gold or reference information enters only in offline evaluation after the decision and blackboard digest are sealed.

Source evidence: MA_SQLGrid/paper_applsci.tex, Sections 3.3-3.6; MA_SQLGrid/original_title_rebuild/ma_sqlgrid_agents.py
