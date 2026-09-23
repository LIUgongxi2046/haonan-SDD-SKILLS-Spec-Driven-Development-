# UI 产物与来源

## 模式对应产物

- `DESIGN`：页面或屏幕映射、设计系统、Token、状态规范、必要资产与审查结果。
- `AUDIT`：现有产物引用、检查范围、证据和问题；无需创建新图片或整套设计文件。
- `IMPLEMENT`：实际修改、适用页面映射、现有规范引用和验证结果；新资产仅在实际需要时增加。

原有完整设计资料继续保留，局部工作引用其版本。默认目录可使用 `ui-delivery/`，根据任务保存 `route-design-map.csv` 或 `screen-design-map.csv`、`design-system.md`、`tokens.json`、`ui-audit.md`、页面与状态资料及必要资产。

## 清单

屏幕映射字段：`source_id,screen_id,name,source_type,status,artifact_path`，可增加 `requirement_refs,required_states,notes`。`source_type` 使用 `EXPLICIT / INFERRED / UNKNOWN`。

资产存在时使用 `asset-manifest.csv`，包含 `asset_id,file_path,usage,width,height,format,transparency,source`。引用关系使用 `page-asset-map.csv`：`screen_id,asset_id,usage`。路径相对交付目录；引用既有原型、代码或资产时，通过 `--source-root` 明确允许的真实来源目录，无需复制已有资料。

生成资产使用 `image-generation-manifest.csv`：`asset_id,generation_tool,prompt_summary,source_image_path,output_file_path`。只有实际调用生成能力时记录，其他合法资产保留准确来源和许可。功能图标可使用现有图标库；用户明确的格式要求优先。

## 资产质量

核对格式、实际尺寸、透明度和引用位置，多个分辨率从同一源文件派生，避免无依据放大或比例失真。名称使用稳定英文标识，源文件和导出文件的关系可追溯。

需要分包时按模块或平台组织，保留清单与校验和，验证文件总量和引用。可编辑设计、PDF 和图片按用户要求提供，缺少相应工具时准确标记未完成部分。

## 校验

`audit_ui_delivery.py /absolute/delivery --mode design` 校验完整设计结构；`--mode audit` 或 `--mode implementation` 校验对应模式。`--source-root /absolute/project/path` 可以重复提供，清单引用文件必须处于交付目录或这些目录中；审查报告和本次必需清单仍位于交付目录。只有任务要求生成图片时使用 `--require-generated`。

校验器检查文件、CSV/JSON、路径、引用及实际图片格式和尺寸，不进行视觉识别，不证明业务交互。执行证据与未执行检查分别报告。

## 完整设计的目录与导出规格

| 路径 | 内容 |
|---|---|
| `screens/` | 全部必需页面稿与页面映射 |
| `states/` | 核心页面的加载、空、错误、确认、反馈与完成状态 |
| `assets/master/` | 高分辨率源资产及可编辑来源 |
| `assets/1x/`、`assets/2x/` | 从同一 Master 导出的目标尺寸 |
| `assets/previews/` | 获准生成的资产预览 |
| `assumptions-and-open-questions.md` | 来源、假设、未知项及用户决定 |

- IP、图标与装饰根据透明度要求导出 PNG/WebP；背景与摄影根据质量、体积选择 WebP/JPG，保留源文件。
- 目标端需要时提供 3x，所有尺寸从同一 Master 导出，不能分别生成造成角色或构图差异。
- 名称采用 `<module>-<purpose>-<state>@<scale>.<ext>`，例如 `profile-empty-history@1x.png`。记录用途、尺寸、格式、透明度及使用页面。
- 资产清单增加 `license_or_restriction`；页面引用增加 `required,notes`。源文件与导出文件通过同一 `asset_id` 关联。
- 生成资产记录实际工具及提示词摘要；第三方或已有资产保留真实来源和使用限制，不要求重新生成。
- 按端、模块或资产类型分包，每个压缩包可独立解压，包含版本与清单；全部包的文件总量、校验和及清单覆盖需要实际检查。
- 可阅读 PDF、Markdown、JSON Token、CSV 清单与源资产各有用途，完整交付保留可维护来源。用户要求 Figma 时提供可编辑组件、变量及页面层级；未创建时准确标记。
