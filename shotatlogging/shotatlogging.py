# -*- coding: utf-8 -*-

"""Main module."""

import logging
import logging.config
import yaml
import os.path


def merge_dict(dict1, dict2):
    """
    Merge dict1 and dict2 just like update() of dict but if the element is a
    dict we will merge it with the same element inside dict2 and won't replace
    it directly.
    """

    # Overwrite same parts in dict1 from dict2
    for k, v in dict1.items():
        if k not in dict2:
            continue

        if not isinstance(v, dict):
            dict1[k] = dict2[k]
            continue

        merge_dict(dict1[k], dict2[k])

    # Merge missing parts from dict2
    for k, v in dict2.items():
        if (k in dict1) and isinstance(v, dict):
            continue

        dict1[k] = dict2[k]


def setup(cfg_file_path="logging.yml",
          cfg_env_key='SHOTATLOGGING_CFG'):
    """
    Simple way to config python's logging module.

    It provided these features:

    1. Load configs from a YAML file, it's more easy than writting an INI file
    style configure file.

    2. Environment variable that override configure file path in script, that
    help lots while we have some temporary changes for logging settings.

    3. Provided default ready for logging environment.
    """

    default_level = logging.INFO
    default_format = logging.BASIC_FORMAT

    # Environment config key will overwrite cfg_file_path variable
    if cfg_env_key in os.environ:
        cfg_file_path = os.environ[cfg_env_key]

    logging.basicConfig(level=default_level, format=default_format)

    # Default configs
    configs = {
        "version": 1,
        # Don't disable existing loggers, so global logger that in other
        # modules will still valid after setup()
        "disable_existing_loggers": False,
        "formatters": {
            "generic": {
                "format": default_format,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "generic",
            },
        },
        "loggers": {
            "root": {
                "level": logging.getLevelName(default_level),
                # Inherit default logger 'handlers' settings
            },
        },

        # Default logger's settings (All loggers will use these settings)
        # They will all use the 'console' handler by default, so you don't
        # have to add 'console' handler to 'handlers' of loggers
        'root': {
            'level': logging.getLevelName(default_level),
            'handlers': ['console'],
        },

    }

    if os.path.exists(cfg_file_path):
        merge_dict(configs, yaml.safe_load(open(cfg_file_path, 'r')))

    logging.config.dictConfig(configs)
