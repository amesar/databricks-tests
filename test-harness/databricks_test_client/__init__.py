from databricks_cli.dbfs import api

def add_repr_to_FileInfo():
    def custom_repr(self):
        try:
            return f"path={self.dbfs_path.absolute_path} file_size={self.file_size} is_dir={self.is_dir}"
        except Exception as e:
            return "??"
    api.FileInfo.__repr__ = custom_repr

add_repr_to_FileInfo()


