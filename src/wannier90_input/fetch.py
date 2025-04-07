"""Fetch the XML files from the Wannier90 Github repo.

the xml files of all tags from https://github.com/wannier-developers/wannier90/blob/<tag>/docs/docs/parameters/parameters.xml and adds them to this folder.
"""

import base64
import os

import github3
from github3.repos import Repository
from github3.repos.commit import RepoCommit
from github3.repos.tag import RepoTag

from wannier90_input.xml_files import directory as xml_directory


def create_github_session(token: str | None = None):
    if token is None:
        gh = github3.GitHub()
    else:
        gh = github3.login(token=token)
    return gh


def get_latest_commit(owner: str, repo: str, token: str | None = None, branch: str | None = None):
    gh = create_github_session(token)
    repository: Repository = gh.repository(owner, repo)
    branch = branch or repository.default_branch
    return repository.branch(branch).commit


def list_repo_tags(owner: str, repo: str, token: str | None = None) -> list[RepoTag]:
    """Lists all tags of a given GitHub repository."""
    gh = create_github_session(token)
    repository: Repository = gh.repository(owner, repo)

    if repository is None:
        print(f"Repository {owner}/{repo} not found or access denied.")
        return []

    return repository.tags()


def download_file(owner: str, repo: str, file_path: str, token: str | None = None, tag: RepoTag | None = None, commit: RepoCommit | None = None):
    """Downloads a specific file from a given GitHub repository at a specified tag using github3."""
    gh = create_github_session(token)
    repository = gh.repository(owner, repo)

    if tag:
        name = tag.name
        commit = tag.commit
    elif commit:
        name = commit.sha[:7]
    else:
        raise ValueError("Either tag or commit must be provided.")

    if repository is None:
        print(f"Repository {owner}/{repo} not found or access denied.")
        return

    # Fetch the file content
    try:
        file_content = repository.file_contents(file_path, ref=commit.sha)
    except:
        return

    # Create the directory (skip already-fetched commits)
    if os.path.exists(xml_directory / name):
        return
    os.makedirs(xml_directory / name)

    if file_content:
        decoded_content = base64.b64decode(file_content.content)
        with open(xml_directory / name / "parameters.xml", 'wb') as f:
            f.write(decoded_content)
        print(f"File {file_path} downloaded successfully for commit {name}.")


def fetch_xml():
    owner = "wannier-developers"
    repo = "wannier90"
    file_path = "docs/docs/parameters/parameters.xml"

    # Load the environment variable GITHUB_TOKEN (if set)
    token = os.getenv("GITHUB_TOKEN")

    # Download the file for all tags
    for tag in list_repo_tags(owner, repo, token=token):
        download_file(owner, repo, file_path, token=token, tag=tag)

    # Download the file for the latest commit
    latest_commit = get_latest_commit(owner, repo, token)
    download_file(owner, repo, file_path, token, commit=latest_commit)

    # Link the latest commit to the folder "latest"
    src = xml_directory / latest_commit.sha[:7] / "parameters.xml"
    dst = xml_directory / "latest" / "parameters.xml"
    if dst.is_file():
        dst.unlink()
    dst.symlink_to(src)
