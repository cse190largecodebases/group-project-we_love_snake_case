"""stash - local version control for IDLE"""
import collections
import difflib
import hashlib
import os

def create_hidden_file(folder_name, file_name):
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
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def read_stash_from_file(file_path):
    contents = read_file_contents(file_path)
    if not contents:
        return []
    stashes = contents.split('😀')
    return stashes

def write_stash_to_file(file_path, stashes):
    print(stashes)
    print(type(stashes))
    content = '😀'.join(map(str,stashes))
    write_to_file(file_path, content)

class Stash:
    "Display code outline in new or existing Pyshell."

    def __init__(self, editwin):
        """File for stashing code
        editwin is the Editor window for the context block.
        self.text is the editor window text widget.
        self.get_region --> gets the region of the highlighted code, or gets the entire code if nothing is highlgighted; inspired from get_region in format.py
        self.previous_stash --> presents the previously saved stash
        self.next_stash --> presents the next saved stash
        self.apply_stash --> applies the stash to the current code region
        """

        self.editwin = editwin
        self.text = editwin.text

        # Handles hidden stash file creation
        self.file_hash = hashlib.sha256(editwin.io.filename.encode()).hexdigest()
        self.file_path = create_hidden_file("idlelibstash", self.file_hash + ".txt")

        self.stashes = read_stash_from_file(self.file_path)  # keep last 10 stashes
        print(self.stashes)

        # read the contents of the stash file
        contents = read_file_contents(self.file_path)
        if not contents:
            print(f"File contents: {contents}")

    def get_region(self):
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
        print('previous stash')

    def next_stash(self):
        print('next stash')

    def apply_stash(self):
        if not self.stashes:
            print('No stashes to apply')
            return
        stash = self.stashes[-1]
        head, tail, chars, lines = self.get_region()
        diff = difflib.unified_diff(lines, stash)
        diff_text = '\n'.join(diff)
        self.text.delete(head, tail)
        self.text.insert(head, diff_text)
        print('Applied stash')

    def stash_code(self):
        stashes_deque = collections.deque()
        head, tail, chars, lines = self.get_region()
        if self.stashes and self.stashes[-1] == lines:
            print('No changes to stash')
            return
        stashes_deque.append(lines)
        self.stashes.append(stashes_deque)
        write_stash_to_file(self.file_path, self.stashes)
        print('self.stashes:', self.stashes)
        print('Stashed code')



if __name__ == "__main__":
    from unittest import main
    main('idlelib.idle_test.test_codecontext', verbosity=2, exit=False)