<br>

## Table Of Contents

- [Project Stracture](#project-stracture)
- [Uses](#uses)
  - [Example](#example)
  - [Explanation](#explanation)
- [Rules for `urls` file](#rules-for-urls-file)
- [To-do](#to-do)

<br>

# Project Stracture

```
LCommit/
├── ...
├── main.py                 - python script file
├── output/                 - directory for results
│   └── ...
├── ...
└── urls/
    ├── neovim_plugins.url  - file with neovim plugin's urls
    └── put_urls_here.url   - plain text file with repositories urls (put urls of repo to get theirs commits hash)
```

# Uses

```
$ python main.py --help
usage: main.py [-h] [--lua] [--json] [--out OUT] [--rname RNAME] [--urls URLS]

options:
  -h, --help            show this help message and exit
  --lua                 save file as lua file
  --json                save file as json file
  --out OUT, -o OUT     file name you want to save as
  --rname RNAME, -r RNAME
                        change '.' and '-' to '_' in plugin names ex: plugin.nivm -> plugin_nvim
  --urls URLS, -u URLS  file containing urls
```

<br>

## Example

```zsh

$ git clone https://github.com/pullape/LCommit
$ cd LCommit
$ tree
.
├── LICENSE.md
├── main.py
└── urls

$ cat urls
https://github.com/wbthomason/packer.nvim           master
https://github.com/jose-elias-alvarez/null-ls.nvim  0.5.1-compat
https://github.com/williamboman/nvim-lsp-installer  main
https://github.com/hrsh7th/nvim-cmp

$ python main.py --json --lua --out commits
$ tree
.
├── LICENSE.md
├── main.py
├── output
│   └── commits.json
├── README.md
└── urls
    ├── neovim_plugins.url
    └── put_urls_here.url

$ cat out/commits.json
{
    "null_ls_nvim": "8828af78d8c2d96a884769a070951a47c2e6a6ff",
    "nvim_cmp": "1cad1815e165c2b436f41a1ee20327701842a761",
    "nvim_lsp_installer": "e557c2a6f5fc2a0665f61908c1204e648f226a7f",
    "packer_nvim": "00ec5adef58c5ff9a07f11f45903b9dbbaa1b422"
}

$ cat out/commits.lua

return {
	null_ls_nvim = '8828af78d8c2d96a884769a070951a47c2e6a6ff',
	nvim_lsp_installer = 'e557c2a6f5fc2a0665f61908c1204e648f226a7f',
	packer_nvim = '00ec5adef58c5ff9a07f11f45903b9dbbaa1b422',
	nvim_cmp = '1cad1815e165c2b436f41a1ee20327701842a761',
}

```

### Explanation

`out` is output directory which will contain our results <br>
`url` contains the list of urls to repositories <br>
`--json` and `--lua` means save result as json and lua file.`--out commits` means result file name is `commits`. <br>
So, `--json --lua --out commits` means save result as `commits.json` and `commits.lua`

<br><br>

# Rules for `urls` file

1. you can provide branch name for repo on same line, example:

```
https://github.com/wbthomason/packer.nvim           master
https://github.com/jose-elias-alvarez/null-ls.nvim  0.5.1-compat
```

2. if you don't provide branch name, `main` will be used as brance name (which can be not true for some repo,
   so it's batter to provide branch name
3. line starting with `#` will be ignored (it will treated as comment line), example:

```
# this and below line will be ignored
# https://github.com/wbthomason/packer.nvim           master
```

# To-do

...
