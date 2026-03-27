"""
mazegen/parser.py: Logic for reading and validating the configuration file.
"""

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
OPTIONAL_KEYS = {"SEED"}
ALLOWED_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS

def parse_coordinate(value: str, key_name: str) -> tuple[int, int]:
    """Converts '0,0' string into (0, 0) tuple."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key_name} must be in x,y format, got: {value}")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(f"{key_name} must contain two integers, got: {value}")

def parse_bool(value: str) -> bool:
    """Converts 'True'/'False' strings into Python booleans."""
    if value.lower() == "true": return True
    if value.lower() == "false": return False
    raise ValueError(f"Value must be True or False, got: {value}")

def load_config(path: str) -> dict:
    """
    Reads the file and returns a validated dictionary of settings.
    Handles comments (#) and empty lines gracefully.
    """
    config = {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                # 1. Strip comments and whitespace
                clean_line = line.split('#')[0].strip()
                if not clean_line:
                    continue

                # 2. Split Key=Value
                if "=" not in clean_line:
                    raise ValueError(f"Line {line_num}: Invalid syntax (missing '=')")
                
                key, value = clean_line.split("=", 1)
                key, value = key.strip(), value.strip()

                if key not in ALLOWED_KEYS:
                    raise ValueError(f"Line {line_num}: Unknown key '{key}'")

                # 3. Convert Values
                if key in {"WIDTH", "HEIGHT", "SEED"}:
                    config[key] = int(value)
                elif key in {"ENTRY", "EXIT"}:
                    config[key] = parse_coordinate(value, key)
                elif key == "PERFECT":
                    config[key] = parse_bool(value)
                elif key == "OUTPUT_FILE":
                    config[key] = value

        # 4. Final Validation (Post-Parsing)
        validate_config_logic(config)
        return config

    except FileNotFoundError:
        raise ValueError(f"Configuration file '{path}' not found.")

def validate_config_logic(config: dict) -> None:
    """Checks if the values make sense (e.g., Width > 0)."""
    # Check for missing keys
    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")

    # Check bounds
    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers.")

    w, h = config["WIDTH"], config["HEIGHT"]
    en_x, en_y = config["ENTRY"]
    ex_x, ex_y = config["EXIT"]

    if not (0 <= en_x < w and 0 <= en_y < h):
        raise ValueError(f"ENTRY {config['ENTRY']} is outside maze bounds.")
    if not (0 <= ex_x < w and 0 <= ex_y < h):
        raise ValueError(f"EXIT {config['EXIT']} is outside maze bounds.")
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must be different coordinates.")
    if config["HEIGHT"] < 2 or config["WIDTH"] < 2:
        raise ValueError("Maze dimensions must be at least 2x2.")