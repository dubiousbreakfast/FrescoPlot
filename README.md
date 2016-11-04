#PyFresco
Python scripts intended for use with Fresco Coupled Channel Reaction Code.

1. **Basic Functions**

   All of the FRESCO file manipulation is handled in the classes and functions defined in the FrescoClasses source file.
   The namespace should be imported as fc.


| Command | Description |
| --- | --- |
| `fc.read_cross` | Given a fresco cross section file(fort.201,202,etc) return an instance of the lineobject class |
| `fc.read_data` | Reads data from a *.dat* file with format angle,cross section,error in x, error in y  |
| `fp.CrossSectionPlot` | This uses sets up a plot with either a tuple/string of file names or a list of lineobjects. Plot with `plot()` with an option to limit angle range.|



