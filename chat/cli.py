import pathlib

import click
import yaml

from chat import modes, session


@click.command()
@click.argument("prompt", type=str, nargs=-1)
@click.option("--with", "-w", "mode_name", type=str, default="assistant")
@click.option("--temperature", "-t", "temperature", type=float, default=1)
def cli(prompt: list[str], mode_name: str, temperature: float):
    all_modes = _load_configuration() + modes.default_modes

    try:
        mode = next((m for m in all_modes if _normalize_name(m.name) == mode_name))
    except StopIteration:
        print(f'Invalid mode "{mode_name}"')
        exit()

    chat_session = session.ChatSession(mode, temperature=temperature)

    if prompt:
        chat_session.add_user_input(" ".join(prompt))

    while True:
        chat_session.step()


def _normalize_name(name: str) -> str:
    return name.lower().replace(" ", "_")


def _load_configuration() -> list[modes.Mode]:
    rc_file = pathlib.Path.home() / ".chat.yml"
    if not rc_file.exists():
        return []

    with rc_file.open("r") as file_handle:
        config = yaml.safe_load(file_handle)

    if "modes" not in config:
        return []

    config_modes = []
    for mode_config in config["modes"]:
        config_modes.append(modes.Mode(**mode_config))

    return config_modes


if __name__ == "__main__":
    cli()
