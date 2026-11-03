# 紫星服务器 · 玩家手册与地图

Minecraft 26.3 生电服（`mc.zixing.fun`）的静态站点：世界地图 + 路径点 + 手册入口。

## 内容

- `index.html` — 首页，Liquid Glass 风格，地图居中（默认视野对准工业村）
- `tiles/overworld/{z}/{x}/{y}.webp` — 稀疏瓦片金字塔，原生 zoom 7 = 1 px/方块
- `waypoints.json` — 主世界路径点（来自 Xaero minimap）
- `manifest.json` — 构建统计（瓦片数、体积、坐标范围、坐标变换）
- `vendor/` — Leaflet 1.9.4、liquid-glass（MIT，`dpawlikowski/liquid-glass`）
- `build.py` — 从 Xaero 数据重建瓦片

## 坐标变换

MC 世界是平面网格，用 Leaflet `CRS.Simple`：

```
Leaflet latlng = [-MC_Z, MC_X]
tile x = floor(MC_X / (512 * 2^(7 - zoom)))
tile y = floor(MC_Z / (512 * 2^(7 - zoom)))
```

原生 zoom 7 时 1 方块 = 1 像素，一个 512 方块的 region 正好一张瓦片。原生层级以上可继续放大但不会增加细节。

## 数据

源包：`26.3生电(based on xplus).mrpack` 里的 `client-overrides/xaero/`。

- 637 个地表 region，全部保留；未探索区域透明
- 主世界 12 个路径点，其中 1 个已禁用，默认展示 11 个
- `manifest.json` 记录各层瓦片数与总字节；`waypoints.json` 保留名称、颜色编号、XYZ 与禁用标记

地图只能表示已有探索数据，不能补全未探索区；时间戳只反映打包记录，不保证地形或路径点当前有效。

## 重建瓦片

需要支持 Xaero 存档格式 8.8 的 `xaerotools` 和 Pillow：

```bash
env -u PYTHONPATH /usr/bin/python3 build.py
```

脚本顶部硬编码输入目录与 renderer 路径，换机器要先改。

Xaero 26.3 的 region 存档是 8.8，官方 v0.5.0 只读到 7.8，必须从 main 分支自行编译：

```bash
git clone --depth 1 https://github.com/dekrom/xaerotools.git
cd xaerotools && cargo build --release -p xaerotools   # 包名是 xaerotools，不是 xaerotools-cli
```

## 后续

下界单独生成 `tiles/nether` 并加维度切换，不与主世界瓦片混合；下界路径点用自身坐标，不乘 8 当主世界点。

## 隐私

本仓库公开即坐标公开。地图是**玩家客户端探索快照**，不代表服务器实时状态；设施是否可用以手册标注为准。仅隐藏正文坐标没有保护作用——地图、标记数据与坐标变换都能还原位置。

## 部署

纯静态，无构建步骤。Cloudflare Pages 直接托管本目录即可。

## 验证

全部瓦片已逐张解码并核对计数；Chromium headless 通过本地 HTTP 实际加载 Leaflet 与瓦片，检查过路径点搜索定位、坐标方向与原生像素变换、禁用点开关。测试脚本见 `test-browser.js`，不随页面加载。
