import sys
import os
import shutil
import argparse
import datetime
import platform
from typing import Optional
import git

def copy_files(source_dir : str, destination_dir : str):
    # copy source_dir to destination_dir/source_dir. overwrites if exists
    try:
        shutil.copytree(source_dir, os.path.join(destination_dir, source_dir), dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"Error copying files: \n{e}")
        return False

def get_git_repo(destination_dir : str, branch : Optional[str] = None) -> git.Repo:
    # if source dir exists, else create it
    os.makedirs(destination_dir, exist_ok=True)
    # if not, create a git repo
    try:
        repo : git.Repo = git.Repo(destination_dir)
    except git.InvalidGitRepositoryError:
        repo : git.Repo = git.Repo.init(destination_dir)

    if branch is not None:
        try:
            repo.git.checkout(branch)
        except git.GitCommandError:
            repo.git.checkout("-b", branch)

    return repo


def commit_changes(repo : git.Repo, message : str) -> git.Commit:
    if message is None:
        message = (f"Snapshot created on {datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
                   f" on {platform.node()}")
    # add all files
    repo.git.add(A=True)
    # commit changes
    commit : git.Commit = repo.index.commit(message)
    return commit

def push_changes(repo : git.Repo, branch : str):
    # try to push to origin, create the branch on remote if it doesn't exist
    try:
        repo.git.push("origin", branch)
    except git.GitCommandError:
        repo.git.push("origin", branch, "--set-upstream")
    return


def create_snapshot(source_dir : str, destination_dir : str, 
                    branch : Optional[str] = None,
                    message : Optional[str] = None,
                    push : bool = False) -> git.Commit:

    # first get the git repo
    repo : git.Repo = get_git_repo(destination_dir, branch)
    # copy the files
    copy_files(source_dir, destination_dir)
        # commit the changes
    commit : git.Commit = commit_changes(repo, message)
    if push:
        push_changes(repo, branch)
    return commit

def run_snapshot(**kwargs):
    # get the arguments
    source_dir = kwargs.get("source_dir")
    destination_dir = kwargs.get("destination_dir")
    branch = kwargs.get("branch")
    message = kwargs.get("message")
    push = kwargs.get("push")
    # create the snapshot
    commit : git.Commit = create_snapshot(source_dir, destination_dir, branch, message, push)
    print(f"Snapshot created on branch {branch} with commit {commit.hexsha}")
    return

def usage():
    strx = \
    """
    Usage: python pygitsnapshot.py <source dir> <destination dir>
    Optional:
    -b --branch <branch_name> : Specify the branch to create the snapshot on
    -m --message <commit_message> : Specify the commit message to use
    -p --push : Boolean flag to push the changes to the remote
    -h --help : Print this help message
    """ 
def main():
    # print("Usage: pygitsnapshot.py <source dir> <destination dir> Optional: <-b> <branch name>")
    arg_parser = argparse.ArgumentParser(description="Create a snapshot of a directory using git")
    arg_parser.add_argument("source_dir", help="The directory to snapshot")
    arg_parser.add_argument("destination_dir", help="The directory to store the snapshot")
    
    # optional arguments
    arg_parser.add_argument("-b", "--branch", help="The branch to create the snapshot on")
    arg_parser.add_argument("-m", "--message", help="The commit message to use")
    arg_parser.add_argument("-p", "--push", help="Push the changes to the remote", action="store_true")
    arg_parser.add_argument("-h", "--help", help="Print this help message", action="store_true")
    args = arg_parser.parse_args()

    if args.help:
        usage()
        sys.exit(0)
    
    # if invalid arguments, print usage
    if args.source_dir is None or args.destination_dir is None:
        usage()
        sys.exit(1)

    # run the script
    run_snapshot(**vars(args))