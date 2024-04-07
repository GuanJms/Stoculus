import os
import json
from _enums import DomainEnum
from typing import Optional, TextIO, Iterator, List
from utils.device_enviroment import get_macbook_enviroment


def update_configure(func):
    def wrapper(*args, **kwargs):
        cls = args[0]
        cls._check_initialized()
        return func(*args, **kwargs)

    return wrapper


class ConfigurationManager:
    _configure_folder_path: str = os.path.join(os.path.dirname(__file__), 'configuration_files')
    _root_system: Optional[str] = None
    _domain_path: dict = {}
    _domain_config: dict ={}
    _initialized: bool = False
    _testing_device: Optional[str] = None

    @classmethod
    def set_testing_device(cls):
        import platform
        os_name = platform.system()
        match os_name:
            case "Darwin":  # MacOS
                cls._testing_device = get_macbook_enviroment()
            case "Windows":
                # Add your code for Windows here
                raise NotImplementedError("Windows is not supported")
            case _:
                raise EnvironmentError(f"Unsupported OS: {os_name}")

    @classmethod
    def _run_path_config(cls, config_file):
        config_data = json.load(config_file)
        cls._root_system = config_data.get(f'DATABASE_ROOT', None).get(cls._testing_device, None)
        cls._domain_path = config_data.get('DOMAIN_PATH', None)

    @classmethod
    def load_configurations(cls):
        """Reads all JSON configuration files in the configuration folder and    updates the class-level configuration
        dictionaries."""
        cls._initialized = True
        for filename in os.listdir(cls._configure_folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(cls._configure_folder_path, filename)
                with open(file_path, 'r') as config_file:
                    cls._run_configure_folder(filename, config_file)

    @classmethod
    def _check_initialized(cls):
        if cls._testing_device is None:
            try:
                cls.set_testing_device()
            except Exception as e:
                print(f"Error setting testing device: {e}")
        if not cls._initialized:
            cls.load_configurations()

    @classmethod
    def _run_configure_folder(cls, filename: str, config_file: TextIO):
        if 'path_config' in filename:
            cls._run_path_config(config_file)
        if 'domain_config' in filename:
            cls._run_domain_config(config_file)

    @classmethod
    def _run_domain_config(cls, config_file):
        config_data = json.load(config_file)
        cls._domain_config = config_data.get('DOMAIN', None)


    @classmethod
    @update_configure
    def get_root_system(cls):
        cls._check_initialized()
        if cls._root_system is None:
            raise ValueError('Missing root_system in path_config')
        return cls._root_system

    @classmethod
    def get_path_config(cls):
        pass

    @classmethod
    @update_configure
    def get_domain_path(cls, domains: List[DomainEnum]):
        domain_path_to_return = {}
        traverser = cls._domain_path
        domain_chain = domains #TODO: Implement a function to sort domains in the list
        for domain in domain_chain:
            traverser = traverser[domain.to_string()]
            domain_path_to_return[domain.to_string()] = traverser.get("BASE")
        return domain_path_to_return

    @classmethod
    @update_configure
    def get_domain_config(cls, domains: List[DomainEnum]):
        domain_config_to_return = {}
        traverser = cls._domain_config
        domain_chain = domains #TODO: Implement a function to sort domains in the list
        for domain in domain_chain:
            traverser = traverser[domain.to_string()]
        domain_config_to_return['FILE_TYPE'] = traverser.get("FILE_TYPE", None)
        domain_config_to_return['TIME_COLUMN'] = traverser.get("TIME_COLUMN", None)
        domain_config_to_return['HAS_HEADER'] = traverser.get("HAS_HEADER", None)
        return domain_config_to_return

