# Haonan 研发流水线统一契约

## 1. 交付信封

每个阶段的交付至少包含：

```yaml
artifact:
  stage: S000
  mode: ROUTE
  status: CREATED
  sources:
    - id: SRC-001
      type: EXPLICIT
      location: path-or-message
  assumptions: []
  missing_inputs: []
  outputs: []
  verification_evidence: []
  next_handoff: []
```

YAML 只是字段示意。状态必须来自 `PLANNED`、`CREATED`、`OBSERVED`、`VERIFIED`、`BLOCKED`。

## 2. 依赖类型

- `REQUIRED`：没有该契约会造成不可逆错误，缺失时阻塞相应动作。
- `CONDITIONAL`：仅特定范围需要，例如无 UI 项目不需要 S003-2/S005-4。
- `ADVISORY`：有助于提升质量，但可用显式假设继续。

不要把“推荐有”写成“必须有”。

## 3. 设计与执行分离

- 设计、评审、计划：默认只读，可在信息不完整时输出草案。
- 文件/代码实施：需要用户明确要求创建或修改。
- 测试与安全执行：需要明确范围和安全环境；扫描结果才可作为观察证据。
- 部署与外部写入：需要用户明确授权目标环境；生产动作不得从“完成研发流程”中推导。

## 4. 设计阶段 DAG

```text
S002
├── S003 ── [S003-2] ──┐
└── S004 ─┬─ S005-1 ───┤
          ├─ S005-2 ────┤
          ├─ S005-3 ────┤
          └─ S005-4 ────┘
                       S006 DESIGN_REVIEW
```

具体顺序由契约决定。例如后端 API 可先形成草案供 Agent/前端对齐，数据表不必在所有项目中先于 UI 组件。

## 5. 实施与发布 DAG

```text
S007 -> S008 -> S009 + S010 -> S006 RELEASE_GATE -> S011 -> S012
```

S009 的测试资产规划可从 S002 并行开始；S010 的威胁建模可从 S004 并行开始。执行结果必须回流 S006 发布门禁。

跨环境发布必须同时使用 [release-state-contract.md](release-state-contract.md)。源码提交、远端推送、服务端部署、数据库迁移、客户端上传和外部审核是不同状态，不允许用其中一个推断其他状态。

## 6. 报告诚信

- 计划命令、生成文件、观察结果和通过结论分栏。
- 模板数字只允许标记为示例。
- 百分比必须给出可核查分母、分子与证据。
- 合规要求只能说明映射或差距，除非有合格主体的正式认证证据。
- “当前版本”必须附 commit、构建物或目标环境证据；不能只凭文件时间、IDE 画面或口头印象判断。
