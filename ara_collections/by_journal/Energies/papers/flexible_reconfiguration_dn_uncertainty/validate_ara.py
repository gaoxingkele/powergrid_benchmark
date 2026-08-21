import os

base = 'D:/aicoding/powergrid_benchmark/ara_collections/by_journal/Energies/papers/flexible_reconfiguration_dn_uncertainty'

checks = {
    'Required files': [
        'PAPER.md',
        'logic/problem.md',
        'logic/claims.md',
        'logic/concepts.md',
        'logic/experiments.md',
        'logic/solution/constraints.md',
        'logic/related_work.md',
        'logic/solution/algorithm.md',
        'src/environment.md',
        'trace/exploration_tree.yaml',
        'evidence/README.md',
    ],
    'Page renders': [f'page_{i:02d}.png' for i in range(1, 27)],
    'Table evidence': [
        'evidence/tables/table01_comparing_dr_methods.md', 'evidence/tables/table01_comparing_dr_methods.png',
        'evidence/tables/table02_renewable_gen_ieee33.md', 'evidence/tables/table02_renewable_gen_ieee33.png',
        'evidence/tables/table03_loss_reduction_coa_ieee33.md', 'evidence/tables/table03_loss_reduction_coa_ieee33.png',
        'evidence/tables/table04_comparison_cases_ieee33.md', 'evidence/tables/table04_comparison_cases_ieee33.png',
        'evidence/tables/table05_optimal_power_procured.md', 'evidence/tables/table05_optimal_power_procured.png',
        'evidence/tables/table06_hourly_cost_power.md', 'evidence/tables/table06_hourly_cost_power.png',
        'evidence/tables/table07_hourly_loss_cost.md', 'evidence/tables/table07_hourly_loss_cost.png',
        'evidence/tables/table08_coa_vs_pso.md', 'evidence/tables/table08_coa_vs_pso.png',
        'evidence/tables/table09_eens_values.md', 'evidence/tables/table09_eens_values.png',
        'evidence/tables/table10_renewable_gen_tpc83.md', 'evidence/tables/table10_renewable_gen_tpc83.png',
        'evidence/tables/table11_loss_reduction_tpc83.md', 'evidence/tables/table11_loss_reduction_tpc83.png',
        'evidence/tables/table12_comparison_tpc83.md', 'evidence/tables/table12_comparison_tpc83.png',
    ],
    'Figure evidence': [
        'evidence/figures/fig01_coa_pseudocode.md', 'evidence/figures/fig01_coa_pseudocode.png',
        'evidence/figures/fig02_coa_flowchart.md', 'evidence/figures/fig02_coa_flowchart.png',
        'evidence/figures/fig03_ieee33_bus.md', 'evidence/figures/fig03_ieee33_bus.png',
        'evidence/figures/fig04_wind_solar_data.md', 'evidence/figures/fig04_wind_solar_data.png',
        'evidence/figures/fig05_load_profile.md', 'evidence/figures/fig05_load_profile.png',
        'evidence/figures/fig06_energy_prices.md', 'evidence/figures/fig06_energy_prices.png',
        'evidence/figures/fig07_power_procured_case4.md', 'evidence/figures/fig07_power_procured_case4.png',
        'evidence/figures/fig08_total_pupn.md', 'evidence/figures/fig08_total_pupn.png',
        'evidence/figures/fig09_hourly_loss.md', 'evidence/figures/fig09_hourly_loss.png',
        'evidence/figures/fig10_total_loss.md', 'evidence/figures/fig10_total_loss.png',
        'evidence/figures/fig11_hourly_vd.md', 'evidence/figures/fig11_hourly_vd.png',
        'evidence/figures/fig12_min_bus_voltage.md', 'evidence/figures/fig12_min_bus_voltage.png',
        'evidence/figures/fig13_coa_pso_voltage.md', 'evidence/figures/fig13_coa_pso_voltage.png',
        'evidence/figures/fig14_eens_variation.md', 'evidence/figures/fig14_eens_variation.png',
        'evidence/figures/fig15_tpc83_bus.md', 'evidence/figures/fig15_tpc83_bus.png',
        'evidence/figures/fig16_total_loss_tpc83.md', 'evidence/figures/fig16_total_loss_tpc83.png',
    ]
}

all_ok = True
for category, files in checks.items():
    missing = []
    for f in files:
        if not os.path.exists(os.path.join(base, f)):
            missing.append(f)
    if missing:
        print('[%s] MISSING: %d files:' % (category, len(missing)))
        for m in missing:
            print('  - %s' % m)
        all_ok = False
    else:
        print('[%s] OK (%d files)' % (category, len(files)))

# Count claims
with open(os.path.join(base, 'logic/claims.md'), 'r', encoding='utf-8') as f:
    claims_text = f.read()
claim_count = claims_text.count('## Claim C')
print('\nClaims found: %d' % claim_count)

# Count experiments
with open(os.path.join(base, 'logic/experiments.md'), 'r', encoding='utf-8') as f:
    exp_text = f.read()
exp_count = exp_text.count('## Experiment E')
print('Experiments found: %d' % exp_count)

# Count concepts
with open(os.path.join(base, 'logic/concepts.md'), 'r', encoding='utf-8') as f:
    conc_text = f.read()
conc_count = conc_text.count('## C')
print('Concepts found: %d' % conc_count)

# Count tree nodes
with open(os.path.join(base, 'trace/exploration_tree.yaml'), 'r', encoding='utf-8') as f:
    tree_text = f.read()
node_count = tree_text.count('type:')
print('Tree nodes: %d' % node_count)

# Count evidence
table_pngs = [f for f in os.listdir(os.path.join(base, 'evidence/tables')) if f.endswith('.png')]
table_mds = [f for f in os.listdir(os.path.join(base, 'evidence/tables')) if f.endswith('.md')]
print('\nTable PNGs: %d, Table MDs: %d' % (len(table_pngs), len(table_mds)))

fig_pngs = [f for f in os.listdir(os.path.join(base, 'evidence/figures')) if f.endswith('.png')]
fig_mds = [f for f in os.listdir(os.path.join(base, 'evidence/figures')) if f.endswith('.md')]
print('Figure PNGs: %d, Figure MDs: %d' % (len(fig_pngs), len(fig_mds)))

# Total file count
total = 0
for root, dirs, files in os.walk(base):
    total += len(files)
print('\nTotal files in ARA artifact: %d' % total)

print('\nValidation: %s' % ('PASSED' if all_ok else 'FAILED'))

# Output JSON summary
import json
summary = {
    'title': 'Flexible Reconfiguration for Optimal Operation of Distribution Network Under Renewable Generation and Load Uncertainty',
    'doi': '10.3390/en18020266',
    'output_dir': base,
    'file_count': total,
    'validation_status': 'PASSED' if all_ok else 'FAILED',
    'claim_count': claim_count,
    'experiment_count': exp_count,
    'concept_count': conc_count,
    'tree_node_count': node_count,
    'evidence_table_count': len(table_pngs),
    'evidence_figure_count': len(fig_pngs)
}
print('\nJSON summary:')
print(json.dumps(summary, indent=2))
