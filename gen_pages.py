import json
import os
import random
from typing import Any, Dict, List


def generate_json_data(
    base_url: str, num_files: int, https_ratio: float
) -> Dict[int, Dict[str, Any]]:
    """
    Generate JSON data with links for the interview question.

    Args:
        base_url: Base URL to use in links
        num_files: Total number of JSON files to generate
        https_ratio: Ratio of HTTPS to HTTP links

    Returns:
        A tuple containing:
        - Dictionary of file data
        - List of file IDs with HTTPS links
    """
    files: Dict[int, Dict[str, Any]] = {}
    for i in range(1, num_files + 1):
        files[i] = {"links": [], "data": f"This is file {i}"}

    isolated_file: int = 3
    print(f"File {isolated_file}.json will be isolated (no links point to it)")

    for i in range(1, num_files + 1):
        num_links: int = random.randint(3, 7)

        links: List[str] = []
        for _ in range(num_links):
            protocol: str = "https" if random.random() < https_ratio else "http"

            link_to: int = random.randint(1, num_files)
            while link_to == isolated_file:
                link_to = random.randint(1, num_files)

            links.append(f"{protocol}::{base_url}/{link_to}.json")

        if random.random() < 0.3 and i not in [
            int(link.split("/")[-1].split(".")[0]) for link in links
        ]:
            self_link_protocol: str = (
                "https" if random.random() < https_ratio else "http"
            )
            links.append(f"{self_link_protocol}::{base_url}/{i}.json")

        if not any(link.startswith("https") for link in links):
            idx: int = random.randint(0, len(links) - 1)
            target: str = links[idx].split("::")[-1]
            links[idx] = f"https::{target}"

        files[i]["links"] = links

    for i in range(1, num_files + 1):
        new_links: List[str] = []
        for link in files[i]["links"]:
            file_id: int = int(link.split("/")[-1].split(".")[0])
            if file_id == isolated_file:
                replacement: int = random.randint(1, num_files)
                while replacement == isolated_file:
                    replacement = random.randint(1, num_files)
                new_protocol: str = "https" if link.startswith("https") else "http"
                new_links.append(f"{new_protocol}::{base_url}/{replacement}.json")
            else:
                new_links.append(link)
        files[i]["links"] = new_links

    return files


def generate_json_files(
    base_dir: str, base_url: str, num_files: int, https_ratio: float
) -> None:
    """
    Generate JSON files with links for the interview question and write them to disk.

    Args:
        base_dir: Directory to save the JSON files
        base_url: Base URL to use in links
        num_files: Total number of JSON files to generate
        https_ratio: Ratio of HTTPS to HTTP links
    """
    os.makedirs(base_dir, exist_ok=True)

    files = generate_json_data(base_url, num_files, https_ratio)

    for i, file_data in files.items():
        file_path: str = os.path.join(base_dir, f"{i}.json")
        with open(file_path, "w") as f:
            json.dump(file_data, f, indent=2)

    print(f"Generated {num_files} JSON files in {base_dir}")


if __name__ == "__main__":
    output_dir: str = os.path.join(os.path.dirname(__file__), "json_files")
    base_url: str = "foo.com"  # Default base URL, can be changed here
    generate_json_files(output_dir, base_url=base_url, num_files=8, https_ratio=0.7)
    print(f"Done! Files are ready at {output_dir}")
