# TODO: Setup a workspace directory where all the agent's files and user files will be stored. Tasks:

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


class PythonFrontendCRUD:
    def create_component(self, component_name: str):
        return f"Creating frontend component '{component_name}'..."
    def retrieve_component(self, component_name: str):
        return f"Retrieving frontend component '{component_name}'..."
    def update_component(self, component_name: str):
        return f"Updating frontend component '{component_name}'..."
    def delete_component(self, component_name: str):
        return f"Deleting frontend component '{component_name}'..."

class PythonBackendFastAPI:
    def create_endpoint(self, endpoint_name: str):
        return f"Creating FastAPI endpoint '{endpoint_name}'..."
    def retrieve_endpoint(self, endpoint_name: str):
        return f"Retrieving FastAPI endpoint '{endpoint_name}'..."
    def update_endpoint(self, endpoint_name: str):
        return f"Updating FastAPI endpoint '{endpoint_name}'..."
    def delete_endpoint(self, endpoint_name: str):
        return f"Deleting FastAPI endpoint '{endpoint_name}'..."
    
class PythonBackendCRUD:
    def create_endpoint(self, endpoint_name: str):
        return f"Creating backend endpoint '{endpoint_name}'..."
    def retrieve_endpoint(self, endpoint_name: str):
        return f"Retrieving backend endpoint '{endpoint_name}'..."
    def update_endpoint(self, endpoint_name: str):
        return f"Updating backend endpoint '{endpoint_name}'..."
    def delete_endpoint(self, endpoint_name: str):
        return f"Deleting backend endpoint '{endpoint_name}'..."
    
class PythonProjectManager:
    def stages(self, stage: str):
        if stage == "setup_virtualenv":
            return self.setup_virtualenv
        elif stage == "install_dependencies":
            return self.install_dependencies
        elif stage == "create_structure":
            return self.create_structure
        elif stage == "create_backend":
            return self.create_backend
        elif stage == "create_frontend":
            return self.create_frontend
        elif stage == "create_main_file":
            return self.create_main_file
        else:
            raise ValueError(f"Unknown stage: {stage}")
    def install_dependencies(self, directory: str, dependencies: list[str]):
        venv_path = os.path.join(directory, "venv")
        for dep in dependencies:
            os.system(f"{os.path.join(venv_path, 'bin', 'pip')} install {dep}")
    
    def create_structure(self, directory: str):
        os.makedirs(os.path.join(directory, "backend"), exist_ok=True)
        os.makedirs(os.path.join(directory, "frontend"), exist_ok=True)
    
    def get_stage_description(self, stage: str) -> str:
        descriptions = {
            "setup_virtualenv": "Sets up a virtual environment for the project.",
            "install_dependencies": "Installs project dependencies.",
            "create_structure": "Creates the basic project structure.",
            "create_backend": "Creates the backend components.",
            "create_frontend": "Creates the frontend components.",
            "create_main_file": "Creates the main application file."
        }
        return descriptions.get(stage, f"No description available for stage '{stage}'")
    
    def setup_virtualenv(self, directory: str):
        os.system(f"python -m venv {os.path.join(directory, 'venv')}")
        os.system(f"{os.path.join(directory, 'venv', 'bin', 'pip')} install --upgrade pip")
        os.system(f"{os.path.join(directory, 'venv', 'bin', 'pip')} install -r requirements.txt")

    def create_backend(self, directory: str):
        os.makedirs(os.path.join(directory, "backend"), exist_ok=True)
        # TODO: Create a base fastapi app structure with main.py, routers, and models
        
    def create_frontend(self, directory: str):
        os.makedirs(os.path.join(directory, "frontend"), exist_ok=True)
        # TODO: Create a base Flet app structure with main.py and components
        
    def create_main_file(self, backend_directory: str, frontend_directory: str):
        main_file_path = os.path.join(backend_directory, "main.py")
        with open(main_file_path, "w") as f:
            f.write("# TODO: Implement the main application logic here\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    print('Hello, World!')\n")
            
            
class WorkspaceTools:
    def execute_command(self, command: str) -> str:
        """Executes a shell command and returns the output."""
        result = os.popen(command).read()
        return result
    
    def execute_python_script(self, project_name: str, script_name: str) -> str:
        """Executes a Python script from the specified project and returns the output."""
        script_path = os.path.join(self.base_path, project_name, script_name)
        result = os.popen(f"python {script_path}").read()
        return result

    def setup_virtualenv(self, project_name: str):
        """Sets up a virtual environment for the specified project."""
        project_path = os.path.join(self.base_path, project_name)
        os.makedirs(project_path, exist_ok=True)
        os.system(f"python -m venv {os.path.join(project_path, 'venv')}")
    
    def install_dependencies(self, project_name: str, dependencies: list[str]):
        """Installs dependencies in the project's virtual environment."""
        project_path = os.path.join(self.base_path, project_name)
        venv_path = os.path.join(project_path, "venv")
        for dep in dependencies:
            os.system(f"{os.path.join(venv_path, 'bin', 'pip')} install {dep}")
    
    
    
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

    def list_projects_templates(self) -> list[str]:
        return ["python"]  # TODO: Implement a way to list available templates dynamically
    
    def create_project_from_template(self, template: ProjectTemplate):
        template.create_structure(base_path=self.base_path, structure=template.STRUCTURE)
        self.projects[template.name] = Project(template.name)