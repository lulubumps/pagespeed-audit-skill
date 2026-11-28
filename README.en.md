<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="PageSpeed Audit icon">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><a href="README.md">Español</a> · <strong>English</strong> · <a href="README.pt.md">Português</a> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.hi.md">हिन्दी</a></p>

**Turn a PageSpeed report into three improvements you can make to your site.**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#how-it-works)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#run-the-script-directly)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#macos-and-linux-compatibility)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#macos-and-linux-compatibility)

[Installation](#installation) · [Usage examples](#usage) · [How it works](#how-it-works) · [Tests](#tests)

`pagespeed-audit` is a skill for **ChatGPT**, **Codex** and **Claude** that turns Google PageSpeed Insights (PSI) results into a short report with up to three priority improvements. Use it to diagnose slow pages, decide what to change in a template or settings, and compare performance before and after a deployment.

It works with public HTTP(S) sites, including WordPress, WooCommerce, Shopify, static sites and client- or server-rendered apps. Start with a public URL, a shared report, screenshots or PSI JSON.

All four environments use the same instructions. Codex loads them from `.agents/skills/`, Claude Code accesses them through a symlink in `.claude/skills/`, and the web interfaces accept uploads when the account has that feature.

## What's included

| Component | Purpose |
| --- | --- |
| `SKILL.md` | Instructions for gathering evidence, diagnosing issues and delivering the report. |
| `scripts/psi.py` | Measures through the official API, normalizes JSON and compares versions. Uses only the Python 3 standard library. |
| `references/` | Measurement rules, thresholds, platform-specific diagnostics including WordPress and WooCommerce, roles and report format. |
| Four subagents | Read-only `psi-field`, `psi-lab`, `psi-implementation` and `psi-review` in `.codex/agents/` for Codex and `.claude/agents/` for Claude Code. |
| Full audit in Claude (New) | `CLAUDE.md` and `.claude/pagespeed/`: complete report, measurement of all four Lighthouse categories and platform diagnostics. It is the counterpart of the Codex extension. |
| Four additional subagents (New) | `psi-scope`, `psi-cms`, `psi-third-party` and `psi-regression`, in `.claude/agents/`. They are read-only too. |

## macOS and Linux compatibility

| How you want to use the skill | Requirements on macOS and Linux |
| --- | --- |
| ChatGPT or Claude.ai in a browser | Permission to upload skills and a prepared ZIP. If you already have the ZIP, you can upload it without installing Git or Python locally. |
| Codex CLI or Claude Code | Git to clone the project and your chosen terminal client. |
| Build the ZIP, run `psi.py` or run tests | Python 3 and its standard library. No `pip` packages are required. Measuring a new URL with `psi.py fetch` also requires access to the PageSpeed Insights API. |

Run the commands in Terminal on macOS or in a Linux terminal with Bash or Zsh. Run the version checks for the tools you need.

```bash
git --version
python3 --version
codex --version
claude --version
```

Install your terminal client using the [official Codex CLI instructions](https://learn.chatgpt.com/docs/codex/cli) or the [Claude Code installation guide](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code).

Git preserves the Claude Code symlink on macOS and Linux when the file system supports symlinks. If it is missing, use a copy of the shared directory as described under Claude Code.

The test suite ran on Linux. The local workflow on macOS is pending verification.

## Installation

| Environment | Install | Invoke |
| --- | --- | --- |
| ChatGPT | Upload the skill under **Plugins → Skills** if your account allows it. | “Use the pagespeed-audit skill…” |
| Codex | Open the repository as a project. | `$pagespeed-audit` |
| Claude.ai | Upload the ZIP under **Customize → Skills**. | “Use the pagespeed-audit skill…” |
| Claude Code | Open the repository as a project. | `/pagespeed-audit` |

### Prepare the ZIP for web interfaces

Clone the repository and run the packager with Python 3. On Windows, use `py -3 tools/build_claude_zip.py` if `python3` is unavailable.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

Upload `dist/pagespeed-audit.zip`. It contains `SKILL.md`, the references and the script. Open the project in Codex or Claude Code to use the four repository subagents. The web interfaces can run the workflow sequentially.

### ChatGPT

1. In the sidebar, open **Plugins → Skills → Create → Upload from your computer**.
2. Select `dist/pagespeed-audit.zip` and wait for the upload review to finish.
3. In a new chat, ask “Use pagespeed-audit to review my site on mobile and desktop” and add a public URL or attach the PSI report.

Uploading depends on access to Skills and workspace permissions. If the menu is missing, use Codex or attach a PSI report and request the analysis directly in chat. See the [official ChatGPT Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

### Codex

You need Git and a Codex environment that supports [skills](https://learn.chatgpt.com/docs/build-skills). To use the four specialists, it must also support [project subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

Invoke `$pagespeed-audit`. Codex loads the skill from `.agents/skills/pagespeed-audit/` and the agents from `.codex/agents/`.

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

Claude Code loads the skill from `.claude/skills/pagespeed-audit/` and the subagents from `.claude/agents/`. Ask in your own words, such as “Check the speed of https://example.com/ on mobile and desktop”, or use `/pagespeed-audit`.

> If the symlink is missing, place a full copy of `.agents/skills/pagespeed-audit/` at `.claude/skills/pagespeed-audit/`. This also works on Windows if Git did not create the link.

### Claude.ai

1. Enable code execution and file creation under **Settings → Capabilities** if your account shows the option. In a managed workspace, check that the organization policy allows skills.
2. Open **Customize → Skills → + → Create skill → Upload a skill**.
3. Select `dist/pagespeed-audit.zip`, enable the skill and ask for it by name in a conversation.

See the [official Claude Skills guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### If the chat cannot measure the URL

In ChatGPT and Claude.ai, automatic measurements depend on access to Google PageSpeed Insights. If the request fails, run the test in [PageSpeed Insights](https://pagespeed.web.dev/) and share the link, mobile and desktop screenshots or JSON. `summarize` processes JSON files. Links and screenshots are analyzed using the visible evidence.

### Add it to another project

1. Copy the full `.agents/skills/pagespeed-audit/` directory to the same path in your project. For Claude Code, also create `.claude/skills/pagespeed-audit` as a copy or symlink.
2. To enable delegation, copy the four `psi-*.toml` files to `.codex/agents/` or the four `psi-*.md` files to `.claude/agents/`. Keep existing definitions and review any matching filenames before replacing them.
3. Launch the agent from the project root.

The skill has no extra dependencies. To test a new URL with the script, the environment needs PSI API access. Anonymous quota is limited. If you need a key, export it as an environment variable and keep it out of the repository.

```bash
export PAGESPEED_API_KEY="..."
```

The script sends the key to Google in the `X-Goog-Api-Key` header. Keep it out of chats and shared reports.

## Usage

**Audit a URL**

> Use pagespeed-audit to review https://example.com/ on mobile and desktop. Give me a short report with the top improvements, where to make them and how to verify them.

**Analyze an existing report**

> Use pagespeed-audit with this PageSpeed JSON. The site runs on WordPress. Propose reversible changes and explain what evidence is missing if a cause cannot be confirmed.

**Compare a deployment**

> Compare these before-and-after reports for the same page and device. Tell me what changed, how the measurements differ and what still needs to be checked.

(In Codex, add `$` before the skill name: `$pagespeed-audit`.)

For a site-wide audit, provide public URLs that represent the templates you want to test, such as a home page, article and product page.

### Run the script directly

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` detects common credential and internal-address patterns. Before measuring, check that the URL is public and contains no tokens, personal data or private identifiers. `summarize` and `compare` accept `--json` for structured output.

## How it works

1. **Gather evidence.** Reuse the PSI results you provide or measure the requested URLs. Record the device, date and final URL to detect redirects or block pages.
2. **Analyze performance.** Separate Chrome UX Report (CrUX) real-world visits when available from Lighthouse lab measurements. Distinguish page-level from origin-level data and classify metrics using explicit thresholds.
3. **Delegate analysis.** When supported, the field and lab roles work in parallel. Implementation turns findings into proposals and review checks the report against the evidence. Other environments run the same steps sequentially.
4. **Deliver the report.** Summarize available metrics and rank up to three actions by impact, confidence and risk. Specify where to make each change, how to verify it and how to roll it back when applicable.

| Subagent | Responsibility |
| --- | --- |
| `psi-field` | Interprets CrUX LCP, INP and CLS by device and scope. |
| `psi-lab` | Examines Lighthouse and ties issues to resources, elements or audits. |
| `psi-implementation` | Proposes platform-specific changes and verification steps. |
| `psi-review` | Flags unsupported claims, double-counted savings and invalid comparisons. |
| `psi-scope` (New) | Proposes representative public URLs by template and device. |
| `psi-cms` (New) | Maps each finding to the platform layer that owns it: theme, component, app, plugin, editor or CDN. |
| `psi-third-party` (New) | Attributes the cost of third-party scripts, embeds and tags to their integration. |
| `psi-regression` (New) | Compares equivalent pages, devices and settings after a deployment. |

## Full audit in Claude (New)

Besides the short report with three improvements, Claude can deliver a full audit: a prioritized summary followed by every evidenced finding across the four Lighthouse categories (performance, accessibility, best practices and SEO). It keeps audit IDs and marks manual checks, errors and coverage gaps. It is the Claude counterpart of the extension that already exists for Codex (`AGENTS.md` and `.codex/pagespeed/`).

| Environment | How it is activated |
| --- | --- |
| Claude Code | `CLAUDE.md` loads when you open the repository as a project. It turns on the full mode when you ask for a complete audit, platform-specific recommendations or deployment verification. |
| Claude.ai | Run `python3 tools/build_claude_zip.py --full`, upload `dist/pagespeed-audit-full.zip` and ask “Use the pagespeed-audit skill in full audit mode…”. The web has no subagents: Claude follows the roles in sequence. |

**Example**

> Use pagespeed-audit to run a full audit of https://example.com/ on mobile and desktop. I want every category, findings grouped by cause with their audit IDs, and steps specific to my platform.

The platform guidance covers Shopify, WordPress and WooCommerce, Drupal, Joomla, Wix, Squarespace, Webflow, Adobe Commerce, PrestaShop and headless CMS. Each recommendation names who owns the change, how to verify it and how to revert it.

### The full audit script

```bash
python3 .claude/pagespeed/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .claude/pagespeed/scripts/psi.py summarize psi-reports/*.json
python3 .claude/pagespeed/scripts/psi.py compare antes.json despues.json
```

This script requests all four categories, does not cap the number of findings and reports manual or errored audits as pending checks. The script in `.agents/skills/pagespeed-audit/scripts/psi.py` still measures performance only. With `--full`, the ZIP ships this script as `scripts/psi_full.py`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests cover metric normalization, URL validation, detection of blocked pages and parity between Codex and Claude subagents. The fixtures in `tests/fixtures/` are **synthetic** and reproduce the v5 API structure without using real measurements. When changing a subagent, update its `.md` and `.toml` together. The parity test detects differences. (New) `tests/test_claude_psi.py` checks that the script covers all four categories, that the eight Claude subagents are read-only, that the four new ones match the Codex versions and that the full ZIP has no broken paths.

## Scope

PageSpeed needs access to the public page. If it hits a login, block or unexpected redirect, the report identifies what could not be measured. It flags metrics with insufficient CrUX data. The default audit delivers recommendations. Changes to a site require a separate request.

[PageSpeed Insights methodology](https://developers.google.com/speed/docs/insights/v5/about) · [Official API](https://developers.google.com/speed/docs/insights/v5/get-started)

## License

This project uses the [MIT License](LICENSE). You may use, modify and redistribute it, including commercially, provided you retain the copyright notice and license text in copies or substantial portions.

**Free download.** I distribute the official version of PageSpeed Audit for free in this repository. I do not sell it, and I keep developing it with no financial interest. If someone charged you for the skill itself, ask the seller for a refund. You can still reuse, modify and redistribute it under the MIT License.

**Report accuracy.** The skill is designed for AI assistants, which can make mistakes or misinterpret incomplete data. Check the conclusions against the original PageSpeed Insights report before making changes.

Created by [Lulu (@lulubumps)](https://github.com/lulubumps).
