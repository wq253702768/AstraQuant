class PromptRenderService:
    def render(self, content: str, variables: dict) -> str:
        result = content
        for key, value in variables.items():
            result = result.replace("{{" + key + "}}", str(value))
        return result
