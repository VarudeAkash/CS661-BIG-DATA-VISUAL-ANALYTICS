## This program shows how to load a vtk polydata file from disk and show it using VTK.
#######################################################################################


## Import VTK
###############
from vtk import *


### Load Data
########################
reader = vtkXMLPolyDataReader()
reader.SetFileName('polyline.vtp') ## polyline.vtp
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
actor.GetProperty().SetLineWidth(1) ## set line width
actor.GetProperty().SetColor(1,0,0) ## set line color red


### Setup render window, renderer, and interactor
##################################################
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)


### Finally render the object
#############################
renderWindow.Render()
renderWindowInteractor.Start()