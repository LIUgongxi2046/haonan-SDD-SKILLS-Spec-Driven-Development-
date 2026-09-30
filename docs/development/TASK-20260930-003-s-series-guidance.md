# TASK-20260930-003 S 系列正文与参考规范整理

## 任务与依据

- task_id：TASK-20260930-003。
- task_source：本文。
- 用户要求：全部执行规则归入正文或 references，保留原有专业内容，并同步 Obsidian 与 Codex。
- 状态：ACCEPTED；内容、格式、引用与同步一致性检查通过。
- 文档有效性：CURRENT，2026-09-30。
- 关联任务：[逐项核查](TASK-20260930-002-s-series-review.md)。

## 当前设计

每个 skill 的执行模式由 SKILL.md 定义，详细流程、证据和交接要求保存在对应 references。正文明确引用实际文件。跨阶段共同要求继续由 S000 的 Codex 执行规则维护。项目任务事实保存于项目开发记录，项目经验不会自动修改全局 skill。

| Skill | 正式参考 |
|---|---|
| S000 | [持续交付](../../haonan-s000-pmp/references/delivery-workflow.md) |
| S001 | [战略验证](../../haonan-s001-ceo-strategy/references/strategy-validation.md) |
| S002 | [需求验收](../../haonan-s002-prd/references/requirements-validation.md) |
| S003-1 | [原型交互](../../haonan-s003-1-prototype/references/interaction-workflow.md) |
| S003-2 | [UI 实施](../../haonan-s003-2-ui/references/ui-workflow.md) |
| S004 | [架构交接](../../haonan-s004-hld/references/architecture-workflow.md) |
| S005-1 | [数据生命周期](../../haonan-s005-1-lld-data/references/data-lifecycle.md) |
| S005-2 | [服务行为](../../haonan-s005-2-lld-back/references/service-behavior.md) |
| S005-3 | [运行控制](../../haonan-s005-3-lld-agent/references/runtime-governance.md) |
| S005-4 | [交互状态](../../haonan-s005-4-lld-front/references/interaction-state.md) |
| S006 | [评审流程](../../haonan-s006-review/references/review-workflow.md) |
| S007 | [任务规划](../../haonan-s007-planner/references/planning-workflow.md) |
| S008 | [实施验证](../../haonan-s008-coder/references/implementation-workflow.md) |
| S009 | [业务验收](../../haonan-s009-test/references/acceptance-workflow.md) |
| S010 | [安全复验](../../haonan-s010-safety/references/security-workflow.md) |
| S011 | [运行部署](../../haonan-s011-devops/references/operations-workflow.md) |
| S012 | [文档交接](../../haonan-s012-docs/references/documentation-workflow.md) |

## 验收条件

- AC-GUIDANCE-01：17 项执行规范的全部正文要求可在相应 skill 正文或参考文件找到。
- AC-GUIDANCE-02：原有专业章节、代码及图表模板、脚本、Schema 与调用配置完整保留。
- AC-GUIDANCE-03：全部 skill 格式、文件引用和引用入口检查通过。
- AC-GUIDANCE-04：Codex 当前加载目录和 Obsidian 对应文件内容一致。

## 验证与继续条件

AC-GUIDANCE-01 至 AC-GUIDANCE-03 已通过：使用 Markdown 解析器比对 308 个正文内容块，全部具有对应内容；17 项格式校验和本地引用检查通过；原有专业章节、代码及图表模板、其他参考、脚本、Schema 和调用配置完整保留。详见 [结构证据](evidence/TASK-20260930-003-structure.txt)。原文件的重复发现元数据和标题由正式 SKILL.md 元数据及参考文件标题承担。

检查命令：在 `/Users/liuhaoxian/Downloads/我的/AI项目/04 企业AI` 运行 `.haonan-s-upgrade/venv/bin/python .haonan-s-upgrade/verify_integration.py`。使用现有 Markdown 解析器和 skill-creator 的 quick_validate.py，未执行应用业务测试。

AC-GUIDANCE-04 已通过：75 个 Codex 对应文件与工作副本的 SHA-256 一致，Obsidian 对应文件同步校验通过，详见 [同步证据](evidence/TASK-20260930-003-sync.txt)。Codex 当前使用 `/Users/liuhaoxian/.agents/skills`；Obsidian 目标为 `/Users/liuhaoxian/Downloads/我的/Obsidian/刘浩南/haonan Skill/产品研发skill`。

当前没有未完成事项。后续执行读取正文模式与所引用的正式流程，项目事实继续保存在项目记录。修改流程规则时维护对应参考文件及引用入口。
