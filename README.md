# Programming Principles and Concepts

Below are several examples of programming principles applied by the Python code of the requisition system.

**KISS (keep it simple, stupid)**

All of the class's methods, as well as the code outside the class that runs the system, are written in a simple way that makes it easy to read the code, understand it's doing, communicate between different parts of it and continue working on it in the future.

For example, the _\_\_init\_\__ method only has one line that's doing the simplest thing possible: creating an empty list of requsitions. This list is used as the single 'source of truth' for anything we need to do throughout the code - whether it's counters, finding items, or adding or modifying data. By applying the KISS principle here, we not only make the code extremely easy to read and understand, but also make it efficient and easier to work with.

Similarly, the _generate_approval_ref_ method has only one line that returns a simple concatenated string; the _find_requisition_by_id_ method only does a basic and simple looping through the list of requisitions, returning the matching item if it finds one; the _start_ method receives a simple input from the user and uses simple if/elif/else check to perform the appropriate actions; and the code outside the class simply creates an instance and calls the _start_ method to run the system, without doing anything else.

**DRY (don't repeat yourself)**

The code is written in a way that aims to minimize repetition, so pieces of code that can or should be used in multiple places are put into reusable methods.

For example, there multiple places in the code that need to generate and assign an approval reference ID to a requisition, based on the exact same formula. Therefore, the _generate_approval_ref_ acts as a reusable method that generates and returns the reference, avoiding the need to duplicate this functionality and formula into several different places.

The method _find_requisition_by_id_ is also included as a potentially reusable method - even though it's currently only being called in one place in the code, it makes the code simpler and easier to read, and if the code gets expanded into a real system, this method would likely be needed in a lot more places.

There can still be slight improvements to the code in terms of applying the DRY principle. For example, there's a part of four lines which is repeated in two different methods, and is responsible for checking if an approval reference ID is available and displaying it. This part could be moved into a reusable method to prevent this repetition.

**Single Responsibility**

The code generally aims to ensure that each of the class's methods would only be doing one thing, so we'd only have to change a method if that specific functionality needs to be updated.

For example, the _generate_approval_ref_ method is solely responsible for generating an approval ref ID, so the only reason we might have to change this method is if the forumla for generating the ID changes.

Similarly, the _display_requisitons_ and _requisition_statistic_ methods are each responsible for a single functionality: displaying output to the user (the list of requisitions and their statistics, respectively), rather than modifying data. This means that either of these methods would only have to change if we need to change the output that we print - for example if we want to display extra details for each requisitions, if we want to display additional stats metrics, or if we want to change the style and format in which the list or statistics are displayed.