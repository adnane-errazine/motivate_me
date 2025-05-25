from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
import os

from src.agents.orchestrator import Orchestrator
from src.data_models import WorkflowState
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
