# 后端 LLD 规范字段

## API

```text
operation_id,caller,method_or_event,path_or_topic,auth,input_schema,output_schema,error_refs,idempotency,timeout,rate_limit,version
```

每个错误定义稳定代码、HTTP/RPC 状态、可重试性、用户安全消息、日志等级和恢复动作。

## 写操作

记录：

- 事务边界和数据所有者。
- 幂等键、唯一约束与重复请求返回语义。
- 并发冲突检测和客户端恢复。
- 部分失败、补偿、重试与审计。

不要默认分布式锁；优先用数据库唯一性、乐观版本或消息去重等与问题匹配的机制。

## 异步任务

```text
job_type,states,lease,timeout,cancel,retry,backoff,dead_letter,result_delivery,idempotency,observability
```

## 权限

```text
subject,resource,action,scope,condition,decision_point,audit_fields
```

## 外部依赖

```text
dependency,owner,data_shared,auth,timeout,retry,circuit_breaker,fallback,slo,monitoring
```

## 验收

- 接口格式校验器通过。
- 合法角色可以建立前置、执行操作、重新读取结果，并完成所承诺的后续业务。
- 配置有运行时使用方，事件完成状态有实际结果或外部回执。
- 认证、授权、租户隔离和负向输入有测试。
- 重试/重复投递/并发冲突有确定性用例。
- 超时、降级、指标、追踪与敏感日志有验证证据。
