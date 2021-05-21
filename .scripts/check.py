#!/usr/bin/env python3

import os
import glob
import yaml
from git import Repo


def rchop(str, suffix):
    if str.endswith(suffix):
        return str[:-len(suffix)]
    return str


def lchop(str, prefix):
    if str.startswith(prefix):
        return str[len(prefix):]
    return str


def get_repo_name(repo_path='../'):
    repo = Repo(repo_path)
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]
    return repo_name


def get_namespace_prefix(repo_path='../'):
    return lchop(rchop(get_repo_name(repo_path),"-gitops"), "gitops-")


def find_yaml_files(file_glob):
    for fname in glob.glob(file_glob, recursive=True):
        if fname.endswith('.yaml') or fname.endswith('.yml'):
            yield fname


def check_resource_kind(rd, fname):
    ok = True
    if rd['kind'] not in ALLOWED_KINDS:
        print("{fname}: resource definition of kind '{rd.kind}' is forbidden")
        ok = False
    return ok


def check_target_namespace(rd, fname):
    ok = True
    if 'namespace' not in rd['metadata']:
        return
    if rd['metadata']['namespace']:
        if not rd['metadata']['namespace'].startswith(ALLOWED_PREFIX):
            print(f"{fname}: targets namespace '{rd['metadata']['namespace']}' is forbidden")
            ok = False
    return ok


def validate_resource(fname):
    ok = True
    with open(fname, 'r') as stream:
        try:
            rd = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            exit(1)
    if not check_resource_kind(rd, fname): ok = False
    if not check_target_namespace(rd, fname): ok = False
    # if not check_project_labels(rd, fname): ok = False

    return ok


def main():
    ok = True
    for fname in find_yaml_files(f"{ROOT_DIR}/**/*ml"):
        validate_resource(fname)

    if not ok:
        exit(1)


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.abspath(SCRIPT_DIR + "/../")
    ALLOWED_PREFIX = get_namespace_prefix(ROOT_DIR)
    ALLOWED_KINDS = set(['Subscription', 'Application'])
    main()
