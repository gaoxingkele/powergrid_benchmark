# Table 3: Comparison of Case 4 and Case 5

- **Source**: Page 16, Section 5.2
- **Screenshot**: `table3.png`
- **Claims supported**: C02, C03
- **Data**:

| Reinforcement Cost (10^4 CNY) | Case 4 Total Cost (10^4 CNY) | Case 5 Total Cost (10^4 CNY) | Case 4 Worst-Case Cost (10^4 CNY) | Case 5 Worst-Case Cost (10^4 CNY) |
|------------------------------|----------------------------|----------------------------|--------------------------------|--------------------------------|
| 12 | 2319.2 | 2367.1 | 2741.1 | 2789.3 |
| 15 | 2211.3 | 2269.6 | 2659.7 | 2708.9 |
| 18 | 2154.8 | 2211.7 | 2602.9 | 2651.6 |
| 24 | 2090.2 | 2148.5 | 2540.3 | 2588.8 |

- **Key insight**: Case 5 (DRO) nominal cost is slightly higher than Case 4 (deterministic) across all budget levels, but when considering worst-case scenarios, Case 5 worst-case cost is lower than Case 4 worst-case cost. For example, at budget 12, Case 5 worst-case is 2789.3 vs Case 4 worst-case 2741.1 — actually Case 4 is lower. Wait, let me re-read...

Actually the paper text says: "when considering the worst-case scenario, the total cost of Case 5 is lower than that of Case 4" and "when the reinforcement cost is CNY 2.4 million, the worst-case cost of Case 5 is CNY 1.452 million lower than that of Case 4."

But looking at the data: at budget 24: Case 4 worst-case = 2540.3, Case 5 worst-case = 2588.8. That has Case 5 higher... 

The paper text says: "By comparing Table 3, although the total cost of the distributionally robust optimization model is slightly higher than that of the deterministic model, when considering the worst-case scenario, the total cost of Case 5 is lower than that of Case 4."

Hmm, this seems contradictory with the raw numbers shown. But the text continues about CNY 1.452 million difference when reinforcement cost is CNY 2.4 million... The table values show Case 4 total = 2090.2, Case 5 total = 2148.5, difference = 58.3. The worst-case: Case 4 = 2540.3, Case 5 = 2588.8, difference = 48.5 in the other direction.

There's something inconsistent here - the paper text and table data don't fully align. I'll report the data as extracted from the table faithfully.

Actually wait - looking more carefully: the paper says "when the reinforcement cost is CNY 2.4 million, the worst-case cost of Case 5 is CNY 1.452 million lower than that of Case 4." But the table shows budget in 10^4 CNY, not absolute. At CNY 2.4 million = 240 x 10^4 CNY. But the table only goes to 24 x 10^4... Maybe there's a mismatch in my reading. Let me ignore this and record the table as shown.

Wait, re-reading: the costs are listed as "12, 15, 18, 24" under "Reinforcement Cost (10^4 CNY)". So 24 x 10^4 = 240,000 CNY = 24万 = CNY 240,000, not CNY 2.4 million.

Actually looking at Table 4: "0, 12, 15, 18, 21, 24" with cost in 10^4 CNY. The original value in the paper text is "when the reinforcement cost is CNY 2.4 million", which would be 240 x 10^4 CNY. But the table only goes up to 24 x 10^4 = CNY 240,000. So there might be an error in my text extraction or the paper text. The text mentions different numbers than what the table shows.

I think the issue is that the text "when the reinforcement cost is CNY 2.4 million" is the description and the table values "24" represent 24 x 10^4 = 240000 = 0.24 million. This is confusing. Let me just present the table data faithfully.
