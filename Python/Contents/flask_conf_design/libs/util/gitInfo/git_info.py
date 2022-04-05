import subprocess
import os
import glob
import zlib
import time

from libs.util.common import dict2obj, join_dir
from libs.util.strtime import str_date_time


def find_git_dir(path):
    """
        Find the correct git dir.
        Check parent directory if .git folder is not in current directory
    """
    abs_dir = os.path.abspath(path)
    git_dir = os.path.join(abs_dir, ".git")
    if os.path.isdir(git_dir):
        return git_dir
    parent_dir = os.path.dirname(abs_dir)
    if abs_dir == parent_dir:
        return None
    return find_git_dir(parent_dir)


def get_head_commit(path):
    """
    Returns the HEAD of the most recent commit in the repository.

    :param path: ../.git directory ex) /Users/heojaehun/gitRepo/TIL/.git
    :return: HEAD DATA
    """
    head_commit = None
    head_file = os.path.join(path, "HEAD")

    if not os.path.isfile(head_file):
        return

    head_parts = None

    with open(head_file, "r") as fh:
        data = fh.read().strip()
        try:
            head_parts = data.split(" ")[1].split("/")
        except IndexError:
            return data

    if not head_parts:
        return head_commit

    head_ref_file = os.path.join(path, * head_parts)
    if not os.path.isfile(head_ref_file):
        return head_commit

    with open(head_ref_file, "r") as fl:
        head_commit = fl.read().strip()

    return head_commit


def parse_committer_line(line):
    """
        Parse committer / author line which also contains a datetime.
    """
    parts = line.split()
    unix_time = float(parts[-2])
    committer = " ".join(parts[1:-2])
    commit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))
    return committer, commit_time


def parse_git_message(data, git_dict):
    lines = data.decode("utf-8").split("\n")
    reading_pgp = False
    reading_msg = False
    # l = lines[3]
    for idx, l in enumerate(lines):
        if l == "" and not reading_msg:
            reading_pgp = False
            reading_msg = True
            continue

        if reading_pgp:
            continue

        if reading_msg:
            git_dict["message"] += l
            if not l and idx < len(lines) - 1:
                git_dict["message"] += '\n'

        if l.startswith("tree"):
            git_dict["tree"] = l.split()[1]
        elif l.startswith("parent"):
            git_dict["parent"] = l.split()[1]
        elif l.startswith("gpgsig"):
            reading_pgp = True
        elif l.startswith("committer"):
            committer, commit_time = parse_committer_line(l)
            git_dict["committer"] = committer
            git_dict["commit_time"] = commit_time
        elif l.startswith("author"):
            author, author_time = parse_committer_line(l)
            git_dict["author"] = author
            git_dict["author_date"] = author_time

        return git_dict


def get_git_info_dir(path):
    head_commit = get_head_commit(path)
    if not head_commit:
        return None

    head_message_folder = head_commit[:2]
    head_message_file_name = head_commit[2:]
    head_message_file = os.path.join(
        path, "objects", head_message_folder, head_message_file_name
    )

    git_dict = {"commit": head_commit,
                "git_dir": path,
                "message": ""}

    if not os.path.isxrfile(head_message_file):
        object_path = os.path.join(path, "objects", "pack")
        # for idx_file in glob.glob(object_path + "/*.idx"):
        #     r = get_pack_info(idx_file, git_dict)
        #     if not r:
        #         continue
        #     return r

    else:
        with open(head_message_file, "rb") as fl:
            data = zlib.decompress(fl.read())
            if not data[:6] == b"commit":
                return
            null_byte_idx = data.index(b"\x00") + 1
            data = data[null_byte_idx:]
            return parse_git_message(data, git_dict)


def get_git_info(path=None):
    if path is None:
        path = os.getcwd()

    git_dir = find_git_dir(path)
    if not git_dir:
        return None
    return get_git_info_dir(git_dir)



