# -*- coding: utf-8 -*-
"""선수 업로드 및 임베딩 인덱싱 서비스."""

import logging
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output import PlayerRepository
from labzang.apps.soccer.hub.repositories.player_repository import PlayerRepository
from labzang.apps.soccer.domain.entities import Player, PlayerEmbedding
from ..infrastructure.embedding_client import EmbeddingClient

logger = logging.getLogger(__name__)


class PlayerService:
    """선수 데이터 업로드 및 임베딩 배치 인덱싱 서비스.

    JSONL 등으로 전달된 players 데이터를 정규화해 DB에 저장하고, 임베딩을 생성합니다.
    """

    def __init__(self, player_repository: Optional[PlayerRepository] = None):
        self._player_repository = player_repository
        self.client = EmbeddingClient()
        logger.info(
            "[PlayerService] initialized (port=%s)",
            "injected" if player_repository else "default",
        )

    def _normalize_player_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """원시 선수 데이터를 DB 스키마에 맞게 정규화합니다.

        Args:
            item: 원시 선수 한 건
        Returns:
            정규화된 필드 딕셔너리
        """
        normalized = {}

        # 필드별 타입/길이 정규화
        if "id" in item:
            normalized["id"] = int(item["id"]) if item["id"] is not None else None

        if "team_id" in item:
            normalized["team_id"] = (
                int(item["team_id"]) if item["team_id"] is not None else None
            )

        if "player_name" in item:
            normalized["player_name"] = (
                str(item["player_name"])[:20] if item["player_name"] else None
            )

        if "e_player_name" in item:
            normalized["e_player_name"] = (
                str(item["e_player_name"])[:40] if item["e_player_name"] else None
            )

        if "nickname" in item:
            normalized["nickname"] = (
                str(item["nickname"])[:30] if item["nickname"] else None
            )

        if "join_yyyy" in item:
            normalized["join_yyyy"] = (
                str(item["join_yyyy"])[:10] if item["join_yyyy"] else None
            )

        if "position" in item:
            normalized["position"] = (
                str(item["position"])[:10] if item["position"] else None
            )

        if "back_no" in item:
            normalized["back_no"] = (
                int(item["back_no"]) if item["back_no"] is not None else None
            )

        if "nation" in item:
            normalized["nation"] = str(item["nation"])[:20] if item["nation"] else None

        if "birth_date" in item:
            birth_date = item["birth_date"]
            if birth_date:
                try:
                    # 문자열이면 파싱
                    if isinstance(birth_date, str):
                        normalized["birth_date"] = datetime.strptime(
                            birth_date, "%Y-%m-%d"
                        ).date()
                    else:
                        normalized["birth_date"] = birth_date
                except (ValueError, TypeError):
                    logger.warning(
                        f"[PlayerService] birth_date 파싱 실패: {birth_date}"
                    )
                    normalized["birth_date"] = None
            else:
                normalized["birth_date"] = None

        if "solar" in item:
            normalized["solar"] = str(item["solar"])[:10] if item["solar"] else None

        if "height" in item:
            normalized["height"] = (
                int(item["height"]) if item["height"] is not None else None
            )

        if "weight" in item:
            normalized["weight"] = (
                int(item["weight"]) if item["weight"] is not None else None
            )

        return normalized

    async def _save_players_to_database(
        self, normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """정규화된 선수 목록을 Repository를 통해 DB에 저장합니다.

        Args:
            normalized_items: 정규화된 선수 딕셔너리 목록
        Returns:
            DB 저장 결과 요약
        """
        if self._player_repository:
            logger.info("[PlayerService] Saving via injected repository...")
            db_result = await self._player_repository.upsert_batch(normalized_items)
            await self._player_repository.commit()
        else:
            async with AsyncSessionLocal() as session:
                repository = PlayerRepository(session)
                logger.info("[PlayerService] Saving via default repository...")
                db_result = await repository.upsert_batch(normalized_items)
                await repository.commit()
        logger.info(
            "[PlayerService] DB done: inserted=%s updated=%s errors=%s",
            db_result.get("inserted_count", 0),
            db_result.get("updated_count", 0),
            db_result.get("error_count", 0),
        )

        return db_result

    async def process_players(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """원시 선수 목록을 정규화한 뒤 DB에 저장합니다.

        Args:
            items: 원시 선수 딕셔너리 목록
        Returns:
            처리 결과 요약
        """
        logger.info(f"[PlayerService] 처리할 건수: {len(items)}건")

        # 1. 정규화
        logger.info("[PlayerService] 데이터 정규화 중...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_player_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(
                    f"[PlayerService] 항목 정규화 실패: {item.get('id', 'unknown')} - {e}",
                    exc_info=True,
                )

        logger.info(f"[PlayerService] 정규화 완료: {len(normalized_items)}건")

        # 2. Repository로 DB 저장
        logger.info("[PlayerService] Repository로 DB 저장 중...")
        db_result = await self._save_players_to_database(normalized_items)

        result = {
            "success": True,
            "method": "rule_based",
            "total_items": len(items),
            "normalized_count": len(normalized_items),
            "database_result": db_result,
        }

        logger.info(
            f"[PlayerService] 처리 완료: "
            f"총 {len(items)}건 중 삽입 {db_result['inserted_count']}건 "
            f"갱신 {db_result['updated_count']}건 오류 {db_result['error_count']}건"
        )
        return result

    def _create_player_content(self, player: Player) -> str:
        """선수 정보로 임베딩용 텍스트를 만듭니다.

        Args:
            player: Player ORM 인스턴스

        Returns:
            임베딩용 문자열
        """
        parts = []
        if player.player_name:
            parts.append(player.player_name)
        if player.e_player_name:
            parts.append(player.e_player_name)
        if player.position:
            parts.append(player.position)
        if player.nation:
            parts.append(player.nation)
        if player.back_no is not None:
            parts.append(f"등번호{player.back_no}")
        if player.nickname:
            parts.append(player.nickname)

        return ", ".join(parts) if parts else ""

    async def run_batch_indexing(self, batch_size: int = 100) -> Dict[str, Any]:
        """DB에 있는 모든 선수를 읽어 임베딩을 생성·갱신합니다.

        Args:
            batch_size: 배치 크기 (기본 100)

        Returns:
            인덱싱 결과 요약
        """
        logger.info("[PlayerService] 배치 인덱싱 시작")

        async with AsyncSessionLocal() as session:
            # 전체 선수 조회
            result = await session.execute(select(Player))
            players = result.scalars().all()

            logger.info(f"[PlayerService] 총 {len(players)}명 선수 임베딩 처리 예정")

            processed_count = 0
            error_count = 0
            updated_count = 0
            created_count = 0

            for player in players:
                try:
                    # 임베딩용 텍스트 생성
                    content = self._create_player_content(player)
                    if not content.strip():
                        logger.warning(
                            f"[PlayerService] 선수 ID {player.id} 스킵 (내용 없음)"
                        )
                        continue

                    # 기존 임베딩 조회
                    existing_embedding_result = await session.execute(
                        select(PlayerEmbedding).where(
                            PlayerEmbedding.player_id == player.id
                        )
                    )
                    existing = existing_embedding_result.scalar_one_or_none()

                    # 벡터 생성
                    vector = await self.client.get_embedding(content)
                    embedding_array = np.array(vector, dtype=np.float32)

                    if existing:
                        # 기존 레코드 갱신
                        existing.content = content
                        existing.embedding = embedding_array
                        updated_count += 1
                        logger.debug(f"[PlayerService] 선수 ID {player.id} 임베딩 갱신")
                    else:
                        # 새 임베딩 레코드 생성
                        new_embedding = PlayerEmbedding(
                            player_id=player.id,
                            content=content,
                            embedding=embedding_array,
                        )
                        session.add(new_embedding)
                        created_count += 1
                        logger.debug(f"[PlayerService] 선수 ID {player.id} 임베딩 생성")

                    processed_count += 1

                    # 주기적 커밋 (batch_size마다)
                    if processed_count % batch_size == 0:
                        await session.commit()
                        logger.info(
                            f"[PlayerService] {processed_count}건 처리 중 커밋 "
                            f"(생성: {created_count}, 갱신: {updated_count}, 오류: {error_count})"
                        )

                except Exception as e:
                    error_count += 1
                    logger.error(
                        f"[PlayerService] 선수 ID {player.id} 임베딩 처리 실패: {str(e)}",
                        exc_info=True,
                    )

            # 최종 커밋
            await session.commit()

            result = {
                "success": True,
                "total_players": len(players),
                "processed_count": processed_count,
                "created_count": created_count,
                "updated_count": updated_count,
                "error_count": error_count,
            }

            logger.info(
                f"[PlayerService] 배치 인덱싱 완료: "
                f"총 {len(players)}명 중 {processed_count}명 "
                f"생성 {created_count}건 갱신 {updated_count}건 오류 {error_count}건"
            )

            return result
