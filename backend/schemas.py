from pydantic import BaseModel
from typing import Optional, List


class SpecialtyOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class AdmissionExamOut(BaseModel):
    id: int
    exam_name: str
    min_score: Optional[str] = None
    max_score: Optional[str] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class AdmissionRequirementOut(BaseModel):
    id: int
    description: Optional[str] = None
    min_gpa: Optional[float] = None
    language_requirement: Optional[str] = None
    exams: List[AdmissionExamOut] = []

    model_config = {"from_attributes": True}


class UniversityListItem(BaseModel):
    id: int
    name: str
    country: str
    city: str
    ranking: Optional[int] = None
    logo_url: Optional[str] = None
    image_url: Optional[str] = None
    tuition_min: Optional[int] = None
    tuition_max: Optional[int] = None
    students_count: Optional[int] = None
    specialties: List[SpecialtyOut] = []

    model_config = {"from_attributes": True}


class UniversityOut(BaseModel):
    id: int
    name: str
    country: str
    city: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    image_url: Optional[str] = None
    website: Optional[str] = None
    ranking: Optional[int] = None
    founded_year: Optional[int] = None
    tuition_min: Optional[int] = None
    tuition_max: Optional[int] = None
    students_count: Optional[int] = None
    specialties: List[SpecialtyOut] = []
    admission: Optional[AdmissionRequirementOut] = None

    model_config = {"from_attributes": True}


class UniversitiesResponse(BaseModel):
    items: List[UniversityListItem]
    total: int
    page: int
    pages: int


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    message: str
    universities: Optional[List[UniversityListItem]] = None
