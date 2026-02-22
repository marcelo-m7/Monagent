# TODO: Setup a workspace directory where all the agent's files and user files will be stored. Tasks:
# - Create a unique directory for each user, using its name or ID, to keep its files organized and separate from other users
# - Inside each user's directory, create subdirectories for different projects or tasks, to further organize the files and make it easier to find them
# - Implement a function to save files to the appropriate directory based on the user's ID and the project or task they are working on, ensuring that files are stored in the correct location and can be easily accessed when needed
# - Implement a function to retrieve files from the workspace based on the user's ID and the project or task they are working on, allowing users to easily access their files when needed
# - Implement a function to delete files from the workspace when they are no longer needed, to keep the workspace organized and free of unnecessary files
# - Implement a function to list all files in the workspace for a given user, to provide an overview of the files they have stored and make it easier to find specific files when needed
# - Implement a function to move files between different directories in the workspace, to allow users to reorganize their files as needed and keep their workspace organized

import os
import shutil


class Workspace:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.base_path = f"./workspace/{user_id}"
        # Create the base directory for the user if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)

    def save_file(self, project_name: str, file_name: str, content: str):
        project_path = os.path.join(self.base_path, project_name)
        os.makedirs(project_path, exist_ok=True)
        file_path = os.path.join(project_path, file_name)
        with open(file_path, "w") as f:
            f.write(content)

    def retrieve_file(self, project_name: str, file_name: str) -> str:
        file_path = os.path.join(self.base_path, project_name, file_name)
        with open(file_path, "r") as f:
            return f.read()

    def delete_file(self, project_name: str, file_name: str):
        file_path = os.path.join(self.base_path, project_name, file_name)
        os.remove(file_path)

    def list_files(self, project_name: str) -> list[str]:
        project_path = os.path.join(self.base_path, project_name)
        return os.listdir(project_path)

    def move_file(self, old_project_name: str, new_project_name: str, file_name: str):
        old_file_path = os.path.join(self.base_path, old_project_name, file_name)
        new_project_path = os.path.join(self.base_path, new_project_name)
        os.makedirs(new_project_path, exist_ok=True)
        new_file_path = os.path.join(new_project_path, file_name)
        shutil.move(old_file_path, new_file_path)