
from queue import Queue
from pytrip.tripexecuter import ExecutorLogger


class HtmlExecutorLogger(ExecutorLogger):
    def __init__(self):
        self.queue = Queue()

    def info(self, text):
        self.queue.put("<b>{}</b>".format(text))

    def log(self, text):
        text = self._format_tags(text)
        text = self._format_ansi(text)
        text = self._format_colors(text)
        self.queue.put(text)

    def error(self, text):
        self.queue.put("<font color=\"Red\"><b>{}</b></font>".format(text))

    def empty(self):
        return self.queue.empty()

    def get(self):
        return self.queue.get(block=False)

    def _format_tags(self, text):
        text = text.replace("<E>", "&lt;E&gt;")  # error
        text = text.replace("<I>", "&lt;I&gt;")  # info
        text = text.replace("<D>", "&lt;D&gt;")  # debug
        return text

    def _format_colors(self, text):
        if "&lt;E&gt;" in text:
            text = "<font color=\"Red\">{}</font>".format(text)
        return text

    def _format_ansi(self, text):
        """Remove ansi excape sequences
        """
        import re
        return re.sub(r"\033\[[0-9]+m", "", text)
