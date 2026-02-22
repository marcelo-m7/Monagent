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
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DirectoryStructure:
    """Defines a directory structure with folders and files at each level."""
    folders: List[str]
    substructure: Dict[str, "DirectoryStructure"] = None
    files: List[str] = None
    
    def __post_init__(self):
        if self.substructure is None:
            self.substructure = {}
        if self.files is None:
            self.files = []


class ProjectTemplate:
    """Base class for project templates with robust folder structure setup."""
    
    STRUCTURE: DirectoryStructure = None
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
    
    @classmethod
    def create_structure(cls, base_path: str, structure: DirectoryStructure, current_path: str = ""):
        """Recursively creates the directory structure."""
        for folder in structure.folders:
            folder_path = os.path.join(current_path, folder) if current_path else folder
            full_path = os.path.join(base_path, folder_path)
            os.makedirs(full_path, exist_ok=True)
            
            # Create files at this level
            for file in structure.files:
                file_path = os.path.join(full_path, file)
                if not os.path.exists(file_path):
                    open(file_path, "a").close()
            
            # Recursively create substructures
            if folder in structure.substructure:
                cls.create_structure(base_path, structure.substructure[folder], folder_path)


class PythonProjectTemplate(ProjectTemplate):
    """Template for Python projects with predefined structure."""
    
    STRUCTURE = DirectoryStructure(
        folders=["src", "tests", "docs", "data"],
        files=[],
        substructure={
            "src": DirectoryStructure(
                folders=["api", "app", "models"],
                files=["main.py", "__init__.py"],
                substructure={
                    "api": DirectoryStructure(
                        folders=["v1"],
                        files=[],
                        substructure={
                            "v1": DirectoryStructure(
                                folders=[],
                                files=["endpoints.py", "__init__.py"]
                            )
                        }
                    ),
                    "app": DirectoryStructure(
                        folders=["models", "services", "controllers"],
                        files=[],
                        substructure={
                            "models": DirectoryStructure(folders=[], files=["abstract.py", "__init__.py"]),
                            "services": DirectoryStructure(folders=[], files=["abstract.py", "__init__.py"]),
                            "controllers": DirectoryStructure(folders=[], files=["abstract.py", "__init__.py"]),
                        }
                    )
                }
            ),
            "tests": DirectoryStructure(
                folders=["unit", "integration"],
                files=["test_main.py", "__init__.py"],
            ),
            "docs": DirectoryStructure(
                folders=["design", "user_manual"],
                files=["README.md"],
            ),
        }
    )
    
    def __init__(self, name: str, description: str = ""):
        super().__init__(name, description)
    
    def setup(self, base_path: str):
        """Sets up the project structure at the given base path."""
        project_path = os.path.join(base_path, self.name)
        self.create_structure(project_path, self.STRUCTURE)

class Project:
    def __init__(self, name: str):
        self.name = name
    

class FileManager:
    base_path: str
    project_name: str
    
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
    
    
class Workspace(FileManager):    
    projects: Dict[str, Project]
    current_project: str | None
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.base_path = f"./workspace/{user_id}"
        # Create the base directory for the user if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)
        
        # Projects settings
        self.projects = {}
        self.current_project = None

    def list_projects(self) -> list[str]:
        return list(self.projects.keys())
    
    def switch_project(self, project_name: str):
        if project_name in self.projects:
            self.current_project = project_name
        else:
            raise ValueError(f"Project '{project_name}' does not exist.")
   
    def get_current_project(self) -> str | None:
        return self.current_project
    
    
    def get_project(self, project_name: str) -> Project:
        if project_name in self.projects:
            return self.projects[project_name]
        else:
            raise ValueError(f"Project '{project_name}' does not exist.")
        
    def create_project(self, project_name: str):
        self.projects[project_name] = Project(project_name)
        project_path = os.path.join(self.base_path, project_name)
        os.makedirs(project_path, exist_ok=True)
    
    def delete_project(self, project_name: str):
        if project_name in self.projects:
            del self.projects[project_name]
        project_path = os.path.join(self.base_path, project_name)
        shutil.rmtree(project_path)