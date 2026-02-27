from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    in_progress = "in_progress"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"

class ApplicationBase(BaseModel):
    company: str
    role: str
    status: ApplicationStatus = ApplicationStatus.in_progress
    project_id: Optional[int] = None
    cv_id: Optional[int] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None

class ApplicationInDBBase(ApplicationBase):
    id: int
    user_id: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)

class Application(ApplicationInDBBase):
    pass
