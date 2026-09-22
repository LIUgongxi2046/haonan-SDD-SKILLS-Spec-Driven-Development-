# 技术文档包清单

## 资产索引

```text
doc_id,audience,path,purpose,source_of_truth,version_or_commit,generation,owner,status,last_verified
```

## 开发者文档

- README/快速开始、环境与命令。
- 架构上下文、ADR 和模块边界。
- OpenAPI/事件/Schema、认证、错误、配额和示例。
- 数据字典、迁移、兼容和本地开发数据。
- 扩展、贡献、测试和调试。

## 运维文档

- 环境矩阵、配置和秘密来源。
- 部署、迁移、备份、恢复、回滚和 smoke test。
- 指标、日志、追踪、告警、SLO 和值班。
- Runbook：症状、确认、缓解、恢复、升级和事后动作。

## 产品与外部文档

- 角色、功能、限制、数据处理和管理员 SOP。
- 外部 API/SDK/Webhook 集成和版本策略。
- FAQ、故障排查、培训与可访问性说明。
- Release Notes、Breaking Changes、迁移步骤和废弃时间线。

## 自动校验

- Markdown lint、链接和锚点。
- OpenAPI/JSON Schema/YAML 语法。
- 代码片段与命令 smoke test。
- 路由/API/Schema 与文档的漂移检查。
- 敏感信息、真实个人数据和过时版本扫描。

校验结果记录工具、版本、命令、退出码和产物路径。

## 当前交付记录

引用同一需求、任务、验收与证据 ID，交接保留全部未完成项、约束来源、授权、当前修改、实际环境、有效证据和下一可执行任务。当前实现与目标范围分别描述，文案调整不能关闭尚未实现的业务需求。
