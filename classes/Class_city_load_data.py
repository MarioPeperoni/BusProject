class city_load_data:
    version = ""
    name = ""
    file_path = "data/cities/"
    creation_date = ""
    imported_from_maps = False

    def __init__(self, version, name, file_path, creation_date, imported_from_maps):
        self.version = version
        self.name = name
        self.file_path = file_path
        self.creation_date = creation_date
        self.imported_from_maps = imported_from_maps

    def to_dict(self):
        return {
            "version": self.version,
            "name": self.name,
            "file_path": self.file_path,
            "creation_date": self.creation_date,
            "imported_from_maps": self.imported_from_maps
        }
