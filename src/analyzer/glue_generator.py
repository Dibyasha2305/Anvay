def generate_glue_code(backend, ai_service, mappings):

    request_mappings = [
        mapping
        for mapping in mappings
        if mapping["direction"] == "request"
    ]

    response_mappings = [
        mapping
        for mapping in mappings
        if mapping["direction"] == "response"
    ]

    request_lines = []

    for mapping in request_mappings:
        request_lines.append(
            f'            "{mapping["ai_service"]}": request.{mapping["backend"]}'
        )

    response_lines = []

    for mapping in response_mappings:
        response_lines.append(
            f'            "{mapping["backend"]}": data["{mapping["ai_service"]}"]'
        )

    request_body = ",\n".join(request_lines)
    response_body = ",\n".join(response_lines)

    code = f'''import requests


def call_ai_service(request):

    response = requests.post(
        "http://localhost:8001{ai_service["path"]}",
        json={{
{request_body}
        }}
    )

    data = response.json()

    return {{
{response_body}
    }}
'''

    return code
