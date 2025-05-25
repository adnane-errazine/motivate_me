import os
from http import HTTPStatus
from typing import Any, Sequence, Optional
import json

from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.agents.orchestrator import Orchestrator
from src.data_models import WorkflowState

app = FastAPI()
router = APIRouter()
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
    file_name: Optional[str] = ""
    user_query: Optional[str] = ""
    # user_metadata: Optional[dict] = {}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
) -> JSONResponse:
    """Custom exception handler for handling FastAPI RequestValidationErrors.

    Pydantic models throw RequestValidationErrors when validation errors occur.

    Args:
        _: FastAPI Request object (unused).
        exc (RequestValidationError): The raised RequestValidationError.

    Returns:
        JSONResponse: A JSON response containing information about the validation errors.
    """
    errors: Sequence[dict[str, Any]] = exc.errors()
    print(errors)

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "message": f"An error occurred: {exc.__class__.__name__}",
                "details": [
                    {
                        "loc": ".".join(map(str, error.get("loc") or [])),
                        "error": error.get("msg"),
                    }
                    for error in errors
                ],
            }
        ),
    )


@router.post("/run_workflow/")
async def run_workflow(request: WorkflowRequest):
    try:
        
        # detele the tmp/workflow_state.json file if it exists
        workflow_state_path = os.path.join("tmp", "workflow_state.json")
        if os.path.exists(workflow_state_path):
            os.remove(workflow_state_path)
        
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


app.include_router(router)




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