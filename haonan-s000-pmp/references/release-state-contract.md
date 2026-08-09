# Haonan 发布状态契约

## 原则

把每个发布面单独记账。一次发布可以同时包含 API、数据库、H5、管理后台和小程序，也可以只包含其中一项。任一状态变化都必须有时间、目标、版本和证据；一个发布面的完成不能自动代表其他发布面完成。

## 发布面与状态

| 发布面 | 状态 | 最小证据 |
|---|---|---|
| 源码 | `LOCAL_CHANGED`、`LOCAL_VERIFIED` | 工作区、测试命令、退出码 |
| Git | `GIT_COMMITTED`、`GIT_PUSHED` | commit、分支、远端 commit |
| 服务端 | `PROD_DEPLOYED`、`PROD_VERIFIED`、`ROLLED_BACK` | 主机/服务、制品校验和、健康检查、核心 smoke |
| 数据库 | `DB_BACKED_UP`、`DB_MIGRATED`、`DB_VERIFIED`、`DB_ROLLED_BACK` | 备份路径、迁移 ID、对账结果 |
| H5/后台 | `WEB_BUILT`、`WEB_DEPLOYED`、`WEB_VERIFIED` | 构建目录/校验和、目标 URL、页面 smoke |
| 小程序 | `MP_BUILT`、`MP_PREVIEW_VERIFIED`、`MP_UPLOADED`、`REVIEW_SUBMITTED`、`RELEASED` | 构建目录/校验和、开发工具/真机结果、版本号、审核状态 |

状态属于发布面而不是全局流水线。例如 `GIT_PUSHED` 不代表 `PROD_DEPLOYED`，`PROD_VERIFIED` 不代表 `MP_UPLOADED`。

## Release Manifest

每次准备部署、上传或审核时记录：

```yaml
release:
  id: release-id
  source_commit: git-sha
  branch: branch-name
  workspace_clean: true
  components:
    - name: api-or-client
      artifact: absolute-or-release-path
      sha256: checksum
      target: environment-or-platform
      state: LOCAL_VERIFIED
  database:
    backup: path-or-not-applicable
    migrations: []
    reconciliation: []
  configuration_changes: [] # 只记录变量名，不记录秘密值
  verification_evidence: []
  rollback:
    artifact: path-or-version
    procedure: command-or-runbook
  approvals: []
```

Manifest 可以是 YAML、JSON、Markdown 表或发布系统记录，但字段语义必须保留。

## 状态转换规则

1. 修改代码默认只改变源码状态，不自动触发 Git 或外部发布。
2. 每次构建记录源 commit、目标平台、时间和产物校验和；重新构建后旧证据失效。
3. 生产发布前冻结候选 commit，集中完成回归；调试性热修必须单独记录原因、影响和回滚点。
4. 数据变更先备份，再迁移、对账和业务抽样；应用部署成功不能替代数据验证。
5. 生产 smoke 使用只读、幂等或可自动清理的数据；产生的测试记录必须回收或显式保留。
6. 小程序/H5/原生客户端分别验证资源、网络、平台 API、导航、安全区和真实构建物。
7. 上传、提交审核和正式发布属于外部状态变化，分别记录版本号、操作者和结果。

## 汇报模板

先说明各发布面的当前状态，再说明下一步。禁止只写“已上线”“已同步”而不说明上线了什么、部署到哪里、基于哪个版本和如何验证。
