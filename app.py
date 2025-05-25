from fastapi import FastAPI
from src.api import router as workflow_router

app = FastAPI(title="MotivateMe API")
app.include_router(workflow_router)


def main():
    print("Hello from motivate-me!")
    
if __name__ == "__main__":
    pass