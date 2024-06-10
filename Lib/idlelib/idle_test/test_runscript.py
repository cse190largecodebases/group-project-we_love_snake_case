"Test runscript, coverage 16%."

from idlelib import runscript
import unittest
from test.support import requires
from tkinter import Tk
from idlelib.editor import EditorWindow


class ScriptBindingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.update_idletasks()
        for id in cls.root.tk.call('after', 'info'):
            cls.root.after_cancel(id)  # Need for EditorWindow.
        cls.root.destroy()
        del cls.root

    def test_init(self):
        ew = EditorWindow(root=self.root)
        sb = runscript.ScriptBinding(ew)
        ew._close()

    # Mock test with user saying Yes to running without saving, so confirm is 0
    def test_getfilename_run_with_saving(self):
        ew = EditorWindow(root=self.root)
        sb = runscript.ScriptBinding(ew)
        ew.io.get_saved = unittest.mock.MagicMock(return_value=True)
        sb.ask_save_dialog = unittest.mock.MagicMock(return_value=False)
        sb.user_confirm = unittest.mock.MagicMock(return_value='custom_file')
        self.assertEqual('custom_file', sb.user_confirm())
        ew._close()

    def test_getfilename_run_without_saving(self):
        ew = EditorWindow(root=self.root)
        sb = runscript.ScriptBinding(ew)
        ew.io.get_saved = unittest.mock.MagicMock(return_value=False)
        sb.ask_save_dialog = unittest.mock.MagicMock(return_value=True)
        filename = sb.user_cancel()
        self.assertEqual(filename, 'write_to_temp_file')
        ew._close()

    def test_write_to_temp_file(self):
        ew = EditorWindow(root=self.root)
        sb = runscript.ScriptBinding(ew)
        ew.text.insert('1.0', 'print("Hello World")')
        filename = sb.write_to_temp_file()
        with open(filename, 'r') as f:
            self.assertEqual(f.read(), 'print("Hello World")\n')
        ew._close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
