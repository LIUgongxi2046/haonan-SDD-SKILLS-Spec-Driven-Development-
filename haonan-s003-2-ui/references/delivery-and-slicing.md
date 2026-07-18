# 切图与交付参考

## 1. 推荐目录

```text
ui-delivery/
├── route-design-map.csv 或 screen-design-map.csv
├── assumptions-and-open-questions.md
├── design-system.md
├── tokens.json
├── ui-audit.md
├── screens/
├── states/
├── assets/
│   ├── master/
│   ├── 1x/
│   ├── 2x/
│   └── previews/
├── asset-manifest.csv
└── page-asset-map.csv
```

只有在用户需要且能力可用时增加 Figma、PDF 或实现代码目录。

## 2. 资产格式

- IP、图标和装饰：透明 PNG、WebP 或适合的矢量源文件。
- 大背景和摄影图：根据透明度与质量选择 WebP/JPG。
- Master 保留高分辨率和可编辑源；1x、2x、3x 从同一 Master 派生。
- 不放大低分辨率源图，不分别生成不同尺寸导致角色漂移。

## 3. 命名

使用稳定英文小写加连字符：

```text
<module>-<purpose>-<state>@<scale>.<ext>
home-hero-welcome@2x.webp
profile-empty-history@1x.png
```

名称不得依赖“最终版”“新新版本”等时间性描述。

## 4. 清单字段

`asset-manifest.csv`：

```text
asset_id,file_path,usage,width,height,format,transparency,source,license_or_restriction
```

`page-asset-map.csv`：

```text
screen_id,asset_id,usage,required,notes
```

所有相对路径以交付根目录为基准。生成资产记录生成方式；第三方资产记录许可和限制。

## 5. 大文件与压缩包

- 按端、模块或资产类型拆包，每个包可独立解压。
- 包内保留清单和版本信息。
- 拆包后检查文件总数、校验和与清单覆盖率。
- 不只交付一个超大且无法稳定下载的文件。

## 6. PDF 与可编辑设计稿

PDF 是阅读型交付，不是唯一事实源；Markdown、JSON Token、CSV 清单和源资产必须保留。需要 Figma 时优先生成可编辑组件、变量和页面层级；若当前无相应能力，输出导入规范并标记阻塞，不伪称已创建文件。
