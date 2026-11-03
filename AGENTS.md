# AGENTS.md

给 AI 编码助手看的项目说明。人看的话，[README.md](README.md) 更合适。

## 这是什么

紫星服务器（Minecraft 26.3 生电服）的玩家站：地图首页 + 文档。托管在 Cloudflare Pages，push 到 `master` 自动构建部署。

线上：<https://mc-zixing-map-site.pages.dev>

## 技术栈

- **Astro 7 + Starlight**：文档从 Markdown 生成，路由 `/docs/*`
- **Leaflet 1.9.4**（本地 vendor，不用 CDN）：首页地图
- 首页 `public/index.html` 是**纯静态 HTML，不经过 Astro 渲染**，改它不影响文档
- 瓦片是预先切好的 WebP 金字塔，构建时不重新生成

## 目录

```
public/index.html              首页。纯静态，手写 HTML + 内联 JS，不经 Astro
src/content/docs/docs/*.md     文档页。改这里就够，不用碰 HTML
src/content.config.ts          Starlight 内容集合定义（别删，删了构建直接失败）
src/styles/theme.css           文档主题变量
astro.config.mjs               侧边栏/站点配置。新增页面要在这里登记
tiles/overworld/{z}/{x}/{y}.webp   地图瓦片。脚本生成，禁止手改
data/facilities.json           设施数据源。地图标记和文档共用
data/bots.json                 假人目录
waypoints.json                 Xaero 路径点导出，游戏数据转换而来
vendor/                        Leaflet + liquid-glass，含许可证
scripts/check_bots.py          SLP 查询服务器在线状态
build.py                       从 Xaero region 重建瓦片（不常跑）
```

## 构建与验证

```bash
npm install        # 首次
npm run build      # 输出到 dist/
npm run dev        # 本地预览，改 md 热更新
```

**改完必须跑一次 `npm run build`**，确认没有构建错误再提交。构建约 3 秒（不含瓦片复制）。

## 常见任务

### 加一页文档

1. 新建 `src/content/docs/docs/<slug>.md`
2. 开头写 frontmatter：

```markdown
---
title: 页面标题
description: 一句话说明，用于搜索和 SEO
---
```

3. 在 `astro.config.mjs` 的 `sidebar` 数组里加 `{ label: '显示名', slug: 'docs/<slug>' }`

slug 就是文件路径去掉 `.md`。漏了第 3 步页面能访问但侧边栏没入口。

### 改设施 / 假人

改 `data/facilities.json` 或 `data/bots.json`，字段说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

这两个文件是**唯一数据源**——地图标记和文档都读它。不要在 Markdown 里另抄一份坐标。

### 改首页

`public/index.html`，单文件，样式和脚本都内联在里面。瓦片路径是相对路径 `tiles/...`，别改成绝对路径。

## 硬规矩

**不许编造内容。** 这是最重要的规则。

- 设施用途、开关位置、挂机方法、假人职责——这些只有常玩的人知道，不知道就留 `null` 或写「待补」
- `status` 默认 `unknown`，别因为名字像就填 `ok`
- 路径点只证明有人在那里标过点，不证明机器能用
- 服务器在线状态、TPS、人数，只能来自实际查询，不能猜

**坐标必须来自真实数据。** 设施坐标以 `waypoints.json` / `data/facilities.json` 为准，不要手打或估算。

**禁忌比描述更有价值。** 「挂机别站那格」「离开前关灯」这种话比「装置正常」有用。

## 不要做的事

- **别改 `tiles/`**：脚本生成的，手改会被下次重建覆盖
- **别删 `vendor/` 里的许可证**：Leaflet 是 BSD-2，liquid-glass 是 MIT
- **别提交** `node_modules/`、`dist/`、`.astro/`、截图、日志、原始 mrpack
- **别装新依赖来解决排版问题**：现有 CSS 够用，加包会拖慢构建
- **别改 `src/content.config.ts`** 的 collection 名，会连带所有 slug 失效
- **别把 `package-lock.json` 用国内镜像重新生成**：npmmirror 生成的 lock 里 pagefind 平台包缺 `version` 字段，Cloudflare 的 `npm clean-install` 会报 `npm error Invalid Version:` 然后整个构建失败。必须用官方 registry：

```bash
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmjs.org
```

## 提交

直接提交到 `master` 即可，会自动部署。提交信息用中文，说清改了什么：

```
docs: 补充女巫塔的开关位置和挂机方法
fix: 修正袭击塔坐标
```

## 已知待办

- 下界地图未加入（现有整合包只带主世界）
- 首页地图内有一处异常黑色区域
- 设施用途、假人职责待群友补充
