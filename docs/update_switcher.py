"""
This script is used to update switcher.json on docs releases. It adds the new version to
the list of versions and sets the latest version to the new version.
"""

import argparse
import json
import os
import re


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

    # first we get the version number of the previous version
    for i, version in enumerate(switcher):
        if version["version"] == "latest":
            latest_index = i
            previous_version = re.search(
                r"latest \(([v.\d]+)\)", version["name"]
            ).group(1)
            if previous_version == args.version:
                print(f"Version {args.version} already is the latest version. Exiting.")
                return

            # now replace the name of this one with the new version
            switcher[i]["name"] = f"latest ({args.version})"
            break
    else:
        raise ValueError("'latest' version not found in switcher.json")

    # Add the previous version to the list of versions (we always insert it after latest)
    if any(version["version"] == previous_version for version in switcher):
        print(
            f"Previous version {previous_version} already exists in switcher.json. Not adding it again."
        )
    else:
        previous_version_entry = {
            "version": previous_version,
            "url": f"https://python-visualization.github.io/folium/{previous_version}/",
        }
        switcher.insert(latest_index + 1, previous_version_entry)

    # Write the updated switcher.json
    with open(switcher_path, "w") as f:
        json.dump(switcher, f, indent=2)


if __name__ == "__main__":
    main()
