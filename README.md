# BkAssist
Bookkeeping assistant software designed to boost productivity at my work

In this branch, a new tkinter gui script (filter.py), has been added.  In this script, you'll see that one of the core BkAssist features has been implemented: the ability to open an Excel file, load its data into a treeview, use filter-as-you-type searching to find the data you want, then double clicking the result to get an at-a-glance view of the record information in a main sidebar to the right of the main treeview.

What's cool about the search feature is that search queries can be written such that you can find not just the specific piece of data you're looking for, but also data which may be related to what you're looking for.  For example, if you launch filter.py and load in the "Example Data Set.xlsx" file, you could search for "IT corporate 0 miami" and the filtered results will be all people in IT who work in corporate who are located in Miami and have a 0 percent bonus percentage.  A very rudimentary implementation, sure, but since i'll eventually be using simple data sets pulled from our work's invoicing software anyway, this is more than good enough.

the interface itself still has a few bugs I'm working out:
- column sorting doesn't quite work right on certain columns with decimal values, likely due to how the excel file data is formatted, with the fact the excel file data is loaded into the treeview columns as strings, or a combination of these.
- additionally, sorting the treeview after performing a search can result in the treeview wiping the filtered results and the program loading the original data set being loaded back into the treeview.  i have a good idea of how to fix this, it's just a matter of figuring out how to work the solution in with the existing code.  shouldn't be too bad. 
  
to create an entire feature like this AND have a working version of it is a huge personal milestone for me.  it's the first time i've ever made this kind of progress in any programming project i've ever attempted.  yes, it's crude and rudimentary, but i'm learning so much.  :)

to anyone watching out there, keep rooting for me.  we're getting there piece by piece!
  


