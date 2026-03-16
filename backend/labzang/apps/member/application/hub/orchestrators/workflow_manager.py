"""
?Œí¬?Œë¡œ??ë§¤ë‹ˆ?€
?ì´?„íŠ¸?¤ì˜ ?¤í–‰ ?œì„œ?€ ?°ì´???ë¦„??ê´€ë¦?"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from labzang.apps.product.spokes.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class WorkflowManager:
    """?Œí¬?Œë¡œ???¤í–‰ ê´€ë¦¬ì"""

    def __init__(self):
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_workflow(
        self,
        name: str,
        agents: List[BaseAgent],
        execution_type: str = "sequential",
        description: str = ""
    ):
        """?Œí¬?Œë¡œ???±ë¡"""
        self.workflows[name] = {
            "agents": agents,
            "execution_type": execution_type,  # "sequential", "parallel", "conditional"
            "description": description,
            "created_at": datetime.now(),
            "execution_count": 0
        }

        logger.info(f"?Œí¬?Œë¡œ??'{name}' ?±ë¡ ?„ë£Œ ({len(agents)}ê°??ì´?„íŠ¸)")

    async def execute_workflow(
        self,
        name: str,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """?Œí¬?Œë¡œ???¤í–‰"""
        if name not in self.workflows:
            raise ValueError(f"?Œí¬?Œë¡œ??'{name}'??ì°¾ì„ ???†ìŠµ?ˆë‹¤")

        workflow = self.workflows[name]
        context = context or {}

        start_time = datetime.now()
        execution_id = f"{name}_{start_time.strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"?Œí¬?Œë¡œ??'{name}' ?¤í–‰ ?œì‘: {task[:50]}...")

        try:
            # ?¤í–‰ ?€?…ì— ?°ë¥¸ ë¶„ê¸°
            if workflow["execution_type"] == "sequential":
                results = await self._execute_sequential(workflow["agents"], task, context)
            elif workflow["execution_type"] == "parallel":
                results = await self._execute_parallel(workflow["agents"], task, context)
            elif workflow["execution_type"] == "conditional":
                results = await self._execute_conditional(workflow["agents"], task, context)
            else:
                raise ValueError(f"ì§€?í•˜ì§€ ?ŠëŠ” ?¤í–‰ ?€?? {workflow['execution_type']}")

            # ?¤í–‰ ?µê³„ ?…ë°?´íŠ¸
            workflow["execution_count"] += 1
            execution_time = (datetime.now() - start_time).total_seconds()

            # ?¤í–‰ ê¸°ë¡ ?€??            execution_record = {
                "execution_id": execution_id,
                "workflow_name": name,
                "task": task,
                "start_time": start_time,
                "execution_time": execution_time,
                "agent_count": len(workflow["agents"]),
                "status": "completed",
                "results_summary": self._summarize_results(results)
            }
            self.execution_history.append(execution_record)

            logger.info(f"?Œí¬?Œë¡œ??'{name}' ?¤í–‰ ?„ë£Œ ({execution_time:.2f}ì´?")

            return {
                "execution_id": execution_id,
                "workflow_name": name,
                "status": "completed",
                "execution_time": execution_time,
                "agent_results": results,
                "final_context": context,
                "summary": self._generate_execution_summary(name, results, execution_time)
            }

        except Exception as e:
            logger.error(f"?Œí¬?Œë¡œ??'{name}' ?¤í–‰ ?¤ë¥˜: {e}")

            # ?¤ë¥˜ ê¸°ë¡
            execution_record = {
                "execution_id": execution_id,
                "workflow_name": name,
                "task": task,
                "start_time": start_time,
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "status": "error",
                "error": str(e)
            }
            self.execution_history.append(execution_record)

            raise

    async def _execute_sequential(
        self,
        agents: List[BaseAgent],
        task: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """?œì°¨ ?¤í–‰"""
        results = []

        for i, agent in enumerate(agents):
            logger.info(f"?ì´?„íŠ¸ {i+1}/{len(agents)} ?¤í–‰: {agent.name}")

            # ?ì´?„íŠ¸ ?¤í–‰
            result = await agent.run(task, context)
            results.append(result)

            # ?¤ìŒ ?ì´?„íŠ¸ë¥??„í•œ ì»¨í…?¤íŠ¸ ?…ë°?´íŠ¸
            context.update(result)

            # ?¤ë¥˜ ë°œìƒ ??ì¤‘ë‹¨
            if result.get("status") == "error":
                logger.warning(f"?ì´?„íŠ¸ '{agent.name}' ?¤ë¥˜ë¡??Œí¬?Œë¡œ??ì¤‘ë‹¨")
                break

        return results

    async def _execute_parallel(
        self,
        agents: List[BaseAgent],
        task: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """ë³‘ë ¬ ?¤í–‰"""
        logger.info(f"{len(agents)}ê°??ì´?„íŠ¸ ë³‘ë ¬ ?¤í–‰")

        # ëª¨ë“  ?ì´?„íŠ¸ë¥??™ì‹œ???¤í–‰
        tasks = [agent.run(task, context.copy()) for agent in agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # ?ˆì™¸ ì²˜ë¦¬
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "agent": agents[i].name,
                    "status": "error",
                    "error": str(result)
                })
            else:
                processed_results.append(result)

        return processed_results

    async def _execute_conditional(
        self,
        agents: List[BaseAgent],
        task: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """ì¡°ê±´ë¶€ ?¤í–‰ (?„ì¬???œì°¨ ?¤í–‰ê³??™ì¼, ?¥í›„ ?•ì¥)"""
        # TODO: ì¡°ê±´ë¶€ ë¡œì§ êµ¬í˜„
        return await self._execute_sequential(agents, task, context)

    def _summarize_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """ê²°ê³¼ ?”ì•½"""
        total_agents = len(results)
        successful_agents = len([r for r in results if r.get("status") != "error"])
        failed_agents = total_agents - successful_agents

        return {
            "total_agents": total_agents,
            "successful": successful_agents,
            "failed": failed_agents,
            "success_rate": successful_agents / total_agents if total_agents > 0 else 0
        }

    def _generate_execution_summary(
        self,
        workflow_name: str,
        results: List[Dict[str, Any]],
        execution_time: float
    ) -> str:
        """?¤í–‰ ?”ì•½ ?ì„±"""
        summary = self._summarize_results(results)

        return (
            f"?Œí¬?Œë¡œ??'{workflow_name}' ?„ë£Œ: "
            f"{summary['successful']}/{summary['total_agents']} ?ì´?„íŠ¸ ?±ê³µ "
            f"({execution_time:.2f}ì´?"
        )

    def get_workflow_info(self, name: str) -> Optional[Dict[str, Any]]:
        """?Œí¬?Œë¡œ???•ë³´ ì¡°íšŒ"""
        if name not in self.workflows:
            return None

        workflow = self.workflows[name]
        return {
            "name": name,
            "description": workflow["description"],
            "execution_type": workflow["execution_type"],
            "agent_count": len(workflow["agents"]),
            "agents": [agent.name for agent in workflow["agents"]],
            "created_at": workflow["created_at"].isoformat(),
            "execution_count": workflow["execution_count"]
        }

    def list_workflows(self) -> List[Dict[str, Any]]:
        """?±ë¡???Œí¬?Œë¡œ??ëª©ë¡"""
        return [self.get_workflow_info(name) for name in self.workflows.keys()]

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """?¤í–‰ ê¸°ë¡ ì¡°íšŒ"""
        return sorted(
            self.execution_history,
            key=lambda x: x["start_time"],
            reverse=True
        )[:limit]
