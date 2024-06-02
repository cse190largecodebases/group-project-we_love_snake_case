# """stash - local version control for IDLE"""
# import collections 


# class Stash:
#     "Display code outline in new or existing Pyshell."

#     def __init__(self, editwin):
#         """File for stashing code 
#         editwin is the Editor window for the context block.
#         self.text is the editor window text widget.
#         self.get_region --> gets the region of the highlighted code, or gets the entire code if nothing is highlgighted; inspired from get_region in format.py
#         self.previous_stash --> presents the previously saved stash
#         self.previous_stash --> presents the next saved stash
#         self.apply_stash --> applies the stash to the current code region
#         self.toggle_code_stash_event --> event handler for the toggle_code_stash_event
#         """
#         self.editwin = editwin
#         self.text = editwin.text

#     def get_region(self):
#         text = self.text
#         first, last = self.editwin.get_selection_indices()
#         if first and last:
#             head = text.index(first + " linestart")
#             tail = text.index(last + "-1c lineend +1c")
#         else:
#             head = text.index("1.0")
#             tail = text.index("insert lineend +1c")
#         chars = text.get(head, tail)
#         lines = chars.split("\n")
#         return head, tail, chars, lines
    
#     @staticmethod
#     def toggle_code_stash_event(self, event=None):  
#         print('stashed')

#     @staticmethod
#     def previous_stash(self):
#         print('previous stash')
    
#     @staticmethod
#     def next_stash(self):
#         print('next stash')

#     @staticmethod
#     def apply_stash(self):
#         print('apply stash')

#     @staticmethod
#     def stash_code(self):
#         print('stash code')



# if __name__ == "__main__":
#     from unittest import main
#     main('idlelib.idle_test.test_codecontext', verbosity=2, exit=False)

"""stash - local version control for IDLE"""
import collections 
import difflib
import hashlib
from idlelib.runscript import ScriptBinding


class Stash:
    "Display code outline in new or existing Pyshell."

    def __init__(self, editwin):
        """File for stashing code 
        editwin is the Editor window for the context block.
        self.text is the editor window text widget.
        self.get_region --> gets the region of the highlighted code, or gets the entire code if nothing is highlgighted; inspired from get_region in format.py
        self.previous_stash --> presents the previously saved stash
        self.previous_stash --> presents the next saved stash
        self.apply_stash --> applies the stash to the current code region
        self.toggle_code_stash_event --> event handler for the toggle_code_stash_event
        """
        self.script = ScriptBinding(editwin)
        self.filename = self.script.getfilename()
        print(self.filename)
        self.editwin = editwin
        self.text = editwin.text
        # self.file_path = hashlib.sha256(editwin.io.filename.encode()).hexdigest()
        self.stashes = collections.deque(maxlen=10)  # keep last 10 stashes

    
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
    
    def toggle_code_stash_event(self, event=None):  
        print('stashed')

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

        head, tail, chars, lines = self.get_region()
        if self.stashes and self.stashes[-1] == lines:
            print('No changes to stash')
            return
        self.stashes.append(lines)
        print('self.stashes:', self.stashes)
        print('Stashed code')



if __name__ == "__main__":
    from unittest import main
    main('idlelib.idle_test.test_codecontext', verbosity=2, exit=False)