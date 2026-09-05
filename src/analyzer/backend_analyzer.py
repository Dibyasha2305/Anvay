import ast


def analyze_backend(file_path):
    with open(file_path, "r") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    models = {}

    # Find all Pydantic models
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):

            fields = {}

            for field in node.body:

                if isinstance(field, ast.AnnAssign):
                    if isinstance(field.target, ast.Name):
                        field_name = field.target.id

                        if isinstance(field.annotation, ast.Name):
                            field_type = field.annotation.id
                            fields[field_name] = field_type

            if fields:
                models[node.name] = fields

    # Find API endpoints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            for decorator in node.decorator_list:

                if isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Attribute):

                        method = decorator.func.attr

                        if decorator.args:
                            path = decorator.args[0].value
                        else:
                            continue

                        request_model = None
                        response_model = None

                        # Find request model
                        for argument in node.args.args:
                            if argument.annotation:
                                if isinstance(argument.annotation, ast.Name):
                                    request_model = argument.annotation.id

                        # Find response model
                        for statement in node.body:
                            if isinstance(statement, ast.Return):
                                if isinstance(statement.value, ast.Call):
                                    if isinstance(statement.value.func, ast.Name):
                                        response_model = statement.value.func.id

                        contract = {
                            "method": method.upper(),
                            "path": path,
                            "function": node.name,
                            "request": models.get(request_model, {}),
                            "response": models.get(response_model, {})
                        }

                        return contract


