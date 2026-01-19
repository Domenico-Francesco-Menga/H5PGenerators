from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from generador_h5p import process_json_input  # importa la tua funzione
from pathlib import Path

app = FastAPI()

class H5PRequest(BaseModel):
    json_data: dict
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
            json_data=req.json_data,
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
