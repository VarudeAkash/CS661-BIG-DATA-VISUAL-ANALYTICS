## How to visualize a 2D uniform grid colored with the array attribute.
#############################################################################

## Import VTK
from vtk import *
#################################


## Load data
#######################################
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

## create a surface representation from 2D uniform grid data
surface = vtkGeometryFilter()
surface.SetInputData(data)
surface.Update()

## Output of geometry filter is a vtkpolydata
pdata = surface.GetOutput()
range = pdata.GetPointData().GetArray('Pressure').GetRange()


# create the scalar_bar
##########################
lut = vtkLookupTable()
lut.Build()
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Pressure")
scalar_bar.SetNumberOfLabels(6)
scalar_bar.SetMaximumWidthInPixels(150)
scalar_bar.SetMaximumHeightInPixels(600)


### Setup mapper and actor
##########################
mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)
mapper.SetScalarRange(range)
mapper.SetLookupTable(lut)
actor = vtkActor()
actor.SetMapper(mapper)

### Axes actor
###############
axes = vtkAxesActor()
axes.SetTotalLength(50, 50, 50)
axes.AxisLabelsOff()


### Setup render window, renderer, and interactor
##################################################
renderer = vtkRenderer()
renderer.SetBackground(0.5,0.5,0.5)
render_window = vtkRenderWindow()
render_window.SetSize(1400,1000)
render_window.AddRenderer(renderer)
render_windowInteractor = vtkRenderWindowInteractor()
render_windowInteractor.SetRenderWindow(render_window)
render_windowInteractor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
renderer.AddActor(actor)
renderer.AddActor(axes)

## show the scalar bar
scalar_bar_widget = vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(render_windowInteractor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()


### Finally render the object
#############################
render_window.Render()
render_windowInteractor.Start()