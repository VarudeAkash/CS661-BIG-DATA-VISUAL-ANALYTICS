#!/usr/bin/env python
# coding: utf-8

# In[9]:


#importing modules
from vtk import *


# In[10]:


#Loading the dataset
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()


# In[11]:


#taking input for isolvalue 
c=float(input("Enter Value of C(isovalue): "))


# In[12]:


#method to calculate lamda and return points
def givePoints(val1,val2,x1,y1,z1,x2,y2,z2):
    x = ((val1 - c)/(val1 - val2)) * (x2-x1)+x1
    y = ((val1 - c)/(val1 - val2)) * (y2-y1)+y1
    z = ((val1 - c)/(val1 - val2)) * (z2-z1)+z1
    return [x,y,z]
        


# In[13]:


#finding no. of cells
n_cells=data.GetNumberOfCells()
#extracting pressure values
data_arr=data.GetPointData().GetArray('Pressure')
points=vtkPoints()
#print(type(data_arr))
for i in range(n_cells):
    #getting the cell
    cell=data.GetCell(i)
    
    #getting the cell id in anti-clock wise direction  
    id1=cell.GetPointId(0)
    id2=cell.GetPointId(1)
    id3=cell.GetPointId(3)
    id4=cell.GetPointId(2)
    
    #getting the values
    val1=data_arr.GetTuple1(id1)
    val2=data_arr.GetTuple1(id2)
    val3=data_arr.GetTuple1(id3)
    val4=data_arr.GetTuple1(id4)
    
    #getting the points
    x1,y1,z1=data.GetPoint(id1)
    x2,y2,z2=data.GetPoint(id2)
    x3,y3,z3=data.GetPoint(id3)
    x4,y4,z4=data.GetPoint(id4)
    
    #checking for all 4 edges whether can find a point or not     
    if((val1<=c and val2>=c)or(val1>=c and val2<=c)):
        points.InsertNextPoint(givePoints(val1,val2,x1,y1,z1,x2,y2,z2))
   
    if((val2<=c and val3>=c) or (val2>=c and val3<=c)):
        points.InsertNextPoint(givePoints(val2,val3,x2,y2,z2,x3,y3,z3))
       
    if((val3<=c and val4>=c) or (val3>=c and val4<=c)):
        points.InsertNextPoint(givePoints(val3,val4,x3,y3,z3,x4,y4,z4))
        
    if((val4<=c and val1>=c) or (val4>=c and val1<=c)):
        points.InsertNextPoint(givePoints(val4,val1,x4,y4,z4,x1,y1,z1))    


# In[14]:


poly_line = vtkPolyLine()
num_of_points = points.GetNumberOfPoints()
cells=vtkCellArray()

#ploting the lines 
for i in range(0,num_of_points,2):
    poly_line.GetPointIds().SetNumberOfIds(2)
    poly_line.GetPointIds().SetId(0,i)
    poly_line.GetPointIds().SetId(1,i+1)
    cells.InsertNextCell(poly_line)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetLines(cells)


# In[15]:


#making the vtp file
def make_vtp(poly_data):
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName("isocontour.vtp")
    writer.SetInputData(poly_data)
    writer.Write()
    
make_vtp(poly_data)


# In[16]:


import vtk
# Loading the polydata isocontour.vtp
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName("isocontour.vtp")
reader.Update()

# Creating the mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(reader.GetOutput())

# Creating the  actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
colors=vtkNamedColors()
actor.GetProperty().SetColor(colors.GetColor3d('Red'))

# Creating a renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# Creating the render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
renderer.SetBackground(colors.GetColor3d('Grey'))

# Creating an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Starting the interactor
interactor.Initialize()

interactor.Start()


# In[ ]:





# In[ ]:




