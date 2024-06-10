import os
from idlelib import stashcode
import unittest
from test.support import requires
from tkinter import Text, Tk
from idlelib.editor import EditorWindow
from unittest import mock

"""
Write tests for stashcode.py
Need to test each function in stashcode
So test stash, stash apply, next stash, previous stash, and restore original
"""

class DummyEditwin:
    def __init__(self, root, text):
        self.root = root
        self.text = text
        self.indentwidth = 8
        self.tabwidth = 8
        self.prompt_last_line = '>>>'
        self.io = mock.Mock()
        self.io.filename = 'dummy.py'
    get_selection_indices = EditorWindow.get_selection_indices
    _close = EditorWindow._close
    update_recent_files_list = EditorWindow.update_recent_files_list
        
class StashCodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = Tk()
        cls.root.withdraw()
        cls.text = Text(cls.root)
        cls.editor = DummyEditwin(cls.root, cls.text)

    @classmethod
    def tearDownClass(cls):
        cls.root.update_idletasks()
        cls.root.destroy()
        del cls.root

    def setUp(self):
        self.text.delete('1.0', 'end')
        self.stashcode = stashcode.Stash(self.editor)

    def test_init(self):
        self.assertEqual(self.stashcode.editwin, self.editor)

    def test_stash_code(self):
        ew = self.editor
        stash = stashcode.Stash(ew)
        stash.stash_code()
        self.assertTrue(stash.stashes)

    def test_apply_stash(self):
        ew = self.editor
        stash = stashcode.Stash(ew)
        stash.stash_code()
        stash.apply_stash()
        self.assertEqual(stash.stashes[stash.index], "['', '']")

    def test_next_stash(self):
        ew = self.editor
        stash = stashcode.Stash(ew)
        stash.index = 0
        stash.stash_code()
        stash.next_stash()
        self.assertEqual(stash.index, 1)

    def test_previous_stash(self):
        ew = self.editor
        stash = stashcode.Stash(ew)
        stash.index = 1
        stash.stash_code()
        stash.previous_stash()
        self.assertEqual(stash.index, 0)

    def test_restore_original(self):
        ew = self.editor
        stash = stashcode.Stash(ew)
        stash.stash_code()
        stash.restore_original()
        self.assertEqual(stash.stashes[stash.index], "['', '']")

    def test_create_hidden_file(self):
        stashcode.create_hidden_file('test_folder', 'test_file')
        self.assertTrue(os.path.exists('.test_folder/test_file'))
        os.remove('.test_folder/test_file')
        os.rmdir('.test_folder')

    def test_read_file_contents(self):
        with open('test_file.txt', 'w') as f:
            f.write('test content')
        content = stashcode.read_file_contents('test_file.txt')
        self.assertEqual(content, 'test content')
        os.remove('test_file.txt')

    def test_write_to_file(self):
        stashcode.write_to_file('test_file.txt', 'test content')
        with open('test_file.txt', 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test content')
        os.remove('test_file.txt')

    def test_read_stash_from_file(self):
        stashcode.write_to_file('test_file.txt', 'test stash')
        stash = stashcode.read_stash_from_file('test_file.txt')
        self.assertEqual(stash, ['test stash'])
        os.remove('test_file.txt')

    def test_write_stash_to_file(self):
        stashcode.write_stash_to_file('test_file.txt', 'test stash')
        with open('test_file.txt', 'r') as f:
            stash = f.read()
        self.assertEqual(stash, 't😀e😀s😀t😀 😀s😀t😀a😀s😀h')
        os.remove('test_file.txt')
    

if __name__ == '__main__':
    unittest.main(verbosity=2)