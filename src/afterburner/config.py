from pathlib import Path

from dynaconf import Dynaconf

# Define o diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOT_DIR / "config"

settings = Dynaconf(
    envvar_prefix="AFTERBURNER",
    settings_files=[
        CONFIG_DIR / "settings.toml",
        CONFIG_DIR / ".secrets.toml",
    ],
    environments=True,
    env_switcher="AFTERBURNER_ENV",
    load_dotenv=True,
)

# `envvar_prefix` = export envvars with `export AFTERBURNER_FOO=bar`.
# `settings_files` = Load these files in the order.
# `environments` = Enable multi-environment support (default, development, production).
# `env_switcher` = Use `export AFTERBURNER_ENV=production` to switch environments.
