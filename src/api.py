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
    file_name: Optional[str] = ""
    user_query: Optional[str] = ""
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
    import httpx
    import json
    import os

    async def main():
        file_name = "linear_algebra_1.pdf"
        user_query = "This lecture covers advanced topics in signal processing and Fourier analysis."

        document_path = os.path.join("tmp", file_name)
        if not os.path.exists(document_path):
            print(f"❌ Document not found at: {document_path}")
            return

        payload = {
            "file_name": file_name,
            "user_query": user_query
        }

        api_url = "http://127.0.0.1:8000/run_workflow/"

        # Set a long timeout (e.g., 300 seconds = 5 minutes)
        timeout = httpx.Timeout(300.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                print(f"📡 Sending request to {api_url}")
                response = await client.post(api_url, json=payload)

                print(f"✅ Status code: {response.status_code}")
                print("=== Response ===")
                print(json.dumps(response.json(), indent=2))

            except httpx.RequestError as e:
                print(f"❌ Request failed: {e}")
    async def test_get_workflow_state():
        api_url = "http://   get_workflow_state/"
    asyncio.run(main())









