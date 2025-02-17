# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from functools import partial
import os
from importlib import import_module
import warnings

from conda import __version__ as CONDA_VERSION

CONDA_VERSION = CONDA_VERSION


def try_exports(module, attr):
    # this assumes conda.exports exists, so only use for conda 4.3 onward
    try:
        return getattr(import_module('conda.exports'), attr)
    except AttributeError:
        return getattr(import_module(module), attr)


try:
    # This monkey patch is addressed at #1825. The ensure_use_local is an outdated vestige
    #   and no longer has any relevant effect.
    import conda.cli.common
    conda.cli.common.ensure_use_local = lambda x: None
except ImportError:
    # no need to patch if it doesn't exist
    pass

# All of these conda's are older than our minimum dependency
conda_43 = True
conda_44 = True
conda_45 = True
conda_46 = True
conda_47 = True
conda_48 = True
conda_411 = True

from conda.exports import (  # noqa: E402
    display_actions,
    execute_actions,
    execute_plan,
    install_actions,
)

display_actions, execute_actions, execute_plan = display_actions, execute_actions, execute_plan
install_actions = install_actions

from conda.exports import _toposort  # NOQA

_toposort = _toposort

from conda.auxlib.packaging import _get_version_from_git_tag  # NOQA

get_version_from_git_tag = _get_version_from_git_tag

from conda.exports import TmpDownload, download, handle_proxy_407  # NOQA
from conda.exports import untracked, walk_prefix  # NOQA
from conda.exports import MatchSpec, NoPackagesFound, Resolve, Unsatisfiable, normalized_version  # NOQA
from conda.exports import human_bytes, hashsum_file, md5_file, memoized, unix_path_to_win, win_path_to_unix, url_path  # NOQA
from conda.exports import get_index  # NOQA
from conda.exports import (Completer, InstalledPackages, add_parser_channels,  # NOQA
                           add_parser_prefix,  # NOQA
                           specs_from_args, spec_from_line, specs_from_url)  # NOQA
from conda.exports import ArgumentParser  # NOQA
from conda.exports import (is_linked, linked, linked_data, prefix_placeholder,  # NOQA
                           rm_rf, symlink_conda, package_cache)  # NOQA
from conda.exports import CondaSession  # NOQA
from conda.exports import (StringIO, input, lchmod,  # NOQA
                           TemporaryDirectory)  # NOQA
from conda.exports import VersionOrder  # NOQA


TmpDownload = TmpDownload
download, handle_proxy_407, untracked, walk_prefix = download, handle_proxy_407, untracked, walk_prefix  # NOQA
MatchSpec, Resolve, normalized_version = MatchSpec, Resolve, normalized_version
human_bytes, hashsum_file, md5_file, memoized = human_bytes, hashsum_file, md5_file, memoized
unix_path_to_win, win_path_to_unix, url_path = unix_path_to_win, win_path_to_unix, url_path
get_index, Completer, InstalledPackages = get_index, Completer, InstalledPackages
add_parser_channels, add_parser_prefix = add_parser_channels, add_parser_prefix
specs_from_args, spec_from_line, specs_from_url = specs_from_args, spec_from_line, specs_from_url
is_linked, linked, linked_data, prefix_placeholder = is_linked, linked, linked_data, prefix_placeholder # NOQA
rm_rf, symlink_conda, package_cache = rm_rf, symlink_conda, package_cache
input, lchmod = input, lchmod
TemporaryDirectory = TemporaryDirectory
ArgumentParser, CondaSession, VersionOrder = ArgumentParser, CondaSession, VersionOrder


from conda.core.package_cache import ProgressiveFetchExtract  # NOQA
from conda.models.dist import Dist, IndexRecord  # NOQA

ProgressiveFetchExtract = ProgressiveFetchExtract
Dist, IndexRecord = Dist, IndexRecord

import configparser  # NOQA
configparser = configparser


from conda.exports import FileMode, PathType  # NOQA
FileMode, PathType = FileMode, PathType
from conda.exports import EntityEncoder  # NOQA

EntityEncoder, FileMode, PathType = EntityEncoder, FileMode, PathType


CondaError = try_exports("conda.exceptions", "CondaError")
CondaHTTPError = try_exports("conda.exceptions", "CondaHTTPError")
LinkError = try_exports("conda.exceptions", "LinkError")
LockError = try_exports("conda.exceptions", "LockError")
NoPackagesFoundError = try_exports("conda.exceptions", "NoPackagesFoundError")
PaddingError = try_exports("conda.exceptions", "PaddingError")
UnsatisfiableError = try_exports("conda.exceptions", "UnsatisfiableError")

non_x86_linux_machines = try_exports("conda.base.context", "non_x86_linux_machines")
context = try_exports("conda.base.context", "context")
context_get_prefix = try_exports("conda.base.context", "get_prefix")
reset_context = try_exports("conda.base.context", "reset_context")
get_conda_build_local_url = try_exports("conda.models.channel", "get_conda_build_local_url")

binstar_upload = context.binstar_upload
bits = context.bits
default_python = context.default_python
envs_dirs = context.envs_dirs
pkgs_dirs = list(context.pkgs_dirs)
cc_platform = context.platform
root_dir = context.root_dir
root_writable = context.root_writable
subdir = context.subdir
create_default_packages = context.create_default_packages

get_rc_urls = lambda: list(context.channels)
get_prefix = partial(context_get_prefix, context)
cc_conda_build = context.conda_build if hasattr(context, 'conda_build') else {}

from conda.exports import Channel  # NOQA
get_conda_channel = Channel.from_value

# disallow softlinks.  This avoids a lot of dumb issues, at the potential cost of disk space.
os.environ['CONDA_ALLOW_SOFTLINKS'] = 'false'
reset_context()

get_local_urls = lambda: list(get_conda_build_local_url()) or []
arch_name = context.arch_name


CondaError, CondaHTTPError, get_prefix, LinkError = CondaError, CondaHTTPError, get_prefix, LinkError  # NOQA
LockError, non_x86_linux_machines, NoPackagesFoundError = LockError, non_x86_linux_machines, NoPackagesFoundError  # NOQA
PaddingError, UnsatisfiableError = PaddingError, UnsatisfiableError


class CrossPlatformStLink:
    def __call__(self, path: str | os.PathLike) -> int:
        return self.st_nlink(path)

    @classmethod
    def st_nlink(cls, path: str | os.PathLike) -> int:
        warnings.warn(
            "`conda_build.conda_interface.CrossPlatformStLink` is pending deprecation and will be removed in a "
            "future release. Please use `os.stat().st_nlink` instead.",
            PendingDeprecationWarning,
        )
        return os.stat(path).st_nlink


class SignatureError(Exception):
    pass


def which_package(path):
    """
    given the path (of a (presumably) conda installed file) iterate over
    the conda packages the file came from.  Usually the iteration yields
    only one package.
    """
    from os.path import abspath, join
    path = abspath(path)
    prefix = which_prefix(path)
    if prefix is None:
        raise RuntimeError("could not determine conda prefix from: %s" % path)
    for dist in linked(prefix):
        meta = is_linked(prefix, dist)
        if any(abspath(join(prefix, f)) == path for f in meta['files']):
            yield dist


def which_prefix(path):
    """
    given the path (to a (presumably) conda installed file) return the
    environment prefix in which the file in located
    """
    from os.path import abspath, join, isdir, dirname
    prefix = abspath(path)
    iteration = 0
    while iteration < 20:
        if isdir(join(prefix, 'conda-meta')):
            # we found the it, so let's return it
            break
        if prefix == dirname(prefix):
            # we cannot chop off any more directories, so we didn't find it
            prefix = None
            break
        prefix = dirname(prefix)
        iteration += 1
    return prefix


def get_installed_version(prefix, pkgs):
    """Primarily used by conda-forge, but may be useful in general for checking when a package
    needs to be updated"""
    from conda_build.utils import ensure_list
    pkgs = ensure_list(pkgs)
    linked_pkgs = linked(prefix)
    versions = {}
    for pkg in pkgs:
        vers_inst = [dist.split('::', 1)[-1].rsplit('-', 2)[1] for dist in linked_pkgs
            if dist.split('::', 1)[-1].rsplit('-', 2)[0] == pkg]
        versions[pkg] = vers_inst[0] if len(vers_inst) == 1 else None
    return versions


# when deactivating envs (e.g. switching from root to build/test) this env var is used,
# except the PR that removed this has been reverted (for now) and Windows doesnt need it.
env_path_backup_var_exists = os.environ.get('CONDA_PATH_BACKUP', None)
