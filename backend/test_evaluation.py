from app.services.evaluation_service import (
    evaluate_answer
)

result = evaluate_answer(
    "What are React Hooks?",
    "Hooks allow state in functional components."
)

print(type(result))
print(result)