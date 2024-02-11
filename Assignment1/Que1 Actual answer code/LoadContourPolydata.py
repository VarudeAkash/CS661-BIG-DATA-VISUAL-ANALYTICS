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

### Setup render window, renderer, and interactor
##################################################
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)        #rendering contour lines .vtp file actor
### Finally render the object
#############################
renderWindow.Render()
renderWindowInteractor.Start()