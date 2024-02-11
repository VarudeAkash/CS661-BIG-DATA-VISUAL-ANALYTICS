
#even though this successful try is more generalized answer and does extra work of storing grid lines of all points in seperate vtp file, it is for my understanding of 
#how vtk works only. For assignment submission, submit Que1_i=finalAnswer.py only

import vtk
userPressure=float(input("Enter Contour to be extracted: "))
# Load data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()
numCells=data.GetNumberOfCells()

# Create vtkPolyData to store cells. I am storing 2 vtp files. one vtp file contains only contour information
#another vtp file will contain all points connected via lines. i.e. grid
contourPolydata = vtk.vtkPolyData()
originalPolydata = vtk.vtkPolyData()

# Create vtkCellArray to store cells
contourCells = vtk.vtkCellArray()
originalCells = vtk.vtkCellArray()

# Create vtkFloatArray to store pressure data for points
contourPressureData = vtk.vtkFloatArray()
contourPressureData.SetName('Pressure')
contourPressureData.SetNumberOfComponents(1)

originalPressureData = vtk.vtkFloatArray()
originalPressureData.SetName('Pressure')
originalPressureData.SetNumberOfComponents(1)

#create vtkPoints to store points
contourPoints = vtk.vtkPoints()
originalDataPoints=vtk.vtkPoints()


# Iterate through all cells
for i in range(numCells):
    cell = data.GetCell(i)
    
    # Extracting the four corner points of the cell
    pid1, pid2, pid3, pid4 = cell.GetPointId(0), cell.GetPointId(1), cell.GetPointId(3), cell.GetPointId(2)

    # Get the array containing scalar data of pressure values
    dataArr = data.GetPointData().GetArray('Pressure')

    # Get scalar values for the four points i.e. pressure values for corner points
    val1, val2, val3, val4 = dataArr.GetTuple1(pid1), dataArr.GetTuple1(pid2), dataArr.GetTuple1(pid3), dataArr.GetTuple1(pid4)
    
    #insert original data points. I am storing grid lines which connects all points in other vtp file. Hence we are writing below code
    #These below 8 lines have nothing to do with contour vtp file.
    originalDataPoints.InsertNextPoint(data.GetPoint(pid1))
    originalDataPoints.InsertNextPoint(data.GetPoint(pid2))
    originalDataPoints.InsertNextPoint(data.GetPoint(pid3))
    originalDataPoints.InsertNextPoint(data.GetPoint(pid4))
    originalPressureData.InsertNextTuple1(val1)
    originalPressureData.InsertNextTuple1(val2)
    originalPressureData.InsertNextTuple1(val3)
    originalPressureData.InsertNextTuple1(val4)
    
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
        continue #Hence we are not adding any information in contourPolydata


    #inserting our newly obtained points in contourPoints
    contourPoints.InsertNextPoint(firstPoint)
    contourPoints.InsertNextPoint(secondPoint)
    # Adding pressure values to contourPressureData. Pressure value is same for both these obtained points. Which is equal to inputed by user
    contourPressureData.InsertNextTuple1(userPressure)  
    contourPressureData.InsertNextTuple1(userPressure)


polyLine = vtk.vtkPolyLine()    #creating Polyline
for i in range(0,contourPoints.GetNumberOfPoints(),2):  #we have stored contourPoints one by one. We just want to draw line between two obtained points. Hence step size of 2
    polyLine.GetPointIds().SetNumberOfIds(2)    #line is between two points
    polyLine.GetPointIds().SetId(0, i)          
    polyLine.GetPointIds().SetId(1, i+1)
    contourCells.InsertNextCell(polyLine)     
  
#Setting the points and cells for the contourPolydata
contourPolydata.SetPoints(contourPoints)
contourPolydata.SetLines(contourCells)
#Adding contourPressureData to point data of contourPolydata
contourPolydata.GetPointData().AddArray(contourPressureData)
#Write the contourPolydata to a .vtp file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('contours_with_pressure.vtp')
writer.SetInputData(contourPolydata)
writer.Write()


#below code is only for all points connected grip .vtp file
polyLineOriginal = vtk.vtkPolyLine()    #creating Polyline for our original all data. Hence named as pulylineOriginal
for i in range(0,originalDataPoints.GetNumberOfPoints(),4):     #we need only 4 points at a time. hence step size of four
    polyLineOriginal.GetPointIds().SetNumberOfIds(5)            # line between 0-1, 1-2, 2-3, 3-0 hence one square will be completed.
                                                                #How? remember 0th point has pid 0, 1st point inserted has pid 1,
                                                                #2nd point inserted has pid 251, 3rd point inserted has pid 250
    
                                                                #now when i increased by step size of 4 then
                                                                #it will be 4-5, 5-6, 6-7, 7-4. Hence next square will be completed
    polyLineOriginal.GetPointIds().SetId(0, i)
    polyLineOriginal.GetPointIds().SetId(1, i+1)
    polyLineOriginal.GetPointIds().SetId(2, i+2)
    polyLineOriginal.GetPointIds().SetId(3, i+3)
    polyLineOriginal.GetPointIds().SetId(4, i)
    originalCells.InsertNextCell(polyLineOriginal)



originalPolydata.SetPoints(originalDataPoints)
originalPolydata.SetLines(originalCells)
originalPolydata.GetPointData().AddArray(originalPressureData)

# Write the originalPolyData to a .vtp file
writer1 = vtk.vtkXMLPolyDataWriter()
writer1.SetFileName('allPoints_with_pressure.vtp')
writer1.SetInputData(originalPolydata)
writer1.Write()
