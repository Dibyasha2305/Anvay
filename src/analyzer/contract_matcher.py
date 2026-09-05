def find_best_match(field, candidates):
    """
    Find the most likely matching field.
    """

    field = field.lower()

    for candidate in candidates:

        candidate_lower = candidate.lower()

        # Exact match
        if field == candidate_lower:
            return candidate

        # Common semantic relationships
        mappings = {
            "input": ["prompt"],
            "prediction": ["result"],
            "confidence": ["score"]
        }

        if field in mappings:
            if candidate_lower in mappings[field]:
                return candidate

    return None


def match_contracts(backend, ai_service):

    mismatches = []
    mappings = []

    # Compare HTTP methods
    if backend["method"] != ai_service["method"]:

        mismatches.append({
            "type": "method_mismatch",
            "backend": backend["method"],
            "ai_service": ai_service["method"]
        })

    # Compare API paths
    if backend["path"] != ai_service["path"]:

        mismatches.append({
            "type": "path_mismatch",
            "backend": backend["path"],
            "ai_service": ai_service["path"]
        })

    # Find request mappings
    backend_request = backend["request"]
    ai_request = ai_service["request"]

    for backend_field in backend_request:

        match = find_best_match(
            backend_field,
            ai_request.keys()
        )

        if match:
            mappings.append({
                "direction": "request",
                "backend": backend_field,
                "ai_service": match
            })

        else:
            mismatches.append({
                "type": "request_field_mismatch",
                "backend": backend_field,
                "ai_service": None
            })

    # Find response mappings
    backend_response = backend["response"]
    ai_response = ai_service["response"]

    for backend_field in backend_response:

        match = find_best_match(
            backend_field,
            ai_response.keys()
        )

        if match:
            mappings.append({
                "direction": "response",
                "backend": backend_field,
                "ai_service": match
            })

        else:
            mismatches.append({
                "type": "response_field_mismatch",
                "backend": backend_field,
                "ai_service": None
            })

    return {
        "mappings": mappings,
        "mismatches": mismatches
    }

