import logging
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

from src.agents.extract_concepts import AgentConceptsExtractor
from src.agents.find_applications import AgentApplicationsFinder
from src.data_models import WorkflowState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrator class to manage the LangGraph workflow"""

    def __init__(self):
        """Initialize the Orchestrator with the agents and workflow"""
        _agent_concept_extractor = AgentConceptsExtractor()
        _agent_applications_finder = AgentApplicationsFinder()

        self.workflow = self._build_workflow()
        self._agent_applications_finder = AgentApplicationsFinder()
        self._agent_concept_extractor = AgentConceptsExtractor()

    def _build_workflow(self) -> Any:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("extract_relevant_concepts", self._agent_concept_extractor.extract_relevant_concepts_node)
        workflow.add_node("find_applications", self._agent_applications_finder.find_applications_node)
        # TODO: add "send_data_to_frontend" node

        # TODO: Add edges

        checkpointer = InMemorySaver()
        graph = workflow.compile(checkpointer=checkpointer)
