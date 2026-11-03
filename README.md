# 紫星服务器 · 玩家手册与地图

Minecraft **26.3 生电服**（`mc.zixing.fun`）的玩家站：世界地图 + 路径点 + 设施手册。

**线上地址：<https://mc-zixing-map-site.pages.dev>**

---

## 这是什么

一张能点的服务器地图，加上每台机器在哪、怎么用的说明。

- **地图**：真实地形瓦片，1 像素 = 1 方块，可拖拽缩放，默认视野对准工业村
- **路径点**：来自游戏内 Xaero 标记，点一下看坐标
- **手册**：设施分类、入服指南、交通、服规（逐步补充中）

## 目录结构

```
index.html                          首页（Liquid Glass 风格，地图居中）
tiles/overworld/{z}/{x}/{y}.webp    稀疏瓦片金字塔
waypoints.json                      主世界路径点（Xaero 原始数据转换）
data/facilities.json                设施数据源（名称/别名/坐标/用途/状态）
manifest.json                       构建统计（瓦片数、体积、坐标范围）
vendor/                             Leaflet 1.9.4、liquid-glass（均含许可证）
build.py                            从 Xaero 数据重建瓦片
CONTRIBUTING.md                     编辑指南：加设施、改说明、发布
```

## 坐标怎么对上

MC 世界是平面网格（X 向东、Z 向南），不用地球经纬度，走 Leaflet `CRS.Simple`：

```
Leaflet latlng = [-MC_Z, MC_X]

tile x = floor(MC_X / (512 * 2^(7 - zoom)))
tile y = floor(MC_Z / (512 * 2^(7 - zoom)))
```

原生 zoom = 7，1 方块 = 1 像素，一个 512 方块的 region 正好一张瓦片。超过 zoom 7 可继续放大，但不会增加细节。

父级瓦片合并必须用 `x // 2, z // 2` 向下取整——负坐标用截断取整会错位。

## 数据从哪来

`26.3生电(based on xplus).mrpack` 里的 `client-overrides/xaero/`：

- `world-map/<server>/null/mw$<id>/<rx>_<rz>.zip` — 主世界地表，637 个 region，全部保留，未探索区域透明
- `minimap/<server>/dim%0/mw$<id>_<n>.txt` — 主世界路径点，12 条（1 条已禁用，默认隐藏）

路径点格式：`waypoint:名称:首字母:x:y:z:颜色:disabled:...`

**地图是玩家客户端的探索快照**，不是服务器实时状态。新建筑要有人走到附近、让 Xaero 记录并保存，才有新数据。

## 重建瓦片

需要支持 Xaero 存档格式 **8.8** 的 `xaerotools` 和 Pillow：

```bash
env -u PYTHONPATH /usr/bin/python3 build.py
```

脚本顶部硬编码了输入目录与 renderer 路径，换机器先改这两处。

Xaero 26.3 的 region 存档是 8.8，官方 v0.5.0 只读到 7.8，必须从 main 分支自行编译：

```bash
git clone --depth 1 https://github.com/dekrom/xaerotools.git
cd xaerotools && cargo build --release -p xaerotools   # 包名是 xaerotools，不是 xaerotools-cli
```

编译后先验证：`doctor --root <xaero目录>` 应输出 `all clear`。

## 部署

Cloudflare Pages 的 **Git 集成**项目 `mc-zixing-map-site`，生产分支 `master`。

**push 到 master 就自动部署**，不需要手动上传，构建约 30 秒。

站点是纯静态、无构建步骤——仓库根目录即站点根目录，所以别把调试文件、截图、日志提交进来。

## 隐私

**本仓库公开 = 地图与路径点坐标公开。** 这是知情的取舍，不是疏漏。

把坐标从正文删掉、只留地图标记，**并不能**保护位置——瓦片、`waypoints.json` 和坐标变换公式都能还原出精确位置。真要私密只能加访问控制（如 Cloudflare Access）。

## 验证

全部瓦片已逐张解码并核对计数；Chromium headless 通过本地 HTTP 实际加载 Leaflet 与瓦片，检查过路径点搜索定位、坐标方向与原生像素变换、禁用点开关。测试脚本见 `test-browser.js`，不随页面加载。

## 已知待办

- 首页地图内有一处异常黑色区域，待排查
- 下界地图未加入（现有整合包只带主世界）
- 设施详情页、入服指南、服规页尚未写
- `data/facilities.json` 里用途与操作步骤待群友补充
