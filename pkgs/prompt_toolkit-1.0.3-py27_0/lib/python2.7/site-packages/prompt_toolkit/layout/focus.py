from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass

__all__ = (
    'Focus',
)

class Focus(with_metaclass(ABCMeta, object)):
    """
    The interface
    """
    _counter = 0

    def get_focussed_buffer(self, cli):  # XXX: rename to get_buffer.
        """
        Return the `Buffer` object that is currently focussed. This can be None
        if there is no buffer inside this widget.
        """
        return None

#    def get_label(self):
#        Focus._conuter += 1
#        return 'focus-%i' % Focus._counter

        # Return SEARCH_BUFFER

    def get_buffer_control(self, cli):
        """
        When a `BufferControl` is focussed, this is supposed to return that
        instance. For all other focusses, this should return None`.
        """
        return None

#    def is_modal(self, cli):
#        " When True, the focus shouldn't be stolen. "
#        return False

    def get_key_bindings(self, cli):
        """
        Return the key bindings for this buffer. When this control has the
        focus, these key bindings are included.
        """

    def get_global_key_bindings(self, cli):
        """
        Key bindings that are supposed to be always active.
        """

#    def get_search_focus(self, cli):
#        """
#        When the user wants to search through the currently focussed widget,
#        this should return either `None` (when searching is impossible) or
#        the `Focus` object that handles the search.
#
#        Probably, this is the `Focus` object that belongs to a `BufferControl`
#        that displays the search.
#        """
#
#    def is_searchable(self, cli):
#        return False

#    def start_searching(self, cli):
#        pass

#    def get_system_focus(self, cli):
#        ""

class DynamicFocus(Focus):
    """
    Object that dynamically redirects the focus to an object.

    :param get_focus_obj: Callable that takes a `CommandLineInterface` and
        returns a `Focus` object.
    """
    def __init__(self, get_focus_obj):
        self.get_focus_obj = get_focus_obj

    def get_focussed_buffer(self, cli):
        return self.get_focus_obj(cli).get_focussed_buffer(cli)

    def get_buffer_control(self, cli):
        return self.get_focus_obj(cli).get_buffer_control(cli)

    def get_key_bindings(self, cli):
        return self.get_focus_obj(cli).get_key_bindings(cli)
