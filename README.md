Repo-diff
=========

Create a list of packages in a Linux repository.

* Prerequisite:

```
apt-get install libxml2-dev
apt-get install libxslt1-dev
#apt-get install zlib1g-dev
apt-get install  lib32z1-dev
pip install -r requirements
```

* Usage:

```
usage: repo_diff.py [-h] [--repo REPO] [--comp COMP]

Save a text copy of packages in a repo

optional arguments:
  -h, --help   show this help message and exit
  --repo REPO  Provide the repo name Example:
               ftp://archive.ubuntu.com/ubuntu/pool
  --comp COMP  Provide the comp name Example: main,universe Default:main


```
* Run

```
python repo_diff.py --repo http://archive.ubuntu.com/ubuntu/pool --comp main,universe,restricted
```

* Output

```
less repo_list
```

Tested with:
* archive.ubuntu.com
