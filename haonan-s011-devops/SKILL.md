---
name: haonan-s011-devops
description: 部署、CI/CD、运维与 MLOps 实施技能。Use when Codex needs to为现有代码设计或实现本地进程、静态托管、容器、Serverless 或 Kubernetes 部署，配置 CI/CD、秘密、迁移、备份、可观测性、发布、回滚和 smoke test；实际部署或外部资源变更需要用户明确授权。
---

# Haonan S011 部署实施

## 定位

选择与项目规模和运行约束匹配的最简单可运营方案。容器、Kubernetes、GPU、MLOps 和多区域部署都是条件能力，不是默认答案。

## 工作模式

- `PLAN`：部署拓扑、环境、发布和运维方案；默认只读。
- `IMPLEMENT`：创建/修改 Dockerfile、CI、IaC、部署和监控配置。
- `DEPLOY`：在用户明确授权的目标环境执行外部变更。
- `AUDIT`：审查现有流水线、运行配置、可靠性、成本和安全。

## 输入处理

读取代码库、运行时/锁文件、构建测试命令、HLD/LLD、数据迁移、质量门禁、目标环境、预算、流量和 SLO。先检测实际平台与 CI 提供商；不把 GitLab `stages` 写进 GitHub Actions，也不硬编码过时运行时版本。

平台能力、镜像、动作、云服务和安全配置会变化，必须使用当前官方文档。未知目标环境时可比较方案，但不生成伪可用生产配置。

## 部署档位

按 `references/deployment-profiles.md` 选择并说明依据：

- `LOCAL_PROCESS` / `STATIC`
- `SIMPLE_MANAGED`
- `CONTAINER_SINGLE_HOST`
- `SERVERLESS`
- `ORCHESTRATED`
- `GPU_OR_PRIVATE_MODEL`（仅确有私有模型需求）

## 工作流

1. 建立服务、端口、依赖、构建产物、配置、秘密、持久化和网络清单。
2. 定义 dev/staging/prod 差异，避免复制真实秘密和生产数据。
3. 选择部署档位，设计健康检查、资源、伸缩、任务和长连接处理。
4. 设计 CI：格式/类型/测试/evals/安全/构建/产物签名/部署/审批。
5. 设计数据库与知识库迁移、备份、对账、前后兼容和回滚顺序。
6. 定义发布策略、smoke test、观测窗口、自动/人工回滚和责任人。
7. 落实日志、指标、追踪、成本、AI 延迟/质量和敏感数据处理。
8. `IMPLEMENT` 后实际 lint/validate 配置；`DEPLOY` 后验证目标环境和回滚路径。

## 质量门禁

- 配置与选定平台语法一致，并使用官方校验器或 dry-run 验证。
- 镜像/进程最小权限运行，秘密不进入仓库、镜像或日志。
- 数据变更先备份/兼容/回滚，再切换应用；不可逆迁移必须显式批准。
- 发布通过健康检查、核心 smoke、监控和回滚验证。
- 方案为 `CREATED`，配置校验为 `VERIFIED` 只限校验范围；未执行部署不声称已上线。

## 授权与交付

`IMPLEMENT` 限于用户授权的仓库。`DEPLOY` 前再次确认目标环境、账号/项目、预计影响和回滚；生产发布、DNS、密钥、付费资源或数据迁移不能由“帮我做 DevOps”默认推导。

输出包括：档位与依据、拓扑、环境/秘密、CI/CD、迁移/备份、发布/回滚、可观测性、成本驱动、验证证据和未决项。交付给 `$haonan-s006-review` 发布门禁和 `$haonan-s012-docs` 运维文档。
