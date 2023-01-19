import kabbes_client
import kabbes_config

class Package:

    _config_dict = {}
    _config_json_Path = kabbes_client._Dir.join_Path( path='Package.json' )

    def __init__( self, _Dir, dict={}, root=kabbes_client.root ):

        valid_root = isinstance( root, kabbes_client.Root )

        ### Load baseline
        self.cfg = kabbes_config.Node( 'TEMP', dict = Package._config_dict )
        self.cfg.merge( kabbes_config.Config( dict = {'_Dir': _Dir} ) )

        ### Load Package.json
        cfg_json = kabbes_config.Config( dict = Package._config_json_Path.read_json_to_dict() )
        self.cfg.merge( cfg_json )

        ### Load _Dir/CONFIG.json
        if self.cfg['package.config.Path'].exists():
            self.cfg.merge( kabbes_config.Config( dict=self.cfg['package.config.Path'].read_json_to_dict() ) )

        ### rename the root
        self.cfg.Key.key = self.cfg['package.name']

        ### get adopted by the root node
        if isinstance( root, kabbes_client.Root ):
            root.cfg.adopt( self.cfg )

        ### Load Cache -> config_cache.json
        if not self.cfg[ 'package.config.cache.Dir' ].exists():
            self.cfg[ 'package.config.cache.Dir' ].create( override=True )

        config_cache_json_Path = self.cfg['package.config.cache.Path']
        if not config_cache_json_Path.exists():
            config_cache_json_Path.write( string='{}' )

        self.cfg.merge( kabbes_config.Config( dict = config_cache_json_Path.read_json_to_dict() ) )

        ### Load cwd config
        if valid_root:
            package_node = root.cfg_cwd.get_node( self.cfg['package.name'], make=False )
            if isinstance( package_node, kabbes_config.Node ):
                self.cfg.merge( package_node )

        ### Load user specified config
        if valid_root:
            package_node = root.cfg_user.get_node( self.cfg['package.name'], make=False )
            if isinstance( package_node, kabbes_config.Node ):
                self.cfg.merge( package_node )

        ### Load dict
        cfg_dict = kabbes_config.Config( dict = dict )
        self.cfg.merge( cfg_dict )

        ### Load system kwargs
        if valid_root:
            package_node = root.cfg_sys.get_node( self.cfg['package.name'], make=False )
            if isinstance( package_node, kabbes_config.Node ):
                self.cfg.merge( package_node )
