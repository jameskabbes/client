# client
A package used to standardize the creation of "client" objects across many other modules.

[Documentation](https://jameskabbes.github.io/client)<br>
[PyPI](https://pypi.org/project/kabbes-client)

# instructions
more details to come

# pecking order, lowest to highest

* Root -> _config_dict
* Root -> _config_json_Path
* Root -> _config_cache_Path
* Root -> cwd_config
* Root -> sys_kwargs
* Root -> user.config.path

* Package -> _config_dict
* Package -> _Dir
* Package -> _config_json_Path
* Package -> package.config.cache.Path
* Package -> Root.cfg_cwd[ 'package.name' ]
* Package -> Root.cfg_user[ 'package.name' ]
* Package -> overwrite dict
* Package -> Root.cfg_sys[ 'package.name' ]

# Author
James Kabbes