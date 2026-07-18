# 数据 LLD 契约字段

## 数据源登记

```text
source_id,owner,location,purpose,license,allowed_use,sensitivity,update_frequency,version,checksum,retention,status
```

## 实体与字段

```text
entity,field,type,nullable,identifier,uniqueness,description,classification,source,lineage,validation,retention
```

物理类型必须与目标存储和版本匹配。示例不能替代实际样本分析。

## 存储决策矩阵

| 访问模式 | 一致性 | 规模/增长 | 延迟 | 可运维性 | 候选 | 决策/证据 |
|---|---|---|---|---|---|---|

只有需求支持时才引入专用缓存、搜索、向量或图存储。

## 管道阶段

```text
stage,input,output,validation,idempotency,failure_state,retry,quarantine,observability,owner
```

## RAG/检索契约

- 文档与 chunk 稳定 ID、版本、页码/坐标和来源许可。
- 分块策略、重叠、语言/表格/图片处理和评测方法。
- metadata 过滤、权限/租户条件、召回/重排输出和置信信号。
- 引用回查、源文档更新、删除传播和缓存失效。
- 黄金集版本、样本分层、人工标注和回归门禁。

## 数据质量

```text
rule_id,dimension,scope,expression,threshold_source,severity,action,owner,evidence
```

阈值必须来自业务要求、历史基线或实验；没有来源时写待基线化。
