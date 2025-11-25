from sync_task import SyncTask
from os import path
import task_utils

class TVShowSyncTask(SyncTask):
    def __init__(self, name: str, paths_map: dict[str,str], copies:str ='Duplicate', show_name:str = ""):
        self.show_name = name if show_name == "" else show_name
        src = path.join(task_utils.resolve_placeholders(paths_map['TVSHOWS'], paths_map),
                       self.show_name)
        match copies:
            case 'Duplicate':
                dst = path.join(task_utils.resolve_placeholders(paths_map['TVSHOWS_BCK_1'], paths_map),
                                self.show_name)
            case 'Triplicate':
                dst = [
                    path.join(task_utils.resolve_placeholders(paths_map['TVSHOWS_BCK_1'], paths_map),
                              self.show_name),
                    path.join(task_utils.resolve_placeholders(paths_map['TVSHOWS_BCK_2'], paths_map),
                              self.show_name)
                ]
            case _:
                raise ValueError("Copies setting not supported: " + copies)
        super().__init__("TVShow " + name, src, dst)