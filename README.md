# Auditoría web con Google PageSpeed Insights

`pagespeed-audit` es una skill para Codex que convierte los resultados de Google PageSpeed Insights (PSI) en un informe breve con hasta tres mejoras prioritarias. Sirve para diagnosticar páginas lentas, decidir qué cambiar en una plantilla o configuración y comparar el rendimiento antes y después de un despliegue.

Funciona con sitios públicos HTTP(S), incluidos WordPress, Shopify, sitios estáticos y aplicaciones con renderizado en cliente o servidor. Puede partir de una URL pública, un informe compartido, capturas o un JSON de PSI.

## Instalación

Necesitas Git y un entorno de Codex compatible con [skills](https://learn.chatgpt.com/docs/build-skills). Para usar los cuatro agentes especializados, el entorno debe admitir [subagentes de proyecto](https://learn.chatgpt.com/docs/agent-configuration/subagents).

### Usar este repositorio como proyecto

```bash
git clone https://github.com/lulubumps/pagespeed-audit-skill.git
cd pagespeed-audit-skill
codex
```

El último comando inicia Codex CLI si ya lo tienes instalado. También puedes abrir la carpeta clonada como proyecto en tu cliente de Codex. La skill se carga desde `.agents/skills/pagespeed-audit/` y los agentes desde `.codex/agents/`.

### Agregarlo a otro proyecto

1. Copia la carpeta completa `.agents/skills/pagespeed-audit/` a la misma ruta dentro de tu proyecto.
2. Para habilitar la delegación, copia los cuatro archivos `psi-*.toml` a `.codex/agents/` del proyecto. Conserva las definiciones que ya existan y revisa cualquier archivo con el mismo nombre antes de reemplazarlo.
3. Abre Codex desde la raíz del proyecto e invoca `$pagespeed-audit`.

La skill no requiere dependencias propias. Para medir una URL nueva, Codex necesita acceso a la interfaz de PSI o a su API. Si tu entorno usa la API y requiere una clave, configúrala fuera del repositorio. También puedes proporcionar evidencia exportada y analizarla sin solicitar otra medición.

## Cómo se usa

**Auditar una URL**

> Usa $pagespeed-audit para revisar https://example.com/ en móvil y escritorio. Dame un informe rápido con las mejoras prioritarias, dónde aplicarlas y cómo verificarlas.

**Analizar un informe existente**

> Usa $pagespeed-audit con este JSON de PageSpeed. El sitio usa WordPress. Propón cambios reversibles y explica qué evidencia falta si no se puede confirmar alguna causa.

**Comparar un despliegue**

> Compara estos informes de antes y después para la misma página y dispositivo. Indica qué cambios se observaron, las diferencias entre mediciones y qué falta verificar.

Para una auditoría de sitio completo, proporciona URLs públicas representativas de las plantillas que quieras evaluar, como portada, artículo y producto.

## Cómo funciona

1. **Reúne evidencia.** Reutiliza los resultados de PSI que entregues o mide las URLs solicitadas. Registra el dispositivo, la fecha y la URL final para detectar redirecciones o páginas de bloqueo.
2. **Analiza el rendimiento.** Separa Chrome UX Report (CrUX), que refleja visitas reales cuando hay datos, de Lighthouse, que mide en condiciones de laboratorio. Distingue entre resultados de la página y del dominio.
3. **Reparte el análisis.** Cuando el entorno lo permite, los roles de campo y laboratorio trabajan en paralelo. Implementación convierte los hallazgos en propuestas y revisión contrasta el informe con la evidencia. En otros entornos, Codex puede seguir los mismos pasos en secuencia.
4. **Entrega un informe.** Resume las métricas disponibles y prioriza hasta tres acciones por impacto, confianza y riesgo. Indica dónde hacer cada cambio, cómo comprobarlo y cómo revertirlo cuando corresponda.

| Subagente | Responsabilidad |
| --- | --- |
| `psi-field` | Interpreta LCP, INP y CLS de CrUX por dispositivo y alcance. |
| `psi-lab` | Examina Lighthouse y vincula los problemas a sus recursos, elementos o auditorías. |
| `psi-implementation` | Propone cambios concretos según la plataforma y define cómo verificarlos. |
| `psi-review` | Detecta afirmaciones sin evidencia, ahorros duplicados y comparaciones inválidas. |

## Alcance

PageSpeed necesita acceder a la página pública. Si encuentra un inicio de sesión, un bloqueo o una redirección inesperada, el informe indica qué quedó sin medir. Si CrUX carece de datos suficientes, el informe marca las métricas faltantes. Por defecto, la auditoría entrega recomendaciones. Cualquier cambio en el sitio requiere una solicitud aparte.

[Metodología de PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) · [API oficial](https://developers.google.com/speed/docs/insights/v5/get-started)
