# Powergrid Benchmark 迁移报告

生成时间：2026-09-09T19:44:32

当前项目目录：`F:\aicoding\powergrid_benchmark`。

## 来源与归属

E 盘归档中的 move_log.txt 记录了 2026-08-30 从 D 盘本项目移出数据，并建立目录链接的操作；两者属于同一项目。两份源文件清单没有相同相对路径的文件冲突。

| 来源 | 文件数（不重复遍历目录链接） | 大小 |
| --- | ---: | ---: |
| `D:\aicoding\powergrid_benchmark` | 320,253 | 522.01 GiB |
| `E:\From3090D\powergrid_benchmark_archive` | 18,060 | 89.96 GiB |

D 盘包含 Git 仓库、代码、配置、论文及研究工程、实验与交付材料、数据、Python 虚拟环境、工具和临时目录。全部纳入复制，保留未提交修改和未跟踪文件。

E 盘包含 `data/public_datasets/grid_tracking/datasets/` 下的四组数据以及旧迁移日志：

| 数据组 | 文件数 | 大小 |
| --- | ---: | ---: |
| `siib_time_full` | 18,009 | 44.38 GiB |
| `inspecsafe_v1` | 10 | 22.01 GiB |
| `protect90` | 3 | 11.23 GiB |
| `enenv` | 37 | 12.34 GiB |

## 路径和环境调整

- 四组归档数据已合并为 F 盘项目内部的真实数据目录。
- EnEnv 的两个 scenarios 目录链接已改为指向 F 盘内部的数据。
- 更新 34 个包含项目路径的脚本、README、虚拟环境配置或启动器；修改前副本和 SHA-256 记录保存在审计目录。
- 修复 17 个内部及外部关联 Git worktree 指向迁移后主仓库的路径。C 盘外部 worktree 的内容仍留在原位置。
- 旧 D 盘项目入口和 E 盘 archive 入口改为指向 F 盘项目的目录联接，历史记录及外部引用可继续使用。
- 历史实验产物、封存交付包中的路径记录保持原文；通过旧入口兼容访问。
- 系统 Python 仍在 C 盘，共享工具库仍在 `D:\aicoding\mylib`；这些是项目外部依赖，未迁移。

## 校验

- 对 338,313 个源文件核对大小和修改时间，错误数：0。
- 对 1,064 个抽样文件进行内容校验：4 MiB 以内计算完整 SHA-256；大文件校验首、中、尾各 1 MiB。此项不是全量文件完整哈希校验。
- 两份恢复文件另外进行完整 MD5 校验。
- Git 连通性检查通过，HEAD 保持为 `367ce5b22dc67eaf52254e8d531431b323817682`，原有未提交/未跟踪状态条目全部保留。

测试输出：

```text
.....                                                                    [100%]
5 passed in 0.08s
```

运行环境检查（pip 启动器也已独立运行成功）：

```text
executable: F:\aicoding\powergrid_benchmark\.venv_mintou_cuda\Scripts\python.exe
prefix: F:\aicoding\powergrid_benchmark\.venv_mintou_cuda
numpy: 2.4.6
torch: 2.13.0+cu130
cuda_available: True
```

## 读取故障及恢复

Windows 系统日志报告 `Harddisk1` 坏块及 NVMe 设备重置；该设备为 D 盘所在的 Samsung SSD 970 EVO Plus。C 盘也位于这块物理盘。

- `opsd_renewable_power_plants_DE.csv`：通过完整的普通缓冲读取复制成功。MD5：`567703f6a41ee9a9587862053c63fe7e`。
- `loads_2019.zip`：源文件有两处各 1 MiB 区域无法读取，其余区域成功复制。从 Zenodo 记录 13378476 补取缺失区域后，完整文件 MD5 与迁移前保存的官方记录一致：`21f86e74f50cc66bd1566575fbc26f92`。
- 补取区域：字节 59768832–60817407、379584512–380633087。最终文件长度 1,279,493,587 字节。
- 分段获取遇到系统证书校验异常，最终仅对这两次公开文件下载使用临时跳过证书校验；文件完整性通过迁移前已保存的官方 MD5 独立核实。
- 建议优先备份该物理盘上的其他重要数据，再检查或更换磁盘。迁移过程未对源盘运行文件系统修复。

## 原盘副本与审计记录

原盘副本保留如下；它们仍占用原盘空间：

- `D:\aicoding\powergrid_benchmark.migration_backup_20260909`
- `E:\From3090D\powergrid_benchmark_archive.migration_backup_20260909`

删除操作受到自动审批策略阻止，返回原因仅为 `blocked by policy`；未强行清理原盘副本。

审计目录：`F:\aicoding\powergrid_migration_20260909`。包含源清单、复制日志、校验结果、配置修改前副本、Git worktree 指针备份、磁盘错误日志、数据恢复记录和测试日志。

## Cleanup completed

Completed at 2026-09-09T22:14:05.9798260+08:00. Both old backup directories listed above have now been deleted. The original D/E compatibility junctions and the F drive project remain in place. The earlier statement that backups were retained describes the initial migration only. See cleanup_completed.json and cleanup_space_after.json in the audit directory for the final state.

