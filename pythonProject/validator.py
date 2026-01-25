from typing import List, Union, Optional, Any
from pydantic import BaseModel, Field

# 1. Modello per le opzioni della scelta multipla
class Option(BaseModel):
    text: str
    is_correct: bool
    feedback: Optional[str] = ""

# 2. Modello per la singola domanda (struttura flessibile)
class Question(BaseModel):
    type: str  # "DragText", "Blank", "TrueFalse", "multichoice"
    question: Union[str, List[str]] # Può essere stringa o lista di stringhe
    distractors: Optional[str] = None
    correct_answer: Optional[bool] = None
    options: Optional[List[Option]] = None
    feedback_correct: Optional[str] = ""
    feedback_incorrect: Optional[str] = ""

# 3. Modello per il contenitore delle domande
class JsonData(BaseModel):
    questions: List[Question]

# 4. Modello principale della richiesta (quello che avevi già, ma potenziato)
class H5PRequest(BaseModel):
    json_data: JsonData # Ora è validato!
    source_name: str
    title: str
    randomization: bool
    pool_size: int
    pass_percentage: int = Field(..., ge=0, le=100) # Validazione: tra 0 e 100