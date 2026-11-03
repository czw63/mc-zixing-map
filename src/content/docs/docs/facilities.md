---
title: 设施目录
description: 服务器上都有哪些机器，在哪，怎么用
---

设施清单数据在仓库的 `data/facilities.json`，地图上的标记和这页读的是同一份。

:::note[先说清楚]
下面这些点的**名称和坐标是真实的**，来自游戏内路径点。但**用途、开关位置、挂机方法还没人补**——路径点只能证明有人在那里标过点，证明不了机器现在能用。没写的就是真的不知道。
:::

## 刷怪类

| 名称 | 坐标 (X / Y / Z) | 用途 | 状态 |
| --- | --- | --- | --- |
| 女巫塔 | -73 / 300 / -2104 | <span class="tbd">待补</span> | <span class="tbd">未确认</span> |
| 袭击塔 | -2136 / 221 / 696 | <span class="tbd">待补</span> | <span class="tbd">未确认</span> |
| 蠹虫笼 | 1375 / 63 / -2136 | <span class="tbd">待补</span> | <span class="tbd">未确认</span> |
| 全物种 | -1556 / 141 / -1068 | <span class="tbd">待补（连是不是刷怪装置都不确定）</span> | <span class="tbd">未确认</span> |
| 哨站 | -998 / 84 / -1242 | <span class="tbd">待补</span> | <span class="tbd">未确认</span> |

## 交易与据点

| 名称 | 坐标 | 用途 | 状态 |
| --- | --- | --- | --- |
| 工业村 | 553 / 70 / -268 | 地图默认中心，村民交易与物资集散 <span class="tbd">（待确认）</span> | <span class="tbd">未确认</span> |
| 龙宫 | 1296 / 84 / -1608 | <span class="tbd">待补（是建筑还是机器不确定）</span> | <span class="tbd">未确认</span> |
| 繁华森林 | 1495 / 70 / 165 | <span class="tbd">待补（看起来是地点标记）</span> | <span class="tbd">未确认</span> |

## 交通与探索

| 名称 | 坐标 | 说明 |
| --- | --- | --- |
| 传送门 | 1491 / 81 / 1756 | 对应的下界坐标和去处 <span class="tbd">待补</span> |
| 古城2 | 7111 / -34 / -3238 | 探索地点，是否已搜刮 <span class="tbd">待补</span> |
| 古城3 | 8172 / -50 / -3239 | 探索地点，是否已搜刮 <span class="tbd">待补</span> |
| 远古 | 2036 / -49 / -1452 | 游戏内已标记为禁用，地图上默认隐藏 |

## 怎么补

在 GitHub 上编辑 `data/facilities.json`，字段说明见 [怎么改文档](/docs/contributing/)。不确定的字段留空就行，**别按名字猜**。
