## This program shows how to create a polyline object from a set of points and store in a file.
###############################################################################################

## Import VTK
from vtk import *

### Create a cell array to store the lines
##########################################
cells = vtkCellArray()

### Data
#########################
p0 = [0,0,0]
p1 = [1,0,0]
p2 = [1,1,0]
p3 = [0,1,0]

p4 = [1,0,0]
p5 = [2,0,0]
p6 = [2,1,0]
p7 = [1,1,0]

### Create points
################################
points = vtkPoints()
points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)



### Create polyline
################################
polyLine = vtkPolyLine()
polyLine.GetPointIds().SetNumberOfIds(5)

## Adding line segments counter clockwise
polyLine.GetPointIds().SetId(0, 0)
polyLine.GetPointIds().SetId(1, 1)
polyLine.GetPointIds().SetId(2, 2)
polyLine.GetPointIds().SetId(3, 3)
polyLine.GetPointIds().SetId(4, 0)
cells.InsertNextCell(polyLine)

points.InsertNextPoint(p4)
points.InsertNextPoint(p5)
points.InsertNextPoint(p6)
points.InsertNextPoint(p7)

polyLine = vtkPolyLine()
polyLine.GetPointIds().SetNumberOfIds(5)
polyLine.GetPointIds().SetId(0, 4)
polyLine.GetPointIds().SetId(1, 5)
polyLine.GetPointIds().SetId(2, 6)
polyLine.GetPointIds().SetId(3, 7)
polyLine.GetPointIds().SetId(4, 4)
cells.InsertNextCell(polyLine)




### Create polydata
####################
pdata = vtkPolyData()

### Add points and cells to polydata
####################################
pdata.SetPoints(points)
pdata.SetLines(cells)

### Store the polydata into a vtkpolydata file with extension .vtp
###################################################################
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('polyline.vtp')
writer.Write()