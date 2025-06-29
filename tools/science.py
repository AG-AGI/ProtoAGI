from tools.llm import ask

def perform_experiment(experiment_description: str) -> str:
    system = """
    You are a scientific assistant. Your task is to perform experiments based on the provided description.
    You must simulate an experiment with utmost accuracy, considering the materials and methods described.
    provide about one paragrah in this format:
    <experiment_details>
    the steps in order to perform the experiment, the materials used, and the expected outcome.
    </experiment_details>
    <reactions_physics>
    the physical reactions that occur during the experiment, including any chemical changes, gas production, etc.
    </reactions_physics>
    <experiment_result>
    the result of the experiment, including any observations, reactions, or outcomes.
    </experiment_result>

    """
    response = ask(system + experiment_description)
    return response


if __name__ == "__main__":
    experiment_desc = "Create mixture A using 15g of bicarbonate, create mixture B using 15g of vinegar and 30g of water mixed with lemon, then mix them together."
    result = perform_experiment(experiment_desc)
    print("Experiment Result:", result)