# 技术评审矩阵

## 问题记录

```text
issue_id,mode,contract_a,contract_b,evidence_a,evidence_b,conflict,severity,impact,fix,verification,owner,status
```

证据引用文件路径、版本以及标题/行号/符号。没有证据的位置不得写成事实。

## 设计评审对照

| 对照对象 | 重点 |
|---|---|
| PRD ↔ Prototype/UI | 角色、任务、页面、状态、权限、AC |
| PRD/NFR ↔ HLD | 边界、SLO、数据、安全、成本、灾备 |
| HLD ↔ LLD | 组件、所有权、协议、失败和部署假设 |
| Data ↔ Backend | 字段、事务、索引、迁移、删除传播 |
| Backend ↔ Agent | 工具 Schema、权限、超时、错误、审计 |
| Backend/Agent ↔ Front | 类型、事件顺序、取消、重连、错误恢复 |
| UI ↔ Front | Token、组件状态、响应式、资产、a11y |

## 完整交付检查

- 原始承诺、验收动作和责任任务无遗漏，范围调整有用户决定。
- 实际断言符合业务结果，结构与安全拒绝证据不替代合法业务成功。
- 配置、事件及 Agent 结果具有承诺的实际使用方。
- 全部未完成任务保留，代码、环境和证据版本一致。

## 发布门禁证据

- 目标 commit/build 和变更范围。
- 自动化测试、Evals、覆盖样本和失败清单。
- 安全扫描/红队范围、授权与残余风险。
- Schema 迁移、备份、对账和回滚演练。
- 部署差异、配置/秘密、健康检查和 smoke test。
- 监控、告警、值班和回滚责任人。

## 决议规则

- P0 未关闭：`NO_GO`。
- P1 未关闭：默认 `NO_GO`；责任人书面接受且有监控/回滚时才可 `CONDITIONAL_GO`。
- 关键证据缺失：`INSUFFICIENT_EVIDENCE`，明确结论范围和待验证内容。
- P2/P3 进入带负责人和期限的技术债清单。
