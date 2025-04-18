import json
import os
from typing import Any, Dict, List, Set


def fetch_json(url: str, base_dir: str = "json_files") -> Dict[str, Any]:
    # Extract the file number from the URL
    file_name = url.split("/")[-1]  # Get "1.json" from "https::foo.com/1.json"
    file_path = os.path.join(base_dir, file_name)

    with open(file_path, "r") as f:
        return json.load(f)


def filter_https_links(links: List[str]) -> List[str]:
    return [link for link in links if link.startswith("https::")]


def crawl_https_links(start_url: str) -> List[str]:
    visited: Set[str] = set()
    queue: List[str] = [start_url]

    while queue:
        url = queue.pop()

        if url in visited:
            continue

        visited.add(url)

        data = fetch_json(url)
        links = data.get("links", [])

        https_links = filter_https_links(links)
        for link in https_links:
            queue.append(link)

    return list(visited)


def main() -> None:
    start_url = "https::foo.com/1.json"
    https_links = crawl_https_links(start_url)

    print("\nResults:")
    print(f"Found {len(https_links)} unique HTTPS links:")
    for link in sorted(https_links):
        print(f"- {link}")


if __name__ == "__main__":
    main()
