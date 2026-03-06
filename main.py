from pyswip import Prolog

QUESTIONS = {
    "engine_does_not_crank": "When you turn the key, does the engine NOT crank at all?",
    "dashboard_lights_dim": "Are the dashboard lights dim or weak?",
    "clicking_sound": "Do you hear a clicking sound when trying to start?",
    "engine_does_not_start": "Does the engine fail to start?",
    "engine_cranks": "Does the engine crank (turn over)?",
    "not_starting": "Does it crank but still not start?",
    "smell_fuel": "Do you smell fuel while trying to start?",
    "temperature_high": "Is the temperature gauge high / overheating?",
    "coolant_low": "Is the coolant level low?",
    "smoke_black": "Is the exhaust smoke black?",
    "smoke_blue": "Is the exhaust smoke blue?",
    "smoke_white": "Is the exhaust smoke white?",
}

def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} (yes/no): ").strip().lower()
        if ans in ("yes", "y"):
            return True
        if ans in ("no", "n"):
            return False
        print("Please type yes or no.")

def clear_facts(prolog: Prolog) -> None:
    # Retract all previously asserted facts to avoid mixing runs
    list(prolog.query("retractall(fact(_))."))

def assert_facts(prolog: Prolog) -> None:
    # Ask questions; for each "yes", assert fact(symptom) into Prolog
    for symptom, question in QUESTIONS.items():
        if ask_yes_no(question):
            # Assert as a Prolog fact: fact(symptom_name).
            list(prolog.query(f"assertz(fact({symptom}))."))

def get_best_diagnosis(prolog: Prolog):
    # Query Prolog: best_diagnosis(D, Score, Advice).
    results = list(prolog.query("best_diagnosis(D, Score, Advice)."))
    # results is a list of dictionaries like: {'D': ..., 'Score': ..., 'Advice': ...}
    if not results:
        return ("No clear diagnosis - consult a mechanic", 0,
                "Symptoms don’t match rules. Get professional inspection.")
    r = results[0]
    return (str(r["D"]), int(r["Score"]), str(r["Advice"]))

def main():
    print("=== Car Fault Diagnosis Expert System (Python + Prolog) ===")

    prolog = Prolog()

    # Load the Prolog knowledge base file
    prolog.consult("car_rules.pl")

    # Reset facts, collect new facts, and infer diagnosis
    clear_facts(prolog)
    assert_facts(prolog)

    diagnosis, score, advice = get_best_diagnosis(prolog)

    print("\n--- Results ---")
    print(f"Diagnosis: {diagnosis}")
    print(f"Confidence: {score}%")
    print(f"Advice: {advice}")

if __name__ == "__main__":
    main()