"""
EXAONE ?? ??????? ??????
EXAONE ?????????????????? ?? ????????????? ??????
"""

import logging
from typing import Dict, Any, List

from labzang.apps.product.spokes.agents.base_agent import BaseAgent
from labzang.apps.tools.analysis.verdict_tools import exaone_tools
from labzang.apps.tools.executors.tool_executor import SimpleToolExecutor

logger = logging.getLogger(__name__)


class ExaoneAnalysisAgent(BaseAgent):
    """EXAONE ?? ??????? ??????"""

    def __init__(self):
        super().__init__(
            name="ExaoneAnalysisAgent",
            instruction="EXAONE ?????????? ?????? ??? ?????????? ???????",
            metadata={
                "model": "EXAONE",
                "capabilities": ["email_analysis", "spam_detection", "detailed_analysis", "quick_verdict"],
                "tools": ["exaone_spam_analyzer", "exaone_quick_verdict", "exaone_detailed_analyzer"]
            }
        )
        self.tools = exaone_tools
        self.tool_executor = SimpleToolExecutor(exaone_tools)
        logger.info("EXAONE ?? ?????? ???????")

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        ?????? ??? ??

        Args:
            task: ???????? ("analyze_email")
            context: ??? ????? (???????? ??KoELECTRA ??)

        Returns:
            ?? ?? ??????
        """
        if task == "analyze_email":
            return await self.analyze_email(
                email_subject=context.get("email_subject", ""),
                email_content=context.get("email_content", ""),
                koelectra_result=context.get("koelectra_result", {}),
                analysis_type=context.get("analysis_type", "detailed")
            )
        else:
            raise ValueError(f"????? ??? ???: {task}")

    async def execute_tool(self, tool_name: str, **kwargs) -> str:
        """
        ??? ?????

        Args:
            tool_name: ??????????
            **kwargs: ??? ??????????
        Returns:
            ????? ??

        Raises:
            ValueError: ??? ?? ????? ??
        """
        try:
            # ???????? ????
            tool_map = {tool.name: tool for tool in self.tools}

            if tool_name not in tool_map:
                available_tools = list(tool_map.keys())
                raise ValueError(f"??'{tool_name}'???? ????????. ??? ???? ?? {available_tools}")

            selected_tool = tool_map[tool_name]
            result = await selected_tool.ainvoke(kwargs)

            logger.info(f"??'{tool_name}' ??? ???")
            return result

        except Exception as e:
            logger.error(f"??'{tool_name}' ??? ???: {e}")
            raise

    async def analyze_email(
        self,
        email_subject: str,
        email_content: str,
        koelectra_result: Dict[str, Any],
        analysis_type: str = "detailed"
    ) -> Dict[str, Any]:
        """
        EXAONE??????????????

        Args:
            email_subject: ????????
            email_content: ????????
            koelectra_result: KoELECTRA ?? ??
            analysis_type: ?? ????("detailed" ??? "quick")

        Returns:
            ?? ?? ??????
        """
        try:
            logger.info(f"EXAONE ??????? ???: {analysis_type} ????)

            if analysis_type == "detailed":
                response = await self.execute_tool(
                    "exaone_detailed_analyzer",
                    email_subject=email_subject,
                    email_content=email_content,
                    koelectra_result=koelectra_result
                )
            else:
                email_text = f"{email_subject} {email_content}"
                confidence = koelectra_result.get("confidence", 0.0)
                response = await self.execute_tool(
                    "exaone_quick_verdict",
                    email_text=email_text,
                    koelectra_confidence=confidence
                )

            # ??? ??
            response_lower = response.lower()
            if "???" in response_lower or "??" in response_lower:
                verdict = "spam"
                confidence_adjustment = 0.1
            elif "???" in response_lower or "???" in response_lower:
                verdict = "normal"
                confidence_adjustment = 0.1
            elif "???? in response_lower or "??" in response_lower:
                verdict = "uncertain"
                confidence_adjustment = 0.0
            else:
                # KoELECTRA ?? ???
                verdict = "spam" if koelectra_result.get("is_spam") else "normal"
                confidence_adjustment = 0.05

            result = {
                "agent_name": self.name,
                "verdict": verdict,
                "confidence_adjustment": confidence_adjustment,
                "analysis_type": analysis_type,
                "exaone_response": response,
                "analysis_summary": f"EXAONE ??: {verdict} (???????: +{confidence_adjustment:.2f})",
                "tool_used": "exaone_detailed_analyzer" if analysis_type == "detailed" else "exaone_quick_verdict",
                "execution_time": None  # BaseAgent??? ??? ????            }

            logger.info(f"EXAONE ??????? ???: {verdict}")
            return result

        except Exception as e:
            logger.error(f"EXAONE ??????? ???: {e}")
            raise

    def get_available_tools(self) -> List[str]:
        """??? ???? ???? ??"""
        return [tool.name for tool in self.tools]

    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """??? ??? ??? ??"""
        tool_map = {tool.name: tool for tool in self.tools}

        if tool_name not in tool_map:
            return {"error": f"??'{tool_name}'???? ????????"}

        tool = tool_map[tool_name]
        return {
            "name": tool.name,
            "description": tool.description,
            "args_schema": tool.args_schema.schema() if tool.args_schema else None
        }

    def get_capabilities(self) -> List[str]:
        """?????? ??? ?? ??"""
        return self.metadata.get("capabilities", [])


# ??? EXAONE ?? ?????? ??????
_exaone_analysis_agent: ExaoneAnalysisAgent = None

def get_exaone_analysis_agent() -> ExaoneAnalysisAgent:
    """EXAONE ?? ?????? ???????????? ??????""
    global _exaone_analysis_agent
    if _exaone_analysis_agent is None:
        _exaone_analysis_agent = ExaoneAnalysisAgent()
        logger.info("?????EXAONE ?? ?????? ?????? ???")
    return _exaone_analysis_agent

# ?????? ??? ??
ExaoneAnalysisService = ExaoneAnalysisAgent
get_exaone_analysis_service = get_exaone_analysis_agent

# MCP ?????? ??? ??
MCPAgentWrapper = ExaoneAnalysisAgent

def get_mcp_agent_wrapper() -> ExaoneAnalysisAgent:
    """MCP ?????? ??? ?????? ??????(????????)"""
    return get_exaone_analysis_agent()


# ??????????? ??
def get_workflow_info() -> Dict[str, Any]:
    """??? ?????? ??????????? ??"""
    return {
        "agent_name": "EXAONE Verdict Agent",
        "description": "EXAONE ?? ???????? ???? ??? ??????",
        "workflow_steps": [
            "Initialize Analysis",
            "Generate Prompt",
            "EXAONE Analysis",
            "Verdict Decision",
            "Finalize Verdict"
        ],
        "analysis_types": {
            "detailed": "??? ?? (???????0.8)",
            "quick": "?? ?? (?????> 0.8)"
        },
        "verdict_options": ["spam", "normal", "uncertain"],
        "features": [
            "??????? ???????",
            "??????? ?????? ???",
            "??? ??? ??",
            "??????? ??"
        ]
    }


# MCP ?????? ?? ?????????
async def analyze_email_with_tools(
    email_subject: str,
    email_content: str,
    koelectra_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    ???? ???????? ?? (MCP ??????)

    Args:
        email_subject: ????????
        email_content: ????????
        koelectra_result: KoELECTRA ?? ??

    Returns:
        ??? ?? ??????
    """
    analysis_agent = get_exaone_analysis_agent()

    # ?? ??????
    confidence = koelectra_result.get("confidence", 0.0)
    analysis_type = "quick" if confidence > 0.8 else "detailed"

    # ???? ?? ???
    result = await analysis_agent.analyze_email(
        email_subject=email_subject,
        email_content=email_content,
        koelectra_result=koelectra_result,
        analysis_type=analysis_type
    )

    return result


async def analyze_email_verdict(
    email_subject: str,
    email_content: str,
    koelectra_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    ???????? ?? ?? ??? (?????????? ?????

    Args:
        email_subject: ????????
        email_content: ????????
        koelectra_result: KoELECTRA ?? ??

    Returns:
        ??? ?? ??????
    """
    # ????? ??????????? ??? (????????????
    return await analyze_email_with_tools(email_subject, email_content, koelectra_result)


async def quick_verdict(
    email_text: str,
    koelectra_confidence: float
) -> Dict[str, Any]:
    """?? ??? (???? ??????"""
    from labzang.apps.tools.analysis.verdict_tools import exaone_quick_verdict

    try:
        response = await exaone_quick_verdict.ainvoke({
            "email_text": email_text,
            "koelectra_confidence": koelectra_confidence
        })

        # ??????? ??
        response_lower = response.lower()
        if "???" in response_lower:
            verdict = "spam"
        elif "???" in response_lower:
            verdict = "normal"
        else:
            verdict = "uncertain"

        result = {
            "verdict": verdict,
            "confidence_adjustment": 0.05,
            "analysis_type": "quick",
            "analysis_summary": f"?? ???: {verdict}",
            "exaone_response": response,
            "processing_steps": ["quick_verdict_completed"]
        }

        return result

    except Exception as e:
        logger.error(f"EXAONE ?? ??? ???: {e}")
        raise
