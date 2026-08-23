# C2GES layout-aware extraction-unit audit

Status: post-result, nonverbatim extraction diagnostic. No model ranking or reference scoring was performed.

Across 27 included reports, the frozen page-wide pipeline contained 12,924 units. The block-preserving PyMuPDF audit produced 14,290 units; 9,824 were exact normalized matches to legacy units. It detected 505 table regions and recorded 0 page-level table-detection failures. 39 retained block-preserving units exceeded 100 words.

The lower or higher unit count is not a quality score. The audit demonstrates a reproducible block/page boundary and supplies hashed samples for manual checking without redistributing report text. Prospective ranking and independent human review remain required.
