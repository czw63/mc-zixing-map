# 编辑指南（数据字段）

这份讲的是 **JSON 数据怎么填**：设施、假人的字段含义。

> 用 AI 助手（Claude Code / Codex / Cursor 等）改的话，让它先读根目录的 [AGENTS.md](AGENTS.md)，那里有完整的项目约定和踩坑记录。

**写文章 / 加页面**请看站点上的 [怎么改文档](https://mc-zixing-map-site.pages.dev/docs/contributing/) —— 那边讲的是 Markdown 怎么写、新页面怎么加。

改完提交到 `master`，Cloudflare 会自动构建部署（约 1 分钟）。

## 最快上手：只改文字

1. 在 GitHub 网页上打开要改的文件，点右上角铅笔图标
2. 改完在下方填一句说明，选 **Create a new branch for this commit and start a pull request**（或者直接提交到 master，看你想不想让人先看一遍）
3. 提交

改 Markdown 和 `data/facilities.json` 都不需要本地环境。

## 加一台设施

设施信息统一放在 **`data/facilities.json`**，不写在 HTML 里。这样地图标记和手册卡片读的是同一份数据，不会出现「文章改了地图没改」。

一条记录长这样：

```json
{
  "id": "witch-farm",
  "name": "女巫塔",
  "aliases": ["女巫"],
  "dimension": "overworld",
  "coords": { "x": -73, "y": 300, "z": -2104 },
  "category": "mob-farm",
  "products": ["红石", "萤石", "红石灯"],
  "status": "ok",
  "verifiedAt": "2026-11-03",
  "usage": "从主城…，上去之后…，挂机位置在…",
  "notes": "别动 XX，会掉线"
}
```

字段说明：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 唯一英文标识，小写加连字符，别改已存在的 |
| `name` | ✅ | 显示名，和游戏里路径点一致最好 |
| `aliases` | | 群里怎么叫它，搜索能命中 |
| `dimension` | ✅ | `overworld` / `nether` / `end` |
| `coords` | ✅ | 方块坐标，整数 |
| `category` | ✅ | 见下方分类 |
| `products` | | 产物，搜「红石」就能找到它 |
| `status` | ✅ | `ok` 正常 / `broken` 坏了 / `removed` 已拆 / `unknown` 不确定 |
| `verifiedAt` | | 最后确认能用的日期，`YYYY-MM-DD` |
| `usage` | | 怎么去、怎么开、在哪挂机、怎么收、走之前要做什么 |
| `notes` | | 禁忌和坑，比如「别拆」「会卡服」 |

分类：`mob-farm` 刷怪类、`crop-farm` 农作物、`iron-farm` 铁/金、`storage` 仓储、`trading` 交易、`transport` 交通、`utility` 其他公用设施。

## 写使用说明的要求

**路径点只证明有人在那里标过一个点，不证明机器现在能用。** 所以：

- 不确定的写 `"status": "unknown"`，别默认 `ok`
- 不知道的字段留空或删掉，**不要凭机器名字猜**
- 写「开关在入口右手边地面上」，不要写「正常开启」这种没有信息量的话
- 有坑一定要写，比如「挂机别站在 XX 那格」「离开前记得关灯」

## 补假人目录

假人目录在 `data/bots.json`，首页「假人目录」区块读它渲染。

加一个假人，就往 `bots` 数组里加一条：

```json
{
  "name": "bot_sleep",
  "purpose": "挂女巫塔",
  "location": "女巫塔旁边的挂机位",
  "owner": "谁在维护",
  "howTo": "怎么召唤、怎么收回",
  "notes": "别踢、别动 XX",
  "status": "online"
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 游戏内 ID，一字不差 |
| `purpose` | | 这个假人在干什么 |
| `location` | | 挂在哪个设施或位置，能对上 `facilities.json` 的名字最好 |
| `owner` | | 谁负责，出问题找谁 |
| `howTo` | | 怎么召唤、怎么收回去 |
| `notes` | | 禁忌：别踢、别拉走、别点 |

目录**不记在线状态**。假人开没开、挂没挂着，去游戏里看或问人，这里只记它是谁、在哪、干什么用的。

不认识的字段就留空或整行删掉，卡片只显示有内容的行。

## 加一张地图上的点

`data/facilities.json` 里的 `coords` 就是地图标记位置，改坐标地图自动跟着变。

要新增地图区域（比如下界），需要重新生成瓦片，找维护者跑 `build.py`，见 README。

## 别做的事

- **别提交** 调试文件、截图、日志、原始 mrpack、`node_modules`
- **别直接改** `tiles/` 里的瓦片——那是脚本生成的，手改会被下次重建覆盖
- **别删** `vendor/` 里的许可证文件，Leaflet 和 liquid-glass 都要求保留
- 改 `waypoints.json` 前想清楚：它是从游戏数据转出来的，手改会和下次导入冲突，一般改 `data/facilities.json` 就够

## 本地预览

```bash
python -m http.server 8000
```

然后开 <http://localhost:8000>。**不要直接双击 `index.html`**——浏览器会因 `file://` 协议挡住 JSON 读取，页面会空白。

## 需要权限或有疑问

仓库地址 <https://github.com/czw63/mc-zixing-map>，找 czw / Jelly / Jeroen。
