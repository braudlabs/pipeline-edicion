# Subagentes y límite de uso

> Lanzar 20 subagentes Opus a la vez agotó el límite de uso del usuario en ~25 min sin dejar casi nada guardado; trabajar en lotes pequeños que persistan pronto

El 10/10/2026 lancé 20 subagentes (Opus) en paralelo para revisar tramos de vídeo. En unos
25 minutos se agotó el límite de uso de la sesión del usuario; los 20 murieron con error 429
y solo uno había escrito una nota parcial, pese a que el encargo pedía guardar cada 3–4 hojas.
El usuario tuvo que continuar el trabajo con Codex. Además, la app limita a 20 subagentes
simultáneos (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).

Esto es una conclusión mía a partir de lo ocurrido, no una instrucción literal del usuario.

**Why:** el límite de uso es compartido entre la sesión principal y sus subagentes; un
abanico grande lo consume de golpe y, si corta a mitad, se pierde lo que no esté en disco.

**How to apply:** en este proyecto, lotes de 4–5 subagentes como mucho; obligar a que el
primer paso de cada uno sea crear su archivo de notas y a que escriba tras cada bloque
pequeño de trabajo; avisar al usuario del coste antes de un abanico grande; preferir un
modelo más barato para trabajo de revisión mecánica cuando la calidad lo permita. Ver
[Estudio del estilo del editor](estudio-estilo-editor.md).
