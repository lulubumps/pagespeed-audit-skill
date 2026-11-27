# Auditoría con Google PageSpeed Insights

Abre este repositorio como proyecto de Codex. La skill vive en `.agents/skills/pagespeed-audit/` y las definiciones de los cuatro subagentes en `.codex/agents/`.

> Usa $pagespeed-audit para revisar https://example.com en móvil y escritorio. Dame un informe rápido con los cambios prioritarios, dónde aplicarlos y cómo comprobarlos.

Puedes usar una URL pública, un informe compartido, capturas o el JSON de Google PageSpeed Insights. Si el entorno admite subagentes, el flujo distribuye la interpretación de CrUX, Lighthouse, las recomendaciones y la revisión de evidencia. También funciona mediante análisis secuencial.
