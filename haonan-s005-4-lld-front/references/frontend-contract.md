# 前端 LLD 契约字段

## 路由追溯

```text
route_id,path,screen_id,roles,fr_refs,ac_refs,api_refs,states,guards,layout
```

## 组件职责

```text
component,responsibility,inputs,outputs,owned_state,side_effects,a11y,tests
```

组件层级不应镜像后端服务；按用户任务、复用和变更边界拆分。

## 状态

- 本地交互状态。
- URL/导航状态。
- 表单与校验状态。
- 服务端数据、缓存和失效状态。
- 会话/权限/租户状态。
- 流式任务和后台任务状态。

每个状态记录来源、所有者、转换事件、持久化、恢复和 UI 反馈。

## API/事件适配

```text
contract_id,backend_ref,frontend_type,request_mapping,response_mapping,error_mapping,cancel,retry,cache,telemetry
```

## UI 恢复矩阵

```text
condition,user_message,preserved_state,primary_action,secondary_action,telemetry,severity
```

## 前端质量

- XSS/Markdown/URL/文件处理。
- 键盘、焦点、语义、触控、对比度和减少动态。
- 长文本、多语言、时区、数字/日期和 RTL（适用时）。
- 性能预算、分包、图片、缓存和弱网。
- 单元、组件、契约、a11y、视觉回归和 E2E 分层。
