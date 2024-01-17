import os
import argparse
import repository
import aiprompt
import aigenerator
import json
from datetime import datetime

def delete_file(fileName):
    print("Deleting file: " + fileName)
    # os.remove(fileName)
    return "File deleted"

def main():
    # Create an argument parser to parse the command line arguments
    parser = argparse.ArgumentParser(description='Code generator')
    parser.add_argument('--path', help='Path to repository', required=True)
    args = parser.parse_args()

    cwd = args.path

    # Check if the folder path is an absolute path
    if not os.path.isabs(cwd):
        cwd = os.path.abspath(cwd)

    generator = aigenerator.AIGenerator("gpt-4")

    repo = repository.Repository(cwd)

    previousPrompt = ""

    while True:
        user_input = input("You: ")
        if user_input.lower() == "#exit":
            break

        if user_input.lower() == "#clear":
            repo.clear()
            repo.init_git_repo()
            continue

        project_files = project_files = repo.get_all_files()

        prompt = aiprompt.Prompt(project_files, user_input)
        print(prompt.create_prompt())
        message = generator.generate_code(prompt.create_prompt())

        
        print(message.content)
        if (repo.has_changes_to_commit()):
            print("Committing changes...")
            repo.commit_all_files(datetime.now())
        repo.update(message.content)

if __name__ == '__main__':
    main()