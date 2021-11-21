
from queue import Queue
from pytrip.tripexecuter import ExecutorLogger


class HtmlExecutorLogger(ExecutorLogger):
    def __init__(self):
        self._queue = Queue()

        self._info_tag = "<b>{}</b>"  # bold
        self._red_font = "<font color=\"Red\">{}</font>"
        self._error_tag = self._red_font.format("<b>{}</b>")  # red and bold

    def info(self, text):
        self._queue.put(self._info_tag.format(text))

    def log(self, text):
        text = self._format_tags(text)
        text = self._format_ansi(text)
        text = self._format_colors(text)
        self._queue.put(text)

    def error(self, text):
        self._queue.put(self._error_tag.format(text))

    def empty(self):
        return self._queue.empty()

    def get(self):
        return self._queue.get(block=False)

    def _format_tags(self, text):
        """ Changes '<' and '>' in tags to html entities
        """
        text = text.replace("<E>", "&lt;E&gt;")  # error
        text = text.replace("<SYS>", "&lt;SYS&gt;")  # system
        text = text.replace("<I>", "&lt;I&gt;")  # info
        text = text.replace("<D>", "&lt;D&gt;")  # debug
        return text

    def _format_colors(self, text):
        """ Changes lines with <E> or <SYS> to red color
        """
        if "&lt;E&gt;" in text or "&lt;SYS&gt;" in text:
            text = self._red_font.format(text)
        return text

    def _format_ansi(self, text):
        """ Remove ansi escape sequences
        """
        import re
        return re.sub(r"\033\[[0-9]+m", "", text)
