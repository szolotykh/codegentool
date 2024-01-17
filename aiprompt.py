class Prompt:
    def __init__(self, project_files, user_input):

        # file_delete = "If you move all code from the file or file no longer need say $$$$Action: Delete file 'file name' at the end."
        self.project_files = project_files
        self.user_input = user_input

    def create_prompt(self):
        messages=[
            {"role": "system", "content": self.read_static_template("main.txt")},
            {"role": "system", "content": self.project_files},
            {"role": "user", "content": self.user_input}
        ]
        return messages
    
    def read_static_template(self, file_name):
        with open("./templates/" + file_name, "r") as f:
            return f.read()

    def __str__(self):
        return self.create_prompt()