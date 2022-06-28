import argparse
import urllib.request
import json as js
from pathlib import Path


# Handle Arguments
# --------------------------
parser = argparse.ArgumentParser()

parser.add_argument(
    "--lua", action="store_const", const=1, help="save file as lua file"
)
parser.add_argument(
    "--json", action="store_const", const=1, help="save file as json file"
)
parser.add_argument(
    "--out", "-o", type=str, default="commits", help="file name you want to save as"
)
parser.add_argument(
    "--rname",
    "-r",
    type=bool,
    default=True,
    help="change '.' and '-' to '_' in plugin names ex: plugin.nivm -> plugin_nvim",
)

lua = parser.parse_args().lua
json = parser.parse_args().json
rname = parser.parse_args().rname
output = parser.parse_args().out

# --------------------------


def make_api(filename, branch="main"):
    api_urls = []
    with open(filename) as url_list:
        urls = url_list.read().splitlines()
    for url in urls:
        if len(url.split(" ")) == 2:
            branch = url[-1]

        url = url.split("/")
        api = f"https://api.github.com/repos/{url[-2]}/{url[-1]}/branches/{branch}"
        api_urls.append(api)
    return api_urls


def get_plugin_name(api_url):
    return api_url.split("/")[-3]


def get_commit(url):
    data = urllib.request.urlopen(url).read()
    commit = js.loads(data)["commit"]["sha"]
    return commit


def save_as(filetype, commits):
    """example: filetype="json" commits = "{key: value}" """

    if rname:
        repair_commits = {}
        # fix file naming
        for plugin_name, commit in commits.items():
            plugin_name = plugin_name.replace("-", "_")
            plugin_name = plugin_name.replace(".", "_")
            repair_commits[plugin_name] = commit
        commits = repair_commits

    # save as lua
    if filetype == "lua":
        filename = f"./out/{output}.lua"
        with open(filename, "w") as file:
            file.write("\nreturn {")

        for plugin_name, commit in commits.items():
            with open(filename, "a") as file:
                file.write(f"\n\t{plugin_name} = '{commit}',")

        with open(filename, "a") as file:
            file.write("\n}\n")

    # save as json
    if filetype == "json":
        filename = f"./out/{output}.json"
        with open(filename, "w") as file:
            file.write(js.dumps(commits, sort_keys=True, indent=4))


def main():

    # create dir to save our result
    save_location = "./out"
    if not Path(save_location).exists():
        Path(save_location).mkdir(parents=True)

    commits = {}
    for url in make_api("./urls"):
        commits[get_plugin_name(url)] = get_commit(url)

    if lua:
        save_as("lua", commits)
    if json:
        save_as("json", commits)
    if not lua and not json:
        save_as("json", commits)


if __name__ == "__main__":
    main()
