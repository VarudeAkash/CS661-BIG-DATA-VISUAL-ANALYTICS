#!/usr/bin/env python

## Import VTK
from vtk import *

### Data
########################
p0 = [1.0, 1.0, 1.0]
p1 = [-1.0, 1.0, 1.0]
p2 = [-1.0, -1.0, 1.0]
p3 = [1.0, -1.0, 1.0]
p4 = [0.0, 0.0, 0.0] ## Apex vertex of the Pyramid

### Create geometric primitives
################################
points = vtkPoints()
points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)
points.InsertNextPoint(p4)

### Create Pyramid geometry
################################
pyramid = vtkPyramid()
pyramid.GetPointIds().SetId(0, 0)
pyramid.GetPointIds().SetId(1, 1)
pyramid.GetPointIds().SetId(2, 2)
pyramid.GetPointIds().SetId(3, 3)
pyramid.GetPointIds().SetId(4, 4)

cells = vtkCellArray()
cells.InsertNextCell(pyramid)

### Create a grid and attach the geometry to it
################################################
ug = vtkUnstructuredGrid()
ug.SetPoints(points)
ug.InsertNextCell(pyramid.GetCellType(), pyramid.GetPointIds())


### Create a mapper and give the grid to it
#############################################
mapper = vtkDataSetMapper()
mapper.SetInputData(ug)

### Create an actor and give the mapper to it
#############################################
actor = vtkActor()
actor.SetMapper(mapper)
## specify color for Pyramid
actor.GetProperty().SetColor(0.5,0.5,0) 

### Create a renderer and give the actor to it
#############################################
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)

### Create a renderwindow and attach it with the renderer and interactor
########################################################################
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Create a nice view
######################
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)
renderer.GetActiveCamera().Elevation(-20)
renderer.ResetCameraClippingRange()

### Finally render the Pyradim object
#############################################
renderWindow.Render()
renderWindowInteractor.Start()

