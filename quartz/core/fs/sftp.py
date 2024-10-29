import logging
import os

from fabric import Connection

logging.getLogger("paramiko").setLevel(logging.WARNING)


def create_temp_file(data, filename) -> str:
    file_with_path = os.path.join("/tmp", filename)
    with open(file_with_path, "wb") as binary_file:
        binary_file.write(data)
    return file_with_path


def remove_local_file(file_path):
    os.remove(file_path)


class SFTP:
    def __init__(self, directory):
        self.directory = directory
        self.host = os.environ.get("QRT_SFTP_HOST")
        self.port = os.environ.get("QRT_SFTP_PORT", "22")
        self.user = os.environ.get("QRT_SFTP_USER")
        self.password = os.environ.get("QRT_SFTP_PASSWORD")

        if not self.password:
            raise Exception("SFTP password is required")
        self.sftp_client = Connection(
            host=self.host,
            port=self.port,
            user=self.user,
            connect_kwargs={"password": self.password},
        ).sftp()
        print(self.host, self.port, self.user, self.password)

    def delete_files(self, files_to_delete):
        for file_to_delete in files_to_delete:
            try:
                self.sftp_client.remove(file_to_delete)
            except FileNotFoundError:
                pass

    def write_data(self, data, filename):
        local_file = create_temp_file(data, filename)
        remote_file = os.path.join(self.directory, filename)
        self.sftp_client.put(local_file, remote_file)
        remove_local_file(local_file)

    def close(self):
        self.sftp_client.close()

    def get_sub_folder(self):
        return self.directory
