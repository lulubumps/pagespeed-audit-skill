<p align="center">
  <img src=".agents/skills/pagespeed-audit/assets/icon.svg" width="72" height="72" alt="Ícono de PageSpeed Audit">
</p>
<h1 align="center">PageSpeed Audit</h1>
<p align="center"><strong>Español</strong> · <a href="README.en.md">English</a> · <a href="README.pt.md">Português</a> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.hi.md">हिन्दी</a></p>

**De un informe de PageSpeed a tres mejoras que puedes aplicar en tu sitio.**

[![Google PageSpeed Insights](https://img.shields.io/badge/Google%20PageSpeed%20Insights-174EA6?style=for-the-badge&logo=google&logoColor=white)](https://pagespeed.web.dev/)
[![Lighthouse](https://img.shields.io/badge/Lighthouse-B3371D?style=for-the-badge&logo=lighthouse&logoColor=white)](#cómo-funciona)
[![MIT](https://img.shields.io/badge/MIT-5B3CC4?style=for-the-badge)](LICENSE)

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
| Auditoría completa en Claude (Nuevo) | `CLAUDE.md` y `.claude/pagespeed/`: informe completo, medición de las cuatro categorías de Lighthouse y diagnóstico por plataforma. Es el equivalente de la extensión de Codex. |
| Cuatro subagentes adicionales (Nuevo) | `psi-scope`, `psi-cms`, `psi-third-party` y `psi-regression`, en `.claude/agents/`. También son de solo lectura. |

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
codex --version
claude --version
```

Si te falta el cliente de terminal, consulta la [instalación oficial de Codex CLI](https://learn.chatgpt.com/docs/codex/cli) o la [guía de instalación de Claude Code](https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code).

En macOS y Linux, Git conserva el enlace simbólico de Claude Code al clonar en un sistema de archivos que admita enlaces. Si tu copia no lo conserva, puedes usar una copia de la carpeta compartida, como se explica en la sección de Claude Code.

La suite del proyecto se ejecutó en Linux. El flujo local en macOS queda pendiente de validación.

### Comprobar e instalar los requisitos

Si solo vas a cargar un ZIP ya preparado en ChatGPT o Claude.ai, puedes saltar la instalación local. Para clonar el repositorio, instala Git. Para generar el ZIP, usar los scripts o ejecutar las pruebas, instala Python 3. Para trabajar en terminal, instala el cliente correspondiente y sigue su guía para iniciar sesión.

#### macOS

Homebrew es opcional. Instálalo desde su sitio oficial y sigue las instrucciones de configuración de `PATH` que muestre el instalador. Después abre una terminal nueva y ejecuta los comandos. Si prefieres instalar directamente, usa Git para macOS y el instalador de Python para macOS.

[Homebrew](https://brew.sh/) · [Git (macOS)](https://git-scm.com/install/mac) · [Python (macOS)](https://www.python.org/downloads/macos/)

```bash
brew --version
brew install git python
git --version
python3 --version
```

#### Linux (Ubuntu, Debian, Fedora y Arch)

Ejecuta solo el bloque de tu distribución. Si usas otra, consulta las instrucciones de Git y la documentación de tu distribución para instalar Git y Python 3.

[Git (Linux)](https://git-scm.com/install/linux) · [Python 3 (Ubuntu)](https://packages.ubuntu.com/search?keywords=python3) · [Python 3 (Debian)](https://packages.debian.org/search?keywords=python3) · [Python 3 (Fedora)](https://docs.fedoraproject.org/en-US/quick-docs/installing-python/) · [Python (Arch)](https://archlinux.org/packages/extra/x86_64/python/)

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install git python3
```

```bash
# Fedora
sudo dnf install git python3
```

```bash
# Arch Linux
sudo pacman -Syu git python
```

```bash
git --version
python3 --version
```

#### Windows (PowerShell)

Instala Git para Windows y Python 3 desde sus sitios oficiales. Abre una ventana nueva de PowerShell y ejecuta las comprobaciones. Si funciona `py -3`, úsalo en lugar de `python3` en los ejemplos que invoquen Python. Si el lanzador `py` no está disponible pero `python --version` muestra Python 3, usa `python`. Si trabajas en WSL, sigue las instrucciones de Linux dentro de tu distribución.

[Git for Windows](https://git-scm.com/install/windows) · [Python (Windows)](https://www.python.org/downloads/windows/) · [WSL](https://learn.microsoft.com/windows/wsl/install)

```powershell
git --version
py -3 --version
python --version
```

#### Clientes de terminal y diagnóstico

Consulta la instalación oficial de Codex CLI o Claude Code para tu sistema y comprueba el cliente elegido con `codex --version` o `claude --version`. Si un comando no se reconoce, vuelve a abrir la terminal y revisa el `PATH` según la guía oficial. Desde la raíz del repositorio, comprueba `python3 -m unittest discover -s tests -v` y ejecuta `python3 tools/build_claude_zip.py --full` si necesitas generar el paquete completo. La medición en vivo también requiere acceso a la API de PageSpeed Insights.

[Codex CLI](https://learn.chatgpt.com/docs/codex/cli) · [Claude Code](https://code.claude.com/docs/en/setup)

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
| `psi-scope` (Nuevo) | Propone URLs públicas representativas por plantilla y dispositivo. |
| `psi-cms` (Nuevo) | Asigna cada hallazgo a la capa responsable de la plataforma: tema, componente, app, plugin, editor o CDN. |
| `psi-third-party` (Nuevo) | Atribuye los costos de scripts, embeds y etiquetas de terceros a su integración. |
| `psi-regression` (Nuevo) | Compara páginas, dispositivos y configuraciones equivalentes después de un despliegue. |

## Auditoría completa en Claude (Nuevo)

Además del informe breve con tres mejoras, Claude puede entregar una auditoría completa: un resumen priorizado seguido de todos los hallazgos con evidencia en las cuatro categorías de Lighthouse (rendimiento, accesibilidad, buenas prácticas y SEO). Conserva los identificadores de auditoría y marca las revisiones manuales, los errores y las brechas de cobertura. Es el equivalente para Claude de la extensión que ya existe para Codex (`AGENTS.md` y `.codex/pagespeed/`).

| Entorno | Cómo se activa |
| --- | --- |
| Claude Code | `CLAUDE.md` se carga al abrir el repositorio como proyecto. Activa el modo completo cuando pides una auditoría completa, recomendaciones por plataforma o la verificación de un despliegue. |
| Claude.ai | Ejecuta `python3 tools/build_claude_zip.py --full`, carga `dist/pagespeed-audit-full.zip` y pide «Usa la skill pagespeed-audit en modo de auditoría completa…». En la web no hay subagentes: Claude sigue los roles en secuencia. |

**Ejemplo**

> Usa pagespeed-audit para hacer una auditoría completa de https://example.com/ en móvil y escritorio. Quiero todas las categorías, los hallazgos agrupados por causa con sus IDs de auditoría y los pasos específicos para mi plataforma.

La guía por plataforma cubre Shopify, WordPress y WooCommerce, Drupal, Joomla, Wix, Squarespace, Webflow, Adobe Commerce, PrestaShop y CMS headless. Cada recomendación indica quién es el responsable del cambio, cómo verificarlo y cómo revertirlo.

### El script de la auditoría completa

```bash
python3 .claude/pagespeed/scripts/psi.py fetch https://example.com/ --strategy both --out psi-reports
python3 .claude/pagespeed/scripts/psi.py summarize psi-reports/*.json
python3 .claude/pagespeed/scripts/psi.py compare antes.json despues.json
```

Este script solicita las cuatro categorías, no limita el número de hallazgos e informa las auditorías manuales o con error como revisiones pendientes. El script de `.agents/skills/pagespeed-audit/scripts/psi.py` sigue midiendo solo rendimiento. Con `--full`, el ZIP incluye este script como `scripts/psi_full.py`.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Cubren la normalización de métricas, los umbrales de validación de URL, la detección de páginas bloqueadas y la paridad entre los subagentes de Codex y Claude. Los fixtures de `tests/fixtures/` son **sintéticos** (replican la estructura de la API v5, no son mediciones reales). Si cambias las instrucciones de un subagente, actualiza su `.md` y su `.toml` a la vez; la prueba de paridad avisa si divergen. (Nuevo) `tests/test_claude_psi.py` verifica que el script cubra las cuatro categorías, que los ocho subagentes de Claude sean de solo lectura, que los cuatro nuevos coincidan con los de Codex y que el ZIP completo no tenga rutas rotas.

## Alcance

PageSpeed necesita acceder a la página pública. Si encuentra un inicio de sesión, un bloqueo o una redirección inesperada, el informe indica qué quedó sin medir. Si CrUX carece de datos suficientes, el informe marca las métricas faltantes. Por defecto, la auditoría entrega recomendaciones. Cualquier cambio en el sitio requiere una solicitud aparte.

[Metodología de PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) · [API oficial](https://developers.google.com/speed/docs/insights/v5/get-started)

## Licencia

Este proyecto se distribuye bajo la [licencia MIT](LICENSE). Puedes usarlo, modificarlo y redistribuirlo, incluso con fines comerciales, conservando el aviso de copyright y el texto de la licencia en las copias o partes sustanciales.

**Descarga gratuita.** Distribuyo la versión oficial de PageSpeed Audit gratis en este repositorio. No la ofrezco a la venta y mantengo el proyecto en desarrollo continuo sin interés monetario. Si alguien te cobró por la skill en sí, pídele la devolución del dinero a quien te la vendió. La reutilización, modificación y redistribución siguen permitidas según la licencia MIT.

**Precisión de los informes.** La skill está hecha para asistentes de IA, que pueden equivocarse o interpretar datos incompletos. Contrasta las conclusiones con el informe original de PageSpeed Insights antes de aplicar cambios.

Creado por [Lulu (@lulubumps)](https://github.com/lulubumps).
