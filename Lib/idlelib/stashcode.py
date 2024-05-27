"""stash - local version control for IDLE"""
import collections 


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
        self.editwin = editwin
        self.text = editwin.text

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
    
    @staticmethod
    def toggle_code_stash_event(self, event=None):  
        print('stashed')

    @staticmethod
    def previous_stash(self):
        print('previous stash')
    
    @staticmethod
    def next_stash(self):
        print('next stash')

    @staticmethod
    def apply_stash(self):
        print('apply stash')

    @staticmethod
    def stash_code(self):
        print('stash code')



if __name__ == "__main__":
    from unittest import main
    main('idlelib.idle_test.test_codecontext', verbosity=2, exit=False)