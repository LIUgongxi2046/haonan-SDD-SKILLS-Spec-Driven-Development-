# 原型交付字段

## 屏幕地图

```text
screen_id,name,role,entry,exit,requirement_refs,source_type,required_states,artifact,status
```

`source_type` 使用 `EXPLICIT`、`INFERRED`、`UNKNOWN`；`status` 使用流水线统一状态。

## 屏幕规格

每个屏幕记录：

- 目标与成功条件。
- 入口、退出、返回和深链行为。
- 内容层级、核心控件和可操作区域。
- 输入规则、校验、确认与反馈。
- 数据来源、加载/空/错误/权限/离线状态。
- 响应式变化、键盘/焦点和触控规则。
- 关联 `FR`、`AC` 与未决问题。

## 流程规格

```text
flow_id,actor,precondition,start,steps,decision_points,failure_recovery,end,requirement_refs
```

## 原型代码交付

仅 `BUILD` 模式适用：

- 记录仓库、启动命令、环境变量占位和变更文件。
- 明确哪些数据为 mock，哪些调用真实接口。
- 运行实际格式化、类型检查、测试和构建。
- 视觉对照记录视口、参考图、实现截图和差异；未执行则标记阻塞。
