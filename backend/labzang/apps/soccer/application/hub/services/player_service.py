"""?? ??? ?? ?? ???"""
import logging
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output import PlayerRepositoryPort
from labzang.apps.soccer.hub.repositories.player_repository import PlayerRepository
from labzang.apps.soccer.models.bases.players import Player
from labzang.apps.soccer.models.bases.player_embeddings import PlayerEmbedding
from ..infrastructure.embedding_client import EmbeddingClient
logger = logging.getLogger(__name__)


class PlayerService:
    """?? ???? ?? ???? ???? ???.

    JSONL ???? players ???? ???? ?? ?? ??? ?????.
    """

    def __init__(self, player_repository: Optional[PlayerRepositoryPort] = None):
        self._player_repository = player_repository
        self.client = EmbeddingClient()
        logger.info("[PlayerService] initialized (port=%s)", "injected" if player_repository else "default")

    def _normalize_player_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """?? ???? ??????.

        Args:
            item: ?? ?? ???
        Returns:
            ???? ?? ???
        """
        normalized = {}

        # ?? ?? ? ??
        if "id" in item:
            normalized["id"] = int(item["id"]) if item["id"] is not None else None

        if "team_id" in item:
            normalized["team_id"] = int(item["team_id"]) if item["team_id"] is not None else None

        if "player_name" in item:
            normalized["player_name"] = str(item["player_name"])[:20] if item["player_name"] else None

        if "e_player_name" in item:
            normalized["e_player_name"] = str(item["e_player_name"])[:40] if item["e_player_name"] else None

        if "nickname" in item:
            normalized["nickname"] = str(item["nickname"])[:30] if item["nickname"] else None

        if "join_yyyy" in item:
            normalized["join_yyyy"] = str(item["join_yyyy"])[:10] if item["join_yyyy"] else None

        if "position" in item:
            normalized["position"] = str(item["position"])[:10] if item["position"] else None

        if "back_no" in item:
            normalized["back_no"] = int(item["back_no"]) if item["back_no"] is not None else None

        if "nation" in item:
            normalized["nation"] = str(item["nation"])[:20] if item["nation"] else None

        if "birth_date" in item:
            birth_date = item["birth_date"]
            if birth_date:
                try:
                    # ???? ??? ??
                    if isinstance(birth_date, str):
                        normalized["birth_date"] = datetime.strptime(birth_date, "%Y-%m-%d").date()
                    else:
                        normalized["birth_date"] = birth_date
                except (ValueError, TypeError):
                    logger.warning(f"[???] ??? ?? ?? ??: {birth_date}")
                    normalized["birth_date"] = None
            else:
                normalized["birth_date"] = None

        if "solar" in item:
            normalized["solar"] = str(item["solar"])[:10] if item["solar"] else None

        if "height" in item:
            normalized["height"] = int(item["height"]) if item["height"] is not None else None

        if "weight" in item:
            normalized["weight"] = int(item["weight"]) if item["weight"] is not None else None

        return normalized

    async def _save_players_to_database(
        self,
        normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """???? ?? ????? Repository? ?? DB? ?????.

        Args:
            normalized_items: ???? ?? ??? ???
        Returns:
            ?? ?? ????
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
        """?? ???? ?? ???? ???? DB? ?????.

        Args:
            items: ??? ?? ??? ???
        Returns:
            ?? ?? ????
        """
        logger.info(f"[???] ?? ?? ?? ??: {len(items)}?")

        # 1. ??? ???
        logger.info("[???] ??? ??? ??...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_player_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(f"[???] ??? ??? ??: {item.get('id', 'unknown')} - {e}", exc_info=True)

        logger.info(f"[???] ??? ??: {len(normalized_items)}?")

        # 2. Repository? ?? DB ??
        logger.info("[???] Repository? ?? DB ?? ??...")
        db_result = await self._save_players_to_database(normalized_items)

        result = {
            "success": True,
            "method": "rule_based",
            "total_items": len(items),
            "normalized_count": len(normalized_items),
            "database_result": db_result,
        }

        logger.info(
            f"[???] ?? ?? ?? ??: "
            f"?{len(items)}? ? ?? {db_result['inserted_count']}? "
            f"???? {db_result['updated_count']}? ?? {db_result['error_count']}?"
        )
        return result

    def _create_player_content(self, player: Player) -> str:
        """?? ??? ???? ???? ?????.

        Args:
            player: Player ?? ????

        Returns:
            ??? ???
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
            parts.append(f"???{player.back_no}")
        if player.nickname:
            parts.append(player.nickname)

        return ", ".join(parts) if parts else ""

    async def run_batch_indexing(self, batch_size: int = 100) -> Dict[str, Any]:
        """DB? ?? ?? ??? ?? ??? ???? ?????.

        Args:
            batch_size: ?? ?? (?? 100)

        Returns:
            ?? ?? ????
        """
        logger.info("[???] ?? ??? ??")

        async with AsyncSessionLocal() as session:
            # ?? ?? ??? ??
            result = await session.execute(select(Player))
            players = result.scalars().all()

            logger.info(f"[???] ?{len(players)}?? ?? ??? ?? ??")

            processed_count = 0
            error_count = 0
            updated_count = 0
            created_count = 0

            for player in players:
                try:
                    # ?? ??? ??? ??
                    content = self._create_player_content(player)
                    if not content.strip():
                        logger.warning(f"[???] ? ID {player.id} ?? (?? ??)")
                        continue

                    # ?? ??? ??
                    existing_embedding_result = await session.execute(
                        select(PlayerEmbedding).where(PlayerEmbedding.player_id == player.id)
                    )
                    existing = existing_embedding_result.scalar_one_or_none()

                    # ??? ??
                    vector = await self.client.get_embedding(content)
                    embedding_array = np.array(vector, dtype=np.float32)

                    if existing:
                        # ???? ????
                        existing.content = content
                        existing.embedding = embedding_array
                        updated_count += 1
                        logger.debug(f"[???] ?? ID {player.id} ???? ??")
                    else:
                        # ??? ?? ??
                        new_embedding = PlayerEmbedding(
                            player_id=player.id,
                            content=content,
                            embedding=embedding_array
                        )
                        session.add(new_embedding)
                        created_count += 1
                        logger.debug(f"[???] ?? ID {player.id} ?? ??")

                    processed_count += 1

                    # ??? ?? (batch_size??)
                    if processed_count % batch_size == 0:
                        await session.commit()
                        logger.info(
                            f"[???] {processed_count}? ?? ? ?? "
                            f"(??: {created_count}, ????: {updated_count}, ??: {error_count})"
                        )

                except Exception as e:
                    error_count += 1
                    logger.error(
                        f"[???] ?? ID {player.id} ?? ? ??: {str(e)}",
                        exc_info=True
                    )

            # ?? ??
            await session.commit()

            result = {
                "success": True,
                "total_players": len(players),
                "processed_count": processed_count,
                "created_count": created_count,
                "updated_count": updated_count,
                "error_count": error_count
            }

            logger.info(
                f"[???] ?? ??? ??: "
                f"?{len(players)}? ? {processed_count}? "
                f"?? {created_count}? ???? {updated_count}? ?? {error_count}?"
            )

            return result
