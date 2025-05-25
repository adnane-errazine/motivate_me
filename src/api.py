from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from src.agents.orchestrator import Orchestrator
from src.data_models import WorkflowState

router = APIRouter()
orchestrator = Orchestrator()


class WorkflowRequest(BaseModel):
    # uuid: str
    file_name: str
    user_query: str
    # user_metadata: Optional[dict] = {}


@router.post("/run_workflow/")
async def run_workflow(request: WorkflowRequest):
    try:
        document_path = os.path.join("tmp", request.file_name)

        if not os.path.exists(document_path):
            raise HTTPException(
                status_code=404, detail=f"Document not found: {document_path}"
            )

        initial_state = WorkflowState(
            uuid="uuid_temporary",
            document_path=document_path,
            text_input=request.user_query,
            user_metadata={},  # request.user_metadata,
            relevant_concepts=[],
            concept_applications={},
            error=None,
        )

        result = await orchestrator.workflow.compile().ainvoke(initial_state)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_workflow_state/")
async def get_workflow_state():
    """ Endpoint to retrieve the tmp/workflow_state.json file."""
    try:
        workflow_state_path = os.path.join("tmp", "workflow_state.json")

        if not os.path.exists(workflow_state_path):
            return {
                "status": "not_found",
                "message": f"Workflow state file not found: {workflow_state_path}"
            }

        with open(workflow_state_path, "r") as file:
            workflow_state = json.load(file)

        return {
            "status": "success",
            "data": workflow_state
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import asyncio
    import json

    async def main():
        # Simulated request data
        file_name = "linear_algebra_1.pdf" #"lecture8-fouriertransforms.pdf"
        user_query = "This lecture covers advanced topics in signal processing and Fourier analysis."

        document_path = os.path.join("tmp", file_name)
        if not os.path.exists(document_path):
            print(f"❌ Document not found at: {document_path}")
            return

        # Create the WorkflowState manually
        state = WorkflowState(
            uuid="test-uuid-main",
            document_path=document_path,
            text_input=user_query,
            user_metadata={"background": "First year engineering student"},
            relevant_concepts=[],
            concept_applications={},
            error=None,
        )

        # Run workflow directly
        print(f"✅ Running workflow on: {document_path}")
        result = await orchestrator.workflow.compile().ainvoke(state)

        print("\n=== Workflow Result ===")
        print(json.dumps(result, indent=2, default=str))

    asyncio.run(main())







