# Instrucciones para agentes de IA

Estas reglas aplican a ChatGPT, Claude, Codex y cualquier agente que contribuya al repositorio.

## Secuencia obligatoria al iniciar

1. Lee [PROJECT-CONTEXT.md](PROJECT-CONTEXT.md) completo.
2. Revisa [DECISIONS.md](../development/DECISIONS.md) y respeta las decisiones `ACCEPTED`.
3. Revisa [HANDOFF.md](HANDOFF.md) para conocer el estado actual y evitar repetir trabajo.
4. Lee los documentos del dominio que vayas a modificar.

## Reglas de trabajo

- No asumas decisiones inexistentes. Etiqueta toda incertidumbre con el estado adecuado.
- Distingue información proporcionada, evidencia investigada, inferencias e hipótesis.
- No conviertas una hipótesis en requisito, compromiso, arquitectura o hecho sin decisión explícita y evidencia.
- Antes de implementar software, confirma que existe una autorización explícita y decisiones de alcance suficientes. Actualmente el desarrollo de aplicación está fuera de alcance.
- Cuando una decisión importante cambie, registra un ADR en `development/DECISIONS.md`, actualiza los documentos afectados y anota el cambio en `development/CHANGELOG.md`.
- Al terminar una sesión significativa, actualiza `ai/HANDOFF.md` con estado, trabajo, decisiones, preguntas, pendientes, siguiente paso y archivos relevantes.
- Evita contradicciones entre documentos. Si detectas una, no ocultes la versión anterior: enlaza o registra la resolución.
- Nunca borres contexto histórico relevante sin justificarlo y dejar una referencia a la decisión o al reemplazo.
- Mantén los cambios pequeños, revisables y coherentes con el alcance solicitado.

## Investigación

- Para afirmaciones externas (APIs, licencias, competencia, regulación, costes o compatibilidad), enlaza fuentes y fecha de consulta.
- Separa lo que una fuente afirma de la interpretación para Proyecto Loreto.
- Registra limitaciones de la evidencia y preguntas que sigan abiertas.

## Calidad antes de cerrar

1. Relee los archivos modificados y sus enlaces relativos.
2. Comprueba que los estados son explícitos y consistentes.
3. Actualiza CHANGELOG y HANDOFF si el trabajo es significativo.
4. Resume qué cambió, qué no se decidió y cuál es el siguiente paso recomendado.
