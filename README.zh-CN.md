🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# 使用 Google PageSpeed Insights 审查网站性能

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)

PageSpeed Audit 是适用于 ChatGPT、Codex 和 Claude 的技能。它根据 PageSpeed 报告给出最多三条优先建议，并说明修改位置、验证方式和回滚方法。适用于公开的 HTTP(S) 网站，包括 WordPress、WooCommerce、Shopify 和静态站点。

## 在 macOS 和 Linux 上安装

使用 Git 克隆仓库。在终端使用时，请安装 Codex CLI 或 Claude Code。生成 ZIP、运行脚本或执行测试需要 Python 3。项目只使用 Python 标准库。测试已在 Linux 上运行，macOS 的本地流程仍待验证。

- **ChatGPT**：使用下方命令生成 ZIP，然后在 **插件 → 技能 → 创建 → 从电脑上传** 中选择 `dist/pagespeed-audit.zip`。此选项取决于账户和工作区权限。
- **Claude.ai**：如有需要，启用代码执行和文件创建。在 **Customize → Skills → + → Create skill → Upload a skill** 中上传同一个 ZIP 并启用技能。
- **Codex CLI**：在克隆后的仓库根目录运行 `codex`，然后调用 `$pagespeed-audit`。
- **Claude Code**：在仓库根目录运行 `claude`，然后调用 `/pagespeed-audit`。如果缺少符号链接，请将 `.agents/skills/pagespeed-audit/` 复制到 `.claude/skills/pagespeed-audit/`。

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

## 使用方法和工作流程

> 用 pagespeed-audit 检查 https://example.com/ 在移动端和桌面端的性能，并说明最优先的三项改进、修改位置和验证方法。

你可以提供公开 URL、PSI 报告链接、截图或导出的 JSON。比较部署效果时，请提供同一 URL 和设备类型的前后报告。如果聊天环境无法访问 Google，请在浏览器中运行 PSI 并分享结果。

技能分别解读 CrUX 的真实用户数据和 Lighthouse 的实验室数据，记录测试的 URL 和设备，并标明缺失的数据或受阻的测试。在 Codex 和 Claude Code 中，四个子代理可分别负责真实用户数据、实验室诊断、实施建议和报告复核。同一流程也可以顺序执行。应用修改需要单独提出请求。

## 命令行和许可证

在仓库根目录执行下方命令。运行新的测量需要访问 PSI API。如需 API 密钥，请设置环境变量 `PAGESPEED_API_KEY`。请使用不含凭据或私密信息的公开 URL。项目采用 [MIT 许可证](LICENSE)。

```bash
python3 .agents/skills/pagespeed-audit/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .agents/skills/pagespeed-audit/scripts/psi.py summarize psi-reports/*.json
python3 .agents/skills/pagespeed-audit/scripts/psi.py compare before.json after.json
python3 -m unittest discover -s tests -v
```

[Lulu (@lulubumps)](https://github.com/lulubumps) · [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about)
