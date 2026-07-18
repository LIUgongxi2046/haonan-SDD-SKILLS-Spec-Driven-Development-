# 测试与 Evals 矩阵

## 追溯表

```text
test_id,requirement_or_risk,layer,scenario,given,when,then,data_ref,environment,automation,status,evidence
```

## 工程测试层

- 单元：纯逻辑、状态转换、边界和错误。
- 契约：请求/响应、事件、Schema、兼容和错误目录。
- 集成：数据库、队列、缓存、外部依赖和迁移。
- UI/E2E：核心任务、权限、恢复、可访问性和跨浏览器。
- 非功能：性能、可靠性、容量、备份恢复和可观测性。

每项按风险选择，不要求所有项目全套使用。

## AI Evals

```text
eval_id,capability,risk,dataset_version,split,metric,threshold,threshold_source,judge,repeats,variance,release_action
```

- 黄金集记录来源、许可、标注规范、难度和覆盖分层。
- 明确确定性断言、规则评分、模型裁判和人工评审的差异。
- 对非确定性结果记录重复次数、方差和失败样本，不只报告均值。
- 模型/Prompt/工具/检索/数据集版本必须可复现。

## 执行记录

```text
run_id,commit,environment,command,started_at,duration,exit_code,passed,failed,skipped,flaky,artifact_path
```

报告数字必须来自执行记录，不能使用模板占位。
