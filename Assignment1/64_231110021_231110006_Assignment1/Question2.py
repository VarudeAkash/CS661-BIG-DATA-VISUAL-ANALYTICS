import vtk
import sys



def color_transfer_function():            #color transfer function and setting the values given in question
    color_tf = vtk.vtkColorTransferFunction()
    color_tf.AddRGBPoint(-4931.54, 0, 1, 1)
    color_tf.AddRGBPoint(-2508.95, 0, 0, 1)
    color_tf.AddRGBPoint(-1873.9, 0, 0, 0.5)
    color_tf.AddRGBPoint(-1027.16, 1, 0, 0)
    color_tf.AddRGBPoint(-298.031, 1, 0.4, 0)
    color_tf.AddRGBPoint(2594.97, 1, 1, 0)
    return color_tf

def opacity_transfer_function():            #opecity transfer function
    opacity_tf = vtk.vtkPiecewiseFunction()
    opacity_tf.AddPoint(-4931.54, 1.0)
    opacity_tf.AddPoint(101.815, 0.002)
    opacity_tf.AddPoint(2594.97, 0.0)
    return opacity_tf


def configure_volume_property(color_tf, opacity_tf, use_phong_shading):
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_tf)
    volume_property.SetScalarOpacity(opacity_tf)

    if(use_phong_shading=='1'):
        volume_property.ShadeOn()
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    elif(use_phong_shading=='0'):
        volume_property.ShadeOff()
    else:
        sys.exit("\nwrong input")
    print("\nVolume property configuration completed")
    return volume_property

def create_volume_actor(volume_mapper, volume_property):
    volume_actor = vtk.vtkVolume()
    volume_actor.SetMapper(volume_mapper)
    volume_actor.SetProperty(volume_property)
    print("Volume actor created")
    return volume_actor

def create_outline_actor(data_reader):
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(data_reader.GetOutput())
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    print("Outline actor created")
    return outline_actor


path = "Data/Isabel_3D.vti"

#Loading data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(path)
reader.Update()


#Deciding whether we want to use Phong shading or not
phong_shading = input("\nEnter 1 for Phong shading and 0 for not using Phong shading: ")

#color transfer function and setting the values given in question
color_tf = vtk.vtkColorTransferFunction()
color_tf.AddRGBPoint(-4931.54, 0, 1, 1)
color_tf.AddRGBPoint(-2508.95, 0, 0, 1)
color_tf.AddRGBPoint(-1873.9, 0, 0, 0.5)
color_tf.AddRGBPoint(-1027.16, 1, 0, 0)
color_tf.AddRGBPoint(-298.031, 1, 0.4, 0)
color_tf.AddRGBPoint(2594.97, 1, 1, 0)

#opecity transfer function
opacity_tf = vtk.vtkPiecewiseFunction()
opacity_tf.AddPoint(-4931.54, 1.0)
opacity_tf.AddPoint(101.815, 0.002)
opacity_tf.AddPoint(2594.97, 0.0)

volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputData(reader.GetOutput())

#Creating volume property
volume_property = configure_volume_property(color_tf, opacity_tf, phong_shading)
volume_actor = create_volume_actor(volume_mapper, volume_property)

outline_actor = create_outline_actor(reader)

#Setting render window, renderer, and interactor
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume_actor)
renderer.AddActor(outline_actor)
render_window = vtk.vtkRenderWindow()
render_window.SetSize(1000, 1000)
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()
print("\nRendered image is opened in another window")
render_window_interactor.Start()

