# claude-os

> 我停止手动阅读财经新闻了。我的 Claude OS 替我做这件事——而且做得更好。

<!-- screenshot: 运行一次"早报"生成 morning-brief.html 后，截图放在这里 -->

Claude Code 是一个终端工具。我把它当作操作系统来用。

**内核** → 一份 [`CLAUDE.md`](./CLAUDE.md)，定义了 Claude 如何思考和行动  
**应用** → [7 个生产级 Skill](./skills/)，覆盖投资研究、信息聚合、开发工作流  
**哲学** → 每个 Skill 都有设计文档，解释"为什么这样做"，而不只是"怎么用"

![stars](https://img.shields.io/github/stars/Hudson7777/claude-os?style=flat-square)
![license](https://img.shields.io/github/license/Hudson7777/claude-os?style=flat-square)

---

## 这套系统在帮我做什么

| 场景 | Skill | 省了什么 |
|------|-------|---------|
| 每日科技 + 财经摘要 | `morning-brief` | 每天 90 分钟的阅读时间 |
| 投资主题研究 | `alpha-hunter` | 把几小时的研究压缩成 20 分钟的结构化分析 |
| 模型选型 | `model-coding-benchmark` | 用数据代替猜测 |
| 微信文章收藏 | `wechat-article-save` | 零摩擦，粘贴链接即完成 |
| 任意网络搜索 | `super-search` | 一个入口，自动路由到最合适的工具 |

---

## Skills 总览

| Skill | 功能 | 安装难度 |
|-------|------|---------|
| [alpha-hunter](./skills/alpha-hunter/) | 科技投资主题生命周期分析 | 📐 模板型 |
| [super-search](./skills/super-search/) | 统一搜索路由器 | 🔧 需配置 |
| [morning-brief](./skills/morning-brief/) | AI + 财经日报，输出 HTML | 🔧 需配置 |
| [evening-brief](./skills/evening-brief/) | 晚报：要闻 + 深度 + 知识充电 | 🔧 需配置 |
| [model-coding-benchmark](./skills/model-coding-benchmark/) | LLM 编程能力盲测横评 | 🔧 需配置 |
| [market-anomaly-monitor](./skills/market-anomaly-monitor/) | 股市异动检测 + 事件归因 | 🔧 需配置 |
| [wechat-article-save](./skills/wechat-article-save/) | 微信公众号文章自动保存 | ⚡ 开箱即用 |

**安装任意 Skill：**
```bash
cp -r skills/SKILL_NAME ~/.claude/skills/
```

---

## 内核：CLAUDE.md

大多数人把 Claude Code 当聊天机器人用。我花了 6 个月持续打磨一份指令文件。

它定义了：回复风格、何时停下来问、代码 Review 标准、Skill 调用规则、输出格式，以及一份持续更新的纠错日志。

其中最有价值的部分：子 Agent 调度逻辑——把复杂任务路由给并行 Agent，带结构化 Review。这一套改变了我处理任何复杂工作的方式。

→ [查看 CLAUDE.md](./CLAUDE.md)

---

## 设计哲学

Skill 不是 Prompt。Prompt 告诉 Claude 做一次某件事。Skill 改变的是 Claude 在某一类场景下的默认行为——持久、可组合、不需要重复。

操作系统的类比是真实的：CLAUDE.md 是内核（始终加载，影响一切），Skill 是应用（按需加载，单一职责），Cron Hook 是守护进程（后台运行，无需干预）。

这个 Repo 里最重要的 Skill，不是最复杂的那个。是那个已经变得"隐形"的——我不再想着它，只是得到输出。

---

English version → [README.md](./README.md)

---

如果这改变了你对 Claude Code 的认知，给个 ⭐ 吧。
