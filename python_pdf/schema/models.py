from pydantic import BaseModel
from typing import Optional, Literal, List


class ImageDetails(BaseModel):
    url: str                       
    altText: Optional[str] = None   
    imageType: Literal["question", "option", "table_cell"]
    mappingImageName: str          


class TableCell(BaseModel):                    
    row: int
    col: int
    text: Optional[str] = None
    imageDetails: Optional[ImageDetails] = None


class Table(BaseModel):
    caption: Optional[str] = None
    headers: List[str] = []
    rows: List[List[TableCell]] = []


class Option(BaseModel):
    key: str                
    optionType: Literal["text", "image", "text_and_image"]
    text: Optional[str] = None
    imageDetails: Optional[ImageDetails] = None


class Answer(BaseModel):
    key: Optional[str] = None       
    explanation: Optional[str] = None 


class Question(BaseModel):
    questionText: str
    questionType: Literal[
        "MCQ_SINGLE",
        "MCQ_MULTIPLE",
        "NUMERICAL_INTEGER",
        "NUMERICAL_DECIMAL",
        "MATRIX_MATCH",
        "PARAGRAPH_BASED",
        "ASSERTION_REASON",
        "TRUE_FALSE",
    ]
    options: List[Option] = []
    answer: Answer = Answer()
    hasImage: bool = False         
    imageDetails: List[ImageDetails] = []
    tables: List[Table] = []      
    difficulty: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    topics: List[str] = []
    learningOutcomes: List[str] = []
    setId: Optional[str] = None
    origin: Optional[str] = None