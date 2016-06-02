class CircList(list):

    """CircList has a head attribute that defines the virtual start of the list

    If the item pointed to by the head index is ever deleted, the head will
    move right (i.e. not change unless last in list, then rolls over to 0)
    """

    def __init__(self, *args, **kwargs):
        super(CircList, self).__init__(*args, **kwargs)
        self._head = 0

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        """Checks if an int and saves mod length of the list"""
        if not isinstance(value, int):
            raise ValueError(
                'head only accepts type int (not "{}")'.format(type(value))
            )
        self._head = value % len(self)

    def _map_index(self, index):
        """Maps index relative to the head

        i.e. If head == 3, a given index of 0 will map to 3
        This allows us to use normal slicing and indexing relative to a
        virtual head of the circular list
        """
        return (index + self.head) % len(self)

    def _map_slice(self, _slice):
        """Maps slice objects relative to the head

        Returns a list of either one or two slice object, as if the stop rolls
        over to before the start, we need two separate slice instances.

        Returns:
            List[slice]: list of mapped slices
        """
        mapped_start = (_slice.start + self.head) % len(self)
        if _slice.stop > len(self):
            mapped_stop = (_slice.start - 1) % len(self)
        else:
            mapped_stop = (_slice.stop + self.head) % len(self)

        # Map into two separate slices if stop rolls over to before start
        if mapped_stop < mapped_start:
            back_slice = slice(mapped_start, len(self), _slice.step)
            step_leftover = _slice.step - ((len(self) - mapped_start) % _slice.step)
            front_slice = slice(step_leftover, mapped_stop, _slice.step)
            return [back_slice, front_slice]

        # Otherwise just return a single mapped slice
        return [slice(mapped_start, mapped_stop, _slice.step)]

    def _raw_cycle(self):
        """Returns an iterator that cycles repeatedly ignoring virtual head"""
        index = -1
        while True:
            index = (index + 1) % len(self)
            yield super(CircList, self).__getitem__(index)

    def __add__(self, obj):
        if isinstance(obj, list):
            for item in obj:
                self.append(item)
        raise TypeError(
            'can only concatenate list (not "{}") to CircList'.format(type(obj))
        )

    def __delitem__(self, index):
        if isinstance(index, slice):
            mapped = self._map_slice(index)
        elif isinstance(index, int):
            mapped = self._map_index(index)
        else:
            raise ValueError(
                '__delitem__ only accepts an int or slice object argument (not "{})'.format(type(index))
            )
        super(CircList, self).__delitem__(mapped)
        self.head = self.head  # Resets the head mod length of list

    def __delslice__(self, start, end):
        self.__delitem__(slice(start, end))

    def __eq__(self, obj):
        """Check circular equality regardless of underlying structure order"""
        try:
            doubled = obj * 2
            for i in xrange(len(obj)):
                if super(CircList, self).__eq__(doubled[i:i+len(obj)]):
                    return True
        except TypeError:
            pass
        return False

    def __getitem__(self, index):
        if isinstance(index, slice):
            mapped = self._map_slice(index)
        elif isinstance(index, int):
            mapped = self._map_index(index)
        else:
            raise ValueError(
                '__getitem__ only accepts an int or slice object argument (not "{})'.format(type(index))
            )
        super(CircList, self).__getitem__(mapped)

    def __getslice__(self, start, end):
        self.__getitem__(slice(start, end))

    def __iter__(self):
        """Returns an iterator over the entire list with custom start point"""
        for index in xrange(self.head, self.head + len(self)):
            yield super(CircList, self).__getitem__(index)
        return

    def __repr__(self):
        return '{cls}<virtual=[{virtual}], raw={raw}, head={head}>'.format(
            cls=self.__class__.__name__,
            virtual=', '.join(map(str, self.__iter__())),
            raw=super(CircList, self).__repr__(),
            head=self.head,
        )

    def __str__(self):
        return '[{}]'.format(', '.join(map(str, self.__iter__())))

    def append(self, obj):
        # I think it might be optimal to just append normally if head == 0
        # Should really look into complexity of append vs insert
        if self.head == 0:
            super(CircList, self).append(obj)
        else:
            self.insert(self._head, obj)
            self.head += 1
