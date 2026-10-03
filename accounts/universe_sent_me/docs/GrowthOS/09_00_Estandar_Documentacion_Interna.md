# Estándar de Documentación Interna — Growth OS

**Propósito:** Formalizar las reglas que rigen cómo Manus crea, actualiza y organiza documentos en este repositorio. Toda instrucción aquí es operativa y permanente; supera cualquier instrucción dada solo en conversación.
**Estado:** Active
**Fecha de creación:** 2026-08-03
**Última actualización:** 2026-08-03
**Versión:** 1.0
**Autor:** Claude (formalización de instrucciones aprobadas por Fernando, 2026-08-03)
**Documentos relacionados:** `../Studio_Governance.md`, `00_Índice.md`

---

## 1. Gestión del Conocimiento

- GitHub es la fuente oficial de verdad del proyecto.
- Toda información con valor permanente debe terminar documentada dentro del repositorio.
- Las conversaciones son temporales. Los documentos del repositorio son permanentes.

## 2. Regla de Documentación

Cuando una tarea produzca conocimiento útil, Manus debe:
- Actualizar un documento existente, si existe uno relacionado.
- Crear un documento nuevo solo cuando represente un concepto realmente nuevo.

**Nunca dejar información importante únicamente dentro de la conversación.**

## 3. Estructura Obligatoria de Todo Documento

```markdown
**Propósito:** [qué hace este documento]
**Estado:** Draft | Review | Active | Canon | Archived
**Fecha de creación:** YYYY-MM-DD
**Última actualización:** YYYY-MM-DD
**Versión:** X.Y
**Autor:** [quién lo creó]
**Documentos relacionados:** [al menos uno]
```

Todo documento nuevo debe enlazar con al menos un documento existente. No se admiten documentos huérfanos.

## 4. Ubicación de Documentos

```
GrowthOS/                  ← documentos operativos del Growth OS
Operations/
  Research/                ← auditorías, análisis puntuales
  Archive/                 ← documentos inactivos
Studio/                    ← gobernanza (no editar sin autorización)
```

Nunca colocar documentos en ubicaciones arbitrarias. Si hay duda sobre dónde va algo, preguntar antes de crear.

## 5. Coherencia entre Documentos

Si un documento modifica información existente, Manus debe indicar explícitamente qué otros documentos requieren actualización para mantener coherencia. Esto incluye el índice (`00_Índice.md`).

## 6. Fuente Única de Verdad

Si existe una diferencia entre una conversación y un documento del repositorio, **el documento del repositorio tiene prioridad**. Si Manus detecta información importante que solo existe en una conversación, debe proponer convertirla en documentación permanente antes de finalizar la tarea.

## 7. Mentalidad de Estudio

Manus no trabaja como asistente conversacional. Trabaja como miembro permanente del estudio Universe Sent Me. Antes de dar una respuesta final, Manus se pregunta: "¿Esto debería existir también como un documento del proyecto?" Si la respuesta es sí, lo crea o actualiza antes de finalizar.

## 8. Reglas Específicas para Canon

Manus tiene **acceso de solo lectura** al repositorio de canon (`universe-sent-me-1`). Puede consultar cualquier ficha para informar su trabajo, pero no puede:
- Crear personajes, lugares ni principios nuevos.
- Usar nombres de personajes que no existan en la Biblia (ver regla de canon en `Canon_Contradictions_Report.md`).
- Marcar el campo `Bloqueado_Canon` como `No` sin validación de Claude o Fernando.

Ante cualquier duda de canon, Manus genera un flag en `Canon_Contradictions_Report.md` y espera resolución antes de avanzar.

## 9. Historial de Versiones de Este Documento

| Fecha | Versión | Cambio | Autor |
|---|---|---|---|
| 2026-08-03 | 1.0 | Creación — formalización de instrucciones de Fernando | Claude |
