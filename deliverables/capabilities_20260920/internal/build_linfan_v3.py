from pathlib import Path
import json
from publications_linfan_complete import PAPERS, GROUPS

ROOT = Path(__file__).resolve().parent.parent
v2 = (ROOT/'internal/build_linfan_v2.py').read_text(encoding='utf-8')

def replace_block(source, start, end, replacement):
    a=source.index(start); b=source.index(end,a)
    return source[:a]+replacement+'\n'+source[b:]

def bibliography():
    by_id={r[0]:r for r in PAPERS}
    assert len(by_id)==27
    used=[]
    for gi,(group,ids) in enumerate(GROUPS):
        page('四  学术论文完整清单' if gi==0 else '四  学术论文清单 续')
        h(group,2)
        if gi==0:
            p('已发表成果涵盖强化学习、图学习、生成模型、多目标优化与跨领域应用。以下完整列出27篇论文，其中21篇期刊论文、6篇会议或论文集论文。',small=True)
            p('期刊按履历中的历史JCR分区分组，同组按研究领域排列；会议单列，并保留履历中的CCF级别。不同年度分区与会议等级不作直接换算。',small=True)
        for ident in ids:
            used.append(ident)
            _,_,authors,title,venue,tier,doi=by_id[ident]
            q=DOC.add_paragraph()
            q.paragraph_format.space_after=Pt(13)
            q.paragraph_format.line_spacing=1.1
            q.paragraph_format.keep_together=True
            r=q.add_run(f'[{ident:02d}] {title}\n');r.bold=True;r.font.size=Pt(10)
            r=q.add_run(authors+'.\n');r.font.size=Pt(9)
            r=q.add_run(venue+'.  '+tier);r.font.size=Pt(9)
            if doi:
                r=q.add_run('\nDOI: '+doi);r.font.size=Pt(8.5)
            ledger.append(q.text)
    assert sorted(used)==list(range(1,28))

def additional_projects():
    records=[
    ['1','在线学习中可解释推荐算法的关键技术研究','国家自然科学基金面上项目','2020–2023','主持'],
    ['2','人类精子成熟相关分子数据库的建立与关键分子的筛选','国家重点研发计划子课题','2020–2023','参与'],
    ['3','面向电信业户外通信设施的综合集中式智能传感器网络监控平台以及相关产品的产业化项目','科技部科技引导计划','2012立项；2019结题','主持'],
    ['4','丝绸之路新疆文化资源集成与文化旅游综合服务应用示范','国家科技支撑计划','2015立项；已结题','子课题负责人'],
    ['5','基于深度学习技术的图应用能力平台研究','教育部中移动联合基金','2016立项；已结题','第一合作者'],
    ['6','基于大健康开放应用平台的智能家居可视对讲终端研发','厦门市科技计划','2015立项；已结题','主持'],
    ['7','基于内容感知的智能大数据存储系统研发','厦门市科技计划','2014立项；已结题','主持'],
    ['8','加密多维码第三方电子凭证系统','国家科技型中小企业技术创新基金','2013立项；已结题','主持'],
    ['9','基于移动云计算的多维码电子权鉴系统开发','福州市科技计划','2013立项；已结题','主持'],
    ['10','多源数据融合环保数据监测设备研发及产业化','福建省发改委产业技术研究开发项目','2013立项；已结题','第一合作者'],
    ['11','基于HD-SDI信息融合设备的交通感知系统研发及产业化','福建省科技厅区域重大专项','2013立项；2019结题','主持'],
    ]
    page('三  其他科研项目与产学研合作')
    p('长期的算法研究也延伸到教育、医疗、金融与物联网领域。这些项目积累的数据治理、软件开发和跨专业协作经验，为电力场景中的知识服务与智能决策提供了基础。')
    table(['序号','项目名称','项目来源','年度或结题记录','承担角色'],records,[.7,7,4.1,2.5,2.5],8.7)
    page('三  企业合作与联合研究平台')
    p('除电力与能源项目外，我们持续与企业开展应用研究，并通过联合实验室和研究中心组织长期合作。既有合作覆盖金融数据分析、医疗健康、城市物联网及工业设备等场景。')
    table(['类别','项目或平台名称'],[
    ['企业委托研究','基于大语言模型的舆情分析系统'],
    ['联合实验室','厦门大学信息学院盖德-金融大数据创新实验室'],
    ['联合实验室','厦门大学信息学院觅健-重大疾病大数据联合实验室'],
    ['研究中心','厦门大学信息学院链合-区块链研究中心'],
    ['研究中心','厦门大学信息学院翼石电子-数字城市与物联网研究中心'],
    ['研究中心','机械设备工业4.0物联网研究中心'],
    ],[3.2,13.6],10)
    h('合作中形成的研究经验',2)
    p('跨行业合作使我们熟悉了业务数据分散、专家知识难以形式化、模型与现有软件难以衔接等常见问题。开展新课题时，可以把已有的数据整理、知识建模和系统开发经验带入项目，再与业务人员共同确定需要改进的环节。')
    p('在电力合作中，这类积累可用于档案解析、设备知识库、自然语言查询、报表生成和生产安全辅助分析。涉及调度与设备控制的任务，则结合电力机理、运行约束和现场试验开展验证。')

def patent_catalogue():
    page('五  专利与成果转化')
    p('已有专利覆盖强化学习推荐、生成模型、数据安全、无线传感与数据存储。累计授权发明专利10项；下面完整列出履历中的17条专利记录，其中8条为授权公告记录、9条为公开申请记录。')
    granted=[
    ['6','一种基于动态递归机制的分层强化学习的推荐系统','CN112597391B','2022-08-12'],
    ['7','一种基于动态注意力和分层强化学习的推荐系统','CN112597392B','2022-09-30'],
    ['8','GRNN结合遗传算法的室内定位方法及系统','CN113310490B','2022-10-04'],
    ['10','一种特定动漫人脸生成方法、终端设备及存储介质','CN109859295B','2021-01-12'],
    ['12','一种无线传感器网络中基于多目标进化算法的优化覆盖方法','CN106131862B','2019-08-16'],
    ['13','基于云重心理论的分布式大数据系统风险评估方法','CN104850727B','2017-09-29'],
    ['16','一种海量数据存储方法','CN102737127B','2015-04-08'],
    ['17','集成电路反剥离光刻方法','CN100437359C','2008-11-26'],
    ]
    h('授权公告记录',2)
    table(['原序号','专利名称','授权公告号','公告日期'],granted,[1,9.3,3.7,2.8],9)
    p('授权总量采用履历汇总，表内为已提供书目记录。具体成果合作中，双方共同确认专利权属、有效状态与许可安排。',small=True)
    page('五  专利清单 续')
    h('公开申请记录',2)
    applications=[
    ['1','一种可解释的商品推荐方法、装置及程序产品','CN120450799A','2025-08-08'],
    ['2','一种农产品期货价格的预测方法、装置、介质及程序产品','CN119515433A','2025-02-25'],
    ['3','一种投资组合优化方法、终端设备及存储介质','CN118552308A','2024-08-27'],
    ['4','一种基于GPT和多智能体强化学习的智能导学方法','CN117808637A','2024-04-02'],
    ['5','一种电网分批分类精准切荷方法及系统','CN117691613A','2024-03-12'],
    ['9','一种慕课可解释推荐方法、终端设备及存储介质','CN115238169A','2022-10-25'],
    ['11','一种根据当前场景及其描述信息生成下一场景的方法','CN111177461A','2020-05-19'],
    ['14','基于AHP-RBF的分布式大数据系统风险预测方法','CN104978612A','2015-10-14'],
    ['15','基于LSA-GCC的分布式大数据系统风险识别方法','CN104636449A','2015-05-20'],
    ]
    table(['原序号','专利名称','申请公布号','公开日期'],applications,[1,9.3,3.7,2.8],9)
    p('公开申请记录与授权成果分别列示。编号保留原清单序号，便于逐项查阅。',small=True)
    assert sorted(int(r[0]) for r in granted+applications)==list(range(1,18))

def classified_resources():
    # Reuse the verified local status ledger, not the old unclassified output.
    exec(script_source[script_source.index('inv=json.loads'):script_source.index('for start in range(0,len(catalog),18):')],globals())
    group_defs=[
    ('电网算例与规划优化','matpower pandapower pglib_opf rts_gmlc simbench tamu_test_cases nrel118 miso_mtep pglearn_small opfdata_landing swiss_der_allocation'),
    ('负荷预测与电力市场','opsd_time_series eia_opendata entsoe_transparency pjm_dataminer ett uci_household_power uci_tetouan_power monash_australian_demand panama_load elia_total_load sgsc'),
    ('新能源与气象场景','nsrdb large_synthetic_power_grid_ml psml ausgrid_solar_home sdwpf_kddcup2022 renewables_ninja_country_sample vce_rare_power eia860_wind_solar_cf secures_energy era5_eu_supply_demand grid_tracking_windfm'),
    ('电池健康与储能运行','nasa_pcoe_battery nasa_randomized_recommissioned_battery oxford_battery_degradation calce_battery battery_archive stanford_tri_high_power_battery m5bat_bess finland_afrr_weather bess_european_balancing_inputs'),
    ('车网互动与多智能体控制','acn_data acn_data_static grid2op_datasets grid_tracking_mapdn grid_tracking_enenv'),
    ('动态稳定与故障波形','lbnl_pmu_event_library gridstage grid_tracking_smib_pinn dataport gap_dataport oscillation_testcases_utk protect90 siib_time_full uci_electrical_grid_stability'),
    ('设备诊断与巡检安全','dgann_duval dgadb sgcc_electricity_theft grid_tracking_fault_location_ieee33 inspecsafe_v1'),
    ('电碳分析与知识资源','carbonx open_grid_emissions c2ges_nerc_reports grid_tracking_code_bundle'),
    ]
    names={
    'matpower':'MATPOWER标准网架','pandapower':'pandapower配网与潮流算例','pglib_opf':'PGLib-OPF最优潮流基准','rts_gmlc':'RTS-GMLC运行与可靠性算例','simbench':'SimBench网架与场景','tamu_test_cases':'TAMU合成电网','nrel118':'NREL 118节点算例','miso_mtep':'MISO输电规划资料','pglearn_small':'PGLearn 14节点子集','opfdata_landing':'OPFData数据入口','swiss_der_allocation':'Swiss DER分布式能源配置',
    'opsd_time_series':'OPSD电力时间序列','eia_opendata':'EIA能源统计','entsoe_transparency':'ENTSO-E透明平台','pjm_dataminer':'PJM市场与负荷','ett':'ETT变压器时间序列','uci_household_power':'UCI家庭用电','uci_tetouan_power':'Tetouan区域负荷','monash_australian_demand':'Monash澳大利亚电力需求','panama_load':'Panama负荷','elia_total_load':'Elia系统总负荷','sgsc':'SGSC智能电表',
    'nsrdb':'NSRDB太阳能气象','large_synthetic_power_grid_ml':'大型合成电网机器学习数据','psml':'PSML多尺度电力时序','ausgrid_solar_home':'Ausgrid家庭光伏与用电','sdwpf_kddcup2022':'SDWPF风电功率预测','renewables_ninja_country_sample':'Renewables.ninja国家级样本目录','vce_rare_power':'VCE RARE新能源数据','eia860_wind_solar_cf':'EIA860风光容量因子','secures_energy':'SECURES能源情景','era5_eu_supply_demand':'ERA5欧洲供需相关数据','grid_tracking_windfm':'WindFM风电基础模型权重',
    'nasa_pcoe_battery':'NASA PCoE电池老化','nasa_randomized_recommissioned_battery':'NASA随机工况电池','oxford_battery_degradation':'Oxford电池退化','calce_battery':'CALCE电池样本','battery_archive':'Battery Archive','stanford_tri_high_power_battery':'Stanford-TRI高功率电池','m5bat_bess':'M5BAT储能电站运行','finland_afrr_weather':'芬兰aFRR与天气','bess_european_balancing_inputs':'欧洲储能平衡市场输入',
    'acn_data':'ACN充电在线数据','acn_data_static':'ACN静态充电子集','grid2op_datasets':'Grid2Op拓扑控制环境','grid_tracking_mapdn':'MAPDN多智能体配网','grid_tracking_enenv':'EnEnv能源环境',
    'lbnl_pmu_event_library':'LBNL PMU事件库','gridstage':'GridSTAGE场景数据','grid_tracking_smib_pinn':'SMIB物理信息模型算例','dataport':'IEEE DataPort动态场景归档','gap_dataport':'IRTSD等事件资源跟踪','oscillation_testcases_utk':'WECC 179和240节点振荡用例','protect90':'PROTECT-90故障波形与标签','siib_time_full':'SIIB-Time逆变器动态数据','uci_electrical_grid_stability':'UCI电网稳定性分类',
    'dgann_duval':'DGA与Duval诊断数据','dgadb':'DGADB溶解气体数据库','sgcc_electricity_theft':'SGCC窃电检测数据','grid_tracking_fault_location_ieee33':'IEEE33故障定位数据','inspecsafe_v1':'InspecSafe-V1多模态巡检',
    'carbonx':'CarbonX时变碳强度','open_grid_emissions':'Open Grid Emissions电网排放','c2ges_nerc_reports':'NERC可靠性技术报告','grid_tracking_code_bundle':'电力研究开源代码集合',
    }
    records={r[0]:r for r in catalog}
    used=[]
    for gi,(title,keys) in enumerate(group_defs):
        ids=keys.split();used+=ids
        page('附录一  分类数据与研究资源目录' if gi==0 else '附录一  分类资源目录 续')
        h(title+'  '+str(len(ids))+'项',2)
        if gi==0:
            p('资源目录共65条，按研究用途归入8类。每条列出资源名称、可用形态和适用任务；数据归档、样本、模型权重、代码和在线入口分别标明。',small=True)
        rows=[]
        for key in ids:
            _,state,note=records[key]
            if key=='sgcc_electricity_theft':note='窃电与异常用电识别'
            if key=='ett':note='变压器油温及电力相关时序预测'
            if key=='grid_tracking_mapdn':note='多智能体配网协调控制'
            if key=='grid_tracking_enenv':note='能源环境仿真；3个场景'
            if key=='grid_tracking_smib_pinn':note='单机无穷大母线动态与物理约束学习'
            if key=='grid_tracking_fault_location_ieee33':note='配网故障定位'
            if key=='siib_time_full':note='逆变器动态仿真；9000个CSV'
            rows.append([names[key],state,note])
        table(['数据集或资源名称','可用形态','研究用途与数据范围'],rows,[6.6,3.1,7.1],9.5)
        if gi==7:
            h('自主开发的研究材料',2)
            p('MA-SQLGrid保存电力数据库查询研究代码与开发样本；C²GES保存技术报告抽取代码及合成测试材料。此类材料用于原型开发、回归测试和压力测试，单独管理，不计入上述65条公共资源，也不作为真实业务验证数据。')
    assert len(used)==65 and len(set(used))==65 and set(used)==set(records)
    (BASE/'resource_classification.json').write_text(json.dumps({'groups':group_defs,'resource_ids':used,'count':65},ensure_ascii=False,indent=2),encoding='utf-8')

v2=v2.replace("BASE=ROOT/'linfan_team_v2'","BASE=ROOT/'linfan_team_v3'")
v2=v2.replace('科研合作业绩与能力介绍_v2.docx','科研合作业绩与能力介绍_v3.docx')
v2=v2.replace("sec.footer.paragraphs[0].runs[0].text='林凡团队科研合作  |  '","sec.footer.paragraphs[0].runs[0].text='电力人工智能科研合作  |  '")

replacements={
'我们为电力行业提供的科研支持':'团队简介',
'我们是以林凡为主要合作联系人，面向电力与能源行业开展人工智能交叉研究的厦门大学科研团队。依托生成模型、强化学习、图学习和优化算法积累，我们与电网企业、科研院所及能源装备企业共同研究预测、诊断、调度、知识服务和安全管控问题，推进算法研发、软件原型与业务场景验证。':'我们来自厦门大学，长期从事人工智能算法研究，并与电网和能源企业合作，将研究工作应用于设备诊断、储能管理、负荷预测和生产安全等业务。近年来，合作课题进一步延伸到电力大模型、企业档案解析、检索增强与车桩网协同优化。',
'林凡具有国家级科研项目组织与跨学科合作经历，长期开展人工智能方法研究和产业应用。结合张志宏在电力图学习与设备智能诊断方面的积累，以及周达在随机建模、机器学习与国网横向研究方面的经验，我们能够组织覆盖算法、数学方法和电力业务的协同研究。':'团队由人工智能、软件工程和应用数学等方向的研究人员协同开展工作。既有国家级课题的研究经历，也积累了与电力企业共同解决业务问题的经验。我们希望把这些积累带入新的合作，在客户关心的具体问题上开展深入研究，形成能继续使用和发展的算法与软件成果。',
'林凡学术与人才培养':'学术与人才培养',
'授权发明专利10项；JCR Q1论文16篇；已毕业硕士22人、博士5人':'授权发明专利10项；已发表论文清单27篇；培养毕业硕士22人、博士5人',
'统计口径：林凡个人、14项项目清单与联合工程成果分别统计，不相加；分担经费采用各项目原登记口径，项目总金额包含合作单位经费。资源目录包含数据、模型、代码和访问入口。':'注：学术与人才培养为负责人履历汇总；项目及联合工程成果分别统计。项目总金额包含合作单位经费，分担经费合计按项目清单计算。',
'我们希望开展的合作':'合作方向',
'围绕客户实际业务，共同申报科研课题、攻关关键算法、建设业务智能原型，并形成技术报告、论文、专利和软件成果。近期重点包括电力大模型与智能体、设备智慧诊断、储能健康管理、负荷与新能源预测，以及源网荷储车协同优化。':'无论是已有课题需要补充算法和实验，还是希望围绕新业务申报项目，都可以从一次具体的技术交流开始。近期重点合作方向包括电力大模型与智能体、设备健康诊断、储能运行、负荷与新能源预测，以及源网荷储车协同优化。',
'一  林凡学术履历':'一  学术背景与人才培养',
'林凡已指导毕业硕士研究生22人、博士研究生5人，获授权发明专利10项，发表JCR Q1论文16篇。具有国家自然科学基金、国家科技支撑计划、科技部中小企业创新基金和国家重点研发计划相关主持或参与经历。':'已指导毕业硕士研究生22人、博士研究生5人，获授权发明专利10项。研究经历包括主持国家自然科学基金面上项目、科技部相关科技计划和创新基金项目，承担国家科技支撑计划子课题，并参与国家重点研发计划。完整论文及项目清单见后文。',
'林凡指导学生参加国家级竞赛并获银奖、铜奖。':'指导学生参加国家级竞赛并获银奖、铜奖。',
'林凡  生成式智能与优化决策':'生成式智能与优化决策',
'林凡在IEEE TNNLS':'相关成果发表于IEEE TNNLS',
'等会议或论文集中发表研究成果，能够支撑':'等会议或论文集，为',
'电力智能体、时序预测和优化算法研发。':'电力智能体、时序预测和优化算法研究提供了方法基础。',
'该组数字为联合完成单位的成果口径，与林凡个人成果分别列示。我们在新合作中以具体业务需求和验证结果确定性能指标，推进已有方法的场景适配和工程实现。':'联合成果覆盖多个完成单位，数量单独列示。新的合作将结合客户的运行条件，进一步开展方法适配与工程验证。',
'跨学科方法如何服务电力客户':'面向电力业务的方法积累',
'分担经费和参与排序沿用各项目负责人原登记口径；本表为团队项目清单，不将全部项目统一归为林凡个人主持。项目总金额不等同于团队到账经费。':'注：分担经费与排序对应各项目登记人员；项目总额包含合作单位经费。',
'四  主要发表期刊与学术布局':'四  主要发表期刊',
'我们已在下列期刊形成代表性成果。此处展示实际发表经历；面向未来合作课题的投稿范围另列于后文。林凡16篇JCR Q1论文采用个人履历统计，不把不同年度期刊分区直接折算为论文总量。':'上述期刊论文分布于以下14种刊物，涵盖人工智能方法、工业信息处理和交叉应用。合作研究的拟投稿期刊另列于后文。',
'我们适合承担的任务':'联合攻关中的工作分工',
'七  我们可以共同开展的研究':'七  重点研究方向',
'我们的实施安排':'项目推进安排',
'林凡履历、个人成果数量及14项项目经费采用2026年9月更新资料；联合成果为主配微协同项目口径，个人与联合统计不相加。以下列出公开学术与政策来源，供合作交流查阅。':'以下链接提供学术背景与政策文件的进一步信息，便于交流时查阅。',
'以下为协同研究力量张志宏、周达及其合作者的代表论文，与林凡个人成果分开列示。':'以下为张志宏、周达及其合作者的相关论文，补充展示电力图学习、设备诊断与时空建模方面的研究积累。',
}
for a,b in replacements.items():
    assert a in v2,a
    v2=v2.replace(a,b)
v2=replace_block(v2,"page('四  林凡代表性学术成果')","page('四  主要发表期刊')",'additional_projects()\nbibliography()')
v2=replace_block(v2,"page('五  知识产权与成果转化基础')","page('六  面向十五五的科研合作布局')",'patent_catalogue()')
v2=replace_block(v2,'# Full resource catalogue,',"page('附录二  代表成果与政策来源')",'classified_resources()')
# Vary the repetitive per-profile boilerplate without changing technical content.
v2=v2.replace("p('我们'+question)","p(question)")
v2=v2.replace("p('研究基础包括'+data)","p('可利用的数据与研究基础包括'+data)")
v2=v2.replace("p('我们可'+deliver)","p('合作中可'+deliver)")
exec(compile(v2,str(ROOT/'internal/build_linfan_v2.py'),'exec'),globals())
(BASE/'publication_coverage.json').write_text(json.dumps({'provided_ids':list(range(1,28)),'included_ids':[r[0] for r in PAPERS],'journal_count':21,'conference_count':6,'historical_Q1_labels':17,'historical_Q2_labels':4,'tier_note':'User CV historical labels; no inference of current quartiles or comparable metric years.'},ensure_ascii=False,indent=2),encoding='utf-8')
