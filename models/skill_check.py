from pydantic import BaseModel, Field
from typing import Optional

class SkillCheck(BaseModel):
    skill: str = Field(..., description="Name of the skill being checked")
    difficulty: str = Field(..., description="Difficulty level of the check")
    success: bool = Field(..., description="Whether the check was successful")
    content: str = Field(..., description="The actual dialogue content")
    category: Optional[str] = Field(None, description="Skill category")

    class Config:
        frozen = True
