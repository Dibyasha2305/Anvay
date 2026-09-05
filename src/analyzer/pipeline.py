from report_generator import generate_report
from docker_verifier import verify_docker_container
from backend_analyzer import analyze_backend
from ai_analyzer import analyze_ai_service
from contract_matcher import match_contracts
from glue_generator import generate_glue_code


backend_path = input("Enter backend Python file: ")
ai_path = input("Enter AI service Python file: ")


backend_contract = analyze_backend(backend_path)

ai_contract = analyze_ai_service(ai_path)


result = match_contracts(
    backend_contract,
    ai_contract
)


print("\n=== BACKEND CONTRACT ===")
print(backend_contract)


print("\n=== AI SERVICE CONTRACT ===")
print(ai_contract)


print("\n=== CONTRACT ANALYSIS ===")
print(result)


glue_code = generate_glue_code(
    backend_contract,
    ai_contract,
    result["mappings"]
)


print("\n=== GENERATED GLUE CODE ===")
print(glue_code)
import os

os.makedirs("generated", exist_ok=True)

with open("generated/glue.py", "w") as file:
    file.write(glue_code)

print("\nGlue code saved to generated/glue.py")
verification = verify_docker_container()

print("\n=== DOCKER VERIFICATION ===")
print(verification)

report = generate_report(
    backend_contract,
    ai_contract,
    result,
    verification
)

print("\n")
print(report)
