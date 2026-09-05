import os
import shutil


def integrate_backend(
    backend_path,
    ai_path,
    backend_contract,
    ai_contract,
    mappings
):
    output_dir = "generated/integrated_project"

    # Remove old generated project
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(
        os.path.join(output_dir, "backend"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(output_dir, "ai_service"),
        exist_ok=True
    )

    # ----------------------------
    # Copy AI service
    # ----------------------------

    with open(ai_path, "r", encoding="utf-8") as file:
        ai_source = file.read()

    with open(
        os.path.join(
            output_dir,
            "ai_service",
            "main.py"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(ai_source)

    # ----------------------------
    # Read backend
    # ----------------------------

    with open(backend_path, "r", encoding="utf-8") as file:
        backend_source = file.read()

    backend_function = backend_contract["function"]
    backend_path_value = backend_contract["path"]

    # Find backend endpoint function
    function_marker = f"def {backend_function}("

    function_index = backend_source.find(
        function_marker
    )

    if function_index == -1:
        raise ValueError(
            "Could not find backend endpoint function"
        )

    # Find original decorator
    decorator_marker = f'@app.post("{backend_path_value}")'

    decorator_index = backend_source.find(
        decorator_marker
    )

    if decorator_index == -1:
        raise ValueError(
            "Could not find backend POST decorator"
        )

    # Keep everything before the original endpoint
    backend_prefix = backend_source[:decorator_index]

    # ----------------------------
    # Generate integrated endpoint
    # ----------------------------

    integrated_endpoint = f'''@app.post("{backend_path_value}")
def {backend_function}(request: PredictionRequest):

    result = call_ai_service(request)

    return PredictionResponse(
        prediction=result["prediction"],
        confidence=result["confidence"]
    )
'''

    # ----------------------------
    # Add glue import
    # ----------------------------

    integrated_backend = (
        "from integration_glue import call_ai_service\n\n"
        + backend_prefix
        + integrated_endpoint
    )

    backend_main_path = os.path.join(
        output_dir,
        "backend",
        "main.py"
    )

    with open(
        backend_main_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(integrated_backend)

    # ----------------------------
    # Generate glue code
    # ----------------------------

    request_mapping = {}
    response_mapping = {}

    for mapping in mappings:

        if mapping["direction"] == "request":
            request_mapping[
                mapping["ai_service"]
            ] = mapping["backend"]

        elif mapping["direction"] == "response":
            response_mapping[
                mapping["backend"]
            ] = mapping["ai_service"]

    # ----------------------------
    # Build glue code
    # ----------------------------

    glue_lines = [
        "import requests",
        "",
        "",
        "def call_ai_service(request):",
        "",
        "    response = requests.post(",
        f'        "http://ai_service:8001{ai_contract["path"]}",',
        "        json={"
    ]

    request_items = list(
        request_mapping.items()
    )

    for index, (ai_field, backend_field) in enumerate(
        request_items
    ):

        comma = ","

        if index == len(request_items) - 1:
            comma = ""

        glue_lines.append(
            f'            "{ai_field}": request.{backend_field}{comma}'
        )

    glue_lines.extend([
        "        }",
        "    )",
        "",
        "    data = response.json()",
        "",
        "    return {"
    ])

    response_items = list(
        response_mapping.items()
    )

    for index, (backend_field, ai_field) in enumerate(
        response_items
    ):

        comma = ","

        if index == len(response_items) - 1:
            comma = ""

        glue_lines.append(
            f'        "{backend_field}": data["{ai_field}"]{comma}'
        )

    glue_lines.extend([
        "    }",
        ""
    ])

    glue_code = "\n".join(
        glue_lines
    )

    glue_path = os.path.join(
        output_dir,
        "backend",
        "integration_glue.py"
    )

    with open(
        glue_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(glue_code)

    # ----------------------------
    # Backend Dockerfile
    # ----------------------------

    backend_dockerfile = """FROM python:3.10-slim

WORKDIR /app

COPY main.py .
COPY integration_glue.py .

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    with open(
        os.path.join(
            output_dir,
            "backend",
            "Dockerfile"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(backend_dockerfile)

    # ----------------------------
    # AI service Dockerfile
    # ----------------------------

    ai_dockerfile = """FROM python:3.10-slim

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
"""

    with open(
        os.path.join(
            output_dir,
            "ai_service",
            "Dockerfile"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(ai_dockerfile)

    # ----------------------------
    # Docker Compose
    # ----------------------------

    docker_compose = """services:

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - ai_service

  ai_service:
    build: ./ai_service
"""

    with open(
        os.path.join(
            output_dir,
            "docker-compose.yml"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(docker_compose)

    return output_dir