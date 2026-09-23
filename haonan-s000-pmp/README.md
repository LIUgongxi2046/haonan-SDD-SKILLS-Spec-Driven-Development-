# Haonan S 系列技能

本系列包含 17 个研发技能，可由 Codex 或具备同等文件访问能力的 Harness 使用。入口为各目录的 `SKILL.md`；根据当前请求选用必要技能，保留用户完整目标与已有授权。

各入口包含原始专业流程、详细模板、示例与验收清单。执行前读取 [Codex 执行规则](references/codex-execution.md) 及当前技能的 `haoemr-experience.md`，将业务完整性、连续执行和证据要求加入完整专业流程。补充内容不能替代正文交付物。

S000 负责选择和持续编排，S001/S002 明确产品与需求，S003 定义原型和 UI，S004/S005 定义架构及详细实现边界，S006 审查，S007 规划完整任务，S008 实施，S009/S010 验证，S011 运行与发布，S012 文档与交接。

多任务工作使用 [交付记录](references/delivery-ledger.md)，跨环境工作使用 [发布状态](references/release-state-contract.md)。任务、证据和能力类型分别管理，设计产物、局部测试与业务验收分别报告。

校验脚本依赖见 `scripts/requirements.txt`。技能说明可直接使用；执行脚本前通过项目认可的 Python 环境安装对应依赖。技能互相引用时按当前发现路径读取，不依赖特定 Harness 的工具名。
