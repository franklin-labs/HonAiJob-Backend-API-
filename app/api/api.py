from fastapi import APIRouter
from app.api.routers import auth, cvs, agents, projects, applications, job_offers

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(cvs.router, prefix="/cvs", tags=["cvs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(job_offers.router, prefix="/job-offers", tags=["job-offers"])
