#this program is for my understanding only. 

## This program loads contour vtp file and also all points connected .vtp file in single renderer. 
#To view file which displays only contour .vtp , please use LoadContourPolydata.py file


## Import VTK
###############
from vtk import *

#These below lines are only for contour vtp file
### Load Data. 
########################
reader = vtkXMLPolyDataReader()
reader.SetFileName('contours_with_pressure.vtp') ## polyline.vtp
reader.Update()
### get polydata object out from reader
#######################################
pdata = reader.GetOutput()
print(pdata)
### Setup mapper and actor
##########################
mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(2) ## set line width
actor.GetProperty().SetColor(1,0,0) ## set line color red



#Load all points data. These below lines are only for all points .vtp grid file
reader1 = vtkXMLPolyDataReader()
reader1.SetFileName('allPoints_with_pressure.vtp') ## polyline.vtp
reader1.Update()
pdata1 = reader1.GetOutput()
print(pdata1)
mapper1 = vtkPolyDataMapper()
mapper1.SetInputData(pdata1)
actor1 = vtkActor()
actor1.SetMapper(mapper1)
actor1.GetProperty().SetLineWidth(1) ## set line width
actor1.GetProperty().SetColor(1,1,0) ## set line color yellow


### Setup render window, renderer, and interactor
##################################################
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

#using only one renderer to show both actors in one image
renderer.AddActor(actor)        #rendering contour lines .vtp file actor
renderer.AddActor(actor1)       #rendering all points grid lines .vtp file actor


### Finally render the object
#############################
renderWindow.Render()
renderWindowInteractor.Start()