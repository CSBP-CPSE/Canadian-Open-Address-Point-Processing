Some files needed to be pre-processed before they could be fed to the collection pipeline, and those are stored here. Over time these may be replaced if the corrections can be incorporated straight into the processing pipeline.

In the case of Alberta, the data from the Alberta Municipal Data Sharing Partnership is a collection of hundreds of distinct files, and so these are combined before they are passed to the pipeline.
In the case of Montreal, the addresses are given in ranges, and so a script is used to separate ranges into individual lines (with identical coordinates to the ones given for the range).
in the other cases, either encoding or file formatting issues made it necessary to essentially read in the file and output it again into a format easier to read by the collection pipeline.
