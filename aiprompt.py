class Prompt:
    def __init__(self, project_files, user_input):
        self.file_separation = "Inclose code with ``` and include file name after first ``` block on the same line as a block."
        self.file_update = "if you doing update to file return whole updated file."
        # file_delete = "If you move all code from the file or file no longer need say $$$$Action: Delete file 'file name' at the end."
        self.project_files = project_files
        self.user_input = user_input

    def create_prompt(self):
        conversation = "\n\n".join([self.project_files, self.user_input, self.file_separation, self.file_update])
        return conversation

    def __str__(self):
        return self.create_prompt()