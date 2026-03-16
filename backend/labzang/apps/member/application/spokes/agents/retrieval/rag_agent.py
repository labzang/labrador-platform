"""
RAG ?ì´?„íŠ¸
ê¸°ì¡´ rag_service.pyë¥??ì´?„íŠ¸ë¡?ë³€??"""

from typing import Dict, Any
from labzang.apps.product.spokes.agents.base_agent import BaseAgent


class RAGAgent(BaseAgent):
    """RAG (Retrieval-Augmented Generation) ?ì´?„íŠ¸"""

    def __init__(self):
        super().__init__(
            name="rag_agent",
            instruction="""You are a RAG (Retrieval-Augmented Generation) agent.
            Your role is to:
            1. Retrieve relevant documents for user queries
            2. Generate contextual responses using retrieved information
            3. Combine search results with language model capabilities
            4. Provide accurate, source-backed answers
            """,
            server_names=["filesystem"],  # ë¬¸ì„œ ?‘ê·¼??            metadata={
                "approach": "Retrieval-Augmented Generation",
                "components": ["Vector Search", "LLM Generation"],
                "languages": ["Korean", "English"]
            }
        )

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """RAG ?Œì´?„ë¼???¤í–‰"""
        question = context.get("question", task)
        k = context.get("k", 3)  # ê²€?‰í•  ë¬¸ì„œ ??
        # 1. ë¬¸ì„œ ê²€???¨ê³„
        search_results = await self._retrieve_documents(question, k)

        # 2. ?‘ë‹µ ?ì„± ?¨ê³„
        generated_answer = await self._generate_answer(question, search_results)

        # 3. ê²°ê³¼ êµ¬ì„±
        return {
            "question": question,
            "answer": generated_answer,
            "sources": search_results,
            "retrieved_count": len(search_results),
            "rag_pipeline": {
                "retrieval": "completed",
                "generation": "completed",
                "total_steps": 2
            }
        }

    async def _retrieve_documents(self, question: str, k: int) -> List[Dict[str, Any]]:
        """ë¬¸ì„œ ê²€???¨ê³„"""
        # TODO: ?¤ì œ ë²¡í„° ê²€???µí•©
        # VectorSearchAgentë¥??¸ì¶œ?˜ê±°??ì§ì ‘ vectorstore ?¬ìš©

        # ?„ìž¬??ëª¨í‚¹ êµ¬í˜„
        mock_documents = [
            {
                "content": f"ê²€?‰ëœ ë¬¸ì„œ {i+1}: {question}???€???ì„¸???•ë³´ë¥??¬í•¨?˜ê³  ?ˆìŠµ?ˆë‹¤.",
                "metadata": {
                    "source": f"knowledge_base_{i+1}.md",
                    "relevance_score": 0.85 - (i * 0.1),
                    "section": f"Section {i+1}"
                }
            }
            for i in range(min(k, 3))
        ]

        return mock_documents

    async def _generate_answer(self, question: str, documents: List[Dict[str, Any]]) -> str:
        """?µë? ?ì„± ?¨ê³„"""
        # TODO: ?¤ì œ LLM ?µí•© (EXAONE, OpenAI ??

        # ê²€?‰ëœ ë¬¸ì„œ?¤ì„ ì»¨í…?¤íŠ¸ë¡?êµ¬ì„±
        context = "\n".join([doc["content"] for doc in documents])

        # ?„ìž¬??ê°„ë‹¨???œí”Œë¦?ê¸°ë°˜ ?‘ë‹µ
        if not documents:
            return f"'{question}'???€??ê´€??ë¬¸ì„œë¥?ì°¾ì? ëª»í–ˆ?µë‹ˆ?? ??êµ¬ì²´?ì¸ ì§ˆë¬¸???´ì£¼?œë©´ ?„ì?????ê²?ê°™ìŠµ?ˆë‹¤."

        return f"""'{question}'???€???µë??…ë‹ˆ??

ê²€?‰ëœ {len(documents)}ê°œì˜ ë¬¸ì„œë¥?ë°”íƒ•?¼ë¡œ ?¤ìŒê³?ê°™ì´ ?µë??œë¦½?ˆë‹¤:

{context[:200]}...

???•ë³´ê°€ ?„ì????˜ì…¨?˜ìš”? ???ì„¸???´ìš©???„ìš”?˜ì‹œë©?êµ¬ì²´?ìœ¼ë¡?ì§ˆë¬¸?´ì£¼?¸ìš”."""

    def get_rag_stats(self) -> Dict[str, Any]:
        """RAG ?µê³„ ì¡°íšŒ"""
        return {
            "total_queries": self.execution_count,
            "last_query": self.last_execution.isoformat() if self.last_execution else None,
            "pipeline_components": [
                "Document Retrieval",
                "Context Assembly",
                "Answer Generation",
                "Source Attribution"
            ],
            "supported_formats": ["Text", "Markdown", "JSON"]
        }
