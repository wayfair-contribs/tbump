import re

import path
import pytest

import tbump.git


@pytest.fixture()
def tmp_path(tmpdir):
    return path.Path(tmpdir)


@pytest.fixture
def test_path():
    this_dir = path.Path(__file__).parent
    return this_dir.abspath()



def setup_repo(tmp_path, test_path):
    src_path = tmp_path.joinpath("src")
    src_path.mkdir()
    test_path.joinpath("tbump.toml").copy(src_path)
    test_path.joinpath("VERSION").copy(src_path)
    test_path.joinpath("package.json").copy(src_path)
    test_path.joinpath("pub.js").copy(src_path)
    tbump.git.run_git(src_path, "init")
    tbump.git.run_git(src_path, "add", ".")
    tbump.git.run_git(src_path, "commit", "--message", "initial commit")
    return src_path


def setup_remote(tmp_path):
    git_path = tmp_path.joinpath("git")
    git_path.mkdir()
    remote_path = git_path.joinpath("repo.git")
    remote_path.mkdir()
    tbump.git.run_git(remote_path, "init", "--bare")

    src_path = tmp_path.joinpath("src")
    tbump.git.run_git(src_path, "remote", "add", "origin", remote_path)
    tbump.git.run_git(src_path, "push", "-u", "origin", "master")
    return src_path


@pytest.fixture
def test_repo(tmp_path, test_path):
    res = setup_repo(tmp_path, test_path)
    setup_remote(tmp_path)
    return res