import jgo.util
import os
import sys
import warnings

from . import version

_paintera_conversion_helper = '@CommandLineConverter'
_paintera_convert           = '@PainteraConvert'
_extract_to_scalar          = '@ExtractHighestResolutionLabelDataset'
_groupId                    = 'org.janelia.saalfeldlab'
_artifactId                 = 'paintera-conversion-helper'

def _add_spark_master(argv, spark_master):
    for arg in argv:
        if '-Dspark.master' in arg:
            return argv

    try:
        double_dash_index = argv.index('--')
    except ValueError:
        double_dash_index = -1

    spark_master_arg = [f'-Dspark.master={spark_master}']
    if double_dash_index == -1:
        spark_master_arg += ['--']
    return  spark_master_arg + argv

def launch_pch(argv=sys.argv[1:]):
    try:
        return jgo.util.main_from_endpoint(
            primary_endpoint            = f'{_groupId}:{_artifactId}',
            primary_endpoint_version    = version._paintera_conversion_helper_version.maven_version(),
            primary_endpoint_main_class = _paintera_conversion_helper,
            argv                        = _add_spark_master(argv, os.getenv('SPARK_MASTER', 'local[*]')))
    finally:
        warnings.warn(
            'The paintera-conversion-helper command has been deprecated. Please use paintera-convert instead.',
            DeprecationWarning,
            stacklevel=2)

def launch_extract_to_scalar(argv=sys.argv[1:]):
    try:
        return jgo.util.main_from_endpoint(
            primary_endpoint            = f'{_groupId}:{_artifactId}',
            primary_endpoint_version    = version._paintera_conversion_helper_version.maven_version(),
            primary_endpoint_main_class = _extract_to_scalar,
            argv                        = _add_spark_master(argv, os.getenv('SPARK_MASTER', 'local[*]')))
    finally:
        warnings.warn(
            'The extract-to-scalar command has been deprecated. Please use paintera-convert instead.',
            DeprecationWarning,
            stacklevel=2)

def launch_paintera_convert(argv=sys.argv[1:]):
    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        primary_endpoint_version    = version._paintera_conversion_helper_version.maven_version(),
        primary_endpoint_main_class = _paintera_convert,
        argv                        = _add_spark_master(argv, os.getenv('SPARK_MASTER', 'local[*]')))


