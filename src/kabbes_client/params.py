import dir_ops as do
import os
from xdg import BaseDirectory
import py_seedlings as ps

sys_args, sys_kwargs = ps.get_system_input_arguments()

# Dir that contains the package
_Dir = do.Dir(os.path.abspath(__file__)).ascend()
_src_Dir = _Dir.ascend()  # src Dir that is one above
_repo_Dir = _src_Dir.ascend()
_cwd_Dir = do.Dir(do.get_cwd())

_src_Dir = _Dir.ascend()  # src Dir that is one above
_repo_Dir = _src_Dir.ascend()
_cwd_Dir = do.Dir(do.get_cwd())
_xdg_Dir = do.Dir(str(BaseDirectory.xdg_config_home))
_home_Dir = do.Dir(do.get_home_dir())
