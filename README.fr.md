🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# Audit de performance avec Google PageSpeed Insights

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)

PageSpeed Audit est une compétence pour ChatGPT, Codex et Claude. Elle transforme les rapports PageSpeed en trois améliorations prioritaires au maximum, avec l’emplacement de chaque modification, la méthode de vérification et la procédure de retour en arrière. Elle prend en charge les sites publics HTTP(S), dont WordPress, WooCommerce, Shopify et les sites statiques.

## Installation sur macOS et Linux

Utilisez Git pour cloner le dépôt. Installez Codex CLI ou Claude Code pour travailler dans le terminal. Python 3 est requis pour générer le ZIP, exécuter le script ou lancer les tests. Le projet utilise la bibliothèque standard. Les tests ont été exécutés sous Linux. L’exécution locale sous macOS reste à vérifier.

- **ChatGPT** — Générez le ZIP avec les commandes ci-dessous, puis importez `dist/pagespeed-audit.zip` dans **Plugins → Compétences → Créer → Importer depuis votre ordinateur**. L’option dépend de votre compte et des autorisations de votre espace de travail.
- **Claude.ai** — Activez l’exécution de code et la création de fichiers si nécessaire. Dans **Customize → Skills → + → Create skill → Upload a skill**, importez le même ZIP et activez la compétence.
- **Codex CLI** — Lancez `codex` à la racine du dépôt et invoquez `$pagespeed-audit`.
- **Claude Code** — Lancez `claude` à la racine et invoquez `/pagespeed-audit`. Si le lien symbolique manque, copiez `.agents/skills/pagespeed-audit/` vers `.claude/skills/pagespeed-audit/`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

## Utilisation et fonctionnement

> Utilise pagespeed-audit pour auditer https://example.com/ sur mobile et ordinateur. Donne-moi les trois améliorations prioritaires, où les appliquer et comment les vérifier.

Fournissez une URL publique, un lien de rapport PSI, des captures ou un export JSON. Pour évaluer un déploiement, comparez des rapports avant et après pour la même URL et le même type d’appareil. Si le chat ne peut pas joindre Google, lancez PSI dans votre navigateur et partagez les résultats.

La compétence distingue les données réelles CrUX des mesures de laboratoire Lighthouse, indique l’URL et l’appareil testés et signale les données manquantes ou les mesures bloquées. Codex et Claude Code peuvent déléguer l’analyse à quatre spécialistes. Le même processus fonctionne aussi en séquence. L’application des changements fait l’objet d’une demande distincte.

## Script et licence

Exécutez les commandes ci-dessous à la racine du dépôt. Les nouvelles mesures nécessitent un accès à l’API PSI. Si une clé est nécessaire, définissez `PAGESPEED_API_KEY` dans votre environnement. Utilisez des URL publiques sans identifiants ni données privées. Projet sous [licence MIT](LICENSE).

```bash
python3 .agents/skills/pagespeed-audit/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .agents/skills/pagespeed-audit/scripts/psi.py summarize psi-reports/*.json
python3 .agents/skills/pagespeed-audit/scripts/psi.py compare before.json after.json
python3 -m unittest discover -s tests -v
```

[Lulu (@lulubumps)](https://github.com/lulubumps) · [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about)
