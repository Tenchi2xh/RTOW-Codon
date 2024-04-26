import re
import shutil
from pathlib import Path
from typing import List


def remove_blocks(lines: List[str], current_mode: str):
    remove_mode = "codon" if current_mode == "python" else "python"

    keep_on    = f"# <{current_mode}-only>"
    keep_off   = f"# </{current_mode}-only>"
    remove_on  = f"# <{remove_mode}-only>"
    remove_off = f"# </{remove_mode}-only>"
    indicators = [keep_on, keep_off, remove_on, remove_off]

    result = []
    remove = False
    for line in lines:
        s = line.strip()
        if s in indicators:
            if s == remove_on:
                remove = True
            elif s == remove_off:
                remove = False
            continue
        if remove:
            continue
        result.append(line)

    return result


def pythonize(lines):
    # Remove @par decorators
    lines = [line for line in lines if not re.match(r"\s*@par", line)]

    class_name = None
    for i, line in enumerate(lines):
        # Remove codon types
        # TODO: More thorough
        lines[i] = line.replace("UInt[8]", "int")

        # Codon supports type hints referring to the currently defined class,
        # Python only does if the type is quoted
        if line.startswith("class "):
            class_name = re.match(r"class (\w+)", line).group(1)
        elif class_name and f": {class_name}" in line:
            lines[i] = line.replace(class_name, f'"{class_name}"')

    return lines


def codonize(lines):
    return lines


def preprocess(src: str, mode: str):
    src_path = Path(src)
    dest = f"{src}_{mode}"

    if Path(dest).exists():
        shutil.rmtree(dest)

    for file in src_path.glob("**/*.py"):
        if file.suffix == ".py":
            new_file = Path(dest, *file.parts[1:])
            new_file.parent.mkdir(parents=True, exist_ok=True)

            with open(file, "r") as f:
                lines = f.readlines()

            lines = remove_blocks(lines, mode)

            if mode == "codon":
                lines = codonize(lines)
            elif mode == "python":
                lines = pythonize(lines)

            with open(new_file, "w") as f:
                f.writelines(lines)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1]
    preprocess("rtow", mode)
