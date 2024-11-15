import openai
import yaml
import json

class CodeBuddy:
    def __init__(self, api_key, instructions, history_size=10):
        openai.api_key = api_key
        self.instructions = instructions
        self.internal_instructions = (
            "You are an agent in a software project and your task is to support the developer in various tasks.\n"
            "Since you response is parsed by an script please provide any response in the following format.\n"
            "In the user request you will get a list of all available files in the project and the user prompt itself.\n"
            "If you need to inspect contents of specific files please use request_files action (see below) to request files and it will be provided with the next request!\n"
            "\n"
            "Possible response actions include:\n"
            "- 'modify': to update file content\n"
            "- 'delete': to remove a file\n"
            "- 'request_files': to request additional files for more context\n"
            "- 'response': to return a user-readable message\n"
            "- 'command': to execute a specific command on the shell\n"
            "Responses should be clear and in YAML format. Make sure to respond in plain yaml without any markdown.\n"
            "\n"
            "--- Response Example ---\n"
            "\n"
            "- action: modify\n"
            "  filename: example.py\n"
            "  content: |\n"
            "    # New content here\n"
            "    # and here\n"
            "- action: delete\n"
            "  filename: unused.py\n"
            "- action: request_files\n"
            "  filename: extra.py\n"
            "- action: response\n"
            "  message: 'This is a user-readable message.'\n"
            "- action: command\n"
            "  command: 'echo Hello World'\n"
        )
        self.history = []
        self.history_size = history_size

    def get_completion(self, user_request, file_list, file_contents, command_result):
        """
        Generates a completion using the provided contextual data and user query by interacting with OpenAI's API.
        Args:
            user_request (str): The query or request that the user wants to process.
            file_list (list): List of all file names available in the project.
            file_contents (list): A list of objects each containing 'name' and 'content' keys for requested files.
            command_result (str): The result of the last executed command
        Returns:
            list: A list of changes determined from the completion, including modifications, deletions, 
                  file requests, user responses, or meta updates.
        """
        files = "\n".join(file_list)
        contents = "\n".join(f"- filename: {file['name']}\n  content: {file['content']}" for file in file_contents)

        message = {"role": "user", "content": (
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
        )}

        self._append_history(message)

        messages = [
            {"role": "system", "content": self.internal_instructions},
            {"role": "system", "content": self.instructions}
        ]
        
        messages.extend(self.history)

        with open('message_log.json', 'w') as filehandle:
            json.dump(messages, filehandle)

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1500
        )
        
        completion_result = response.choices[0].message.content.strip()
        completion_result = str.removeprefix(completion_result, "```yaml")
        completion_result = str.removesuffix(completion_result, "```")

        self._append_history({"role": "assistant", "content": completion_result})

        return yaml.safe_load(completion_result)

    def _append_history(self, message):
        self.history.append(message)
        if len(self.history) > self.history_size:
            self.history.pop(1)
