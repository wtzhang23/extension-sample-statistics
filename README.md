# extension-sample-statistics
`ess.py` is a script to get statistics for numbers written in files with a certain extension. The script reads a lone floating point or integer value stored a file for every file and computes the mean, standard deviation, first quartile, second quartile and median values. It also supports graphing distributions for visual analysis.

# Using the script.
## Prerequisites 
* Python 3
* Matplotlib and Numpy

## Running the script
It may be helpful in Unix systems to make the script executable. Run `chmod +x ess.py` to do so.

For all optional and positional arguments and their functions, run `ess.py --help`.
  
To view the sample statistics of files with a certain extension, run `ess.py E` where `E` is the file extension to analyze. All files with that extension are then used to determine the sample statistics.

To plot a distribution graph, run `ess.py -p P E` where `P` is the type of graph you would like to plot and `E` is the file extension to analyze. This will write the plot to `x.png` by default. Check out the other flags for more customization.

## Common Errors
* **I'm getting a "no display name and no $DISPLAY environment variable" error:** Matplotlib relies on a backend to draw its graphs. Your backend relies on having a display. If you are using this command through `ssh` try X11 forwarding or using a backend that does not need a display such as Agg. You can set the backend used by matplotlib by passing its name into the `-b` argument.  
* **I'm getting a "no such file or directory" error:** At this point, this script does not support creating directories that do not exist.