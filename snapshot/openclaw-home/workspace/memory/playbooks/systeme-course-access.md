# systeme-course-access.md - Systeme.io Course Access

## Objetivo
- Validar acesso a um curso na Systeme.io sem depender de browser interativo quando isso nao for necessario.

## Fluxo recomendado
1. Ler URL e credenciais do item correto no 1Password usando apenas service account.
2. Autenticar em ${SYSTEME_BASE_URL}/api/security/login.
3. Validar matriculas em /api/membership/enrollments/list.
4. Abrir o curso em /api/membership/course/<course_path> e o menu em /api/membership/course/<course_id>/menu.
5. Confirmar a primeira aula disponivel em /school/course/<course_path>/lecture/<lecture_id>.

## Ferramenta recomendada
- Preferir /root/.openclaw/bin/check-systeme-course-access.sh com as variaveis:
- SYSTEME_BASE_URL
- SYSTEME_EMAIL
- SYSTEME_PASSWORD
- SYSTEME_COURSE_PATH

## Regra operacional
- Se o login passar mas o curso nao aparecer em enrollments/list, parar e reportar falta de matricula ou conta incorreta.
- Se a aula inicial abrir com HTTP 200, o acesso ao curso deve ser considerado validado.

- Para o Nutroboost, consultar primeiro o mapa salvo em /root/.openclaw/workspace/memory/research/nutroboost-course-map.md.
- O exportador do mapa fica em /root/.openclaw/workspace/scripts/export_systeme_course_map.py.
