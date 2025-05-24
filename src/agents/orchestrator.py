import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, TypedDict
from pathlib import Path

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.config import config
from src.data_models import WorkflowState


from src.agents.extract_concepts import AgentConceptsExtractor
from src.agents.find_applications import AgentApplicationsFinder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrator class to manage the LangGraph workflow"""

    def __init__(self):
        _agent_concept_extractor = AgentConceptsExtractor()
        _agent_applications_finder = AgentApplicationsFinder()
        _
        """Initialize the Orchestrator with the agents and workflow"""

        self.workflow = self._build_workflow()
        self._agent_applications_finder = AgentApplicationsFinder()
        self._agent_concept_extractor = AgentConceptsExtractor()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("extract_relevant_concepts", self._agent_concept_extractor.extract_relevant_concepts_node)
        workflow.add_node("find_applications", self._agent_applications_finder.find_applications_node)
        #workflow.add_node("search_application_images", _search_google_images)
        #workflow.add_node("combine_content", self._combine_content_node)

        # Add edges
        
        

    def _agent_concepts_extractor(self):
        """Create an instance of the concepts extractor agent"""
