# Agent LLD 契约字段

## Agent 注册表

```text
agent_id,goal,non_goals,input_schema,output_schema,allowed_tools,data_scope,budget,termination,escalation,owner
```

## 工具注册表

```text
tool_id,purpose,input_schema,output_schema,permission,side_effect,idempotency,timeout,error_codes,audit,approval
```

工具错误应稳定、可恢复且不泄露敏感实现细节。

## 状态机

至少覆盖：`READY`、`PLANNING`、`EXECUTING`、`WAITING_APPROVAL`、`RETRYING`、`COMPLETED`、`FAILED`、`CANCELLED`。按项目裁剪，不强制名称一致。

每条转换记录：事件、守卫条件、动作、预算消耗、验证器、失败去向。

## 上下文与记忆

- 固定规则、任务输入、检索证据、工具结果、对话历史分层。
- PII/PHI/秘密最小化、保留、删除、跨租户隔离。
- 压缩或摘要保留事实来源和未决状态，不保留隐式推理。
- 缓存键包含影响行为的版本；动态能力变化有失效策略。

## 预算与终止

```text
max_wall_time,max_turns,max_tool_calls,max_retries,cost_or_token_budget,no_progress_rule,cancel_behavior
```

## Evals

```text
eval_id,risk,scenario,dataset_version,metric,threshold_source,judge,variance_policy,release_action
```

区分确定性验证、模型评测、人工评审和线上监控。
