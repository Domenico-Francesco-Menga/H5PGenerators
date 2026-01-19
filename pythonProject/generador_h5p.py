#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import zipfile
import io
import logging
from pathlib import Path
import sys
import GenFunctions #file che ho creato io

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
log = logging.getLogger("h5p_cli")


def map_questions_to_h5p(llm_questions, source_name):
    """Itera la lista de preguntas y las mapea según el tipo."""
    h5p_questions = []
    for idx, q in enumerate(llm_questions, start=1):
        q_type = str(q.get("type", "")).strip().upper()
        if q_type == "MULTICHOICE":
            h5p_q = GenFunctions.map_multiple_choice(q)
        elif q_type == "TRUEFALSE":
            h5p_q = GenFunctions.map_true_false(q)
        elif q_type == "DRAGTEXT":
            h5p_q = GenFunctions.mapDragText(q)
        elif q_type == "BLANK":
            h5p_q = GenFunctions.mapBlank(q)
        else:
            log.warning(f"Tipo no soportado '{q_type}' en '{source_name}'. Se salta pregunta #{idx}.")
            continue

        if h5p_q:
            h5p_questions.append(h5p_q)

    log.info(f"Mapeadas {len(h5p_questions)} preguntas desde '{source_name}'.")
    return h5p_questions


def create_h5p_content(questions, title, randomization, pool_size, pass_percentage):
    """Crea el JSON de H5P.QuestionSet (content/content.json)."""
    # ajustar pool_size a la cantidad de preguntas
    pool_size = max(1, min(pool_size, len(questions)))

    h5p_content = {
        "introPage": {
            "showIntroPage": True,
            "startButtonText": "Iniciar Quiz",
            "title": title,
            "introduction": (
                "<p style=\"text-align:center\"><strong>Inicie el Quiz para poner a prueba sus conocimientos.</strong></p>"
                "<p style=\"text-align:center\"> </p>"
                f"<p style=\"text-align:center\"> <strong>Por ronda se mostrarán aleatoriamente {pool_size} preguntas.</strong></p>"
                "<p style=\"text-align:center\"><strong>Repita el ejercicio para responder más preguntas.</strong></p>"
            ),
            "backgroundImage": {
                # Usa la imagen que ya tenga la plantilla
                "path": "images/file-_jmSDW4b9EawjImv.png",
                "mime": "image/png",
                "copyright": {
                    "license": "U"
                },
                "width": 52,
                "height": 52
            }
        },
        "progressType": "textual",
        "passPercentage": pass_percentage,
        "disableBackwardsNavigation": True,
        "randomQuestions": randomization,
        "endGame": {
            "showResultPage": True,
            "showSolutionButton": True,
            "showRetryButton": True,
            "noResultMessage": "Quiz finalizado",
            "message": "Tu resultado:",
            "scoreBarLabel": "Has conseguido @score de @total puntos.",
            "overallFeedback": [
                {
                    "from": 0,
                    "to": 50,
                    "feedback": "¡No hay de qué preocuparse! Consejo: revisa las soluciones antes de empezar la próxima ronda."
                },
                {
                    "from": 51,
                    "to": 75,
                    "feedback": "Ya sabes bastante sobre el tema. Con cada repetición puedes mejorar."
                },
                {
                    "from": 76,
                    "to": 100,
                    "feedback": "¡Bien hecho!"
                }
            ],
            "solutionButtonText": "Mostrar solución",
            "retryButtonText": "Siguiente ronda",
            "finishButtonText": "Finalizar",
            "submitButtonText": "Enviar",
            "showAnimations": False,
            "skippable": False,
            "skipButtonText": "Omitir video"
        },
        "override": {
            "checkButton": True
        },
        "texts": {
            "prevButton": "Anterior",
            "nextButton": "Siguiente",
            "finishButton": "Finalizar",
            "submitButton": "Enviar",
            "textualProgress": "Pregunta @current de @total",
            "jumpToQuestion": "Pregunta %d de %total",
            "questionLabel": "Pregunta",
            "readSpeakerProgress": "Pregunta @current de @total",
            "unansweredText": "Sin responder",
            "answeredText": "Respondido",
            "currentQuestionText": "Pregunta actual",
            "navigationLabel": "Preguntas"
        },
        "poolSize": pool_size,
        "questions": questions
    }
    return h5p_content


def clean_json_content(content_str):
    """Reemplaza ß por ss y valida que siga siendo JSON válido."""
    try:
        cleaned_content = content_str.replace('ß', 'ss')
        json.loads(cleaned_content)
        return cleaned_content
    except json.JSONDecodeError as e:
        log.error(f"JSON inválido tras limpieza: {e}")
        return None
    except Exception as e:
        log.error(f"Error inesperado limpiando JSON: {e}")
        return None


def create_h5p_package(content_json_str, template_zip_path, title):
    """
    Crea el .h5p:
    - Copia la plantilla tal cual.
    - Sustituye solo content/content.json.
    - Genera h5p.json con título dinámico.
    """
    i = 0
    try:
        if not template_zip_path.exists():
            log.error(f"No se encontró la plantilla: {template_zip_path}")
            return None
        template_bytes = template_zip_path.read_bytes()

        with zipfile.ZipFile(io.BytesIO(template_bytes), 'r') as template_zip:
            in_memory_zip = io.BytesIO()
            with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                # Copiar todo desde la plantilla
                for item in template_zip.infolist():
                    file_data = template_zip.read(item.filename)
                    new_zip.writestr(item, file_data)

                # content.json
                new_zip.writestr('content/content.json', content_json_str.encode('utf-8'))

                # h5p.json
                h5p_content = {
                    "embedTypes": ["iframe"],
                    "language": "es",
                    "license": "U",
                    "extraTitle": title,
                    "title": title,
                    "mainLibrary": "H5P.QuestionSet",
                    "preloadedDependencies": [
                        {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                        {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                        {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                        {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                        {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                        {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6},
                        {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20}
                    ],
                    "defaultLanguage": "es"
                }

                h5p_json_str = json.dumps(h5p_content, indent=4)
                new_zip.writestr('h5p.json', h5p_json_str.encode('utf-8'))

        in_memory_zip.seek(0)
        return in_memory_zip.getvalue()

    except Exception as e:
        log.error(f"Error creando paquete H5P: {e}")
        return None


def process_json_input(json_data, source_name, title,
                       randomization, pool_size, pass_percentage):
    """Pipeline: JSON → preguntas → QuestionSet → content.json → .h5p (bytes)."""

    BASE_DIR = Path(__file__).resolve().parent
    zip_path = BASE_DIR / "MC_TF.zip"
    try:
        template_zip_path = Path(zip_path)
        if not isinstance(json_data, dict):
            log.error(f"Se esperaba un objeto JSON, recibido: {type(json_data).__name__}")
            return None

        questions = json_data.get("questions", [])
        if not isinstance(questions, list):
            log.error(f"'questions' debería ser lista en '{source_name}', recibido: {type(questions).__name__}")
            return None

        if not questions:
            log.error(f"No se encontraron preguntas en '{source_name}'.")
            return None

        h5p_questions = map_questions_to_h5p(questions, source_name)
        if not h5p_questions:
            log.error(f"No se mapearon preguntas válidas en '{source_name}'.")
            return None

        h5p_content = create_h5p_content(h5p_questions, title, randomization, pool_size, pass_percentage)
        h5p_content_str = json.dumps(h5p_content, ensure_ascii=False, indent=4)

        cleaned_content = clean_json_content(h5p_content_str)
        if not cleaned_content:
            log.error("Falló la limpieza/validación del JSON final.")
            return None

        base_name = Path(title).stem if isinstance(title, str) else "H5P_Content"
        h5p_package_bytes = create_h5p_package(cleaned_content, template_zip_path, base_name)

        if not h5p_package_bytes:
            log.error(f"Fallo al crear el paquete .h5p para '{source_name}'.")
            return None
        return h5p_package_bytes

    except Exception as e:
        log.error(f"Error procesando '{source_name}': {e}")
        return None

