import os
import shutil
import re
import subprocess

def save_history(text):
    with open("./history.txt", "w") as file:
        # Write the string to the file
        file.write(text)

def read_history():
    with open("./history.txt", "r") as file:
        # Write the string to the file
        return file.read()
    
class Repository:
    directory = ""
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            self.init_git_repo()

    # Function is creating or updating a file in the repository
    # Return "File <file_name> created or updated" if the file was created or updated
    # Return "File <file_name> wasn't created or updated" if the file was not created or updated
    def create_or_update_file(self, file_name, file_content):
        print(f"CREATING_OR_UPDATING_FILE ({file_name}, {file_content})")
        try:
            file_path = os.path.join(self.directory, file_name)
            with open(file_path, 'w') as file:
                file.write(file_content)
            return f"File {file_name} created or updated"
        except Exception as e:
            return f"File {file_name} wasn't created or updated"

    def update(self, text):
        # Regex pattern to find the block with file name and content
        pattern = r'```(.*?)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            file_name, content = match
            file_name = file_name.strip()
            content = content.strip()

            # Save the content to a file with the provided file name
            with open(self.directory + "/" + file_name, 'w') as file:
                file.write(content)

    def get_all_files(self):
        result = ""
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)
            
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    result += f"```{file_name}\n{content}\n```\n\n"
                    
        return result

    def clear(self):
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, item)

            if os.path.isfile(item_path):
                os.remove(item_path)  # Remove file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory
        
    def init_git_repo(self):
        try:
            subprocess.run(["git", "init"], cwd=self.directory, check=True)
            print(f"Initialized empty Git repository in {self.directory}")
        except subprocess.CalledProcessError as e:
            print(f"Error initializing Git repository in {self.directory}: {e}")

    def commit_all_files(self, commit_message):
        # get the current working directory
        cwd = os.getcwd()

        # change directory to the Git repository
        os.chdir(self.directory)

        # stage all changes
        os.system('git add -A')

        # commit changes with the given commit message
        os.system('git commit -m "{}"'.format(commit_message))

        # change back to the original working directory
        os.chdir(cwd)

    def has_changes_to_commit(self):
        # get the current working directory
        cwd = os.getcwd()

        # change directory to the Git repository root directory
        os.chdir(self.directory)

        # check if there are any changes to commit
        has_changes = os.system('git status --porcelain') != 0

        # change back to the original working directory
        os.chdir(cwd)

        return has_changes