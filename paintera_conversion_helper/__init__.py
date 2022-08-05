import jgo.util
import os
import sys
import warnings

from . import version

_paintera_convert = '@PainteraConvert'
_extract_to_scalar = '@ExtractHighestResolutionLabelDataset'
_groupId = 'org.janelia.saalfeldlab'
_artifactId = 'paintera-conversion-helper'


def _jgo_arg_is_present(arg: str, argv: list[str], substring: bool = False) -> bool:
    sep = _jgo_args_separator_idx(argv)
    if sep == -1:
        return False

    jgo_args = argv[:sep]
    for a in jgo_args:
        if not substring and arg == a:
            return True
        elif substring and arg in a:
            return True
    return False


def _inject_jgo_arg(arg: str, argv: list[str]):
    jgo_arg_sep_idx = _jgo_args_separator_idx(argv)
    if jgo_arg_sep_idx == -1:
        return [arg, '--'] + argv
    else:
        return [arg] + argv


def _jgo_args_separator_idx(argv):
    try:
        jgo_arg_sep_idx = argv.index('--')
    except ValueError:
        jgo_arg_sep_idx = -1
    return jgo_arg_sep_idx


def _add_manage_dependencies(argv) -> list[str]:
    if _jgo_arg_is_present("-m", argv) or _jgo_arg_is_present("--manage-dependencies", argv):
        return argv
    return _inject_jgo_arg("--manage-dependencies", argv)

def _add_spark_master(argv, spark_master) -> list[str]:
    if _jgo_arg_is_present('-Dspark.master', argv, True):
        return argv

    return _inject_jgo_arg(f'-Dspark.master={spark_master}', argv)


def _inject_jgo_args(argv) -> list[str] :
    argv = _add_spark_master(argv, os.getenv('SPARK_MASTER', 'local[*]'))
    argv =  _add_manage_dependencies(argv)
    print(argv)
    return argv


def launch_extract_to_scalar(argv=sys.argv[1:]):
    try:
        return jgo.util.main_from_endpoint(
            primary_endpoint=f'{_groupId}:{_artifactId}',
            primary_endpoint_version=version._paintera_conversion_helper_version.maven_version(),
            primary_endpoint_main_class=_extract_to_scalar,
            argv=_inject_jgo_args(argv))
    finally:
        warnings.warn(
            'The extract-to-scalar command has been deprecated. Please use paintera-convert instead.',
            DeprecationWarning,
            stacklevel=2)


def launch_paintera_convert(argv=sys.argv[1:]):
    return jgo.util.main_from_endpoint(
        primary_endpoint=f'{_groupId}:{_artifactId}',
        primary_endpoint_version=version._paintera_conversion_helper_version.maven_version(),
        primary_endpoint_main_class=_paintera_convert,
        argv=_inject_jgo_args(argv))
