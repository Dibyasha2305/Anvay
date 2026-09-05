import importlib.util


def verify_generated_glue():

    try:
        # Load the generated glue code
        spec = importlib.util.spec_from_file_location(
            "generated_glue",
            "generated/glue.py"
        )

        glue = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(glue)

        # Create a simple request object
        class Request:
            input = "I love this movie"

        # Call the generated function
        result = glue.call_ai_service(Request())

        # Check the generated response
        if "prediction" not in result:
            return {
                "success": False,
                "message": "Generated glue is missing prediction"
            }

        if "confidence" not in result:
            return {
                "success": False,
                "message": "Generated glue is missing confidence"
            }

        return {
            "success": True,
            "message": "Generated glue works",
            "response": result
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }
    