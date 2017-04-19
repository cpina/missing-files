Small utility to find missing files from one directory in another based only on the file name. It also shows files that the size is different.

This was quickly developed during the ACE 2016-2017 (Antarctic Circumnavigation Expedition) because some scientists move generated files in different directoris. For example, they move from generated files "EK80/*.raw" to "EK80/$DATE".

As it is now it might be useful for when copying files from cameras to the hard disk: it's easy to verify that all the files in the camera memory are available on the hard disk before deleting the camera's memory.

It needs unit tests, some small refactoring (not big, it's a small utility) and better documentation but, since it proved to be useful as it now we thought of sharing it.

Carles Pina (carles@pina.cat), 2017
