# 安全评估矩阵

## 范围记录

```text
target,owner_or_authorization,environment,allowed_methods,excluded_methods,rate_limit,time_window,data_policy,stop_condition
```

## 威胁记录

```text
threat_id,asset,actor,trust_boundary,entry,precondition,attack_path,impact,existing_control,detection,residual_risk,owner
```

## 传统应用面

- 身份、会话、授权、租户隔离和审计。
- 输入、查询、模板、文件、URL、反序列化和输出编码。
- 密钥、依赖、构建、制品、CI 权限和供应链。
- 网络、CORS/CSRF、速率限制、错误泄露和日志敏感数据。
- 数据最小化、加密、备份、删除、保留和环境隔离。

## AI 系统面

- 直接/间接 Prompt Injection 和指令/数据边界。
- 不可信模型输出进入 HTML、代码、SQL、URL 或工具参数。
- 工具越权、跨租户、重复调用、成本耗尽和循环。
- RAG 投毒、来源许可、引用伪造、删除传播和数据泄露。
- Prompt/模型/工具/数据集供应链与版本回滚。
- 记忆污染、跨会话泄露和人工审批绕过。

## 发现记录

```text
finding_id,evidence,reproduction,impact,likelihood,severity,control_gap,remediation,verification,residual_risk,status
```

Payload 使用最小无害样本，真实攻击执行遵守授权范围和停止条件。

每项控制记录需求或风险来源、适用环境、合法操作路径与拒绝路径。附加审核和发布条件有依据，不能通过阻断全部操作取得通过。身份在请求、异步结果、跳转及采用时一致。
