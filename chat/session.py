import openai
from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.formatted_text import FormattedText
import time
from chat import modes


class ChatSession:
    """Manages OpenAI chat."""

    history: list[dict[str, str]]
    model: str
    mode: modes.Mode
    temperature: float
    retries: int = 3
    retry_wait: float = 5.0

    def __init__(
        self, mode: modes.Mode, temperature: float = 1.0, model: str = "gpt-3.5-turbo"
    ) -> None:
        """Initialize ChatSession.

        Args:
            mode: Mode to use.
            temperature: Temperature for sampling.
            model: Which OpenAI model to use.
        """
        self.model = model
        self.mode = mode
        self.temperature = temperature

        self.history = []
        if mode.instruction is not None:
            self.history.append({"role": "system", "content": mode.instruction})
        for example in mode.conversation:
            if "user" in example:
                self.history.append({"role": "user", "content": example["user"]})
            if "assistant" in example:
                self.history.append(
                    {"role": "assistant", "content": example["assistant"]}
                )

    def step(self):
        if self.history[-1]["role"] != "user":
            self.prompt()
        for trial_id in range(self.retries):
            try:
                self.get_response()
                break
            except openai.OpenAIError as err:
                message = (
                    f"Error occurred on trial {trial_id}: {err.user_message}. "
                    f"Retrying in {self.retry_wait}s..."
                )
                print_formatted_text(FormattedText([("red", message)]))
                time.sleep(self.retry_wait)

    def add_user_input(self, user_input: str) -> None:
        """Add a user input manually.

        Args:
            user_input: Input to add.
        """
        self.history.append({"role": "user", "content": user_input})

    def prompt(self) -> None:
        """Prompt user for new input."""
        user_input = prompt(FormattedText([("green", "User: ")]), multiline=True)
        print()
        self.add_user_input(user_input)

    def get_response(self) -> None:
        """Query OpenAI model an output response."""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            temperature=self.temperature,
        )
        assert isinstance(response, dict)
        assistant_output: dict[str, str] = response["choices"][0]["message"]
        self.history.append(assistant_output)
        print_formatted_text(
            FormattedText(
                [
                    ("red", self.mode.name + ": "),
                    ("", assistant_output["content"]),
                ]
            )
        )
        print()
