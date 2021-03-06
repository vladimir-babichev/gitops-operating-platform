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
        print(f"{lchop(fname, ROOT_DIR)}: resource definition of kind '{rd.kind}' is forbidden")
        ok = False
    return ok


def check_target_namespace(rd, fname):
    ok = True
    if 'namespace' not in rd['metadata']: return ok
    if not rd['metadata']['namespace'].startswith(ALLOWED_PREFIX):
        print(f"{lchop(fname, ROOT_DIR)}: targets namespace '{rd['metadata']['namespace']}' is forbidden")
        ok = False
    return ok


def check_project_label(rd, fname):
    if 'labels' not in rd['metadata']:
        print(f"{fname}: resource definition is missing label metadata")
        return False
    if 'project' not in rd['metadata']['labels']:
        print(f"{fname}: resource definition is missing 'project' label")
        return False
    if rd['metadata']['labels']['project'] != ALLOWED_PREFIX:
        print(f"{fname}: resource project label '{rd['metadata']['labels']['project']}' is forbidden")
        return False
    return True


def validate_resource(fname):
    ok = True
    with open(fname, 'r') as stream:
        try:
            rdefinition = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            exit(1)
    rlocation = lchop(fname, ROOT_DIR)

    if not check_resource_kind(rdefinition, rlocation): ok = False
    if not check_target_namespace(rdefinition, rlocation): ok = False
    if not check_project_label(rdefinition, rlocation): ok = False

    return ok


def main():
    ok = True
    for fname in find_yaml_files(f"{ROOT_DIR}/**/*ml"):
        ok = validate_resource(fname)
    if not ok:
        exit(1)


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.abspath(SCRIPT_DIR + "/../")
    ALLOWED_PREFIX = get_namespace_prefix(ROOT_DIR)
    ALLOWED_KINDS = set(['Subscription', 'Application'])
    main()
