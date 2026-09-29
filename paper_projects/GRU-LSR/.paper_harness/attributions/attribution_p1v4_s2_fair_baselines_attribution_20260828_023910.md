## 1. 近因（Proximate cause）

第二项 evidence 验收在执行科学测试前的包导入预检中异常退出：

```text
Path(powergrid_benchmark.__file__)
TypeError: ... not 'NoneType'
```

当前工作树中的 `powergrid_benchmark` 是 namespace package，合法地满足 `__file__ = None`；共享验收脚本却假定所有包都有文件型 `__file__`，因此产生假阴性，Hard Gate 随即按 fail-closed 规则将阶段标记为 `BLOCKED`。

## 2. 根因（Root cause）

根因是共享 harness 的工作树来源校验不兼容 PEP 420 namespace package：

- 校验只读取 `package.__file__`，未处理 `package.__path__` 或 `package.__spec__.submodule_search_locations`。
- 它把“没有单一包文件”误判成“未从工作树导入”。
- 该预检直到约 842 秒的完整实验结束后才触发，导致导入问题被发现得过晚。
- 现有回归测试覆盖了实验和科学验收逻辑，却未覆盖 namespace package、环境中同名包以及工作树路径绑定等启动场景。

这不是实验协议、指标完整性或结果方向造成的失败。实验验证器已确认 2,310/2,310 行完整、240/240 训练轨迹完成且零失败单元；负向、零效应和 onset 不适用结果也是 plan v4 明确要求保留的合法证据。

## 3. 分类

**主分类：harness blocker**

更具体地说，这是由当前 Python 包布局触发的 harness 兼容性缺陷，而不是独立的环境故障。

| 类别 | 判定 | 依据 |
|---|---|---|
| manuscript/evidence | 否 | 实验 validator 通过，证据行完整；不利结果不构成协议失败 |
| executor | 否 | `exit_code=0`，实验执行完整 |
| harness | **是** | 共享导入预检对 `__file__ = None` 处理错误 |
| environment | 次要触发条件 | namespace package 布局暴露了 harness 假设，但布局本身合法 |
| human-input | 否 | 不缺作者身份、专家判断或其他人工材料 |

置信度：**高**。

## 4. 安全恢复

1. 保留当前锁定工作树、日志、acceptance 文件和 nonce `20260828_020912-491c1541`，不得清理或改写现场。
2. 在共享 harness 中单独修复导入来源预检，不修改 plan v4、冻结合同、实验代码、结果文件或科学验收标准。
3. 对普通包、namespace package、错误的 ambient package 和缺失工作树源码分别运行回归测试。
4. 先在保存的工作树上只读验证修复后的预检确实绑定到该工作树的 `src`。
5. 按 harness 正式流程请求重试同一已批准阶段，并重新运行原始两条 acceptance 命令。
6. 只有两项验收均通过后才能产生 candidate/accept；不得手工修改 `acceptance.json`、跳过 evidence gate，或把当前实验 validator 的通过等同于阶段通过。

## 5. Harness 改进提案

将来源校验改为同时支持普通包和 namespace package：

```python
spec = importlib.util.find_spec("powergrid_benchmark")

if spec is None:
    fail("package_not_found")

locations = []

if spec.origin and spec.origin not in {"namespace", "built-in", "frozen"}:
    locations.append(Path(spec.origin).resolve())

if spec.submodule_search_locations:
    locations.extend(
        Path(path).resolve()
        for path in spec.submodule_search_locations
    )

require_expected_worktree_source(locations, expected_worktree_src)
```

同时建议：

- 在昂贵实验启动前运行独立的工作树导入预检。
- 记录 `sys.executable`、规范化后的 `sys.path`、`spec.origin` 和全部搜索路径。
- 明确区分 `HARNESS_PREFLIGHT_ERROR` 与 `SCIENTIFIC_ACCEPTANCE_FAILURE`。
- 若解析到 ambient 安装而非工作树源码，必须 fail closed。
- 为普通包、namespace package、路径污染和 `__file__ = None` 建立固定回归用例。
- 保持 `sys.executable -m pytest`，避免解释器与 pytest 启动器错配。

该改进只消除错误的 harness 假阴性，不降低或绕过 Hard Gate。
