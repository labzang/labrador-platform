# Hub (헥사고날 – 애플리케이션 코어)

이 디렉터리는 **헥사고날**에서 오케스트레이션·저장소 구현·서비스가 모여 있는 코어에 해당합니다.

## 역할

- **orchestrators**: 업로드/처리 흐름 조합. 필요한 서비스(및 포트)를 조합해 호출.
- **repositories**: `application/ports/output`의 저장소 **포트 구현**.  
  예: `TeamRepository(TeamRepositoryPort)`, `PlayerRepository(PlayerRepositoryPort)` 등.
- **services**: 규칙 기반 정규화·저장. 생성자에서 **출력 포트(RepositoryPort)를 선택적으로 주입** 가능.  
  주입 시 해당 포트로 저장하고, 미주입 시 기존처럼 `AsyncSessionLocal` + 해당 Repository 사용.

## 의존성

- **의존하는 쪽**: `application/ports/output`, `hub/repositories`, `spokes/services`(서비스 재노출), 인프라(DB, embedding 등).
- **의존받는 쪽**: `use_cases`, 어댑터(라우터·MCP 등)에서 오케스트레이터·서비스를 사용.

## 포트 주입 예시

```python
# 포트 없이 사용 (기본 DB 세션 사용)
team_service = TeamService()

# 테스트/대체 저장소 주입
team_service = TeamService(team_repository=my_fake_repository)
```
