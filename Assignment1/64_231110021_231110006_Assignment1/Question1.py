import vtk
from vtk import *
userPressure=float(input("\nEnter Contour to be extracted. Value range -1438 to +630 :  "))

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
    point=[-1,-1,-1]       #initializing points cordinates (third coordinate is 25 in original .vti file for all points)

    if((val1 >= userPressure and val2 <= userPressure) or(val1 <= userPressure and val2 >= userPressure)):
        point[0]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[0]-data.GetPoint(pid1)[0]) + data.GetPoint(pid1)[0]
        point[1]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[1]-data.GetPoint(pid1)[1]) + data.GetPoint(pid1)[1]
        point[2]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[2]-data.GetPoint(pid1)[2]) + data.GetPoint(pid1)[2]
        contourPoints.InsertNextPoint(point)    #inserting our newly obtained point in contourPoints
        contourPressureData.InsertNextTuple1(userPressure)  #Adding pressure value to contourPressureData Which is equal to inputed by user
        
    if((val2 >= userPressure and val3 <= userPressure) or (val2 <= userPressure and val3 >= userPressure)):
        point[0]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[0]-data.GetPoint(pid2)[0]) + data.GetPoint(pid2)[0]
        point[1]=(val2-userPressure)/(val2-val3)*(data.GetPoint(pid3)[1]-data.GetPoint(pid2)[1]) + data.GetPoint(pid2)[1]
        point[2]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[2]-data.GetPoint(pid1)[2]) + data.GetPoint(pid1)[2]
        contourPoints.InsertNextPoint(point)    #inserting our newly obtained point in contourPoints
        contourPressureData.InsertNextTuple1(userPressure)  #Adding pressure value to contourPressureData Which is equal to inputed by user

    if((val3 >= userPressure and val4 <= userPressure) or(val3 <= userPressure and val4 >= userPressure)):
        point[0]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[0]-data.GetPoint(pid3)[0]) + data.GetPoint(pid3)[0]
        point[1]=(val3-userPressure)/(val3-val4)*(data.GetPoint(pid4)[1]-data.GetPoint(pid3)[1]) + data.GetPoint(pid3)[1]
        point[2]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[2]-data.GetPoint(pid1)[2]) + data.GetPoint(pid1)[2]
        contourPoints.InsertNextPoint(point)    #inserting our newly obtained point in contourPoints
        contourPressureData.InsertNextTuple1(userPressure)  #Adding pressure value to contourPressureData Which is equal to inputed by user

    if((val4>=userPressure and val1<=userPressure) or (val4<=userPressure and val1>=userPressure)):
        point[0]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[0]-data.GetPoint(pid4)[0]) + data.GetPoint(pid4)[0]
        point[1]=(val4-userPressure)/(val4-val1)*(data.GetPoint(pid1)[1]-data.GetPoint(pid4)[1]) + data.GetPoint(pid4)[1]
        point[2]=(val1-userPressure)/(val1-val2)*(data.GetPoint(pid2)[2]-data.GetPoint(pid1)[2]) + data.GetPoint(pid1)[2]
        contourPoints.InsertNextPoint(point)    #inserting our newly obtained point in contourPoints
        contourPressureData.InsertNextTuple1(userPressure)  #Adding pressure value to contourPressureData Which is equal to inputed by user

    else:   #i.e. if cell is not active. 
        continue    #Hence we are not adding any information in contourPolydata

polyLine = vtk.vtkPolyLine()        #creating Polyline
for i in range(0,contourPoints.GetNumberOfPoints(),2):  #we have stored only contourPoints one by one. We just want to draw line between two obtained points. Hence step size of 2
    polyLine.GetPointIds().SetNumberOfIds(2)        
    polyLine.GetPointIds().SetId(0, i)              #line is between two points
    polyLine.GetPointIds().SetId(1, i+1)
    contourCells.InsertNextCell(polyLine)

#Setting points and cells for the contourPolyData
contourPolyData.SetPoints(contourPoints)
contourPolyData.SetLines(contourCells)
#Adding contourPressureData to point data of contourPolyData
contourPolyData.GetPointData().AddArray(contourPressureData)

# Write the combinedPolyData to a .vtp file
writer = vtk.vtkXMLPolyDataWriter()
filename="contours_with_pressure.vtp"
writer.SetFileName(filename)
writer.SetInputData(contourPolyData)
writer.Write()
print("\nContour is extraced successfully and it is stored in",filename," file")


#Below code is to view extracted contour  which we have stored in .vtp file using above code

#Loading .vtp file which we have saved in above code
reader = vtkXMLPolyDataReader()
reader.SetFileName(filename) ## polyline.vtp
reader.Update()
print("\n",filename," file is loaded successfully") 

#extracting polydata object from reader
pdata = reader.GetOutput()
#print(pdata)                   #if want to view data summary then just uncomment this line


#Setting mapper and actor
print("Setting Mapper and Actor")
mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(2) #Line width
actor.GetProperty().SetColor(1,0,0)    #Setting color to red



print("Setting render window, renderer, and interactor")
#Setting render window, renderer, and interactor
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)

renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)        #rendering contour lines .vtp file actor

print("\nRendering...")
#Now just rendering the object
renderWindow.Render()
print("\nContour is opened in New window")
print("\n You can also view extracted contour by importing",filename," in paraview")
renderWindowInteractor.Start()
