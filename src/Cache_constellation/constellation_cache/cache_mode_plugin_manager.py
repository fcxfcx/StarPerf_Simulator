import importlib
import os


def clear_cache(constellation):
    for shell in constellation.shells:
        for orbit in shell.orbits:
            for satellite in orbit.satellites:
                satellite.cache.clear()  # clear satellite cache


class Cache_mode_plugin_manager:
    def __init__(self, database_manager):
        self.plugins = {}
        package_name = "src.Cache_constellation.constellation_cache.cache_plugin"
        plugins_path = package_name.replace(".", os.path.sep)  # the path where the plug-in is stored
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        self.current_cache_mode = "LFU"
        self.database_manager = database_manager

    # the function of this function is to clear all cache content in the incoming satellite constellation.

    def set_cache_mode(self, plugin_name):
        self.current_cache_mode = plugin_name  # set the current connection mode to the specified mode

    def execute_cache_policy(self, constellation):
        clear_cache(constellation)  # clear all existing ISLs
        function = self.plugins[self.current_cache_mode]
        function(constellation,self.database_manager)  # go to execute the corresponding connection mode function
