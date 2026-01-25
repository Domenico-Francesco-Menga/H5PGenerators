import json
import uuid
import logging

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
log = logging.getLogger("h5p_cli")
def load_json_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

'''def readJsonTemp(filepath):
    TemplateJson = dict()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            TemplateJson = json.load(file)

            return TemplateJson
    except FileNotFoundError:
        log.error(f"Error: file '{filepath}' not found.")
    except json.JSONDecodeError:
        log.error(f"Error: file '{filepath}' not found.")
'''

def generate_uuid():
    return str(uuid.uuid4())


'''def mapBlank(question):
    """Mapea una pregunta Drag text de tu JSON al formato H5P.drag text."""

    try:
        h5p_question = readJsonTemp(r"")
        #correct_answer = question.get("correct_answer", False)
        #feedback_correct = question.get("feedback_correct", "")
        #eedback_incorrect = question.get("feedback_incorrect", "")
        questions = ",".join(question["question"]) #join all elements in question because  question section of a fill in the blank type need a list

        h5p_question = {
            "library": "H5P.Blanks 1.14",
            "params": {
                "media": {
                    "disableImageZooming": False
                },
                "text": "<p>Fill in the missing words</p>",
                "overallFeedback": [
                    {
                        "from": 0,
                        "to": 100
                    }
                ],
                "showSolutions": "Show solution",
                "tryAgain": "Retry",
                "checkAnswer": "Check",
                "submitAnswer": "Submit",
                "notFilledOut": "Please fill in all blanks to view solution",
                "answerIsCorrect": "':ans' is correct",
                "answerIsWrong": "':ans' is wrong",
                "answeredCorrectly": "Answered correctly",
                "answeredIncorrectly": "Answered incorrectly",
                "solutionLabel": "Correct answer:",
                "inputLabel": "Blank input @num of @total",
                "inputHasTipLabel": "Tip available",
                "tipLabel": "Tip",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "autoCheck": False,
                    "caseSensitive": False,
                    "showSolutionsRequiresInput": True,
                    "separateLines": False,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "acceptSpellingErrors": False
                },
                "scoreBarLabel": "You got :num out of :total points",
                "a11yCheck": "Check the answers. The responses will be marked as correct, incorrect, or unanswered.",
                "a11yShowSolution": "Show the solution. The task will be marked with its correct solution.",
                "a11yRetry": "Retry the task. Reset all responses and start the task over again.",
                "a11yCheckingModeHeader": "Checking mode",
                "confirmCheck": {
                    "header": "Finish ?",
                    "body": "Are you sure you wish to finish ?",
                    "cancelLabel": "Cancel",
                    "confirmLabel": "Finish"
                },
                "confirmRetry": {
                    "header": "Retry ?",
                    "body": "Are you sure you wish to retry ?",
                    "cancelLabel": "Cancel",
                    "confirmLabel": "Confirm"
                },
                "questions": [questions]
            },
            "metadata": {
                "contentType": "Fill in the Blanks",
                "license": "U",
                "title": "Untitled Fill in the Blanks",
                "authors": [],
                "changes": [],
                "extraTitle": "Untitled Fill in the Blanks"
            },
            "subContentId": generate_uuid()
        }
        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando TrueFalse: {e}")
        return {}
'''


def mapBlank(question_data):
    """Mapea una pregunta al formato H5P leggendo il template da JSON."""
    try:

        h5p_question = load_json_template('templates/template_blanks.json')

        text_with_blanks = ",".join(question_data["question"])
        h5p_question["params"]["questions"] = [text_with_blanks]
        h5p_question["subContentId"] = generate_uuid()
        if "title" in question_data:
            h5p_question["metadata"]["title"] = question_data["title"]

        return h5p_question

    except Exception as e:
        print(f"Error mapeando Blanks: {e}")
        return {}


'''def mapDragText(question):
    """Mapea una pregunta Drag text de tu JSON al formato H5P.drag text."""
    try:
        #correct_answer = question.get("correct_answer", False)
        #feedback_correct = question.get("feedback_correct", "")
        #feedback_incorrect = question.get("feedback_incorrect", "")

        h5p_question = {
            "library": "H5P.DragText 1.10",
            "params": {
                "media": {
                    "disableImageZooming": False
                },
                "taskDescription": "<p>Drag the words into the correct boxes</p>",
                "overallFeedback": [
                    {
                        "from": 0,
                        "to": 100
                    }
                ],
                "checkAnswer": "Check",
                "submitAnswer": "Submit",
                "tryAgain": "Retry",
                "showSolution": "Show solution",
                "dropZoneIndex": "Drop Zone @index.",
                "empty": "Drop Zone @index is empty.",
                "contains": "Drop Zone @index contains draggable @draggable.",
                "ariaDraggableIndex": "@index of @count draggables.",
                "tipLabel": "Show tip",
                "correctText": "Correct!",
                "incorrectText": "Incorrect!",
                "resetDropTitle": "Reset drop",
                "resetDropDescription": "Are you sure you want to reset this drop zone?",
                "grabbed": "Draggable is grabbed.",
                "cancelledDragging": "Cancelled dragging.",
                "correctAnswer": "Correct answer:",
                "feedbackHeader": "Feedback",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "instantFeedback": False
                },
                "scoreBarLabel": "You got :num out of :total points",
                "a11yCheck": "Check the answers. The responses will be marked as correct, incorrect, or unanswered.",
                "a11yShowSolution": "Show the solution. The task will be marked with its correct solution.",
                "a11yRetry": "Retry the task. Reset all responses and start the task over again.",
                "textField": question.get("question", "No se ha planteado ninguna pregunta."),
                "distractors": question.get("distractors", "No se ha planteado ninguna pregunta."),
            },
            "metadata": {
                "contentType": "Drag the Words",
                "license": "U",
                "title": "Untitled Drag the Words",
                "authors": [

                ],
                "changes": [

                ],
                "extraTitle": "Untitled Drag the Words"
            },
            "subContentId": generate_uuid()
        }

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando TrueFalse: {e}")
        return {}'''


'''def map_multiple_choice(question):
    """Mapea una pregunta MultipleChoice de tu JSON al formato H5P.MultiChoice."""
    try:
        h5p_question = {
            "library": "H5P.MultiChoice 1.16",
            "params": {
                "question": question.get("question", "No se ha planteado ninguna pregunta."),
                "answers": [],
                "behaviour": {
                    "singleAnswer": True,
                    "enableRetry": False,
                    "enableSolutionsButton": False,
                    "enableCheckButton": True,
                    "type": "auto",
                    "singlePoint": False,
                    "randomAnswers": True,
                    "showSolutionsRequiresInput": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "passPercentage": 100,
                    "showScorePoints": True
                },
                "media": {
                    "disableImageZooming": False
                },
                "overallFeedback": [
                    {
                        "from": 0,
                        "to": 100
                    }
                ],
                "UI": {
                    "checkAnswerButton": "Verificar respuesta",
                    "submitAnswerButton": "Enviar",
                    "showSolutionButton": "Mostrar solución",
                    "tryAgainButton": "Reintentar",
                    "tipsLabel": "Mostrar pista",
                    "scoreBarLabel": "Has conseguido :num de :total puntos.",
                    "tipAvailable": "Pista disponible",
                    "feedbackAvailable": "Retroalimentación disponible",
                    "readFeedback": "Leer retroalimentación",
                    "wrongAnswer": "Respuesta incorrecta",
                    "correctAnswer": "Respuesta correcta",
                    "shouldCheck": "Se debería haber seleccionado",
                    "shouldNotCheck": "No se debería haber seleccionado",
                    "noInput": "Por favor contesta antes de ver la solución",
                    "a11yCheck": "Comprueba las respuestas. Las selecciones serán marcadas como correctas, incorrectas o faltantes.",
                    "a11yShowSolution": "Mostrar la solución. Las respuestas correctas se indican en la tarea.",
                    "a11yRetry": "Reintentar la tarea. Todos los intentos se resetearán y la tarea se iniciará de nuevo."
                },
                "confirmCheck": {
                    "header": "¿Terminar?",
                    "body": "¿Seguro que quieres terminar?",
                    "cancelLabel": "Cancelar",
                    "confirmLabel": "Terminar"
                },
                "confirmRetry": {
                    "header": "¿Reintentar?",
                    "body": "¿Seguro que quieres reintentar?",
                    "cancelLabel": "Cancelar",
                    "confirmLabel": "Confirmar"
                }
            },
            "subContentId": generate_uuid(),
            "metadata": {
                "contentType": "Multiple Choice",
                "license": "U",
                "title": "Multiple Choice",
                "authors": [],
                "changes": [],
                "extraTitle": "Multiple Choice"
            }
        }

        options = question.get("options", [])
        if not isinstance(options, list):
            log.warning("'options' no es una lista en una MultipleChoice. Se omiten respuestas.")
            return h5p_question

        for option in options:
            answer = {
                "text": option.get("text", ""),
                "correct": option.get("is_correct", False),
                "tipsAndFeedback": {
                    "tip": "",
                    "chosenFeedback": f"<div>{option.get('feedback', '')}</div>\n",
                    "notChosenFeedback": ""
                }
            }
            h5p_question["params"]["answers"].append(answer)

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando MultipleChoice: {e}")
        return {}
'''


def map_multiple_choice(question_data):
    """Mapea una domanda MultipleChoice usando un template JSON esterno."""
    try:
        h5p_question = load_json_template('templates/template_multichoice.json')
        h5p_question["params"]["question"] = question_data.get("question", "No se ha planteado ninguna pregunta.")
        h5p_question["subContentId"] = generate_uuid()
        options = question_data.get("options", [])
        if not isinstance(options, list):
            return h5p_question

        for option in options:
            answer = {
                "text": option.get("text", ""),
                "correct": option.get("is_correct", False),
                "tipsAndFeedback": {
                    "tip": "",
                    "chosenFeedback": f"<div>{option.get('feedback', '')}</div>\n",
                    "notChosenFeedback": ""
                }
            }
            h5p_question["params"]["answers"].append(answer)

        if "title" in question_data:
            h5p_question["metadata"]["title"] = question_data["title"]
            h5p_question["metadata"]["extraTitle"] = question_data["title"]

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando MultipleChoice: {e}")
        return {}


def mapDragText(question):
    """Mapea una pregunta Drag text usando un template JSON externo."""
    try:

        h5p_question = load_json_template('templates/template_dragtext.json')
        text_field = question.get("question", "No se ha planteado ninguna pregunta.")
        distractors = question.get("distractors", "")
        h5p_question["params"]["textField"] = text_field
        h5p_question["params"]["distractors"] = distractors
        h5p_question["subContentId"] = generate_uuid()
        if "title" in question:
            h5p_question["metadata"]["title"] = question["title"]
            h5p_question["metadata"]["extraTitle"] = question["title"]

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando DragText: {e}")
        return {}



'''def map_true_false(question):
    """Mapea una pregunta True/False de tu JSON al formato H5P.TrueFalse."""
    try:
        correct_answer = question.get("correct_answer", False)
        feedback_correct = question.get("feedback_correct", "")
        feedback_incorrect = question.get("feedback_incorrect", "")

        h5p_question = {
            "library": "H5P.TrueFalse 1.8",
            "params": {
                "question": question.get("question", "No se ha planteado ninguna pregunta."),
                "correct": "true" if correct_answer else "false",
                "behaviour": {
                    "enableRetry": False,
                    "enableSolutionsButton": False,
                    "enableCheckButton": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "feedbackOnCorrect": feedback_correct,
                    "feedbackOnWrong": feedback_incorrect
                },
                "media": {
                    "disableImageZooming": False
                },
                "l10n": {
                    "trueText": "Verdadero",
                    "falseText": "Falso",
                    "score": "Has conseguido @score de @total puntos.",
                    "checkAnswer": "Verificar",
                    "submitAnswer": "Enviar",
                    "showSolutionButton": "Mostrar solución",
                    "tryAgain": "Reintentar",
                    "wrongAnswerMessage": "Respuesta incorrecta",
                    "correctAnswerMessage": "Respuesta correcta",
                    "scoreBarLabel": "Has conseguido :num de :total puntos.",
                    "a11yCheck": "Comprueba las respuestas. La respuesta será marcada como correcta, incorrecta o sin responder.",
                    "a11yShowSolution": "Mostrar la solución. La respuesta correcta se indicará en la tarea.",
                    "a11yRetry": "Reintentar la tarea. Todos los intentos se reiniciarán, y la tarea se iniciará de nuevo."
                },
                "confirmCheck": {
                    "header": "¿Terminar?",
                    "body": "¿Seguro que quieres terminar?",
                    "cancelLabel": "Cancelar",
                    "confirmLabel": "Terminar"
                },
                "confirmRetry": {
                    "header": "¿Reintentar?",
                    "body": "¿Seguro que quieres reintentar?",
                    "cancelLabel": "Cancelar",
                    "confirmLabel": "Confirmar"
                }
            },
            "subContentId": generate_uuid(),
            "metadata": {
                "contentType": "Pregunta Verdadero/Falso",
                "license": "U",
                "title": "Verdadero/Falso",
                "authors": [],
                "changes": [],
                "extraTitle": "Verdadero/Falso"
            }
        }

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando TrueFalse: {e}")
        return {}'''


def map_true_false(question_data):
    """Mapea una pregunta True/False usando un template JSON esterno."""
    try:

        h5p_question = load_json_template('templates/template_truefalse.json')
        correct_answer = question_data.get("correct_answer", False)
        params = h5p_question["params"]
        params["question"] = question_data.get("question", "No se ha planteado ninguna pregunta.")
        params["correct"] = "true" if correct_answer else "false"
        params["behaviour"]["feedbackOnCorrect"] = question_data.get("feedback_correct", "")
        params["behaviour"]["feedbackOnWrong"] = question_data.get("feedback_incorrect", "")
        h5p_question["subContentId"] = generate_uuid()
        if "title" in question_data:
            h5p_question["metadata"]["title"] = question_data["title"]
            h5p_question["metadata"]["extraTitle"] = question_data["title"]

        return h5p_question

    except Exception as e:
        log.error(f"Error mapeando TrueFalse: {e}")
        return {}
