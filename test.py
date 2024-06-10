
class AutoCompleteWindow:

    def __init__(self, widget, tags):
        # The widget (Text) on which we place the AutoCompleteWindow
        self.widget = widget
        # Tags to mark inserted text with
        self.tags = tags
        # The widgets we create
        self.autocompletewindow = self.listbox = self.scrollbar = None
        # The default foreground and background of a selection. Saved because
        # they are changed to the regular colors of list items when the
        # completion start is not a prefix of the selected completion
        self.origselforeground = self.origselbackground = None
        # The list of completions
        self.completions = None
        # A list with more completions, or None
        self.morecompletions = None
        # The completion mode, either autocomplete.ATTRS or .FILES.
        self.mode = None
        # The current completion start, on the text box (a string)
        self.start = None
        # The index of the start of the completion
        self.startindex = None
        # The last typed start, used so that when the selection changes,
        # the new start will be as close as possible to the last typed one.
        self.lasttypedstart = None
        # Do we have an indication that the user wants the completion window
        # (for example, he clicked the list)
        self.userwantswindow = None
        # event ids
        self.hideid = self.keypressid = self.listupdateid = \
            self.winconfigid = self.keyreleaseid = self.doubleclickid = None
        # Flag set if last keypress was a tab
        self.lastkey_was_tab = False
        # Flag set to avoid recursive <Configure> callback invocations.
        self.is_configuring = False

    

