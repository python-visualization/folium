"""
This script is used to update switcher.json on docs releases. It adds the new version to
the list of versions and sets the latest version to the new version.
"""

import argparse
import json
import os


def main():
    # Define CLI arguments
    parser = argparse.ArgumentParser(description="Update switcher.json")
    parser.add_argument(
        "--version", "-v", required=True, type=str, help="The new version to add"
    )
    args = parser.parse_args()

    # Setup path to switcher.json (relative to this script) and load it
    switcher_path = os.path.join(os.path.dirname(__file__), "_static", "switcher.json")
    with open(switcher_path) as f:
        switcher = json.load(f)

    # Find index of 'latest' entry
    latest_index = None
    for i, version in enumerate(switcher):
        if version["version"] == "latest":
            latest_index = i
            break
    if latest_index is None:
        raise ValueError("'latest' version not found in switcher.json")

    # Add the new version to the list of versions (we always insert it after latest)
    new_version = {
        "version": args.version,
        "url": f"https://python-visualization.github.io/folium/{args.version}/",
    }

    # Update the latest version
    switcher[latest_index]["url"] = new_version["url"]

    # Make sure version is unique
    if any(version["version"] == args.version for version in switcher):
        print(
            f"Version {args.version} already exists in switcher.json. Not adding it again."
        )
    else:
        switcher.insert(latest_index + 1, new_version)

    # Write the updated switcher.json
    with open(switcher_path, "w") as f:
        json.dump(switcher, f, indent=2)


if __name__ == "__main__":
    main()
