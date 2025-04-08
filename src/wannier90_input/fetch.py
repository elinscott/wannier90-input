"""Fetch the XML files from the Wannier90 Github repo."""

import base64
import os
import shutil
import warnings
from collections.abc import Iterable

from github3 import GitHub, login
from github3.exceptions import NotFoundError
from github3.repos import Repository
from github3.repos.commit import RepoCommit
from github3.repos.tag import RepoTag

from wannier90_input.xml_files import directory as xml_directory


def create_github_session(token: str | None = None) -> GitHub:
    """Create a GitHub session with optional authentication."""
    if token is None:
        gh = GitHub()
    else:
        gh = login(token=token)
    return gh


def get_latest_commit(
    owner: str, repo: str, token: str | None = None, branch: str | None = None
) -> RepoCommit:
    """Get the latest commit of a given GitHub repository."""
    gh = create_github_session(token)
    repository: Repository = gh.repository(owner, repo)
    branch = branch or repository.default_branch
    return repository.branch(branch).commit


def list_repo_tags(owner: str, repo: str, token: str | None = None) -> Iterable[RepoTag]:
    """List all tags of a given GitHub repository."""
    gh = create_github_session(token)
    repository: Repository = gh.repository(owner, repo)

    if repository is None:
        warnings.warn(f"Repository {owner}/{repo} not found or access denied.", stacklevel=2)
        return []

    tags = repository.tags()
    if not isinstance(tags, Iterable):
        raise ValueError(f"Failed to find tags for {owner}/{repo}")
    return tags


def download_file(
    owner: str,
    repo: str,
    file_path: str,
    token: str | None = None,
    tag: RepoTag | None = None,
    commit: RepoCommit | None = None,
) -> None:
    """Download a specific file from a given GitHub repository at a specified tag using github3."""
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
        warnings.warn(f"Repository {owner}/{repo} not found or access denied.", stacklevel=2)
        return

    # Fetch the file content
    try:
        file_content = repository.file_contents(file_path, ref=commit.sha)
    except NotFoundError:
        return

    # Create the directory (skip already-fetched commits)
    if os.path.exists(xml_directory / name):
        return
    os.makedirs(xml_directory / name)

    if file_content:
        decoded_content = base64.b64decode(file_content.content)
        with open(xml_directory / name / "parameters.xml", "wb") as f:
            f.write(decoded_content)


def fetch_xml() -> None:
    """Fetch the XML files from the Wannier90 GitHub repo."""
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

    # Copy the latest commit to the folder "latest"
    src = xml_directory / latest_commit.sha[:7] / "parameters.xml"
    dst = xml_directory / "latest" / "parameters.xml"
    if dst.is_file():
        dst.unlink()
    shutil.copy(src, dst)
