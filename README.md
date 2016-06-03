#Circular List
Defines a CircList class that subclasses a default Python list but treats it as a circular data structure. This means we need a starting point for indexing and iteration, so I added a head attribute to the CircList class that is the virtual starting point for all indexing and slicing. This head can be altered to "virtually rotate" the circular list without actually rebuilding the underlying list itself.

##Usage
Attempts to emulate a default list as closely as possible with the exception of having a head attribute that defines the virtual beginning of the list as opposed to all indexing and slicing starting from the beginning of the actual underlying list element.

Any slicing of the list without a beginning or end point wrap around the circular list until hitting the head again.

For example:  If the underlying list is [0, 1, 2, 3, 4, 5] and head == 3, a slice of <CircList>[1:] will return [4, 5, 0, 1, 2]. Notice that the head element (true index == 3 and virtual index == 0) is not included, as the wrap around only returns to the head, not the start of the slice.

Also not that equality of two CircList objects checkout for circular permutation equivalence ignoring where the current heads are. For example, two CircList with underlying list structures of [0, 1, 2, 3] and [3, 0, 1, 2] will always be equal, regardless of if they head of each list is equal. Checking if the heads are also equal should be trivial, if it is required you should be able to implement it quickly. I may add it as an extra method in a further release if that feature is commonly requested.

##Usage Example
```Python
import circular_list

circ_list = circular_list.CircList([0, 1])

circ_list.append(2)
```
