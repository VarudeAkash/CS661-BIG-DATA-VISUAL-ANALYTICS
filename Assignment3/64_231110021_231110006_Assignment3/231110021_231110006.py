from vtk import *
import vtk

# Function to get the vector at a point in the dataset
def get_vector_at_point(point, dataset):
    #vtkProbeFilter object to query the dataset
    pf = vtk.vtkProbeFilter()
    pf.SetSourceData(dataset)    
    #vtkPoints object and insert the point
    pn = vtk.vtkPoints()
    pn.InsertNextPoint(point)    
    #vtkPolyData object and set its points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(pn)    
    # Set the input of the probe filter
    pf.SetInputData(polydata)
    pf.Update()
    
    # Get the queried vector
    q_vector = pf.GetOutput().GetPointData().GetVectors().GetTuple(0)
    return q_vector

# Function to perform Runge-Kutta 4 (RK4) integration
def rk4_integration(current_position, step_size, data):
    # Get the vector at the current position
    a = get_vector_at_point(current_position, data)
    
    # Calculate k1
    k1 = [x * step_size for x in a]

    # Calculate k2
    b_position = [(current_position[i] + k1[i] / 2) for i in range(3)]
    b = get_vector_at_point(b_position, data)
    k2 = [x * step_size for x in b]

    # Calculate k3
    c_position = [(current_position[i] + k2[i] / 2) for i in range(3)]
    c = get_vector_at_point(c_position, data)
    k3 = [x * step_size for x in c]

    # Calculate k4
    d_position = [(current_position[i] + k3[i]) for i in range(3)]
    d = get_vector_at_point(d_position, data)
    k4 = [x * step_size for x in d]

    # Update the position using the weighted sum of the intermediate steps
    new_position = [current_position[i] + (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(3)]
    return new_position

# Function to create a render window and visualize the streamline
def render_window_fun(streamline_file):
    rd = vtk.vtkXMLPolyDataReader()
    rd.SetFileName(streamline_file)
    rd.Update()
    mp = vtk.vtkPolyDataMapper()
    mp.SetInputConnection(rd.GetOutputPort())
    ac = vtk.vtkActor()
    ac.SetMapper(mp)
    renderer = vtk.vtkRenderer()
    renderer.AddActor(ac)
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window.Render()
    render_window_interactor.Start()

# Function to trace the streamline in both directions from a seed location
def trace_streamline(seed_location, step_size, max_steps, data):
    list1 = []
    list2 = []

    stm_cells = vtk.vtkCellArray()
    stm_points = vtk.vtkPoints()

    # doing Forward tracing
    temp = seed_location
    for _ in range(max_steps):
        new_point = rk4_integration(temp, step_size, data)
        if not check(new_point, data.GetBounds()):
            break
        # stm_points.InsertNextPoint(new_point)
        list1.append(new_point)
        temp = new_point

    # doing Backward tracing
    temp = seed_location
    for _ in range(max_steps):
        new_point = rk4_integration(temp, -step_size, data)
        if not check(new_point, data.GetBounds()):
            break
        list2.append(new_point)
        temp = new_point

    # Insert seed point
    # stm_points.InsertNextPoint(seed_location)
    list1.reverse()
    for point in list1:
        stm_points.InsertNextPoint(point)
    stm_points.InsertNextPoint(seed_location)

    for point in list2:
        stm_points.InsertNextPoint(point)
    # Create polyline cells
    for i in range(1, stm_points.GetNumberOfPoints()):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, i - 1)
        line.GetPointIds().SetId(1, i)
        stm_cells.InsertNextCell(line)

    stream = vtk.vtkPolyData()
    stream.SetPoints(stm_points)
    stream.SetLines(stm_cells)

    # streamline.SetLines(stm_cells)
    return stream

# Function to check if a point is within the dataset bounds
def check(point, bounds):
    array = []
    for i in range(len(point)):
        if not bounds[2*i] <= point[i] <= bounds[2*i+1]:
            array.append(1)
            return False
    return True

if __name__ == "__main__":
    # Load vector field data set
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName('tornado3d_vector.vti')
    reader.Update()
    data = reader.GetOutput()

    # Get seed location from user input
    seed_location = (
        float(input("Enter seed x: ")),
        float(input("Enter seed y: ")),
        float(input("Enter seed z: "))
    )

    # Set integration parameters
    step_size = 0.05
    max_steps = 1000

    # Trace streamline
    streamline = trace_streamline(seed_location, step_size, max_steps, data)

    # Write streamline to file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("streamline.vtp")
    writer.SetInputData(streamline)
    writer.Write()

    # Visualize the streamline
    render_window_fun("streamline.vtp")
