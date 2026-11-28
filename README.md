# Auditoría web con Google PageSpeed Insights

`pagespeed-audit` es una skill para **Codex** y **Claude** que convierte los resultados de Google PageSpeed Insights (PSI) en un informe breve con hasta tres mejoras prioritarias. Sirve para diagnosticar páginas lentas, decidir qué cambiar en una plantilla o configuración y comparar el rendimiento antes y después de un despliegue.

Funciona con sitios públicos HTTP(S), incluidos WordPress, WooCommerce, Shopify, sitios estáticos y aplicaciones con renderizado en cliente o servidor. Puede partir de una URL pública, un informe compartido, capturas o un JSON de PSI.

Una sola fuente (`.agents/skills/pagespeed-audit/`) sirve a ambos agentes: Claude Code la lee desde `.claude/skills/` mediante un enlace simbólico.

## Qué incluye

| Pieza | Para qué sirve |
| --- | --- |
| `SKILL.md` | Flujo de trabajo en seis pasos y reglas que no se negocian. |
| `scripts/psi.py` | Mide con la API oficial, normaliza el JSON y compara versiones. Solo librería estándar de Python 3. |
| `references/` | Reglas de medición, umbrales, diagnóstico por plataforma (con sección de WordPress y WooCommerce), roles y formato de informe. |
| Cuatro subagentes | `psi-field`, `psi-lab`, `psi-implementation` y `psi-review`, en `.codex/agents/` (Codex) y `.claude/agents/` (Claude Code). Son de solo lectura. |

## Instalación

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

> En Windows, si Git no crea el enlace simbólico de `.claude/skills/pagespeed-audit`, copia a mano la carpeta `.agents/skills/pagespeed-audit/` en esa ruta.

### Claude.ai (web, escritorio y móvil)

1. Genera el paquete con `python3 tools/build_claude_zip.py`. Queda en `dist/pagespeed-audit.zip`.
2. Súbelo en la sección de Skills de la configuración de Claude.

Limitación: en Claude.ai el entorno de ejecución puede no tener acceso a Google, así que `fetch` podría fallar. En ese caso, mide la URL en [pagespeed.web.dev](https://pagespeed.web.dev/) (o con Claude Code) y entrega el JSON, el enlace o las capturas; la skill los analiza con `summarize` sin pedir otra medición.

### Agregarlo a otro proyecto

1. Copia la carpeta completa `.agents/skills/pagespeed-audit/` a la misma ruta de tu proyecto. Para Claude Code, crea también `.claude/skills/pagespeed-audit` (copia o enlace simbólico).
2. Para habilitar la delegación, copia los cuatro `psi-*.toml` a `.codex/agents/` o los cuatro `psi-*.md` a `.claude/agents/`. Conserva las definiciones que ya existan y revisa cualquier archivo con el mismo nombre antes de reemplazarlo.
3. Abre el agente desde la raíz del proyecto.

La skill no requiere dependencias propias. Para medir una URL nueva necesita acceso a la API de PSI. Sin clave la cuota anónima es baja; si tu entorno la requiere, expórtala como variable de entorno y no la guardes en el repositorio:

```bash
export PAGESPEED_API_KEY="..."
```

La clave viaja en la cabecera `X-Goog-Api-Key`, nunca en la URL, en los archivos guardados ni en los mensajes de error.

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

`fetch` rechaza URLs con credenciales, tokens, hosts internos o IP privadas antes de enviar nada a Google. `summarize` y `compare` aceptan `--json` para salida estructurada.

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
