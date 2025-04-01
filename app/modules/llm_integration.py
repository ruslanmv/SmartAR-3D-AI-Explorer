# app/modules/llm_integration.py

class LLMIntegration:
    """
    Handles queries to a large language model (LLM) regarding the environment.
    For instance, if the user says:
      "What am I looking at?"
    the system can compile relevant context (e.g., recognized objects, building
    layout) into a textual prompt for the LLM, then parse or return the LLM's response.
    """

    def __init__(self, llm_instance):
        """
        :param llm_instance: A handle or client to a loaded LLM. Could be:
          - A local model object (e.g., a GPT-2 or GPT-Neo instance).
          - A remote API client (e.g., OpenAI, Hugging Face Inference API).
          - A placeholder or mock string for testing.
        """
        self.llm = llm_instance  # In real code, store an API key or loaded model.

    def query_environment(self, user_query, recognized_objects, building_model):
        """
        Formulate a structured prompt about the recognized objects and building
        context, then call the LLM to generate an answer.
        
        :param user_query: A string containing the user's question (e.g. "What am I looking at?")
        :param recognized_objects: A list of dictionaries describing each recognized object:
            Example:
              [
                {
                  "name": "chair",
                  "type": "furniture",
                  "position": (x, y, z),
                  "confidence": 0.94
                },
                ...
              ]
        :param building_model: The 3D building data structure loaded by ingestion (useful if you want
                               to reference walls, rooms, or other architectural info).
        
        :return: A string containing the LLM's textual response.
        """
        # 1. Construct a simple textual summary of recognized objects
        if recognized_objects:
            object_descriptions = []
            for obj in recognized_objects:
                name = obj.get("name", "unknown object")
                pos = obj.get("position", (0, 0, 0))
                conf = obj.get("confidence", 0.0)
                object_descriptions.append(
                    f"Object: {name}, at {pos}, confidence {conf:.2f}"
                )
            recognized_summary = "\n".join(object_descriptions)
        else:
            recognized_summary = "No objects recognized at the moment."

        # 2. Build a prompt combining user_query + recognized object data
        prompt = (
            f"User Query: {user_query}\n"
            f"Environment Data:\n"
            f"{recognized_summary}\n\n"
            "Please answer the user query based on the recognized objects and building layout.\n"
        )

        # 3. Send prompt to the LLM
        # Here, we have a simple stub that returns a dummy response.
        # In production, you might do something like:
        # response_text = self.llm.generate(prompt)
        # or:
        # response_text = openai.Completion.create(
        #     model="text-davinci-003", prompt=prompt, max_tokens=100
        # ).choices[0].text.strip()
        
        print("[LLMIntegration] Prompt constructed for LLM:\n", prompt)
        
        # For demonstration, return a mock response:
        response_text = (
            "I see there are some recognized objects in front of you. "
            "It looks like a placeholder answer because the LLM is mocked."
        )
        
        return response_text
