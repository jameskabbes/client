from parent_class import ParentClass
import kabbes_config
import kabbes_client

class Client( ParentClass ):

    _DEFAULT_CONFIG = {
        "_Dir":       kabbes_client._Dir,
        "cwd.Dir":    kabbes_client._cwd_Dir,
        "xdg.Dir":    kabbes_client._xdg_Dir,
        "home.Dir":   kabbes_client._home_Dir,
    }

    _IMP_ATTS = ['cfg']
    _ONE_LINE_ATTS = ['cfg']

    # For child class instances to define
    _CONFIG = {}

    def __init__( self, cfg=None, dict={} ):

        ParentClass.__init__( self )

        self.override_dict = dict
        if cfg == None:
            cfg = kabbes_config.Config( dict=dict )
        self.cfg = cfg

        self.load_DEFAULT_CONFIG()
        self.load_CONFIG()
        self.load_CLIENT_JSON()
        package_config_Path = self.load_PACKAGE_CONFIG()
        package_config_cache_Path = self.load_PACKAGE_CONFIG_CACHE()
        user_config_Path = self.load_USER_CONFIG()
        self.load_CLIENT_OVERRIDE()
        self.load_SYSTEM_KWARGS()

        # reload ones that have file paths
        package_config_Path2 = self.load_PACKAGE_CONFIG( create=True )
        package_config_cache_Path2= self.load_PACKAGE_CONFIG_CACHE( create=True )
        user_config_Path2 = self.load_USER_CONFIG()

        if package_config_Path != None:
            assert package_config_Path == package_config_Path2
        if package_config_cache_Path != None:
            assert package_config_cache_Path == package_config_cache_Path2
        if user_config_Path != None:
            assert user_config_Path == user_config_Path2


    def load_DEFAULT_CONFIG( self ):

        # 1. _DEFAULT_CONFIG attribute
        self.cfg.load_dict( self._DEFAULT_CONFIG )

    def load_CONFIG( self ):

        # 2. _CONFIG
        self.cfg.load_dict( self._CONFIG )

    def load_CLIENT_JSON( self ):

        # 3. Client DEFAULT JSON
        self.cfg.load_dict( kabbes_client.DEFAULT_CONFIG_PATH.read_json_to_dict() )

    def load_PACKAGE_CONFIG( self, create=False ):

        # 4. Package Config - FILE MAY CHANGE
        if not self.cfg['package.config.Path'].exists() and create:
            self.cfg['package.config.Path'].write( string='{}' )

        if self.cfg['package.config.Path'].exists():
            self.cfg.load_dict( self.cfg['package.config.Path'].read_json_to_dict() )

            return self.cfg['package.config.Path']

    def load_PACKAGE_CONFIG_CACHE( self, create=False ):

        # 5. Package cached config - FILE MAY CHANGE
        if not self.cfg['package.config.cache.Dir'].exists() and create:       
            self.cfg['package.config.cache.Dir'].create( override=True )

        if not self.cfg['package.config.cache.Path'].exists() and create:
            self.cfg['package.config.cache.Path'].write( string='{}' )

        if self.cfg['package.config.cache.Path'].exists():
            self.cfg.load_dict( self.cfg['package.config.cache.Path'].read_json_to_dict() )

            return self.cfg['package.config.cache.Path']

    def load_USER_CONFIG( self, **kwargs ):

        # 6. User-specified file override
        if self.cfg.has_attr( 'user.config.Path' ):
            if self.cfg['user.config.Path'].exists():
                self.cfg.load_dict( self.cfg['user.config.Path'].read_json_to_dict() )

                return self.cfg['user.config.Path']

    def load_CLIENT_OVERRIDE( self, **kwargs ):

        # 7. Client override
        self.cfg.load_dict( self.override_dict )

    def load_SYSTEM_KWARGS( self, **kwargs ):

        # 8. system args
        self.cfg.load_dict( kabbes_client.sys_kwargs )
    