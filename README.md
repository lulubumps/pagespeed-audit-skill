🌐 [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [简体中文](README.zh-CN.md) · [हिन्दी](README.hi.md)

<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>

# Auditoría web con Google PageSpeed Insights

**De un informe de PageSpeed a tres mejoras que puedes aplicar en tu sitio.**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#cómo-funciona)
[![Licencia MIT](https://img.shields.io/badge/Licencia%20MIT-5B3CC4?style=for-the-badge)](LICENSE)

[![ChatGPT](https://img.shields.io/badge/ChatGPT-176B56?style=for-the-badge)](#chatgpt)
[![Codex](https://img.shields.io/badge/Codex-343541?style=for-the-badge)](#codex)
[![Claude](https://img.shields.io/badge/Claude-984425?style=for-the-badge&logo=claude&logoColor=white)](#claudeai)

[![Python 3](https://img.shields.io/badge/Python%203-306998?style=for-the-badge&logo=python&logoColor=white)](#el-script-por-sí-solo)
[![macOS](https://img.shields.io/badge/macOS-24292F?style=for-the-badge&logo=apple&logoColor=white)](#compatibilidad-con-macos-y-linux)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#compatibilidad-con-macos-y-linux)

[Instalación](#instalación) · [Ejemplos de uso](#cómo-se-usa) · [Cómo funciona](#cómo-funciona) · [Pruebas](#pruebas)

`pagespeed-audit` es una skill para **ChatGPT**, **Codex** y **Claude** que convierte los resultados de Google PageSpeed Insights (PSI) en un informe breve con hasta tres mejoras prioritarias. Sirve para diagnosticar páginas lentas, decidir qué cambiar en una plantilla o configuración y comparar el rendimiento antes y después de un despliegue.

Funciona con sitios públicos HTTP(S), incluidos WordPress, WooCommerce, Shopify, sitios estáticos y aplicaciones con renderizado en cliente o servidor. Puede partir de una URL pública, un informe compartido, capturas o un JSON de PSI.

La misma carpeta de instrucciones se usa en los cuatro entornos. Codex la carga desde `.agents/skills/`, Claude Code accede mediante un enlace simbólico en `.claude/skills/` y las interfaces web permiten cargar la skill cuando la cuenta tiene esa función habilitada.

## Qué incluye

| Pieza | Para qué sirve |
| --- | --- |
| `SKILL.md` | Instrucciones para recopilar evidencia, diagnosticar problemas y entregar el informe. |
| `scripts/psi.py` | Mide con la API oficial, normaliza el JSON y compara versiones. Solo librería estándar de Python 3. |
| `references/` | Reglas de medición, umbrales, diagnóstico por plataforma (con sección de WordPress y WooCommerce), roles y formato de informe. |
| Cuatro subagentes | `psi-field`, `psi-lab`, `psi-implementation` y `psi-review`, en `.codex/agents/` (Codex) y `.claude/agents/` (Claude Code). Son de solo lectura. |

## Compatibilidad con macOS y Linux

| Cómo quieres usar la skill | Requisitos en macOS y Linux |
| --- | --- |
| ChatGPT o Claude.ai en el navegador | Una cuenta con permiso para cargar skills y el ZIP preparado. Si ya tienes el ZIP, puedes cargarlo sin instalar Git ni Python en tu equipo. |
| Codex CLI o Claude Code | Git para clonar el proyecto y el cliente de terminal que vayas a usar. |
| Generar el ZIP, ejecutar `psi.py` o correr las pruebas | Python 3. El proyecto usa la biblioteca estándar y no requiere instalar paquetes con `pip`. Para medir una URL nueva con `psi.py fetch` también necesitas acceso a la API de PageSpeed Insights. |

Los comandos de esta guía se pueden ejecutar en Terminal en macOS o en una terminal de Linux con Bash o Zsh. Para comprobar las herramientas que necesitas, ejecuta los comandos correspondientes a tu caso.

```bash
git --version
python3 --version
codex --version   # Si usarás Codex CLI
claude --version  # Si usarás Claude Code
```

Si te falta el cliente de terminal, consulta la [instalación oficial de Codex CLI](https://learn.chatgpt.com/docs/codex/cli) o la [guía de instalación de Claude Code](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code).

En macOS y Linux, Git conserva el enlace simbólico de Claude Code al clonar en un sistema de archivos que admita enlaces. Si tu copia no lo conserva, puedes usar una copia de la carpeta compartida, como se explica en la sección de Claude Code.

La suite del proyecto se ejecutó en Linux. El flujo local en macOS queda pendiente de validación.

## Instalación

| Entorno | Cómo se instala | Cómo se invoca |
| --- | --- | --- |
| ChatGPT | Carga la skill en **Plugins → Habilidades** si tu cuenta lo permite. | «Usa la skill pagespeed-audit…» |
| Codex | Abre el repositorio como proyecto. | `$pagespeed-audit` |
| Claude.ai | Carga el ZIP en **Customize → Skills**. | «Usa la skill pagespeed-audit…» |
| Claude Code | Abre el repositorio como proyecto. | `/pagespeed-audit` |

### Preparar el ZIP para las interfaces web

Clona el repositorio y ejecuta el empaquetador con Python 3. En Windows, si `python3` no está disponible, usa `py -3 tools/build_claude_zip.py`.

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
python3 tools/build_claude_zip.py
```

Carga `dist/pagespeed-audit.zip`. El paquete contiene `SKILL.md`, las referencias y el script. Para usar los cuatro subagentes configurados en el repositorio, abre el proyecto en Codex o Claude Code. En las interfaces web, la skill puede seguir el flujo de forma secuencial.

### ChatGPT

1. En la barra lateral, abre **Plugins → Habilidades → Crear → Cargar desde tu computadora**.
2. Selecciona `dist/pagespeed-audit.zip` y espera a que termine la revisión de la carga.
3. En un chat nuevo, escribe «Usa la skill pagespeed-audit para revisar mi sitio en móvil y escritorio» y añade la URL pública o adjunta el informe de PSI.

La carga depende del acceso a Habilidades y de los permisos del espacio de trabajo. Si el menú no aparece, puedes usar la instalación de Codex o adjuntar un informe de PSI y pedir el análisis directamente en el chat. Consulta la [guía oficial de Habilidades en ChatGPT](https://help.openai.com/es-419/articles/20001066-skills-in-chatgpt).

### Codex

Necesitas Git y un entorno de Codex compatible con [skills](https://learn.chatgpt.com/docs/build-skills). Para usar los cuatro agentes especializados, el entorno debe admitir [subagentes de proyecto](https://learn.chatgpt.com/docs/agent-configuration/subagents).

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

Invoca la skill con `$pagespeed-audit`. La skill se carga desde `.agents/skills/pagespeed-audit/` y los agentes desde `.codex/agents/`.

### Claude Code

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
claude
```

La skill se carga desde `.claude/skills/pagespeed-audit/` y los subagentes desde `.claude/agents/`. Pídele la auditoría con tus palabras (por ejemplo, «revisa la velocidad de https://example.com/ en móvil y escritorio») o invócala con `/pagespeed-audit`.

> Si tu copia del proyecto no conserva el enlace simbólico, coloca una copia completa de `.agents/skills/pagespeed-audit/` en `.claude/skills/pagespeed-audit/`. En Windows también puedes usar esta alternativa si Git no crea el enlace.

### Claude.ai

1. Habilita la ejecución de código y creación de archivos en **Settings → Capabilities** si tu cuenta muestra esa opción. En un espacio administrado, comprueba que la política de la organización permita usar skills.
2. Abre **Customize → Skills → + → Create skill → Upload a skill**.
3. Selecciona `dist/pagespeed-audit.zip`, activa la skill y pídela por nombre en una conversación.

Consulta la [guía oficial de Skills en Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Si el chat no puede medir la URL

En ChatGPT y Claude.ai, la medición automática depende del acceso del entorno a PageSpeed Insights. Si la solicitud falla, ejecuta la prueba en [PageSpeed Insights](https://pagespeed.web.dev/) y comparte el enlace, las capturas de móvil y escritorio o el JSON. El comando `summarize` procesa archivos JSON. Los enlaces y las capturas se interpretan con la evidencia visible.

### Agregarlo a otro proyecto

1. Copia la carpeta completa `.agents/skills/pagespeed-audit/` a la misma ruta de tu proyecto. Para Claude Code, crea también `.claude/skills/pagespeed-audit` (copia o enlace simbólico).
2. Para habilitar la delegación, copia los cuatro `psi-*.toml` a `.codex/agents/` o los cuatro `psi-*.md` a `.claude/agents/`. Conserva las definiciones que ya existan y revisa cualquier archivo con el mismo nombre antes de reemplazarlo.
3. Abre el agente desde la raíz del proyecto.

La skill no requiere dependencias propias. Para medir una URL nueva con el script, el entorno necesita acceso a la API de PSI. Sin clave la cuota anónima es baja; si tu entorno la requiere, expórtala como variable de entorno y no la guardes en el repositorio:

```bash
export PAGESPEED_API_KEY="..."
```

El script envía la clave a Google en la cabecera `X-Goog-Api-Key`. Evita pegarla en el chat o incluirla en informes compartidos.

## Cómo se usa

**Auditar una URL**

> Usa pagespeed-audit para revisar https://example.com/ en móvil y escritorio. Dame un informe rápido con las mejoras prioritarias, dónde aplicarlas y cómo verificarlas.

**Analizar un informe existente**

> Usa pagespeed-audit con este JSON de PageSpeed. El sitio usa WordPress. Propón cambios reversibles y explica qué evidencia falta si no se puede confirmar alguna causa.

**Comparar un despliegue**

> Compara estos informes de antes y después para la misma página y dispositivo. Indica qué cambios se observaron, las diferencias entre mediciones y qué falta verificar.

(En Codex antepón `$` al nombre de la skill: `$pagespeed-audit`.)

Para una auditoría de sitio completo, proporciona URLs públicas representativas de las plantillas que quieras evaluar, como portada, artículo y producto.

### El script por sí solo

```bash
cd .agents/skills/pagespeed-audit
python3 scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 scripts/psi.py summarize psi-reports/*.json
python3 scripts/psi.py compare antes.json despues.json
```

`fetch` detecta varios patrones comunes de credenciales y direcciones internas. Antes de medir, revisa que la URL sea pública y que no incluya tokens, datos personales ni identificadores privados. `summarize` y `compare` aceptan `--json` para salida estructurada.

## Cómo funciona

1. **Reúne evidencia.** Reutiliza los resultados de PSI que entregues o mide las URLs solicitadas. Registra el dispositivo, la fecha y la URL final para detectar redirecciones o páginas de bloqueo.
2. **Analiza el rendimiento.** Separa Chrome UX Report (CrUX), que refleja visitas reales cuando hay datos, de Lighthouse, que mide en condiciones de laboratorio. Distingue entre resultados de la página y del dominio, y clasifica los valores con umbrales explícitos.
3. **Reparte el análisis.** Cuando el entorno lo permite, los roles de campo y laboratorio trabajan en paralelo. Implementación convierte los hallazgos en propuestas y revisión contrasta el informe con la evidencia. En otros entornos, el agente sigue los mismos pasos en secuencia.
4. **Entrega un informe.** Resume las métricas disponibles y prioriza hasta tres acciones por impacto, confianza y riesgo. Indica dónde hacer cada cambio, cómo comprobarlo y cómo revertirlo cuando corresponda.

| Subagente | Responsabilidad |
| --- | --- |
| `psi-field` | Interpreta LCP, INP y CLS de CrUX por dispositivo y alcance. |
| `psi-lab` | Examina Lighthouse y vincula los problemas a sus recursos, elementos o auditorías. |
| `psi-implementation` | Propone cambios concretos según la plataforma y define cómo verificarlos. |
| `psi-review` | Detecta afirmaciones sin evidencia, ahorros duplicados y comparaciones inválidas. |

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Cubren la normalización de métricas, los umbrales de validación de URL, la detección de páginas bloqueadas y la paridad entre los subagentes de Codex y Claude. Los fixtures de `tests/fixtures/` son **sintéticos** (replican la estructura de la API v5, no son mediciones reales). Si cambias las instrucciones de un subagente, actualiza su `.md` y su `.toml` a la vez; la prueba de paridad avisa si divergen.

## Alcance

PageSpeed necesita acceder a la página pública. Si encuentra un inicio de sesión, un bloqueo o una redirección inesperada, el informe indica qué quedó sin medir. Si CrUX carece de datos suficientes, el informe marca las métricas faltantes. Por defecto, la auditoría entrega recomendaciones. Cualquier cambio en el sitio requiere una solicitud aparte.

[Metodología de PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) · [API oficial](https://developers.google.com/speed/docs/insights/v5/get-started)

## Licencia

Este proyecto se distribuye bajo la [licencia MIT](LICENSE). Puedes usarlo, modificarlo y redistribuirlo, incluso con fines comerciales, conservando el aviso de copyright y el texto de la licencia en las copias o partes sustanciales.

Creado por [Lulu (@lulubumps)](https://github.com/lulubumps).
