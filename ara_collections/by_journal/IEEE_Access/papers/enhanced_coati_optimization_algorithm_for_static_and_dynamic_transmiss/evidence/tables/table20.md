# Table 20 - SR%, MIT, and MST values of the optimization algorithms for all case studies

**Source**: Table 20, §IV-B (p.35096)
**Caption**: "SR%, MIT, and MST values of the optimization algorithms for all case studies."
**Screenshot**: table20.png (full-page table)
**Extraction type**: raw_table

SR% = success rate (feasibility across 30 runs); MIT = mean iteration number to feasibility; MST = mean search time to feasibility. Higher SR% = more reliable.

| Test System | Case | Algorithm | SR% | MIT | MST |
|-------------|------|-----------|-----|-----|-----|
| Garver | Without Generation Resizing | COA | 26.6667 | 10.0000 | 5.0371 |
| Garver | Without Generation Resizing | FDBCOA1 | 50.0000 | 13.3333 | 5.6884 |
| Garver | Without Generation Resizing | FDBCOA1-OBL5 | 53.3333 | 16.2500 | 6.9674 |
| Garver | Without Generation Resizing | GA | 20.0000 | 63.0000 | 21.6462 |
| Garver | Without Generation Resizing | PSO | 63.3333 | 12.2105 | 2.9179 |
| Garver | With Generation Resizing | COA | 0.0000 | 0.0000 | 0.0000 |
| Garver | With Generation Resizing | FDBCOA1 | 40.0000 | 9.8333 | 4.0926 |
| Garver | With Generation Resizing | FDBCOA1-OBL5 | 66.6667 | 21.2500 | 8.5520 |
| Garver | With Generation Resizing | GA | 0.0000 | 0.0000 | 0.0000 |
| Garver | With Generation Resizing | PSO | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | Without Generation Resizing | COA | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | Without Generation Resizing | FDBCOA1 | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | Without Generation Resizing | FDBCOA1-OBL5 | 80.0000 | 35.7083 | 17.8236 |
| IEEE 25-Bus | Without Generation Resizing | GA | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | Without Generation Resizing | PSO | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | With Generation Resizing | COA | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | With Generation Resizing | FDBCOA1 | 0.0000 | 0.0000 | 0.0000 |
| IEEE 25-Bus | With Generation Resizing | FDBCOA1-OBL5 | 40.0000 | 100.4167 | 50.8601 |
| IEEE 25-Bus | With Generation Resizing | GA | 3.33333 | 404 | 168.2686 |
| IEEE 25-Bus | With Generation Resizing | PSO | 26.6667 | 54.5000 | 12.5254 |
| Colombian 93-Bus | Stage P1 | COA | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P1 | FDBCOA1 | 3.3333 | 22.0000 | 12.6374 |
| Colombian 93-Bus | Stage P1 | FDBCOA1-OBL5 | 100.0000 | 3.8333 | 2.0476 |
| Colombian 93-Bus | Stage P1 | GA | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P1 | PSO | 63.3333 | 159.7895 | 35.3460 |
| Colombian 93-Bus | Stage P2 | COA | 3.3333 | 5.0000 | 2.8983 |
| Colombian 93-Bus | Stage P2 | FDBCOA1 | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P2 | FDBCOA1-OBL5 | 90.0000 | 63.0000 | 27.0192 |
| Colombian 93-Bus | Stage P2 | GA | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P2 | PSO | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P3 | COA | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P3 | FDBCOA1 | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P3 | FDBCOA1-OBL5 | 90.0000 | 49.0370 | 19.5801 |
| Colombian 93-Bus | Stage P3 | GA | 0.0000 | 0.0000 | 0.0000 |
| Colombian 93-Bus | Stage P3 | PSO | 0.0000 | 0.0000 | 0.0000 |

## Mean Values (across all case studies)
| Algorithm | SR% | MIT | MST |
|-----------|-----|-----|-----|
| COA | 4.2857 | 2.1428 | 1.1336 |
| FDBCOA1 | 13.3333 | 6.4523 | 3.2026 |
| FDBCOA1-OBL5 | 74.2857 | 41.3564 | 18.9785 |
| GA | 3.3333 | 66.7142 | 27.1306 |
| PSO | 21.9047 | 32.3571 | 7.2556 |

**Reading**: FDBCOA1-OBL5 is the only algorithm feasible across essentially all seven case studies (mean SR% 74.2857); COA, FDBCOA1, GA, PSO have negligible mean SR% (feasible in only a few scenarios). This is the core evidence for the stability claim C05.
