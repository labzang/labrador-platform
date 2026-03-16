# Use Cases (헥사고날 – 입력 포트 구현)

이 디렉터리는 **헥사고날**의 **입력 포트(드라이빙)** 를 구현하는 유스케이스들이 모여 있습니다.

## 역할

- **입력 포트 구현**: `application/ports/input`에 정의된 계약을 구현.
- **출력 포트에만 의존**: 유스케이스는 **출력 포트(RepositoryPort 등)** 만 주입받아 사용.  
  DB 세션, HTTP, 구체 Repository 클래스에는 의존하지 않음.
- **진입점**: 라우터·CLI·MCP 등 **드라이빙 어댑터**가 유스케이스 `execute(...)` 를 호출.

## 의존성

- **의존하는 쪽**: `application/ports/input`, `application/ports/output`(인터페이스만), 필요 시 domain.
- **의존받는 쪽**: `adapter/input`(API 라우터 등)에서 유스케이스를 생성·호출.

## 예시

- `ProcessTeamUploadUseCase`: 팀 JSONL 업로드. 생성자에 `TeamRepositoryPort` 등을 주입받고, `execute(items)` 에서 정규화 후 `upsert_batch` 호출.
