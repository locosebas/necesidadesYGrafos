# Examen GitLab: Admin / Platform Engineer (Service Account Migration)

**Reglas**
- Una pregunta a la vez. Claude califica de 0 a 10, explica qué faltó y pasa a la siguiente.
- "paso" = 0 puntos, con la explicación completa.
- Al final: promedio por bloque, promedio general y plan de repaso.

**Escala:** 9-10 experto · 7-8 sólido · 5-6 básico · <5 repasar

**Estado actual:** Pregunta 1 de 50

---

## Bloque A: Fundamentos
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 1 | ¿Qué diferencia hay entre Git y GitLab? | | |
| 2 | Menciona 3 diferencias entre GitLab y GitHub | | |
| 3 | ¿Qué es GitLab self-managed frente a GitLab.com? ¿Qué planes existen? | | |
| 4 | ¿Qué es un Group, un Subgroup y un Project? ¿Para qué sirve agrupar? | | |
| 5 | Ordena los roles de menor a mayor. ¿Qué puede hacer un Maintainer que un Developer no? | | |

## Bloque B: Git esencial
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 6 | merge vs rebase: diferencia y cuándo NO usar rebase | | |
| 7 | git fetch vs git pull | | |
| 8 | git revert vs git reset: ¿cuál usarías en `main` y por qué? | | |
| 9 | ¿Para qué sirven `git stash` y `git cherry-pick`? Da un caso real de cada uno | | |
| 10 | ¿Cómo resuelves un conflicto de merge en un MR? | | |

## Bloque C: Flujo de trabajo
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 11 | ¿Qué es un Merge Request y qué elementos incluye? | | |
| 12 | Describe el flujo completo desde un issue hasta el merge. ¿Cómo cierras el issue automáticamente? | | |
| 13 | GitLab Flow vs Git Flow vs Trunk-based | | |
| 14 | ¿Qué son las protected branches y cómo configurarías `main`? | | |
| 15 | ¿Qué es CODEOWNERS y cómo se combina con las approval rules? | | |

## Bloque D: CI/CD
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 16 | Stage vs job: ¿cómo se ejecutan? | | |
| 17 | ¿Qué es un Runner? Tipos de runner y tipos de executor | | |
| 18 | `build` genera `dist/` y `deploy` lo necesita: ¿cache o artifacts? ¿Por qué? | | |
| 19 | Variables predefinidas vs personalizadas. ¿Qué significan masked y protected? | | |
| 20 | Escribe un job que corra SOLO en Merge Requests | | |
| 21 | ¿Qué hace `needs` y qué ventaja tiene sobre los stages? | | |
| 22 | Deploy a producción manual y solo desde `main`: escribe el job | | |
| 23 | ¿Para qué sirven `include` y `extends`? | | |
| 24 | Un job se queda en "pending" para siempre. ¿Causas y solución? | | |
| 25 | ¿Cómo acelerarías un pipeline lento? (mínimo 4 técnicas) | | |

## Bloque E: DevSecOps
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 26 | ¿Qué es el Container Registry y cómo publicas una imagen desde CI? | | |
| 27 | SAST vs DAST vs Dependency Scanning vs Container Scanning vs Secret Detection | | |
| 28 | ¿Qué son los Environments y las Review Apps? ¿Cómo haces rollback? | | |
| 29 | ¿Qué es `CI_JOB_TOKEN` y qué ventaja tiene sobre un PAT guardado en una variable? | | |

## Bloque F: Administración de la instancia
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 30 | ¿Dónde se configura GitLab self-managed y cómo aplicas los cambios? | | |
| 31 | Nombra los componentes principales de la arquitectura y qué hace cada uno | | |
| 32 | ¿Cómo haces un backup completo? ¿Qué NO incluye `gitlab-backup`? | | |
| 33 | ¿Cómo planeas un upgrade de versión mayor? | | |
| 34 | Un usuario reporta errores en la API. ¿Qué logs revisas y dónde están? | | |
| 35 | LDAP vs SAML vs SCIM | | |
| 36 | ¿Qué cambió en el registro de runners (registration token vs authentication token)? | | |
| 37 | ¿Qué son Admin Mode y Audit Events? ¿Por qué importan? | | |

## Bloque G: Identidades y Service Accounts
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 38 | ¿Qué tipos de identidad existen para automatizaciones en GitLab? Problemas de cada una | | |
| 39 | ¿Qué es una Service Account y cuáles son sus características? | | |
| 40 | Group Access Token vs Service Account: ¿cuándo usarías cada uno? | | |
| 41 | Un sistema solo lee imágenes del registry: ¿qué rol y qué scopes le das? | | |
| 42 | ¿Qué cambió con la expiración de tokens en GitLab 16.0 y qué implica? | | |
| 43 | Escribe el `curl` para dar Reporter a la service account con ID 555 en el grupo 42 | | |
| 44 | Hay 400 PATs activos: ¿cómo identificas cuáles son de automatizaciones y si se usan? | | |
| 45 | Un dev se fue ayer y hoy fallan el deploy y un bot. ¿Qué pasó? Solución hoy y permanente | | |

## Bloque H: Migración y escenarios
| # | Pregunta | Nota | Comentario |
|---|---|---|---|
| 46 | Diseña el plan completo de migración a service accounts | | |
| 47 | ¿Por qué no revocas el token viejo al momento del cambio? | | |
| 48 | 120 tokens vencen el mismo día: ¿cómo lo evitas en adelante? | | |
| 49 | Aparece un token filtrado en un repo público: ¿qué haces, en orden? | | |
| 50 | Pregunta abierta (STAR): "Cuéntame de una migración compleja que hayas liderado" | | |

---

## Resultado final
| Bloque | Promedio |
|---|---|
| A Fundamentos | |
| B Git | |
| C Flujo | |
| D CI/CD | |
| E DevSecOps | |
| F Administración | |
| G Service Accounts | |
| H Migración | |
| **General** | |

**Nivel:**
**Temas a repasar:**
