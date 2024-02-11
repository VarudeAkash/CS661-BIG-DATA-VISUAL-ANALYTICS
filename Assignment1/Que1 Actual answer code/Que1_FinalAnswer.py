import vtk
userPressure=float(input("Enter Contour to be extracted. Value range -1438 to +630 :  "))

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()
numCells=data.GetNumberOfCells() #to get number of cells


#Creating vtkPolyData to store all cells. I am storing vtp file that contains only contour information
contourPolyData = vtk.vtkPolyData() 

#Creating vtkCellArray to store cells which are involved in contour
contourCells = vtk.vtkCellArray()

#Creating vtkFloatArray to store pressure data for points which are involved in contour
contourPressureData = vtk.vtkFloatArray()
contourPressureData.SetName('Pressure')
contourPressureData.SetNumberOfComponents(1)

#creating vtkPoints to store points
contourPoints = vtk.vtkPoints()

#Iterating through all cells present int data given in .vti file
for i in range(numCells):
    cell = data.GetCell(i)  #extracting one cell at a time
    
    # Extracting the four corner points of the cell
    pid1, pid2, pid3, pid4 = cell.GetPointId(0), cell.GetPointId(1), cell.GetPointId(3), cell.GetPointId(2)

    #Array containing scalar data of pressure values
    dataArr = data.GetPointData().GetArray('Pressure')

    #Scalar values for the four points i.e. pressure values for corner points
    val1, val2, val3, val4 = dataArr.GetTuple1(pid1), dataArr.GetTuple1(pid2), dataArr.GetTuple1(pid3), dataArr.GetTuple1(pid4)

    #Calculating cordinates of our required points using the formula in sir's PPT
    firstPoint=[-1,-1,25]       #initializing points cordinates (third coordinate is 25 in original .vti file for all points)
    secondPoint=[-1,-1,25]
    if(val1 >= userPressure and val2 <= userPressure):
        firstPoint[0]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
        firstPoint[1]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
        if(val3>= userPressure):
            secondPoint[0]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[0]-data.GetPoint(pid2)[0]) + data.GetPoint(pid2)[0]
            secondPoint[1]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[1]-data.GetPoint(pid2)[1]) + data.GetPoint(pid2)[1]
        elif(val4>= userPressure):
            secondPoint[0]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[0]-data.GetPoint(pid3)[0]) + data.GetPoint(pid3)[0]
            secondPoint[1]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[1]-data.GetPoint(pid3)[1]) + data.GetPoint(pid3)[1]
        else:
            secondPoint[0]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[0]-data.GetPoint(pid4)[0]) + data.GetPoint(pid4)[0]
            secondPoint[1]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[1]-data.GetPoint(pid4)[1]) + data.GetPoint(pid4)[1]
    elif(val2 >= userPressure and val3 <= userPressure):
        firstPoint[0]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[0]-data.GetPoint(pid2)[0]) + data.GetPoint(pid2)[0]
        firstPoint[1]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[1]-data.GetPoint(pid2)[1]) + data.GetPoint(pid2)[1]
        if(val4>= userPressure):
            secondPoint[0]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[0]-data.GetPoint(pid3)[0]) + data.GetPoint(pid3)[0]
            secondPoint[1]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[1]-data.GetPoint(pid3)[1]) + data.GetPoint(pid3)[1]
        elif(val1>=userPressure):
            secondPoint[0]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[0]-data.GetPoint(pid4)[0]) + data.GetPoint(pid4)[0]
            secondPoint[1]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[1]-data.GetPoint(pid4)[1]) + data.GetPoint(pid4)[1]
        else:
            secondPoint[0]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
            secondPoint[1]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
    elif(val3 >= userPressure and val4 <= userPressure):
        firstPoint[0]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[0]-data.GetPoint(pid3)[0]) + data.GetPoint(pid3)[0]
        firstPoint[1]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[1]-data.GetPoint(pid3)[1]) + data.GetPoint(pid3)[1]
        if(val1>=userPressure):
            secondPoint[0]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[0]-data.GetPoint(pid4)[0]) + data.GetPoint(pid4)[0]
            secondPoint[1]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[1]-data.GetPoint(pid4)[1]) + data.GetPoint(pid4)[1]
        elif(val2>=userPressure):
            secondPoint[0]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
            secondPoint[1]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
        else:
            secondPoint[0]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[0]-data.GetPoint(pid2)[0]) + data.GetPoint(pid2)[0]
            secondPoint[1]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[1]-data.GetPoint(pid2)[1]) + data.GetPoint(pid2)[1]
    elif(val4>=userPressure and val1<=userPressure):
        firstPoint[0]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[0]-data.GetPoint(pid4)[0]) + data.GetPoint(pid4)[0]
        firstPoint[1]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[1]-data.GetPoint(pid4)[1]) + data.GetPoint(pid4)[1]
        if(val2>=userPressure):
            secondPoint[0]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
            secondPoint[1]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
        elif(val3>=userPressure):
            secondPoint[0]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[0]-data.GetPoint(pid2)[0]) + data.GetPoint(pid2)[0]
            secondPoint[1]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[1]-data.GetPoint(pid2)[1]) + data.GetPoint(pid2)[1]
        else:
            secondPoint[0]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[0]-data.GetPoint(pid3)[0]) + data.GetPoint(pid3)[0]
            secondPoint[1]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[1]-data.GetPoint(pid3)[1]) + data.GetPoint(pid3)[1]
    else:   #i.e. if cell is not active. 
        continue    #Hence we are not adding any information in contourPolydata

    #inserting our newly obtained points in contourPoints
    contourPoints.InsertNextPoint(firstPoint)
    contourPoints.InsertNextPoint(secondPoint)

    # Adding pressure values to contourPressureData. Pressure value is same for both these obtained points. Which is equal to inputed by user
    contourPressureData.InsertNextTuple1(userPressure)
    contourPressureData.InsertNextTuple1(userPressure)

polyLine = vtk.vtkPolyLine()        #creating Polyline
for i in range(0,contourPoints.GetNumberOfPoints(),2):  #we have stored only contourPoints one by one. We just want to draw line between two obtained points. Hence step size of 2
    polyLine.GetPointIds().SetNumberOfIds(2)        #line is between two points
    polyLine.GetPointIds().SetId(0, i)
    polyLine.GetPointIds().SetId(1, i+1)
    contourCells.InsertNextCell(polyLine)

#Setting points and cells for the contourPolyData
contourPolyData.SetPoints(contourPoints)
contourPolyData.SetLines(contourCells)
#Adding contourPressureData to point data of contourPolyData
contourPolyData.GetPointData().AddArray(contourPressureData)

# Write the combinedPolyData to a .vtp file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('contours_with_pressure.vtp')
writer.SetInputData(contourPolyData)
writer.Write()
