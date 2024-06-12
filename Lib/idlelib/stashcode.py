"""stash - local version control for IDLE"""
import hashlib
import os
import ast
from tkinter import messagebox

def create_hidden_file(folder_name, file_name):
    """
    Create a hidden file in the specified folder.

    Parameters:
    folder_name (str): Name of the folder to create.
    file_name (str): Name of the file to create.

    Returns:
    str: Path to the created file.
    """
    hidden_folder = '.' + folder_name
    file_path = os.path.join(hidden_folder, file_name)
    # Create the hidden folder if it doesn't exist
    os.makedirs(hidden_folder, exist_ok=True)
    # Check if the file exists in the hidden folder
    if not os.path.isfile(file_path):
        # Create the file if it doesn't exist
        with open(file_path, 'w') as f:
            pass
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")
    return file_path

def read_file_contents(file_path):
    """
    Read the contents of a file.

    Parameters:
    file_path (str): Path to the file to read.

    Returns:
    str: Contents of the file, or None if the file doesn't exist.
    """
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def write_to_file(file_path, content):
    """
    Write content to a file.

    Parameters:
    file_path (str): Path to the file to write.
    content (str): Content to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def read_stash_from_file(file_path):
    """
    Read stashes from a file.

    Parameters:
    file_path (str): Path to the file to read.

    Returns:
    list: List of stashes read from the file.
    """
    contents = read_file_contents(file_path)
    if not contents:
        return []
    stashes = contents.split('😀')
    return stashes

def write_stash_to_file(file_path, stashes):
    """
    Write stashes to a file.

    Parameters:
    file_path (str): Path to the file to write.
    stashes (list): List of stashes to write to the file.
    """
    content = '😀'.join(map(str, stashes))
    write_to_file(file_path, content)

class Stash:
    """
    Class for managing stashes of code in an IDLE editor window.
    """

    def __init__(self, editwin):
        """
        Initialize the Stash object.

        Parameters:
        editwin: The editor window for the context block.
        """
        self.editwin = editwin
        self.text = editwin.text
        if editwin.io.filename is None:
            return
        # Handles hidden stash file creation
        self.file_hash = hashlib.sha256(editwin.io.filename.encode()).hexdigest()
        self.file_path = create_hidden_file("idlelibstash", self.file_hash + ".txt")
        self.original_content = self.text.get('1.0', 'end')
        self.stashes = read_stash_from_file(self.file_path)  # keep last 10 stashes
        if self.stashes:
            self.index = len(self.stashes) - 1  # Initialize index to the last stash
        else:
            self.index = 0

    def restore_original(self):
        """
        Restore the original code in the editor window.
        """
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', self.original_content)
        print('Restored original code')

    def get_region(self):
        """
        Get the region of the highlighted code, or the entire code if nothing is highlighted.

        Returns:
        tuple: A tuple containing the start index, end index, code characters, and lines of code.
        """
        text = self.text
        first, last = self.editwin.get_selection_indices()
        if first and last:
            head = text.index(first + " linestart")
            tail = text.index(last + "-1c lineend +1c")
        else:
            head = text.index("1.0")
            tail = text.index("insert lineend +1c")
        chars = text.get(head, tail)
        lines = chars.split("\n")
        return head, tail, chars, lines

    def previous_stash(self):
        """
        Present the previous saved stash.
        """
        if not self.stashes or self.index <= 0:
            print('No previous stash')
            messagebox.showinfo("Message", "No previous stash")
            return
        self.index -= 1  # Move to the previous stash
        previous_stash = self.stashes[self.index]
        self.update_editor_window(previous_stash)

    def next_stash(self):
        """
        Present the next saved stash.
        """
        if not self.stashes or self.index >= len(self.stashes) - 1:
            print('No next stash')
            messagebox.showinfo("Message", "No next stash")
            return
        self.index += 1  # Move to the next stash
        next_stash = self.stashes[self.index]
        self.update_editor_window(next_stash)

    def apply_stash(self):
        """
        Apply the latest stash to the current code region.
        """
        if not self.stashes:
            print('No stashes to apply')
            messagebox.showinfo("Message", "No stashes to apply")
            return
        self.update_editor_window(self.stashes[-1])
        print('Applied stash')

    def update_editor_window(self, stash):
        """
        Update the editor window with the provided stash.

        Parameters:
        stash (str): The stash to apply to the editor window.
        """
        recent_stash = self.convert_from_string(stash)
        self.text.delete('1.0', 'end')
        counter = 1.0
        for line in recent_stash:
            self.text.insert(f'{counter}', line + '\n')
            counter += 1.0

    def convert_from_string(self, stash):
        """
        Convert a stash from a string to its original format.

        Parameters:
        stash (str): The stash in string format.

        Returns:
        list: The stash in its original format.
        """
        if isinstance(stash, str):
            return ast.literal_eval(stash)
        else:
            return stash

    def stash_code(self):
        """
        Stash the current code region.
        """
        head, tail, chars, lines = self.get_region()
        if self.stashes and self.stashes[-1] == lines:
            print('No changes to stash')
            messagebox.showinfo("Message", "No changes to stash")
            return
        self.stashes.append(lines)
        write_stash_to_file(self.file_path, self.stashes)
        self.index = len(self.stashes) - 1

if __name__ == "__main__":
    from unittest import main
    main('idlelib.idle_test.test_codecontext', verbosity=2, exit=False)
