## This program shows how to load a VTK Image data with extension *.vti and then
## how to access the cell data, extract one cell from the list of cells,
## access data values at each cell corner and then store the cell into a 
## vtkpolydata file format.
#################################################################################

## Import VTK
from vtk import *

## Load data
#######################################
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

## Query how many cells the dataset has
#######################################
numCells = data.GetNumberOfCells()

## Get a single cell from the list of cells
###########################################
cell = data.GetCell(0) ## cell index = 0

## Query the 4 corner points of the cell
#########################################
pid1 = cell.GetPointId(0)
pid2 = cell.GetPointId(1)
pid3 = cell.GetPointId(3)
pid4 = cell.GetPointId(2)

## Print the 1D indices of the corner points
############################################
# print('1D indices of the cell corner points:')
# print(pid1,pid2,pid3,pid4) ## in counter-clockwise order
# Print the point indices and coordinates
print('1D indices and coordinates of the cell corner points in counter-clockwise order:')
print(f'Point {0}: {pid1}')
print(f'Point {1}: {pid2}')
print(f'Point {3}: {pid3}')
print(f'Point {2}: {pid4}')
#like this
#   Point 3 (2)--------Point 2 (3)
#          |             |
#          |             |
#   Point 0 (0)--------Point 1 (1)


## Get values at each vertex
## First Get the array
dataArr = data.GetPointData().GetArray('Pressure')
val1 = dataArr.GetTuple1(pid1)
val2 = dataArr.GetTuple1(pid2)
val3 = dataArr.GetTuple1(pid3)
val4 = dataArr.GetTuple1(pid4)
#print(val1,val2,val3,val4)

## Print the locations (3D coordinates) of the points
#######################################################
print('Point locations of cell corners in counter clockwise order and their data values:')
print(data.GetPoint(pid1),val1)
print(data.GetPoint(pid2),val2)
print(data.GetPoint(pid3),val3)
print(data.GetPoint(pid4),val4)


## Extract and store one cell
#############################
points = vtkPoints()
points.InsertNextPoint(data.GetPoint(pid1))
points.InsertNextPoint(data.GetPoint(pid2))
points.InsertNextPoint(data.GetPoint(pid3))
points.InsertNextPoint(data.GetPoint(pid4))

## The Data Array for holding data values
#########################################
dataArray = vtkFloatArray()
dataArray.SetName('Pressure')
dataArray.InsertNextTuple1(val1)
dataArray.InsertNextTuple1(val2)
dataArray.InsertNextTuple1(val3)
dataArray.InsertNextTuple1(val4)

## Create the cell, which is a polyline
#########################################
polyLine = vtkPolyLine()
polyLine.GetPointIds().SetNumberOfIds(5)    
polyLine.GetPointIds().SetId(0, 0)
polyLine.GetPointIds().SetId(1, 1)
polyLine.GetPointIds().SetId(2, 2)
polyLine.GetPointIds().SetId(3, 3)
polyLine.GetPointIds().SetId(4, 0)

### Create a polydata
######################
pdata = vtkPolyData()

### Create a cell array to store the polyline
#############################################
cells = vtkCellArray()
cells.InsertNextCell(polyLine)

### Add points and cells to polydata
####################################
pdata.SetPoints(points)
pdata.SetLines(cells)
pdata.GetPointData().AddArray(dataArray)


### Store the polydata into a vtkpolydata file with extension .vtp
####################################################################
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('onecell.vtp')
writer.Write()