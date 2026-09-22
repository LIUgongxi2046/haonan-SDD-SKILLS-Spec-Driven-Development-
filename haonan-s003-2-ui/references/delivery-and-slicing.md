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
