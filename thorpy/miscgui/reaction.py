class Reaction(object):
    """Reacts to a pygame event <reacts_to> by running <reac_func>. Designed
    to belong to a specific element, normally through element.reactions.
    """

    def __init__(self, reacts_to, reac_func, event_args=None, params=None,
                 reac_name=None):
        """
        <reacts_to> : pygame event
        <reac_func> : function ro run
        <args_dict> : args to filter the pygame event
        <params> : constant params for the function to run (not depending on
            the event.
        <name> : the name of the reaction (optionnal). Reaction names that are
            int comprised in range(13) are reserved. Use REAC_USER + n for your
            nth reaction, or use any other structure than int.
        """
        if not event_args:
            event_args = {}
        if not params:
            params = {}
        self.reacts_to = reacts_to
        self.event_args = event_args
        self.reac_func = reac_func
        self.params = params
        self.reac_name = reac_name

    def _is_right_event(self, event):
        """Returns True if <event> match the requirements for self."""
        if event.type == self.reacts_to:
            for k in self.event_args.keys():
                if event.dict.get(k) != self.event_args[k]:  # if has not arg
                    return False
            return True
        else:
            return False

    def _try_activation(self, event):
        """Tests if has to react to <event>
        NB : the reac_func function shall always take event as argument"""
        if self._is_right_event(event):
            self.reac_func(event, **self.params)

class ConstantReaction(Reaction):
    """Reaction whose behaviour is not influed by event. See Reaction for more.
    """

    def _try_activation(self, event):
        """Tests if has to react to <event>"""
        if self._is_right_event(event):
            self.reac_func(**self.params)
