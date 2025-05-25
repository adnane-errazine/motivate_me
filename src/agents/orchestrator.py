# -*- coding: utf-8 -*-
"""Orchestrator for LangGraph workflow with agents
orchestrator.py
"""
import asyncio
import logging


from langgraph.graph import StateGraph, END

from src.data_models import WorkflowState


from src.agents.extract_concepts import AgentConceptsExtractor
from src.agents.find_applications import AgentApplicationsFinder
from src.agents.roadmap_agent import AgentRoadmap
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrator class to manage the LangGraph workflow"""

    def __init__(self):
        """Initialize the Orchestrator with the agents and workflow"""
        
        self._agent_applications_finder = AgentApplicationsFinder()
        self._agent_concept_extractor = AgentConceptsExtractor()
        self._agent_roadmap = AgentRoadmap()

        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node(
            "extract_relevant_concepts",
            self._agent_concept_extractor.extract_relevant_concepts_node,
        )
        workflow.add_node(
            "find_applications", self._agent_applications_finder.find_applications_node
        )
        workflow.add_node(
            "generate_roadmaps", self._generate_roadmaps_wrapper
        )
        # Add edges
        # Define the workflow flow
        workflow.set_entry_point("extract_relevant_concepts")
        
        workflow.add_edge("extract_relevant_concepts", "find_applications")
        workflow.add_edge("find_applications", "generate_roadmaps")
        workflow.add_edge("generate_roadmaps", END)
        return workflow
        
        
    async def _generate_roadmaps_wrapper(self, state: WorkflowState) -> WorkflowState:
        """Generate roadmaps for each application"""
        try:
            if state.get("error"):
                logger.warning("Skipping roadmap generation due to previous error")
                return state
                
            logger.info(f"Starting roadmap generation for workflow {state['uuid']}")
            
            concept_applications = state.get("concept_applications", {})
            roadmaps_generated = 0
            
            # Generate roadmaps for each application
            for concept_name, applications in concept_applications.items():
                
                logger.info(f"Processing applications for concept: {concept_name}")

                for app in applications:
                    try:
                        # Generate roadmap for this application
                        roadmap_state = await self._agent_roadmap.generate_roadmap(
                            state, app["name"]
                        )
                        
                        # Add the roadmap to the application data
                        if "roadmap" in roadmap_state:
                            app["RoadmapData"] = [roadmap_state["roadmap"]]
                            roadmaps_generated += 1
                            logger.info(f"Generated roadmap for {app['name']}")
                        
                        # Small delay to respect rate limits
                        await asyncio.sleep(0.1)
                        
                    except Exception as e:
                        logger.error(f"Error generating roadmap for {app['name']}: {e}")
                        app["RoadmapData"] = None
            
            logger.info(f"Generated {roadmaps_generated} roadmaps total")
            return state
        except Exception as e:
            logger.error(f"Error in roadmap generation: {e}")
            state["error"] = f"Roadmap generation failed: {str(e)}"
            return state
        

if __name__ == "__main__":
    import asyncio
    from src.data_models import WorkflowState

    async def main():
        orchestrator = Orchestrator()

        # Create a test workflow state
        test_state = WorkflowState(
            uuid="test-uuid-orchestrator",
            document_path="tmp/lecture8-fouriertransforms.pdf",
            text_input="This lecture covers advanced topics in signal processing.",
            user_metadata={"background": "First year engineering student"}, # list of interests, career goals, education_level, backgroundn, hobbies.
            relevant_concepts=[],
            concept_applications={},
            error=None,
        )

        # Run the graph directly with this input state
        result_state = await orchestrator.workflow.compile().ainvoke(test_state)

        print("\n=== Orchestrator Workflow Result ===")
        print(f"Status: {result_state.get('workflow_summary', {}).get('status', 'N/A')}")
        print(f"Concepts Extracted: {len(result_state.get('relevant_concepts', []))}")
        print(f"Applications Found: {sum(len(apps) for apps in result_state.get('concept_applications', {}).values())}")
        print("Printing result state:")
        print(result_state)
        if result_state.get("error"):
            print(f"\nError: {result_state['error']}")

    asyncio.run(main())
