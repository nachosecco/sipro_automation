import logging
import os

logger = logging.getLogger(__name__)


class S3Local:
    def __init__(self, directory, sub_folder):
        self.parent_directory = directory
        self.sub_folder = S3Local.create_dirs(directory, sub_folder)

    @staticmethod
    def create_dirs(initial_directory, *sub_folder):
        directory = os.path.join(initial_directory, sub_folder)
        os.makedirs(directory, exist_ok=True)
        return directory

    def is_file_found_in_folder(self, folder, file_name):
        file_with_path = os.path.join(folder, file_name)
        if os.path.isfile(file_with_path):
            return bool(True)

    def delete_files(self, files_to_delete):
        for file_to_delete in files_to_delete:
            file_with_path = os.path.join(self.parent_directory, file_to_delete)
            try:
                if os.path.isfile(file_with_path):
                    os.remove(file_with_path)
            except Exception:
                logger.exception("Couldn't remove file '%s'.", file_with_path)
                raise

    def write_data(self, data, filename):
        file_with_path = os.path.join(self.sub_folder, filename)
        with open(file_with_path, "wb") as binary_file:
            binary_file.write(data)

    def close(self):
        pass

    def get_sub_folder(self):
        return self.sub_folder
