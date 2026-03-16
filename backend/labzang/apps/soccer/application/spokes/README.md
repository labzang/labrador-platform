# Spokes (헥사고날 – 드리븐/외부 연동)

이 디렉터리는 **헥사고날**에서 외부 시스템·에이전트·인프라와 맞닿는 **드리븐** 쪽에 해당합니다.

## 역할

- **agents**: 에이전트·LLM 연동 등 외부 서비스 호출.
- **infrastructure**: 임베딩 클라이언트 등 인프라 클라이언트.
- **retrievers**: 검색·조회용 리트리버.
- **services**: `hub.services`의 서비스를 **재노출**.  
  오케스트레이터 등에서는 `from labzang.apps.soccer.spokes.services import TeamService` 형태로 사용해, 구현은 hub에 두고 spokes를 진입점으로 둡니다.

## 의존성

- **의존하는 쪽**: `hub.services`, 인프라(API, DB 클라이언트 등).
- **의존받는 쪽**: `hub/orchestrators` 등이 spokes 서비스를 import 해서 사용.

## 참고

- 실제 비즈니스 로직·저장소 구현은 **hub**에 있고, spokes는 그 조합·재노출 및 외부 연동(에이전트, 인프라)을 담당합니다.
