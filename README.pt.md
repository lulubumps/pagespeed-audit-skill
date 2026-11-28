🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# Auditoria de desempenho com o Google PageSpeed Insights

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)

PageSpeed Audit é uma skill para ChatGPT, Codex e Claude. Ela transforma relatórios do PageSpeed em até três melhorias prioritárias, indicando onde aplicar cada mudança, como verificá-la e como revertê-la. Funciona com sites públicos HTTP(S), incluindo WordPress, WooCommerce, Shopify e sites estáticos.

## Instalação no macOS e no Linux

Use o Git para clonar o repositório e instale Codex CLI ou Claude Code se quiser trabalhar pelo terminal. Para gerar o ZIP, executar o script ou rodar os testes, use Python 3. O projeto usa a biblioteca padrão. Os testes foram executados no Linux. A execução local no macOS ainda precisa ser validada.

- **ChatGPT:** Gere o ZIP com os comandos abaixo e envie `dist/pagespeed-audit.zip` em **Plugins → Skills → Criar → Carregar do computador**. A opção depende da conta e das permissões do espaço de trabalho.
- **Claude.ai:** Habilite a execução de código e a criação de arquivos se necessário. Em **Customize → Skills → + → Create skill → Upload a skill**, envie o mesmo ZIP e ative a skill.
- **Codex CLI:** Execute `codex` na raiz do repositório e use `$pagespeed-audit`.
- **Claude Code:** Execute `claude` na raiz e use `/pagespeed-audit`. Se o link simbólico estiver ausente, copie `.agents/skills/pagespeed-audit/` para `.claude/skills/pagespeed-audit/`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

## Como usar e como funciona

> Use pagespeed-audit para avaliar https://example.com/ em dispositivos móveis e computadores. Indique as três melhorias prioritárias, onde aplicá-las e como verificá-las.

Envie uma URL pública, um link de relatório do PSI, capturas de tela ou JSON exportado. Para comparar uma implantação, use relatórios de antes e depois para a mesma URL e o mesmo dispositivo. Se o chat não tiver acesso ao Google, execute o PSI no navegador e envie os resultados.

A skill distingue os dados reais do CrUX das medições de laboratório do Lighthouse, registra a URL e o dispositivo testados e indica dados ausentes ou medições bloqueadas. Codex e Claude Code podem distribuir o trabalho entre quatro especialistas. O mesmo fluxo pode ser executado em sequência. As alterações precisam ser solicitadas separadamente.

## Script e licença

Execute os comandos abaixo na raiz do repositório. Novas medições exigem acesso à API do PSI. Se precisar de uma chave, configure `PAGESPEED_API_KEY` no ambiente. Use URLs públicas sem credenciais ou dados privados. Projeto sob a [licença MIT](LICENSE).

```bash
python3 .agents/skills/pagespeed-audit/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .agents/skills/pagespeed-audit/scripts/psi.py summarize psi-reports/*.json
python3 .agents/skills/pagespeed-audit/scripts/psi.py compare before.json after.json
python3 -m unittest discover -s tests -v
```

[Lulu (@lulubumps)](https://github.com/lulubumps) · [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about)
