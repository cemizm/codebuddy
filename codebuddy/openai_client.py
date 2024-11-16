from openai import OpenAI
import yaml

from .config_loader import Configuration
from .base_client import BaseClient


class OpenAIClient(BaseClient):
    def __init__(self, config: Configuration):
        super().__init__(config)
        self.client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key
        )

    def get_completion(self, user_request, file_list, file_contents,
                       command_result):
        files = "\n".join(file_list)
        contents = "\n".join(
            f"- filename: {file['name']}\n  content: {file['content']}"
            for file in file_contents
        )

        message = {
            "role": "user",
            "content": (
                "## Project Files ##\n"
                f"{files}"
                "\n"
                "## Requested Files ##\n"
                f"{contents}"
                "\n"
                "## Command Result ##\n"
                f"{command_result}"
                "\n"
                "## User Query ##\n"
                f"{user_request}\n"
                "\n"
            )
        }

        self._append_history(message)

        messages = [
            {"role": "system", "content": self.internal_instructions},
            {"role": "system", "content": self._get_user_instructions()}
        ]

        messages.extend(self.history)

        result = None
        retries = 3
        while result is None:
            try:
                response = self.client.chat.completions.create(
                    model=self._get_model(),
                    messages=messages,
                    max_tokens=1500
                )

                completion_result = response.choices[0].message.content.strip()
                completion_result = str.removeprefix(
                    completion_result, "```yaml"
                )
                completion_result = str.removesuffix(
                    completion_result, "```"
                )

                result = yaml.safe_load(completion_result)

                self._append_history({
                    "role": "assistant",
                    "content": completion_result
                })

            except yaml.YAMLError:
                retries -= 1
                if retries == 0:
                    result = [{
                        "action": "response",
                        "message": f"Could not process response\n"
                        f"{command_result}"
                    }]

        return result
