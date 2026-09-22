# 需求、任务与验收记录

本文件供 S000、S002、S006、S007、S008、S009、S011、S012 共同使用。多任务与跨会话工作维护唯一当前记录；既有任务系统可映射同样信息。小型单项工作可在任务正文记录这些关系，无需额外文件。

## 范围和映射

项目中的 `delivery-ledger.json` 使用 [JSON Schema](delivery-ledger.schema.json)。先从原始用户要求建立 `commitments`，再建立 `acceptances` 和 `tasks`。不能只扫描现有代码生成全部承诺。

既有任务系统继续作为唯一当前记录。多任务或跨会话工作需要自动校验时，由 S007 建立字段映射，当前执行者在状态更新后导出符合本 Schema 的 JSON 快照，S012 在交接中记录来源版本与快照时间。状态修改回到原系统进行，再重新导出，不能并行维护两套任务状态。校验器只读取 JSON，不直接读取正文或外部任务系统。小型单项正文记录按同样关系人工核对，无需为了运行校验器额外建立任务系统。

| 对象 | 字段及含义 |
|---|---|
| `baseline` | `id` 标识当前代码与环境组合；`environment_ref` 指向不含秘密的实际运行环境记录 |
| `commitments` | `id`、`source_ref`、`outcome`、`disposition`、`acceptance_ids`；排除范围需要 `decision_ref` 引用用户决定 |
| `acceptances` | `id`、`commitment_id`、`scenario`、`expected_result`、`outcome_type`、`capability`、`required_checks`、`status`、`evidence_ids`、`consumer` |
| `tasks` | `id`、`acceptance_ids`、`depends_on`、`state`、`allowed_paths`、`blockers` |
| `evidence` | `id`、`check_id`、`kind`、`baseline_id`、`receipt_path`、`receipt_sha256` |
| `continuation` | `mode`、全部 `remaining_task_ids`、`next_task_id`、`constraints`、`authorization_refs` |

`source_ref` 引用用户消息或批准需求，`decision_ref` 只用于真实范围决定。所有 ID 稳定，跨会话保持一致。每项范围内承诺有验收，每项验收有任务，每项任务有可检查结果。共享验证可服务多个验收，但须分别检查其实际断言。

## 独立状态

- 任务：`TODO / IN_PROGRESS / IMPLEMENTED / ACCEPTED / BLOCKED`。
- 验收：`NOT_RUN / PASS / FAIL / STALE / BLOCKED`。
- 能力：`REAL / READONLY / SIMULATION / PROTOTYPE / DESIGN`。
- 结果类型：`BUSINESS / DESIGN / QUALITY / EXTERNAL`。
- 证据类型：`STRUCTURE / STATIC / UNIT / API / SECURITY / BUSINESS / INTEGRATION / EXTERNAL / EVAL / VISUAL`。

证据类型说明检查内容，能力类型说明被检查的对象。授权模拟中的业务操作可以得到 `BUSINESS` 证据，但能力仍为 `SIMULATION`，不能升级为真实外部接入。只读能力检查实际查询结果，不能仅验证控件存在。

业务验收需要 `BUSINESS` 或 `INTEGRATION` 检查；外部接入需要 `EXTERNAL`。配置、事件、Agent 结果等需要后续使用时，`consumer.required=true`，填写使用方和相应 `check_id`。不适用时给出原因。

## 执行证据

使用当前具有依赖的 Python，执行技能目录中的脚本。S000 脚本依赖见 `scripts/requirements.txt`，按项目依赖管理方式安装，不跳过缺少的依赖。

`capture_check.py` 接收以下参数：

- `--output-dir`：本次检查独立产物目录，必须尚不存在。
- `--check-id`、`--kind`、`--baseline-id`：绑定计划中的检查、类型与当前基线。
- `--cwd`：实际执行目录。
- `--input`：重复指定所有影响结论的源码、测试、配置和环境记录文件。
- `--artifact`：重复指定命令结束后应存在的测试报告等产物。
- `--timeout`：明确执行时限。
- `--` 后提供实际命令及参数，不通过 shell 拼接命令。

`environment_ref` 必须指向实际文件，路径相对于记录文件所在目录。每次执行将该文件加入 `--input`，使代码、检查和环境共同绑定；环境改变后更新该文件并重新执行相关检查。

脚本运行真实命令，保存输出、退出码、起止时间、输入校验和及产物校验和。返回失败状态时不得登记通过；执行期间输入改变也不能使用该证据。不要把凭据放入命令参数或输出。

将生成的 `receipt.json` 路径及校验和关联到 `evidence`。验收记录只引用实际执行的对应检查，不能手写通过结果代替执行记录。人工或代理行为审查保留实际产物，并通过专门检查命令核对审查依据；未经运行的人工判断不伪装成命令证据。

## 校验命令

`validate_delivery.py /absolute/path/to/delivery-ledger.json` 校验结构、ID、覆盖、依赖、持续任务集合和所有通过声明的执行证据。

追加 `--require-complete` 时，要求当前范围的全部任务达到 `ACCEPTED`、全部验收通过、没有剩余任务。每项声明使用当前基线的有效证据，校验器核查原始结果、输入与产物是否仍匹配。

校验工具不能证明原始需求已经完整提取，也不能理解命令断言是否符合业务含义。S006 负责核对承诺集合和完成声明，S009 负责核对预期结果及实际测试；`exit_code=0` 与校验器通过均不能替代该审查。

## 续接和范围变化

每次完成、失败、范围变更或会话续接时更新完整待办集合。用户暂停后保留状态；新会话读取当前文件及环境，证据不适用时标记 `STALE` 并复验。存在并发修改时核对任务拥有的文件和进程。

阶段报告注明本次检查过的范围、尚未验收承诺、真实阻塞及下一可执行任务。局部说明修正与能力实现分别登记。用户明确排除范围时记录决定，其他工作继续按原始承诺执行。
