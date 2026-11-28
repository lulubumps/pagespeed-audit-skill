<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Icône de PageSpeed Audit">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><a href="README.md">Español</a> · <a href="README.en.md">English</a> · <a href="README.pt.md">Português</a> · <strong>Français</strong> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.hi.md">हिन्दी</a></p>

**Transformez un rapport PageSpeed en trois améliorations à appliquer à votre site.**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#fonctionnement)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#exécuter-directement-le-script)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#compatibilité-avec-macos-et-linux)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#compatibilité-avec-macos-et-linux)

[Installation](#installation) · [Exemples d’utilisation](#utilisation) · [Fonctionnement](#fonctionnement) · [Tests](#tests)

`pagespeed-audit` est une compétence pour **ChatGPT**, **Codex** et **Claude**. Elle transforme les résultats de Google PageSpeed Insights (PSI) en un rapport court avec trois améliorations prioritaires au maximum. Elle aide à diagnostiquer les pages lentes, à choisir les réglages ou modèles à modifier et à comparer les performances avant et après un déploiement.

Elle fonctionne avec les sites publics HTTP(S), notamment WordPress, WooCommerce, Shopify, les sites statiques et les applications rendues côté client ou serveur. Fournissez une URL publique, un rapport partagé, des captures ou un JSON PSI.

Les quatre environnements utilisent les mêmes instructions. Codex les charge depuis `.agents/skills/`, Claude Code y accède via un lien symbolique dans `.claude/skills/` et les interfaces web acceptent l’import si le compte dispose de cette fonctionnalité.

## Contenu du projet

| Élément | Rôle |
| --- | --- |
| `SKILL.md` | Instructions pour collecter les preuves, diagnostiquer les problèmes et produire le rapport. |
| `scripts/psi.py` | Mesure via l’API officielle, normalise le JSON et compare les versions. Utilise uniquement la bibliothèque standard de Python 3. |
| `references/` | Règles de mesure, seuils, diagnostics par plateforme dont WordPress et WooCommerce, rôles et format du rapport. |
| Quatre sous-agents | `psi-field`, `psi-lab`, `psi-implementation` et `psi-review`, en lecture seule, dans `.codex/agents/` et `.claude/agents/`. |
| Audit complet dans Claude (Nouveau) | `CLAUDE.md` et `.claude/pagespeed/` : rapport complet, mesure des quatre catégories Lighthouse et diagnostic par plateforme. C’est l’équivalent de l’extension Codex. |
| Quatre sous-agents supplémentaires (Nouveau) | `psi-scope`, `psi-cms`, `psi-third-party` et `psi-regression`, dans `.claude/agents/`. Ils sont aussi en lecture seule. |

## Compatibilité avec macOS et Linux

| Mode d’utilisation | Prérequis sur macOS et Linux |
| --- | --- |
| ChatGPT ou Claude.ai dans le navigateur | Un compte autorisé à importer des compétences et le ZIP préparé. Si vous avez déjà le ZIP, vous pouvez l’importer sans installer Git ni Python. |
| Codex CLI ou Claude Code | Git pour cloner le projet et le client de terminal choisi. |
| Générer le ZIP, exécuter `psi.py` ou lancer les tests | Python 3 et sa bibliothèque standard, sans installation via `pip`. Pour mesurer une nouvelle URL avec `psi.py fetch`, il faut également accéder à l’API PageSpeed Insights. |

Exécutez les commandes dans Terminal sous macOS ou dans un terminal Linux avec Bash ou Zsh. Vérifiez la version des outils dont vous avez besoin.

```bash
git --version
python3 --version
codex --version
claude --version
```

Consultez les [instructions officielles de Codex CLI](https://learn.chatgpt.com/docs/codex/cli) ou le [guide d’installation de Claude Code](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code).

Git préserve le lien symbolique de Claude Code sous macOS et Linux si le système de fichiers le permet. Si le lien est absent, utilisez une copie du dossier partagé, comme indiqué dans la section Claude Code.

La suite de tests a été exécutée sous Linux. Le fonctionnement local sous macOS reste à vérifier.

## Installation

| Environnement | Installation | Invocation |
| --- | --- | --- |
| ChatGPT | Importez la compétence dans **Plugins → Compétences** si votre compte le permet. | « Utilise la compétence pagespeed-audit… » |
| Codex | Ouvrez le dépôt comme projet. | `$pagespeed-audit` |
| Claude.ai | Importez le ZIP dans **Customize → Skills**. | « Utilise la compétence pagespeed-audit… » |
| Claude Code | Ouvrez le dépôt comme projet. | `/pagespeed-audit` |

### Préparer le ZIP pour les interfaces web

Clonez le dépôt et lancez l’empaquetage avec Python 3. Sous Windows, si `python3` est indisponible, utilisez `py -3 tools/build_claude_zip.py`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

Importez `dist/pagespeed-audit.zip`, qui contient `SKILL.md`, les références et le script. Pour utiliser les quatre sous-agents du dépôt, ouvrez le projet dans Codex ou Claude Code. Les interfaces web peuvent suivre le flux en séquence.

### ChatGPT

1. Dans la barre latérale, ouvrez **Plugins → Compétences → Créer → Importer depuis votre ordinateur**.
2. Sélectionnez `dist/pagespeed-audit.zip` et attendez la fin de la vérification.
3. Dans une nouvelle conversation, demandez « Utilise pagespeed-audit pour auditer mon site sur mobile et ordinateur » et ajoutez l’URL publique ou joignez le rapport PSI.

L’import dépend de l’accès aux compétences et des autorisations de l’espace de travail. Si le menu manque, utilisez Codex ou joignez un rapport PSI et demandez l’analyse directement dans le chat. Consultez le [guide officiel de ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

### Codex

Vous avez besoin de Git et d’un environnement Codex compatible avec les [compétences](https://learn.chatgpt.com/docs/build-skills). Pour utiliser les quatre spécialistes, il doit aussi prendre en charge les [sous-agents de projet](https://learn.chatgpt.com/docs/agent-configuration/subagents).

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

Invoquez `$pagespeed-audit`. Codex charge la compétence depuis `.agents/skills/pagespeed-audit/` et les sous-agents depuis `.codex/agents/`.

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

Claude Code charge la compétence depuis `.claude/skills/pagespeed-audit/` et les sous-agents depuis `.claude/agents/`. Demandez par exemple « Vérifie la vitesse de https://example.com/ sur mobile et ordinateur » ou invoquez `/pagespeed-audit`.

> Si le lien symbolique manque, placez une copie complète de `.agents/skills/pagespeed-audit/` dans `.claude/skills/pagespeed-audit/`. Cette solution fonctionne aussi sous Windows si Git ne crée pas le lien.

### Claude.ai

1. Activez l’exécution de code et la création de fichiers dans **Settings → Capabilities** si votre compte affiche l’option. Dans un espace administré, vérifiez que la politique de l’organisation autorise les compétences.
2. Ouvrez **Customize → Skills → + → Create skill → Upload a skill**.
3. Sélectionnez `dist/pagespeed-audit.zip`, activez la compétence et demandez-la par son nom dans une conversation.

Consultez le [guide officiel de Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Si le chat ne peut pas mesurer l’URL

Dans ChatGPT et Claude.ai, les mesures automatiques dépendent de l’accès à Google PageSpeed Insights. En cas d’échec, lancez le test dans [PageSpeed Insights](https://pagespeed.web.dev/) et partagez le lien, les captures mobile et ordinateur ou le JSON. `summarize` traite les fichiers JSON. Les liens et captures sont interprétés à partir des éléments visibles.

### Ajouter la compétence à un autre projet

1. Copiez le dossier complet `.agents/skills/pagespeed-audit/` au même emplacement dans votre projet. Pour Claude Code, créez aussi `.claude/skills/pagespeed-audit` comme copie ou lien symbolique.
2. Pour déléguer, copiez les quatre `psi-*.toml` vers `.codex/agents/` ou les quatre `psi-*.md` vers `.claude/agents/`. Conservez les définitions existantes et vérifiez les noms identiques avant tout remplacement.
3. Lancez l’agent depuis la racine du projet.

La compétence ne nécessite aucune dépendance supplémentaire. Le script doit accéder à l’API PSI pour mesurer une nouvelle URL. Le quota anonyme est limité. Si vous avez besoin d’une clé, exportez-la comme variable d’environnement et gardez-la hors du dépôt.

```bash
export PAGESPEED_API_KEY="..."
```

Le script transmet la clé à Google dans l’en-tête `X-Goog-Api-Key`. Évitez de l’inclure dans les conversations ou les rapports partagés.

## Utilisation

**Auditer une URL**

> Utilise pagespeed-audit pour vérifier https://example.com/ sur mobile et ordinateur. Donne un rapport court avec les améliorations prioritaires, où les appliquer et comment les vérifier.

**Analyser un rapport existant**

> Utilise pagespeed-audit avec ce JSON PageSpeed. Le site utilise WordPress. Propose des changements réversibles et précise les preuves qui manquent si une cause ne peut pas être confirmée.

**Comparer un déploiement**

> Compare ces rapports avant et après pour la même page et le même appareil. Indique les changements observés, les écarts de mesure et les points qui restent à vérifier.

(Dans Codex, préfixez le nom de la compétence par `$` : `$pagespeed-audit`.)

Pour un audit complet, fournissez des URL publiques représentant les modèles à tester, par exemple l’accueil, un article et une fiche produit.

### Exécuter directement le script

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` détecte les formes courantes d’identifiants et d’adresses internes. Avant toute mesure, vérifiez que l’URL est publique et qu’elle ne contient ni jeton, ni donnée personnelle, ni identifiant privé. `summarize` et `compare` acceptent `--json` pour une sortie structurée.

## Fonctionnement

1. **Collecte des preuves.** Réutilise les résultats PSI fournis ou mesure les URL demandées. Relève l’appareil, la date et l’URL finale pour détecter les redirections et blocages.
2. **Analyse des performances.** Sépare les visites réelles du Chrome UX Report (CrUX), lorsqu’elles sont disponibles, des mesures de laboratoire Lighthouse. Distingue les données de la page et de l’origine et classe les métriques selon des seuils explicites.
3. **Répartition du travail.** Si l’environnement le permet, les rôles terrain et laboratoire travaillent en parallèle. L’implémentation propose des modifications et la révision vérifie le rapport  à partir des preuves. Dans les autres environnements, les étapes s’enchaînent.
4. **Remise du rapport.** Résume les mesures disponibles et classe trois actions au maximum selon leur impact, le degré de confiance et le risque. Précise où intervenir, comment vérifier et comment revenir en arrière si nécessaire.

| Sous-agent | Responsabilité |
| --- | --- |
| `psi-field` | Interprète les mesures LCP, INP et CLS de CrUX selon l’appareil et le périmètre. |
| `psi-lab` | Analyse Lighthouse et relie les problèmes aux ressources, éléments ou audits. |
| `psi-implementation` | Propose des changements adaptés à la plateforme et explique comment les vérifier. |
| `psi-review` | Repère les affirmations sans preuve, les gains comptés deux fois et les comparaisons invalides. |
| `psi-scope` (Nouveau) | Propose des URL publiques représentatives par modèle de page et par appareil. |
| `psi-cms` (Nouveau) | Rattache chaque constat à la couche responsable de la plateforme : thème, composant, application, extension, éditeur ou CDN. |
| `psi-third-party` (Nouveau) | Attribue le coût des scripts, intégrations et balises tiers à leur intégration. |
| `psi-regression` (Nouveau) | Compare des pages, appareils et réglages équivalents après un déploiement. |

## Audit complet dans Claude (Nouveau)

En plus du rapport court avec trois améliorations, Claude peut remettre un audit complet : une synthèse priorisée suivie de tous les constats étayés dans les quatre catégories Lighthouse (performance, accessibilité, bonnes pratiques et SEO). Il conserve les identifiants d’audit et signale les vérifications manuelles, les erreurs et les lacunes de couverture. C’est l’équivalent pour Claude de l’extension qui existe déjà pour Codex (`AGENTS.md` et `.codex/pagespeed/`).

| Environnement | Activation |
| --- | --- |
| Claude Code | `CLAUDE.md` se charge à l’ouverture du dépôt comme projet. Il active le mode complet lorsque vous demandez un audit complet, des recommandations par plateforme ou la vérification d’un déploiement. |
| Claude.ai | Exécutez `python3 tools/build_claude_zip.py --full`, importez `dist/pagespeed-audit-full.zip` et demandez « Utilise la skill pagespeed-audit en mode audit complet… ». Le web n’a pas de sous-agents : Claude suit les rôles à la suite. |

**Exemple**

> Utilise pagespeed-audit pour faire un audit complet de https://example.com/ sur mobile et ordinateur. Je veux toutes les catégories, les constats regroupés par cause avec leurs identifiants d’audit et les étapes propres à ma plateforme.

Les consignes par plateforme couvrent Shopify, WordPress et WooCommerce, Drupal, Joomla, Wix, Squarespace, Webflow, Adobe Commerce, PrestaShop et les CMS headless. Chaque recommandation indique qui est responsable du changement, comment le vérifier et comment l’annuler.

### Le script de l’audit complet

```bash
python3 .claude/pagespeed/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .claude/pagespeed/scripts/psi.py summarize psi-reports/*.json
python3 .claude/pagespeed/scripts/psi.py compare antes.json despues.json
```

Ce script demande les quatre catégories, ne limite pas le nombre de constats et signale les audits manuels ou en erreur comme vérifications en attente. Le script `.agents/skills/pagespeed-audit/scripts/psi.py` continue de ne mesurer que la performance. Avec `--full`, le ZIP inclut ce script sous le nom `scripts/psi_full.py`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Les tests couvrent la normalisation des métriques, la validation des URL, le repérage des pages bloquées et la parité des sous-agents Codex et Claude. Les fichiers de `tests/fixtures/` sont **synthétiques** et reproduisent la structure de l’API v5. Si vous modifiez un sous-agent, actualisez ensemble son `.md` et son `.toml`. Le test de parité détecte les écarts. (Nouveau) `tests/test_claude_psi.py` vérifie que le script couvre les quatre catégories, que les huit sous-agents de Claude sont en lecture seule, que les quatre nouveaux correspondent à ceux de Codex et que le ZIP complet ne contient aucun chemin cassé.

## Périmètre

PageSpeed doit pouvoir accéder à la page publique. Une connexion, un blocage ou une redirection inattendue est signalé dans le rapport, avec ce qui n’a pas pu être mesuré. Les métriques CrUX insuffisantes sont indiquées. L’audit fournit des recommandations par défaut. Toute modification du site nécessite une demande distincte.

[Méthodologie PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) · [API officielle](https://developers.google.com/speed/docs/insights/v5/get-started)

## Licence

Ce projet est distribué sous [licence MIT](LICENSE). Vous pouvez l’utiliser, le modifier et le redistribuer, y compris à des fins commerciales, en conservant la mention de copyright et le texte de la licence dans les copies ou parties substantielles.

Créé par [Lulu (@lulubumps)](https://github.com/lulubumps).
