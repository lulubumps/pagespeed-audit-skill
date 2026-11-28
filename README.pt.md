<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícone do PageSpeed Audit">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><a href="README.md">Español</a> · <a href="README.en.md">English</a> · <strong>Português</strong> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.hi.md">हिन्दी</a></p>

**Transforme um relatório do PageSpeed em três melhorias que você pode aplicar no seu site.**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#como-funciona)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#executar-o-script-diretamente)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#compatibilidade-com-macos-e-linux)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#compatibilidade-com-macos-e-linux)

[Instalação](#instalação) · [Exemplos de uso](#como-usar) · [Como funciona](#como-funciona) · [Testes](#testes)

`pagespeed-audit` é uma skill para **ChatGPT**, **Codex** e **Claude** que transforma resultados do Google PageSpeed Insights (PSI) em um relatório breve com até três melhorias prioritárias. Use-a para diagnosticar páginas lentas, decidir o que alterar em um modelo ou configuração e comparar o desempenho antes e depois de uma implantação.

Funciona com sites públicos HTTP(S), incluindo WordPress, WooCommerce, Shopify, sites estáticos e aplicativos com renderização no cliente ou servidor. Aceita URL pública, relatório compartilhado, capturas de tela ou JSON do PSI.

Os quatro ambientes usam as mesmas instruções. Codex as carrega de `.agents/skills/`, Claude Code usa um link simbólico em `.claude/skills/` e as interfaces web aceitam o envio quando a conta tem acesso ao recurso.

## O que está incluído

| Componente | Finalidade |
| --- | --- |
| `SKILL.md` | Instruções para reunir evidências, diagnosticar problemas e entregar o relatório. |
| `scripts/psi.py` | Mede pela API oficial, normaliza JSON e compara versões. Usa apenas a biblioteca padrão do Python 3. |
| `references/` | Regras de medição, limites, diagnóstico por plataforma, incluindo WordPress e WooCommerce, funções e formato do relatório. |
| Quatro subagentes | `psi-field`, `psi-lab`, `psi-implementation` e `psi-review`, somente leitura, em `.codex/agents/` e `.claude/agents/`. |
| Auditoria completa no Claude (Novo) | `CLAUDE.md` e `.claude/pagespeed/`: relatório completo, medição das quatro categorias do Lighthouse e diagnóstico por plataforma. É o equivalente da extensão do Codex. |
| Quatro subagentes adicionais (Novo) | `psi-scope`, `psi-cms`, `psi-third-party` e `psi-regression`, em `.claude/agents/`. Também são somente leitura. |

## Compatibilidade com macOS e Linux

| Forma de uso | Requisitos no macOS e no Linux |
| --- | --- |
| ChatGPT ou Claude.ai no navegador | Permissão para enviar skills e o ZIP preparado. Se já tiver o ZIP, pode enviá-lo sem instalar Git ou Python localmente. |
| Codex CLI ou Claude Code | Git para clonar o projeto e o cliente de terminal escolhido. |
| Gerar o ZIP, executar `psi.py` ou rodar testes | Python 3 e sua biblioteca padrão. Não é necessário instalar pacotes via `pip`. Medir uma nova URL com `psi.py fetch` também requer acesso à API do PageSpeed Insights. |

Execute os comandos no Terminal do macOS ou em um terminal Linux com Bash ou Zsh. Verifique as versões das ferramentas que vai usar.

```bash
git --version
python3 --version
codex --version
claude --version
```

Para instalar o cliente de terminal, consulte a [documentação do Codex CLI](https://learn.chatgpt.com/docs/codex/cli) ou o [guia do Claude Code](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code).

O Git preserva o link simbólico do Claude Code em macOS e Linux quando o sistema de arquivos oferece suporte. Se o link estiver ausente, use uma cópia da pasta compartilhada, conforme a seção do Claude Code.

A suíte de testes foi executada no Linux. O fluxo local no macOS ainda precisa ser validado.

## Instalação

| Ambiente | Como instalar | Como invocar |
| --- | --- | --- |
| ChatGPT | Envie a skill em **Plugins → Skills** se sua conta permitir. | “Use a skill pagespeed-audit…” |
| Codex | Abra o repositório como projeto. | `$pagespeed-audit` |
| Claude.ai | Envie o ZIP em **Customize → Skills**. | “Use a skill pagespeed-audit…” |
| Claude Code | Abra o repositório como projeto. | `/pagespeed-audit` |

### Preparar o ZIP para interfaces web

Clone o repositório e execute o empacotador com Python 3. No Windows, se `python3` não estiver disponível, use `py -3 tools/build_claude_zip.py`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

Envie `dist/pagespeed-audit.zip`. Ele contém `SKILL.md`, as referências e o script. Abra o projeto no Codex ou Claude Code para usar os quatro subagentes do repositório. As interfaces web podem executar o fluxo em sequência.

### ChatGPT

1. Na barra lateral, abra **Plugins → Skills → Criar → Carregar do computador**.
2. Selecione `dist/pagespeed-audit.zip` e aguarde a revisão do envio.
3. Em uma nova conversa, peça “Use pagespeed-audit para avaliar meu site em dispositivos móveis e computadores” e informe a URL pública ou anexe o relatório do PSI.

O envio depende do acesso a Skills e das permissões do espaço de trabalho. Se o menu não aparecer, use Codex ou anexe o relatório do PSI e peça a análise no chat. Consulte o [guia oficial do ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

### Codex

Você precisa de Git e de um ambiente Codex que aceite [skills](https://learn.chatgpt.com/docs/build-skills). Para usar os quatro especialistas, o ambiente precisa aceitar [subagentes de projeto](https://learn.chatgpt.com/docs/agent-configuration/subagents).

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

Use `$pagespeed-audit`. O Codex carrega a skill de `.agents/skills/pagespeed-audit/` e os subagentes de `.codex/agents/`.

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

Claude Code carrega a skill de `.claude/skills/pagespeed-audit/` e os subagentes de `.claude/agents/`. Faça o pedido com suas palavras, por exemplo “Avalie a velocidade de https://example.com/ no celular e no computador”, ou use `/pagespeed-audit`.

> Se o link simbólico estiver ausente, coloque uma cópia completa de `.agents/skills/pagespeed-audit/` em `.claude/skills/pagespeed-audit/`. Essa alternativa também vale no Windows quando o Git não cria o link.

### Claude.ai

1. Ative a execução de código e a criação de arquivos em **Settings → Capabilities** se a opção aparecer. Em um espaço gerenciado, verifique se a política da organização permite skills.
2. Abra **Customize → Skills → + → Create skill → Upload a skill**.
3. Selecione `dist/pagespeed-audit.zip`, ative a skill e peça por ela pelo nome em uma conversa.

Consulte o [guia oficial do Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Quando o chat não consegue medir a URL

No ChatGPT e no Claude.ai, a medição automática depende do acesso ao Google PageSpeed Insights. Se falhar, execute o teste no [PageSpeed Insights](https://pagespeed.web.dev/) e compartilhe o link, as capturas de celular e computador ou o JSON. `summarize` processa arquivos JSON. Links e capturas são analisados com as evidências visíveis.

### Adicionar a outro projeto

1. Copie a pasta completa `.agents/skills/pagespeed-audit/` para o mesmo caminho no projeto. Para Claude Code, crie também `.claude/skills/pagespeed-audit` como cópia ou link simbólico.
2. Para delegar, copie os quatro arquivos `psi-*.toml` para `.codex/agents/` ou os quatro `psi-*.md` para `.claude/agents/`. Preserve as definições existentes e revise nomes coincidentes antes de substituí-los.
3. Abra o agente a partir da raiz do projeto.

A skill não tem dependências adicionais. Para medir uma URL nova com o script, é preciso acessar a API do PSI. A cota anônima é limitada. Se precisar de uma chave, exporte-a como variável de ambiente e mantenha-a fora do repositório.

```bash
export PAGESPEED_API_KEY="..."
```

O script envia a chave ao Google no cabeçalho `X-Goog-Api-Key`. Evite incluí-la em conversas ou relatórios compartilhados.

## Como usar

**Auditar uma URL**

> Use pagespeed-audit para avaliar https://example.com/ no celular e no computador. Dê um relatório breve com as melhorias prioritárias, onde aplicá-las e como verificá-las.

**Analisar um relatório existente**

> Use pagespeed-audit com este JSON do PageSpeed. O site usa WordPress. Proponha mudanças reversíveis e indique quais evidências faltam se não for possível confirmar uma causa.

**Comparar uma implantação**

> Compare os relatórios de antes e depois para a mesma página e o mesmo dispositivo. Mostre as mudanças observadas, as diferenças nas medições e o que falta verificar.

(No Codex, use `$` antes do nome da skill: `$pagespeed-audit`.)

Para auditar o site inteiro, forneça URLs públicas representativas dos modelos a testar, como página inicial, artigo e produto.

### Executar o script diretamente

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` detecta padrões comuns de credenciais e endereços internos. Antes de medir, confira se a URL é pública e não contém tokens, dados pessoais ou identificadores privados. `summarize` e `compare` aceitam `--json` para saída estruturada.

## Como funciona

1. **Reúne evidências.** Reutiliza os resultados do PSI enviados ou mede as URLs solicitadas. Registra dispositivo, data e URL final para detectar redirecionamentos ou bloqueios.
2. **Analisa o desempenho.** Separa dados de visitas reais do Chrome UX Report (CrUX), quando disponíveis, das medições de laboratório do Lighthouse. Distingue página e origem e classifica métricas com limites explícitos.
3. **Distribui a análise.** Quando possível, campo e laboratório trabalham em paralelo. A implementação transforma achados em propostas e a revisão confere o relatório com as evidências. Nos demais ambientes, as etapas seguem em sequência.
4. **Entrega o relatório.** Resume as métricas e prioriza até três ações por impacto, confiança e risco. Indica onde aplicar, como verificar e como reverter quando necessário.

| Subagente | Responsabilidade |
| --- | --- |
| `psi-field` | Interpreta LCP, INP e CLS do CrUX por dispositivo e escopo. |
| `psi-lab` | Analisa Lighthouse e associa problemas a recursos, elementos ou auditorias. |
| `psi-implementation` | Propõe mudanças concretas por plataforma e como verificá-las. |
| `psi-review` | Detecta alegações sem evidência, ganhos contados duas vezes e comparações inválidas. |
| `psi-scope` (Novo) | Propõe URLs públicas representativas por modelo de página e dispositivo. |
| `psi-cms` (Novo) | Associa cada achado à camada responsável da plataforma: tema, componente, app, plugin, editor ou CDN. |
| `psi-third-party` (Novo) | Atribui o custo de scripts, embeds e tags de terceiros à sua integração. |
| `psi-regression` (Novo) | Compara páginas, dispositivos e configurações equivalentes após uma implantação. |

## Auditoria completa no Claude (Novo)

Além do relatório curto com três melhorias, o Claude pode entregar uma auditoria completa: um resumo priorizado seguido de todos os achados com evidência nas quatro categorias do Lighthouse (desempenho, acessibilidade, boas práticas e SEO). Mantém os identificadores das auditorias e sinaliza verificações manuais, erros e lacunas de cobertura. É o equivalente para o Claude da extensão que já existe para o Codex (`AGENTS.md` e `.codex/pagespeed/`).

| Ambiente | Como ativar |
| --- | --- |
| Claude Code | `CLAUDE.md` é carregado ao abrir o repositório como projeto. Ativa o modo completo quando você pede uma auditoria completa, recomendações por plataforma ou a verificação de uma implantação. |
| Claude.ai | Execute `python3 tools/build_claude_zip.py --full`, carregue `dist/pagespeed-audit-full.zip` e peça «Use a skill pagespeed-audit em modo de auditoria completa…». Na web não há subagentes: o Claude segue os papéis em sequência. |

**Exemplo**

> Use pagespeed-audit para fazer uma auditoria completa de https://example.com/ em celular e desktop. Quero todas as categorias, os achados agrupados por causa com seus IDs de auditoria e os passos específicos para a minha plataforma.

A orientação por plataforma cobre Shopify, WordPress e WooCommerce, Drupal, Joomla, Wix, Squarespace, Webflow, Adobe Commerce, PrestaShop e CMS headless. Cada recomendação indica quem é responsável pela mudança, como verificá-la e como revertê-la.

### O script da auditoria completa

```bash
python3 .claude/pagespeed/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .claude/pagespeed/scripts/psi.py summarize psi-reports/*.json
python3 .claude/pagespeed/scripts/psi.py compare antes.json despues.json
```

Este script solicita as quatro categorias, não limita o número de achados e informa as auditorias manuais ou com erro como verificações pendentes. O script de `.agents/skills/pagespeed-audit/scripts/psi.py` continua medindo apenas desempenho. Com `--full`, o ZIP inclui este script como `scripts/psi_full.py`.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem normalização de métricas, validação de URLs, páginas bloqueadas e paridade entre os subagentes de Codex e Claude. Os arquivos em `tests/fixtures/` são **sintéticos** e reproduzem a estrutura da API v5. Ao mudar um subagente, atualize seu `.md` e `.toml` juntos. O teste de paridade identifica divergências. (Novo) `tests/test_claude_psi.py` verifica se o script cobre as quatro categorias, se os oito subagentes do Claude são somente leitura, se os quatro novos coincidem com os do Codex e se o ZIP completo não tem caminhos quebrados.

## Escopo

O PageSpeed precisa acessar a página pública. Se encontrar login, bloqueio ou redirecionamento inesperado, o relatório informa o que ficou sem medir. Se faltarem dados CrUX, indica as métricas indisponíveis. A auditoria entrega recomendações por padrão. Alterações no site exigem um pedido separado.

[Metodologia do PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) · [API oficial](https://developers.google.com/speed/docs/insights/v5/get-started)

## Licença

O projeto é distribuído sob a [licença MIT](LICENSE). Você pode usá-lo, modificá-lo e redistribuí-lo, inclusive comercialmente, preservando o aviso de direitos autorais e o texto da licença nas cópias ou partes substanciais.

Criado por [Lulu (@lulubumps)](https://github.com/lulubumps).
