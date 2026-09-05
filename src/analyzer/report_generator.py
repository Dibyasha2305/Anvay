def generate_report(backend, ai_service, analysis, verification):

    report = []

    report.append("========================================")
    report.append("             ANVAY REPORT")
    report.append("========================================")

    report.append("\n[BACKEND]")
    report.append(
        f"{backend['method']} {backend['path']}"
    )

    report.append("\nRequest:")
    for field, field_type in backend["request"].items():
        report.append(f"  - {field}: {field_type}")

    report.append("\nResponse:")
    for field, field_type in backend["response"].items():
        report.append(f"  - {field}: {field_type}")

    report.append("\n[AI SERVICE]")
    report.append(
        f"{ai_service['method']} {ai_service['path']}"
    )

    report.append("\nRequest:")
    for field, field_type in ai_service["request"].items():
        report.append(f"  - {field}: {field_type}")

    report.append("\nResponse:")
    for field, field_type in ai_service["response"].items():
        report.append(f"  - {field}: {field_type}")

    report.append("\n[MAPPINGS]")

    for mapping in analysis["mappings"]:
        report.append(
            f"  {mapping['backend']} -> {mapping['ai_service']}"
        )

    report.append("\n[MISMATCHES]")

    if analysis["mismatches"]:
        for mismatch in analysis["mismatches"]:
            report.append(
                f"  - {mismatch['type']}: "
                f"{mismatch.get('backend')} -> "
                f"{mismatch.get('ai_service')}"
            )
    else:
        report.append("  None")

    report.append("\n[VERIFICATION]")
    report.append(
        f"  Status: "
        f"{'PASSED' if verification['success'] else 'FAILED'}"
    )
    report.append(
        f"  Message: {verification['message']}"
    )

    report.append("\n========================================")

    return "\n".join(report)