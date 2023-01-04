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

    # For child class instances to define
    _CONFIG = {}

    def __init__( self, **override_config ):
        ParentClass.__init__( self )
        self.override_config = override_config

        self.cfg = kabbes_config.Config()

        order = {
            1: {
                "method": self.load_DEFAULT_CONFIG,
                "obj": None,
            },
            2: {
                "method": self.load_CONFIG,
                "obj": None
            },
            3: {
                "method": self.load_CLIENT_JSON,
                "obj": None
            },
            4: {
                "method": self.load_PACKAGE_CONFIG,
                "obj": None
            },
            5: {
                "method": self.load_PACKAGE_CACHE,
                "obj": None
            },
            6: {
                "method": self.load_USER_CONFIG,
                "obj": None
            },
            7: {
                "method": self.load_CLIENT_OVERRIDE,
                "obj": None
            },
            8: {
                "method": self.load_SYSTEM_KWARGS,
                "obj": None
            }
        }

        for key in order:
            order[ key ][ 'obj '] = order[ key ][ 'method' ]()

        for key in range(4,9):
            order[ key ][ 'obj '] = order[ key ][ 'method' ]( create=True )


    def load_DEFAULT_CONFIG( self ):

        # 1. _DEFAULT_CONFIG attribute
        self.cfg.load_dict( self._DEFAULT_CONFIG )
        self.cfg.reevaluate()

    def load_CONFIG( self ):

        # 2. _CONFIG
        self.cfg.load_dict( self._CONFIG )
        self.cfg.reevaluate()

    def load_CLIENT_JSON( self ):

        # 3. Client DEFAULT JSON
        self.cfg.load_dict( kabbes_client.DEFAULT_CONFIG_PATH.read_json_to_dict() )
        self.cfg.reevaluate()

    def load_PACKAGE_CONFIG( self, create=False ):

        # 4. Package Config - FILE MAY CHANGE
        if not self.cfg.package.config.get_attr('Path',use_ref=True).exists() and create:
            self.cfg.package.config.get_attr('Path',use_ref=True).write( string='{}' )

        if self.cfg.package.config.get_attr('Path',use_ref=True).exists():
            self.cfg.load_dict( self.cfg.package.config.get_attr('Path',use_ref=True).read_json_to_dict() )
            self.cfg.reevaluate()

    def load_PACKAGE_CACHE( self, create=False ):

        # 5. Package cached config - FILE MAY CHANGE
        if not self.cfg.cache.package.get_attr('Dir',use_ref=True).exists() and create:       
            self.cfg.cache.package.get_attr('Dir',use_ref=True).create( override=True )

        if not self.cfg.cache.package.get_attr('Path',use_ref=True).exists() and create:
            self.cfg.cache.package.get_attr('Path',use_ref=True).write( string='{}' )

        if self.cfg.cache.package.get_attr('Path',use_ref=True).exists():
            self.cfg.load_dict( self.cfg.cache.package.get_attr('Path',use_ref=True).read_json_to_dict() )
            self.cfg.reevaluate()


    def load_USER_CONFIG( self, **kwargs ):

        # 6. User-specified file override

        if self.cfg.has_attr( 'user.config.Path' ):
            if self.cfg.user.config.get_attr('Path',use_ref=True).exists():
                self.cfg.load_dict( self.cfg.user.config.get_attr('Path',use_ref=True).read_json_to_dict() )
                self.cfg.reevaluate()

    def load_CLIENT_OVERRIDE( self, **kwargs ):

        # 7. Client override
        self.cfg.load_dict( self.override_config )
        self.cfg.reevaluate()

    def load_SYSTEM_KWARGS( self, **kwargs ):

        # 8. system args
        self.cfg.load_dict( kabbes_client.sys_kwargs )
        self.cfg.reevaluate()


