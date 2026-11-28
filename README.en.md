🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# Website performance audit with Google PageSpeed Insights

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)

PageSpeed Audit is a skill for ChatGPT, Codex and Claude. It turns PageSpeed reports into up to three prioritized recommendations, with where to make each change, how to verify it and how to roll it back. It works with public HTTP(S) sites, including WordPress, WooCommerce, Shopify and static sites.

## Installation on macOS and Linux

Install Git to clone the repository. Install Codex CLI or Claude Code for terminal use. Python 3 is required to build the web upload package, run the helper or run tests. It uses the standard library. The test suite was run on Linux. Local execution on macOS has yet to be verified.

- **ChatGPT:** Build the ZIP using the commands below. In **Plugins → Skills → Create → Upload from your computer**, select `dist/pagespeed-audit.zip`. Availability depends on your account and workspace permissions.
- **Claude.ai:** Enable code execution and file creation if required. Open **Customize → Skills → + → Create skill → Upload a skill**, upload the same ZIP and enable the skill.
- **Codex CLI:** Run `codex` from the cloned repository and invoke `$pagespeed-audit`.
- **Claude Code:** Run `claude` from the repository and invoke `/pagespeed-audit`. If the Git symlink is missing, copy `.agents/skills/pagespeed-audit/` to `.claude/skills/pagespeed-audit/`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

## Usage and workflow

> Use pagespeed-audit to audit https://example.com/ on mobile and desktop. Give me the three highest-priority changes, where to make them and how to verify them.

You can supply a public URL, a PSI report link, screenshots or exported JSON. To compare a deployment, supply before and after reports for the same URL and device. If the chat cannot reach Google, run PSI in your browser and share the results.

The skill separates CrUX real-user metrics from Lighthouse lab results, records the tested URL and device, and flags missing data and blocked runs. Codex and Claude Code can delegate to four specialists for field data, lab diagnostics, implementation and evidence review. The same steps can run sequentially. An audit proposes changes. Applying them requires a separate request.

## CLI and license

Run the helper commands below from the repository root. Live measurements require access to the PSI API. If you need a key, set `PAGESPEED_API_KEY` in your environment. Use public URLs without credentials or private data. Released under the [MIT License](LICENSE).

```bash
python3 .agents/skills/pagespeed-audit/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .agents/skills/pagespeed-audit/scripts/psi.py summarize psi-reports/*.json
python3 .agents/skills/pagespeed-audit/scripts/psi.py compare before.json after.json
python3 -m unittest discover -s tests -v
```

[Lulu (@lulubumps)](https://github.com/lulubumps) · [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about)
