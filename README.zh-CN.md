<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="PageSpeed Audit 图标">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><a href="README.md">Español</a> · <a href="README.en.md">English</a> · <a href="README.pt.md">Português</a> · <a href="README.fr.md">Français</a> · <strong>简体中文</strong> · <a href="README.hi.md">हिन्दी</a></p>

**把 PageSpeed 报告转化为三项可在网站上实施的改进。**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#工作原理)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#直接运行脚本)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#macos-和-linux-兼容性)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#macos-和-linux-兼容性)

[安装](#安装) · [使用示例](#使用方法) · [工作原理](#工作原理) · [测试](#测试)

`pagespeed-audit` 是适用于 **ChatGPT**、**Codex** 和 **Claude** 的技能，将 Google PageSpeed Insights（PSI）结果整理成简报，最多给出三项优先改进。可用于诊断慢页面、确定应修改的模板或设置，以及比较部署前后的性能。

支持公开的 HTTP(S) 网站，包括 WordPress、WooCommerce、Shopify、静态网站、客户端或服务端渲染的应用。可提供公共 URL、共享报告、截图或 PSI JSON。

四种环境共用同一套说明。Codex 从 `.agents/skills/` 加载，Claude Code 通过 `.claude/skills/` 中的符号链接访问。账号启用技能上传后，也可通过网页界面导入。

## 项目内容

| 组件 | 用途 |
| --- | --- |
| `SKILL.md` | 指导收集证据、诊断问题并交付报告。 |
| `scripts/psi.py` | 通过官方 API 测量，将 JSON 标准化并比较版本。只使用 Python 3 标准库。 |
| `references/` | 测量规则、阈值、平台诊断（含 WordPress 与 WooCommerce）、角色与报告格式。 |
| 四个子代理 | 在 Codex 的 `.codex/agents/` 和 Claude Code 的 `.claude/agents/` 中提供只读的 `psi-field`、`psi-lab`、`psi-implementation` 和 `psi-review`。 |

## macOS 和 Linux 兼容性

| 使用方式 | macOS 和 Linux 的要求 |
| --- | --- |
| 在浏览器中使用 ChatGPT 或 Claude.ai | 需要可上传技能的账号和准备好的 ZIP。已有 ZIP 时，可直接上传，无需在本机安装 Git 或 Python。 |
| Codex CLI 或 Claude Code | 安装 Git 以克隆仓库，并安装所选终端客户端。 |
| 生成 ZIP、运行 `psi.py` 或执行测试 | 需要 Python 3 标准库，无需通过 `pip` 安装包。使用 `psi.py fetch` 测量新 URL 还需访问 PageSpeed Insights API。 |

在 macOS 的“终端”或 Linux 的 Bash 或 Zsh 中运行命令。按实际需要检查对应工具的版本。

```bash
git --version
python3 --version
codex --version
claude --version
```

请参阅 [Codex CLI 官方安装说明](https://learn.chatgpt.com/docs/codex/cli)或 [Claude Code 安装指南](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code)。

在支持符号链接的文件系统上，Git 会保留 Claude Code 的链接。如链接缺失，请按 Claude Code 章节说明复制共享目录。

测试套件已在 Linux 上运行。macOS 上的本地流程仍待验证。

## 安装

| 环境 | 安装方法 | 调用方法 |
| --- | --- | --- |
| ChatGPT | 如果账号允许，在 **插件 → 技能** 中上传。 | “使用 pagespeed-audit 技能……” |
| Codex | 将仓库作为项目打开。 | `$pagespeed-audit` |
| Claude.ai | 在 **Customize → Skills** 中上传 ZIP。 | “使用 pagespeed-audit 技能……” |
| Claude Code | 将仓库作为项目打开。 | `/pagespeed-audit` |

### 为网页界面准备 ZIP

克隆仓库后用 Python 3 运行打包脚本。在 Windows 上如无 `python3`，可用 `py -3 tools/build_claude_zip.py`。

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

上传 `dist/pagespeed-audit.zip`，其中包含 `SKILL.md`、参考资料和脚本。若要使用仓库配置的四个子代理，请在 Codex 或 Claude Code 中打开项目。网页环境可以顺序执行相同流程。

### ChatGPT

1. 在侧栏打开 **插件 → 技能 → 创建 → 从电脑上传**。
2. 选择 `dist/pagespeed-audit.zip` 并等待审核完成。
3. 在新对话中输入“用 pagespeed-audit 检查我网站的移动端和桌面端”，并提供公开 URL 或附上 PSI 报告。

上传取决于技能功能与工作区权限。如果菜单不可见，可以用 Codex，或在对话中附上 PSI 报告并直接请求分析。参阅 [ChatGPT 技能官方指南](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)。

### Codex

需要 Git 和支持[技能](https://learn.chatgpt.com/docs/build-skills)的 Codex 环境。要使用四个专用代理，环境还需支持[项目子代理](https://learn.chatgpt.com/docs/agent-configuration/subagents)。

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

调用 `$pagespeed-audit`。技能从 `.agents/skills/pagespeed-audit/` 加载，代理从 `.codex/agents/` 加载。

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

技能从 `.claude/skills/pagespeed-audit/` 加载，子代理从 `.claude/agents/` 加载。可直接说“检查 https://example.com/ 在移动端和桌面端的速度”，也可调用 `/pagespeed-audit`。

> 如果符号链接缺失，请将完整的 `.agents/skills/pagespeed-audit/` 复制到 `.claude/skills/pagespeed-audit/`。Windows 上 Git 未创建链接时也可使用此方法。

### Claude.ai

1. 如果账号显示相应选项，请在 **Settings → Capabilities** 中启用代码执行和文件创建。使用受管理的工作区时，请确认组织策略允许使用技能。
2. 打开 **Customize → Skills → + → Create skill → Upload a skill**。
3. 选择 `dist/pagespeed-audit.zip`，启用技能，然后在对话中按名称调用。

参阅 [Claude 技能官方指南](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

### 当聊天环境无法测量 URL

ChatGPT 和 Claude.ai 中的自动测量取决于是否可以访问 Google PageSpeed Insights。若请求失败，请在 [PageSpeed Insights](https://pagespeed.web.dev/) 中运行测试并共享链接、移动和桌面端截图或 JSON。`summarize` 处理 JSON 文件。链接和截图按其中可见的证据解读。

### 添加到其他项目

1. 将完整的 `.agents/skills/pagespeed-audit/` 复制到项目中的同一路径。使用 Claude Code 时，也请创建 `.claude/skills/pagespeed-audit` 的副本或符号链接。
2. 要启用任务委派，将四个 `psi-*.toml` 文件复制到 `.codex/agents/`，或将四个 `psi-*.md` 文件复制到 `.claude/agents/`。保留已有配置，同名文件在替换前应先检查。
3. 从项目根目录启动代理。

技能无需额外依赖。脚本测量新 URL 时需要访问 PSI API。匿名配额有限。如需 API 密钥，请将其设为环境变量，并保存在仓库之外。

```bash
export PAGESPEED_API_KEY="..."
```

脚本通过 `X-Goog-Api-Key` 请求头将密钥发送给 Google。请避免在对话或共享报告中粘贴密钥。

## 使用方法

**审查 URL**

> 使用 pagespeed-audit 审查 https://example.com/ 的移动端和桌面端性能，给出优先改进、修改位置及验证方法的简报。

**分析已有报告**

> 用 pagespeed-audit 分析这个 PageSpeed JSON。网站使用 WordPress。提出可回退的修改，并说明无法确认原因时还缺哪些证据。

**比较部署前后**

> 比较同一页面、同一设备的部署前后报告。列出观察到的变化、测量差异和仍待核实的内容。

（在 Codex 中，在技能名称前加 `$`：`$pagespeed-audit`。）

审查整个站点时，请提供代表不同模板的公开 URL，例如首页、文章页和商品页。

### 直接运行脚本

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` 可识别常见的凭据和内部地址模式。测量前，请确认 URL 是公开的，并且不含令牌、个人数据或私有标识符。`summarize` 和 `compare` 可通过 `--json` 输出结构化结果。

## 工作原理

1. **收集证据。** 复用已有 PSI 结果或测量指定 URL。记录设备、日期和最终 URL，以识别重定向或拦截页面。
2. **分析性能。** 将 Chrome UX Report（CrUX）的真实访问数据（如有）与 Lighthouse 实验室数据分开。区分页面与源站范围，并使用明确的阈值分类。
3. **分配分析任务。** 在环境支持时，现场数据和实验室角色并行处理。实施角色把发现转为建议，复核角色对照证据检查报告。其他环境可顺序执行相同步骤。
4. **交付报告。** 汇总可用指标，按影响、置信度和风险排列最多三项行动。说明修改位置、验证方法和适用时的回滚方式。

| 子代理 | 职责 |
| --- | --- |
| `psi-field` | 按设备和范围解读 CrUX 的 LCP、INP 和 CLS。 |
| `psi-lab` | 检查 Lighthouse，并将问题定位到资源、元素或审计项。 |
| `psi-implementation` | 按平台提出具体更改并说明如何验证。 |
| `psi-review` | 识别缺乏证据的陈述、重复计算的收益和无效比较。 |

## 测试

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖指标标准化、URL 验证、拦截页面检测，以及 Codex 和 Claude 子代理的一致性。`tests/fixtures/` 中的用例数据是**合成数据**，复现 API v5 的结构，不是实际测量。修改子代理指令时，请同时更新 `.md` 和 `.toml`。一致性测试会报告差异。

## 适用范围

PageSpeed 必须能访问公开页面。遇到登录、拦截或意外重定向时，报告会注明未测量的内容。CrUX 数据不足时，会标记缺失的指标。审查默认只给出建议。修改网站需要另行请求。

[PageSpeed Insights 方法说明](https://developers.google.com/speed/docs/insights/v5/about) · [官方 API](https://developers.google.com/speed/docs/insights/v5/get-started)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。允许使用、修改和重新分发，包括商业用途，但须在副本或实质部分中保留版权声明和许可证文本。

作者为 [Lulu (@lulubumps)](https://github.com/lulubumps)。
