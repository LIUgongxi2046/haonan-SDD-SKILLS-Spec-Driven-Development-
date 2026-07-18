# 部署档位选择

## LOCAL_PROCESS / STATIC

适用：本地工具、个人使用、纯静态站点或无需服务端状态。

检查：构建产物、环境配置、静态缓存、错误页、回滚版本和备份。

## SIMPLE_MANAGED

适用：小团队、标准 Web/API、可接受托管数据库与平台能力。

检查：平台运行时、区域、秘密、数据库迁移、预览环境、配额和供应商退出路径。

## CONTAINER_SINGLE_HOST

适用：需要可移植运行时、少量服务和可控运维，但无需集群调度。

检查：非 root、健康检查、卷、网络、日志轮转、备份、重启策略和主机故障恢复。

## SERVERLESS

适用：事件驱动、突发流量、无常驻进程；先确认时长、连接、文件系统和冷启动限制。

检查：函数超时、并发、幂等、队列、长任务拆分、区域、观测和成本上限。

## ORCHESTRATED

适用：有明确的多服务、隔离、扩缩容、滚动发布或组织平台需求。

检查：调度、资源、探针、PDB、网络策略、配置/秘密、Stateful 服务、灾备和集群成本。

## GPU_OR_PRIVATE_MODEL

仅适用：模型私有化、数据驻留或成本/性能证据支持。

检查：模型许可/版本、显存、批处理、队列、冷启动、权重存储、灰度、质量回归、GPU 监控和降级到外部/小模型策略。

## 选择记录

```text
profile,drivers,alternatives,rejected_reasons,cost_drivers,operational_owner,validation,status
```
