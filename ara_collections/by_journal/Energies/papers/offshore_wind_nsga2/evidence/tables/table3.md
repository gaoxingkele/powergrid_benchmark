# Table 3: Comparison of Cycle Times and Expected Service Life of Energy Storage Batteries with Different Solutions on Pareto Front

**Source**: Page 11 of the PDF.

**Description**: Cycle counts and expected service life for different (P_es, S_es) configurations on the Pareto frontier, used to build the multiple linear regression model for battery life correction.

| Leading Edge Point (P_es, S_es) | Cycle Number | Expected Service Life (Years) |
|----------------------------------|-------------|------------------------------|
| (4, 4)                           | 35          | 4.1                          |
| (6, 6)                           | 33          | 4.4                          |
| (8, 8)                           | 30          | 4.8                          |
| (8, 11)                          | 25          | 5.8                          |
| (9, 13)                          | 23          | 6.3                          |
| (7, 16)                          | 19          | 7.7                          |
| (9, 21)                          | 17          | 8.6                          |
| (8, 25)                          | 15          | 9.7                          |
| (10, 27)                         | 15          | 9.7                          |
| (12, 33)                         | 14          | 10.4                         |
| (10, 37)                         | 13          | 11.2                         |
| (10, 40)                         | 12          | 12.0                         |

**Note**: These data points were used to fit the multiple linear regression model:
Y = 3.73292 - 0.05076*P_es + 0.22835*S_es (R^2 = 0.96965)

**Image**: `table3.png`
