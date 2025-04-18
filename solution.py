import argparse
import json
import os
import urllib.request
from typing import Any, Dict, List, Set


def fetch_json(
    url: str, base_dir: str | None = None, use_local: bool = True
) -> Dict[str, Any]:
    if use_local and base_dir is not None:
        file_name = url.split("/")[-1]
        file_path = os.path.join(base_dir, file_name)

        with open(file_path, "r") as f:
            return json.load(f)
    else:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode("utf-8"))


def filter_https_links(links: List[str]) -> List[str]:
    return [link for link in links if link.startswith("https")]


def crawl_https_links(
    start_url: str, base_dir: str | None = None, use_local: bool = True
) -> List[str]:
    visited: Set[str] = set()
    queue: List[str] = [start_url]
    while queue:
        url = queue.pop()

        if url in visited:
            continue

        data = fetch_json(url, base_dir, use_local)
        links = data.get("links", [])

        https_links = filter_https_links(links)
        for link in https_links:
            queue.append(link)

    return list(visited)


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl HTTPS links from JSON files.")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use local files instead of making HTTP requests",
    )
    parser.add_argument(
        "--dir",
        default="json_files",
        help="Directory containing JSON files (when using --local)",
    )

    args = parser.parse_args()

    start_url = "https://dskart.github.io/https-search/1.json"
    https_links = crawl_https_links(start_url, args.dir, args.local)

    print("\nResults:")
    print(f"Found {len(https_links)} unique HTTPS links:")
    for link in sorted(https_links):
        print(f"- {link}")


if __name__ == "__main__":
    main()
