# CLAUDE.md

项目说明见 [AGENTS.md](AGENTS.md) —— 技术栈、目录结构、常见任务、硬规矩都在那里，开工前先读。

要点摘要（详情看 AGENTS.md）：

- 文档改 `src/content/docs/docs/*.md`，新页面要在 `astro.config.mjs` 的 `sidebar` 登记
- 数据改 `data/facilities.json` / `data/bots.json`，那是唯一数据源
- 改完跑 `npm run build` 验证
- **不知道的内容写「待补」，不许编造**——设施用途、开关位置、假人职责只能来自实际知情者
- 别动 `tiles/`、别删 `vendor/` 许可证、别用国内镜像重生成 `package-lock.json`
