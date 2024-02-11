import vtk

# Load data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

# Create vtkPolyData to store all cells
combinedPolyData = vtk.vtkPolyData()

# Create vtkCellArray to store all cells
combinedCells = vtk.vtkCellArray()

# Create vtkFloatArray to store pressure data for all points
combinedPressureData = vtk.vtkFloatArray()
combinedPressureData.SetName('Pressure')
combinedPressureData.SetNumberOfComponents(1)

combinedPoints = vtk.vtkPoints()

# Iterate through all cells
for i in range(data.GetNumberOfCells()):
    cell = data.GetCell(i)
    
    # Extract the four corner points of the cell
    pid1, pid2, pid3, pid4 = cell.GetPointId(0), cell.GetPointId(1), cell.GetPointId(3), cell.GetPointId(2)

    # Get the array containing scalar data
    dataArr = data.GetPointData().GetArray('Pressure')

    # Get scalar values for the four points
    val1, val2, val3, val4 = dataArr.GetTuple1(pid1), dataArr.GetTuple1(pid2), dataArr.GetTuple1(pid3), dataArr.GetTuple1(pid4)

    # Print information for the first few cells (optional). Just to find out coordinates and pids
    # if i < 5:
    #     print(f'Cell {i+1}:')
    #     print(f'  Point {pid1} - Coordinates: {data.GetPoint(pid1)}, Pressure: {val1}')
    #     print(f'  Point {pid2} - Coordinates: {data.GetPoint(pid2)}, Pressure: {val2}')
    #     print(f'  Point {pid3} - Coordinates: {data.GetPoint(pid3)}, Pressure: {val3}')
    #     print(f'  Point {pid4} - Coordinates: {data.GetPoint(pid4)}, Pressure: {val4}')
    #     print()



    # Add pressure values to combinedPressureData
    combinedPressureData.InsertNextTuple1(val1)
    combinedPressureData.InsertNextTuple1(val2)
    combinedPressureData.InsertNextTuple1(val3)
    combinedPressureData.InsertNextTuple1(val4)
    # Add points to combinedPoints
    combinedPoints.InsertNextPoint(data.GetPoint(pid1))
    combinedPoints.InsertNextPoint(data.GetPoint(pid2))
    combinedPoints.InsertNextPoint(data.GetPoint(pid3))
    combinedPoints.InsertNextPoint(data.GetPoint(pid4))

for i in range(0,combinedPoints.GetNumberOfPoints(),4):
    # Create a new vtkPolyLine for the current cell
    polyLine = vtk.vtkPolyLine()
    polyLine.GetPointIds().SetNumberOfIds(5)
    polyLine.GetPointIds().SetId(0, i)
    polyLine.GetPointIds().SetId(1, i+1)
    polyLine.GetPointIds().SetId(2, i+2)
    polyLine.GetPointIds().SetId(3, i+3)
    polyLine.GetPointIds().SetId(4, i)
    # Add the vtkPolyLine to the combinedCells
    combinedCells.InsertNextCell(polyLine)


# Set the points and cells for the combinedPolyData
combinedPolyData.SetPoints(combinedPoints)
combinedPolyData.SetLines(combinedCells)

# Add combinedPressureData to point data of combinedPolyData
combinedPolyData.GetPointData().AddArray(combinedPressureData)

# # Write the combinedPolyData to a .vtp file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('allPoints_with_pressure.vtp')
writer.SetInputData(combinedPolyData)
writer.Write()

print("Connected All Points in grid successfully")
