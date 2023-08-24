from tkinter import *
from tkinter import messagebox
from class_graph import Graph
import funcions as f

root = Tk()
root.title("Seach ur Hospital")
root.geometry('900x600')
root.configure(bg='#ABCDE5')


def sol_page():
    
    sol_frame = Frame(main_frame, bg='#ABCDE5')
    
    yourName_label=Label(sol_frame, text='Hola '+Name+'!', bg='#FFFFFF', fg='#000000', font=('Arial',20))
    sol_label=Label(sol_frame, text="Ingrese nombre del hospital", bg='#ABCDE5', fg='#23587D', font=('Arial',20))
    
    hospital_label=Label(sol_frame, text="Ingresa Hospital", bg='#ABCDE5', fg='#23587D', font=('Arial', 15))
    hospital_entry=Entry(sol_frame)
    
    ciudad_label=Label(sol_frame, text="Ingresa Ciudad", bg='#ABCDE5', fg='#23587D', font=('Arial', 15))
    ciudad_entry=Entry(sol_frame)
    
    estado_label=Label(sol_frame, text="Ingresa Estado", bg='#ABCDE5', fg='#23587D', font=('Arial', 15))
    estado_entry=Entry(sol_frame)
    
    buscaPorHospital_boton=Button(sol_frame, text="Busca por Hospital", bg='#86DB5E', font=('Arial', 15), command=lambda: [set_searchedParam(hospital_entry.get()), searchHospitalName()])
    buscaPorEstado_boton=Button(sol_frame, text="Busca por Estado", bg='#86DB5E', font=('Arial', 15), command=lambda: [set_searchedParam(estado_entry.get()), searchByState()])
    buscaPorCiudad_boton=Button(sol_frame, text="Busca por Ciudad", bg='#86DB5E', font=('Arial', 15), command=lambda: [set_searchedParam(ciudad_entry.get()), searchByCity()])
    
    sol_label.grid(row=1, column=1, pady=20)
    hospital_label.grid(row=2, column=1, pady=10)
    hospital_entry.grid(row=2, column=2, pady=10)
    ciudad_entry.grid(row=3, column=2, pady=10)
    ciudad_label.grid(row=3, column=1, pady=20)
    estado_label.grid(row=4, column=1, pady=20)
    estado_entry.grid(row=4, column=2, pady=20)
    buscaPorHospital_boton.grid(row=2, column=3, columnspan=1, pady=20)
    buscaPorEstado_boton.grid(row=4, column=3, columnspan=1, pady=20)
    buscaPorCiudad_boton.grid(row=3, column=3, pady=20)
    yourName_label.grid(row=0, column=0)
    
    sol_frame.pack()

def hospital_info():
    info_frame = Frame(main_frame, bg='#ABCDE5')
    
    masCercano_label=Label(info_frame, text="Los hospitales más cercanos a "+param+" son:", bg='#ABCDE5', fg='#23587D', font=('Arial', 12))
    for i in range(len(data)):
        respuesta_label=Label(info_frame, text=data[i], bg='#ABCDE5', fg='#000000', font=('Arial', 12))
        respuesta_label.grid(row=i+1, column=0)
        if i > 10: break
    volver_butotn=Button(info_frame, text="Vuelve", bg='#86DB5E', font=('Arial', 15), command=lambda: [change_page(sol_page)])
    verGrafos_button=Button(info_frame, text="Ver grafo", bg='#86DB5E', font=('Arial', 15), command=lambda: [verGrafoS(grafo)])
    verGrafoCalidad_button=Button(info_frame, text="Ver grafo calidad", bg='#86DB5E', font=('Arial', 15), command=lambda: [verGrafoCalidad(data)])
    
    masCercano_label.grid(row=0, column=0)
    volver_butotn.grid(row=14, column=0)
    verGrafos_button.grid(row=15, column=0)
    verGrafoCalidad_button.grid(row=16, column=0)
    info_frame.pack()

def home_page():

    w_frame = Frame(main_frame, bg='#ABCDE5')
    
    #Creando elementos
    welcome_label=Label(w_frame, text="Welcome to Search ur Hospital!", bg='#ABCDE5', fg='#23587D', font=('Arial', 30))
    name_label=Label(w_frame, text="What's you name?", bg='#ABCDE5', fg='#23587D', font=('Arial', 15))
    name_entry=Entry(w_frame, font=('Arial', 15))
    
    go_button=Button(w_frame, text="Go!", bg='#86DB5E', font=('Arial', 15), command=lambda: [set_name(name_entry.get()), change_page(sol_page)])
    
    #Ordenándolos en pantalla
    welcome_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
    name_label.grid(row=1, column=0, pady=20)
    name_entry.grid(row=1, column=1)
    go_button.grid(row=2, column=0, columnspan=2, pady=30)
    
    w_frame.pack()

def change_page(page):
    delete_pages()
    page()
    
def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def set_name(nam):
    global Name
    Name = nam

def set_searchedParam(h):
    global param
    param = h

  


hospitals = []
hospitals_names = []

# Leyendo hospitales y guardandolos en structs, Guardando el nombre de los hospitales
hospitals, hospitals_names = f.read_hospitals_csv()
# Generando aristas
list_of_edges = f.generate_edges(hospitals)

# Creando y rellenando las aristas del grafo hospitales
hospitals_graph = Graph()
hospitals_graph.add_nodes(hospitals_names)
hospitals_graph.add_edges(list_of_edges)

# Creando el arbol de expasion minima con kruskal
kruskal_graph = f.kruskal_mst(hospitals_graph)

# Consulta a hospitales mas cercanos al hospital ingresado:
def searchHospitalName():
    result, nxGraph = f.bfs_with_limitations(kruskal_graph,param,max_depth=5)
    global data
    global grafo 
    
    grafo = nxGraph
    data = result
    print(result)
    change_page(hospital_info)
    #f.visualize_graph(nxGraph) #Ejecutar esta linea demora 2 segundos

def searchByState():
    path, dfs_graph = f.dfs_by(kruskal_graph, type_='STATE' , name=param , hospitals=hospitals)
    global data
    global grafo 
    
    grafo = dfs_graph
    data = path
    print(path)
    change_page(hospital_info)
    #f.visualize_graph(dfs_graph) #Ejecutar esta linea demora 2 segundos
    
def searchByCity():
    path, dfs_graph = f.dfs_by(kruskal_graph, type_='CITY' , name=param , hospitals=hospitals)
    global data
    global grafo 
    
    grafo = dfs_graph
    data = path
    print(path)
    change_page(hospital_info)
    #f.visualize_graph(dfs_graph) #Ejecutar esta linea demora 2 segundos

def verGrafoS(gra):
    f.visualize_graph(gra)

def verGrafoCalidad(miData):
    sccs = f.generate_quality(kruskal_graph)
    f.visualize_qualityGraph(sccs, kruskal_graph, miData)
    
main_frame=Frame(root, highlightbackground='White', highlightthickness=2)
change_page(home_page)
main_frame.pack()
root.mainloop()
