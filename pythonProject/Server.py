from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
from io import BytesIO
from generador_h5p import process_json_input  # importa la tua funzione
from typing import List, Union, Optional, Any
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse



app = FastAPI()



# Applichiamo il divieto di campi extra a tutti i modelli
class Option(BaseModel):
    model_config = ConfigDict(extra='forbid') # <-- Blocca yipr o altri errori
    text: str
    is_correct: bool
    feedback: str = ""

class Question(BaseModel):
    model_config = ConfigDict(extra='forbid') # <-- Blocca chiavi inventate
    type: str
    question: Any
    distractors: Optional[str] = None
    correct_answer: Optional[bool] = None
    options: Optional[List[Option]] = None
    feedback_correct: Optional[str] = ""
    feedback_incorrect: Optional[str] = ""

class JsonData(BaseModel):
    model_config = ConfigDict(extra='forbid')
    questions: List[Question]

class H5PRequest(BaseModel):
    model_config = ConfigDict(extra='forbid') # <-- Blocca errori nel root (es. "sourxe_name")
    json_data: JsonData
    source_name: str
    title: str
    randomization: bool
    pool_size: int
    pass_percentage: int

@app.post("/generate-h5p")
async def generate_h5p(req: H5PRequest):
    print("DEBUG: request arrivo:", req)
    try:
        # Chiama la tua funzione
        h5p_bytes = process_json_input(
            json_data=req.json_data.model_dump(),
            source_name=req.source_name,
            title=req.title,
            randomization=req.randomization,
            pool_size=req.pool_size,
            pass_percentage=req.pass_percentage
        )

        if not h5p_bytes:
            raise HTTPException(status_code=500, detail="Nessun contenuto generato")

        # Wrappa i bytes in uno stream
        file_stream = BytesIO(h5p_bytes)

        return StreamingResponse(
            file_stream,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="quiz.h5p"'
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_200_OK, # Sempre 200 per non bloccare n8n
        content={
            "is_valid": False,
            "feedback": ["Error de sintaxis en el JSON: el archivo está mal formado (revisa comas dobles o paréntesis)."],
            "error_type": "syntax_error"
        },
    )


@app.post("/validate-h5p-json")
async def validate_json(raw_data: dict = Body(...)):
    try:
        H5PRequest(**raw_data)
        return {
            "is_valid": True,
            "feedback": ["El JSON es perfecto y sigue la estructura H5P."]
        }
    except ValidationError as e:
        lista_errores = []
        for error in e.errors():
            path = " -> ".join([str(x) for x in error['loc']])
            msg = error['msg']

            # Gestione specifica per campi inventati o nomi errati
            if error['type'] == 'extra_forbidden':
                campo_erroneo = error['loc'][-1]
                msg_sp = f"El campo '{campo_erroneo}' no está permitido o está mal escrito. Revisa si quisiste decir 'type' u otro campo válido."
            else:
                # Altre traduzioni come prima
                msg_sp = msg.replace("field required", "campo obligatorio faltante")

            lista_errores.append(f"En [{path}]: {msg_sp}")

        return {
            "is_valid": False,
            "feedback": lista_errores,
            "instrucciones": "Por favor, corrige los errores mencionados y devuelve solo el JSON corregido."
        }