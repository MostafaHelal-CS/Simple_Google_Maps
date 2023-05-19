from tkinter import * 
from tkinter import ttk
from queue import Queue
import folium
from functools import partial
import openrouteservice as ors
import os
import webbrowser
from tkintermapview import TkinterMapView
import haversine as hs

Coordinates={
    #Elmenofia 
    "ShebinElkom":[30.554928799816988, 31.012393143088957],
    "Minouf":[30.45841991481536, 30.933867041463532],
    "Tala":[30.683127111837056, 30.950034191578247],
    "BerketAlseb3":[30.627495984801378, 31.07244250380298],
    "Elbagoor":[30.43186671298956, 31.031983255977398],
    "Ashmoon":[30.300117313578117, 30.97564036423758],
    "Quesna":[30.56765698894867, 31.149568418149613],
    "Elsadat":[30.362811748009076, 30.533153025293895],
    "Alshohda":[30.59768043193886, 30.895758793318098],
    #Elgharbia
    "KafrElZayat":[30.828935887979828, 30.81468363315086],
    "Basioun":[30.941234859668185, 30.819787152459256],
    "Tanta":[30.78236661466976, 31.003931835360497],
    "Qutur":[30.97124133198592, 30.952896608684792],
    "ElMahallaElKubra":[30.969841036674914, 31.166019730570685],
    "AsSantah":[30.749281457375343, 31.129532111290036],
    "Samannoud":[30.96202482138702, 31.241725792395766],
    "Zefta":[30.714483753839744, 31.240197668420624],
    #Elkalubia
    "Banha":[30.46954041758182, 31.18372798445176],
    "Qalyub":[30.180143566835696, 31.20638419614639],
    "AlQanatirAlKhayriyyah":[30.194609758641715, 31.13391214967144],
    "ShubraAlKhaymah":[30.124142365522676, 31.260465002556664],
    "Elkhankah":[30.22039965655326, 31.368612270866304],
    "Kafrshokr":[30.552839823187284, 31.255430468410704],
    "ShibinElQanatir":[30.31214792794175, 31.32292278281032],
    "Toukh":[30.353756127836252, 31.2014138527108],
}

def BFS(start, goal):
    adj_list={
    'ShebinElkom':['Tala','Alshohda','Minouf','Elbagoor','Quesna','BerketAlseb3'],
    'Minouf':['Alshohda','ShebinElkom','Elbagoor','Ashmoon','Elsadat'],
    'Tala':['BerketAlseb3','ShebinElkom','Alshohda','KafrElZayat','Tanta','AsSantah'],
    'BerketAlseb3':['Tala','ShebinElkom','Quesna','AsSantah','Zefta'],
    'Elbagoor':['Quesna','ShebinElkom','Minouf','Ashmoon','Banha','Toukh','AlQanatirAlKhayriyyah'],
    'Ashmoon':['Elbagoor','Minouf','Elsadat','AlQanatirAlKhayriyyah','Toukh'],
    'Quesna':['BerketAlseb3','ShebinElkom','Elbagoor','Zefta','Kafrshokr','Banha'],
    'Elsadat':['Ashmoon','Minouf'],
    'Alshohda':['Tala','ShebinElkom','Minouf'],
    'KafrElZayat':['Basioun','Tanta','Tala'],
    'Basioun':['Qutur','Tanta','KafrElZayat'],
    'Qutur':['Basioun','Tanta','ElMahallaElKubra'],
    'ElMahallaElKubra':['Qutur','Tanta','AsSantah','Zefta','Samannoud'],
    'Samannoud':['ElMahallaElKubra','AsSantah','Zefta'],
    'Zefta':['Samannoud','ElMahallaElKubra','AsSantah','Quesna','BerketAlseb3','Kafrshokr'],
    'AsSantah':['Samannoud','ElMahallaElKubra','BerketAlseb3','Tanta'],
    'Tanta':['Tala','KafrElZayat','Basioun','Qutur','ElMahallaElKubra','AsSantah'],
    'Kafrshokr':['Zefta','Quesna','Banha'],
    'Banha':['Kafrshokr','Quesna','Elbagoor','Toukh','ShibinElQanatir'],
    'Toukh':['Banha','Elbagoor','Ashmoon','AlQanatirAlKhayriyyah','Qalyub','ShibinElQanatir'],
    'AlQanatirAlKhayriyyah':['Toukh','Ashmoon','ShubraAlKhaymah','Qalyub'],
    'ShubraAlKhaymah':['AlQanatirAlKhayriyyah','Qalyub','Elkhankah'],
    'Qalyub':['Elkhankah','ShibinElQanatir','Toukh','AlQanatirAlKhayriyyah','ShubraAlKhaymah'],
    'ShibinElQanatir':['Banha','Toukh','Qalyub','Elkhankah'],
    'Elkhankah':['ShibinElQanatir','Qalyub','ShubraAlKhaymah']
    }
    visited = set()
    queue = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start)
    #Add start noda as visited
    visited.add(start)
    
    # first Start node has no parent
    parent = dict()
    parent[start] = None
    #Test the queue if the queue is empty then there is no node
    path_found = False
    while not queue.empty():
        current_node = queue.get() #add current node in queue
        if current_node == goal:   #check the goal
            path_found = True      #if the path is true return pass 
            break
        #Checking the adjacent nodes
        for next_node in adj_list[current_node]:
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)
                
    # get the path
    path = []
    if path_found:
        path.append(goal)
        while parent[goal] is not None:
            path.append(parent[goal]) 
            goal = parent[goal]
        path.reverse()
    return path
#-=======================DFS Algorithm======================

def DFS(start, end):
    #Adjacent nodes for every node
    adj_list={

        'ShebinElkom':['Tala','Alshohda','Minouf','Elbagoor','Quesna','BerketAlseb3'],
        'Minouf':['Alshohda','ShebinElkom','Elbagoor','Ashmoon','Elsadat'],
        'Tala':['BerketAlseb3','ShebinElkom','Alshohda','KafrElZayat','Tanta','AsSantah'],
        'BerketAlseb3':['Tala','ShebinElkom','Quesna','AsSantah','Zefta'],
        'Elbagoor':['Quesna','ShebinElkom','Minouf','Ashmoon','Banha','Toukh','AlQanatirAlKhayriyyah'],
        'Ashmoon':['Elbagoor','Minouf','Elsadat','AlQanatirAlKhayriyyah','Toukh'],
        'Quesna':['BerketAlseb3','ShebinElkom','Elbagoor','Zefta','Kafrshokr','Banha'],
        'Elsadat':['Ashmoon','Minouf'],
        'Alshohda':['Tala','ShebinElkom','Minouf'],
        'KafrElZayat':['Basioun','Tanta','Tala'],
        'Basioun':['Qutur','Tanta','KafrElZayat'],
        'Qutur':['Basioun','Tanta','ElMahallaElKubra'],
        'ElMahallaElKubra':['Qutur','Tanta','AsSantah','Zefta','Samannoud'],
        'Samannoud':['ElMahallaElKubra','AsSantah','Zefta'],
        'Zefta':['Samannoud','ElMahallaElKubra','AsSantah','Quesna','BerketAlseb3','Kafrshokr'],
        'AsSantah':['Samannoud','ElMahallaElKubra','BerketAlseb3','Tanta'],
        'Tanta':['Tala','KafrElZayat','Basioun','Qutur','ElMahallaElKubra','AsSantah'],
        'Kafrshokr':['Zefta','Quesna','Banha'],
        'Banha':['Kafrshokr','Quesna','Elbagoor','Toukh','ShibinElQanatir'],
        'Toukh':['Banha','Elbagoor','Ashmoon','AlQanatirAlKhayriyyah','Qalyub','ShibinElQanatir'],
        'AlQanatirAlKhayriyyah':['Toukh','Ashmoon','ShubraAlKhaymah','Qalyub'],
        'ShubraAlKhaymah':['AlQanatirAlKhayriyyah','Qalyub','Elkhankah'],
        'Qalyub':['Elkhankah','ShibinElQanatir','Toukh','AlQanatirAlKhayriyyah','ShubraAlKhaymah'],
        'ShibinElQanatir':['Banha','Toukh','Qalyub','Elkhankah'],
        'Elkhankah':['ShibinElQanatir','Qalyub','ShubraAlKhaymah']
    }


    visited = [] # Set to keep track of visited nodes of graph.
    allpath = []
    path = []

    def dfs(visited, adj_list, node):  #function for dfs 
        if node not in visited:
            # print (node, end = " ")
            allpath.append(node)
            visited.append(node)
            for neighbour in adj_list[node]:
                dfs(visited, adj_list, neighbour)
                    

    # Driver Code
    first = start
    last = end
    # print("Following is the Depth-First Search")
    dfs(visited, adj_list, first)
    # print(path)
    # print the path
    for point in allpath:
        # print(point)
        path.append(point);
        if point == last:
            break
    # print(allpath)
    # print(path)
    return path

#=======================A_Star Search=======================
graph ={
    #Elmenofia
    'shebin': {'tala': 18, 'el shohada': 16.5,'minuf':16.4,'el-bagour':14.6,'quwaysna':18.7,'birket as sab': 14},
    'minuf': {'el shohada':18.2, 'shebin': 16.1,'el-bagour':11.4,'ashmun':27,'el sadat city':55.9},
    'tala': {'birket as sab':18.1,'shebin': 18,'el shohada':14.4,'Kafr El-Zayat':25.6,'tanta':15.3,'As Santah':29.2},
    'birket as sab': {'tala':18.1, 'shebin': 14,'quwaysna':13.3,'As Santah':16,'zefta':24.5},
    'el-bagour': {'quwaysna':29.8, 'shebin':14.9,'minuf':11.5,'ashmun':22.5,'banha':26.6,'toukh':39.7,'Al Qanatir Al Khayriyyah':30.8},
    'ashmun': {'el-bagour':23.8, 'minuf':27.1,'el sadat city':61.7,'Al Qanatir Al Khayriyyah':23.5,'toukh':56.3},
    'quwaysna': {'birket as sab':13.9,'shebin':18.1,'el-bagour':18.1,'zefta':21.1,'kafr shokr':26.8,'banha':15.1},
    'el sadat city': {'ashmun':73.8,'minuf':54.5},
    'el shohada': {'tala':14.4,'shebin':17.5,'minuf':18.2},
    #Elgarbia
    'Kafr El-Zayat':{'basioun':20.2,'tanta':27.6,'tala':25.6},
    'basioun':{'qutur':16.8,'tanta':28.8,'Kafr El-Zayat':20.2},
    'qutur':{'basioun':17.1,'tanta':16.3,'El-Mahalla El-Kubra':28.8},
    'El-Mahalla El-Kubra':{'qutur':30.8,'tanta':31.5,'As Santah':30.8,'zefta':33.3,'Samannoud':7.7},
    'Samannoud':{'El-Mahalla El-Kubra':7.8,'As Santah':46.6,'zefta':33.1},
    'zefta':{'Samannoud':35,'El-Mahalla El-Kubra':32.7,'As Santah':17.9,'quwaysna':21.1,'birket as sab':25.3,'kafr shokr':27.9},
    'As Santah':{'Samannoud':48.7,'El-Mahalla El-Kubra':30.3,'birket as sab':16.2,'tanta':25.3},
    'tanta':{'tala':15,'Kafr El-Zayat':26.4,'basioun':28.3,'qutur':16,'El-Mahalla El-Kubra':29.2,'As Santah':25.9},
    'kafr shokr':{'zefta':32.7,'quwaysna':23.1,'banha':13.4},
    #Elkalubia
    'banha':{'kafr shokr':17.7,'quwaysna':17.8,'el-bagour':29.4,'toukh':15.6,'shibin el qanatir':28.8},
    'toukh':{'banha':17.5,'el-bagour':40,'ashmun':57.5,'Al Qanatir Al Khayriyyah':25,'qalyub':22,'shibin el qanatir':14},
    'Al Qanatir Al Khayriyyah':{'toukh':24.7,'ashmun':23.5,'Shubra Al Khaymah':18.5,'qalyub':7.6},
    'Shubra Al Khaymah':{'Al Qanatir Al Khayriyyah':18.4,'qalyub':11.6,'el khankah':22.4},
    'qalyub':{'el khankah':26.9,'shibin el qanatir':20.6,'toukh':22.7,'Al Qanatir Al Khayriyyah':7.6,'Shubra Al Khaymah':12.1},
    'shibin el qanatir':{'banha':29.8,'toukh':14,'qalyub':20.4,'el khankah':17.6},
    'el khankah':{'shibin el qanatir':15.9,'qalyub':27.4,'Shubra Al Khaymah': 24.4},
}

Coordinates={
    #Elmenofia
    "ShebinElkom":[30.554928799816988, 31.012393143088957],
    "Minouf":[30.45841991481536, 30.933867041463532],
    "Tala":[30.683127111837056, 30.950034191578247],
    "BerketAlseb3":[30.627495984801378, 31.07244250380298],
    "Elbagoor":[30.43186671298956, 31.031983255977398],
    "Ashmoon":[30.300117313578117, 30.97564036423758],
    "Quesna":[30.56765698894867, 31.149568418149613],
    "Elsadat":[30.362811748009076, 30.533153025293895],
    "Alshohda":[30.59768043193886, 30.895758793318098],
    #Elgharbia
    "KafrElZayat":[30.828935887979828, 30.81468363315086],
    "Basioun":[30.941234859668185, 30.819787152459256],
    "Tanta":[30.78236661466976, 31.003931835360497],
    "Qutur":[30.97124133198592, 30.952896608684792],
    "ElMahallaElKubra":[30.969841036674914, 31.166019730570685],
    "AsSantah":[30.749281457375343, 31.129532111290036],
    "Samannoud":[30.96202482138702, 31.241725792395766],
    "Zefta":[30.714483753839744, 31.240197668420624],
    #Elkalubia
    "Banha":[30.46954041758182, 31.18372798445176],
    "Qalyub":[30.180143566835696, 31.20638419614639],
    "AlQanatirAlKhayriyyah":[30.194609758641715, 31.13391214967144],
    "ShubraAlKhaymah":[30.124142365522676, 31.260465002556664],
    "Elkhankah":[30.22039965655326, 31.368612270866304],
    "Kafrshokr":[30.552839823187284, 31.255430468410704],
    "ShibinElQanatir":[30.31214792794175, 31.32292278281032],
    "Toukh":[30.353756127836252, 31.2014138527108],
}
""""""
#functon to get the shortest path
def AStar(start , end):
    def path_f_cost(path):
        g_cost = 0
        for(node , cost) in path:
            g_cost += cost
        last_node = path[-1][0]
        h_cost =hs.haversine(Coordinates[last_node] , Coordinates[end])
        f_cost = g_cost + h_cost
        return f_cost , last_node

    visited =[]
    queue =[[(start , 0)]]
    while queue:
        queue.sort(key=path_f_cost)
        path = queue.pop(0)
        node = path[-1][0]
        if node in visited:
            continue
        visited.append(node)
        if node == end:
            return path
        else:
            adjacent_nodes= graph.get(node , [])
            for(node2 , cost) in adjacent_nodes:
                new_path = path.copy()
                new_path.append((node2 , cost))
                queue.append(new_path)

#=======================Display function========================
def display_function(start, end, algo):
    start= Select_Start.get()
    end  = Select_End.get()
    algo = Select_Algorithm.get()
    path = []

    if start != "Intial State" and end != "Goal State" and algo != "Algorithm":

        #  Check Algorithm type
        if algo == 'BFS':
            path = BFS(start , end)
        elif algo == 'DFS':
            path = DFS(start , end)
        elif algo == 'AStar':
            path = AStar(start , end)
        # Creat API Map Key
        client = ors.Client(key='5b3ce3597851110001cf62489f97821fab9b46a18afb841b2c9226af')
        # create MAP object
        #===========================================================================.
        mapobj = folium.Map(location=[30.683127111837056, 30.950034191578247] , zoom_start=10 )
        #=======================Marker Elmenofia====================================.

        folium.Marker(location=[30.554928799816988, 31.012393143088957] , tooltip='ShebinElkom' , popup='30.554928799816988, 31.012393143088957').add_to(mapobj)
        folium.Marker(location=[30.45841991481536, 30.933867041463532],tooltip='Minouf' , popup='30.45841991481536, 30.933867041463532',icon=folium.Icon(icon='star')).add_to(mapobj)
        folium.Marker(location=[30.683127111837056, 30.950034191578247],tooltip='Tala',popup='30.683127111837056, 30.950034191578247' , icon=folium.Icon(icon='pencil')).add_to(mapobj)
        folium.Marker(location=[30.627495984801378, 31.07244250380298],tooltip='BerketAlseb3',popup='30.627495984801378, 31.07244250380298').add_to(mapobj)
        folium.Marker(location=[30.43186671298956, 31.031983255977398],tooltip='Elbagoor',popup='30.43186671298956, 31.031983255977398').add_to(mapobj)
        folium.Marker(location=[30.300117313578117, 30.97564036423758],tooltip='Ashmoon',popup='30.300117313578117, 30.97564036423758').add_to(mapobj)
        folium.Marker(location=[30.56765698894867, 31.149568418149613],tooltip='Quesna',popup='30.56765698894867, 31.149568418149613').add_to(mapobj)
        folium.Marker(location=[30.362811748009076, 30.533153025293895],tooltip='Elsadat',popup='30.362811748009076, 30.533153025293895').add_to(mapobj)
        folium.Marker(location=[30.59768043193886, 30.895758793318098],tooltip='Alshohda',popup='30.59768043193886, 30.895758793318098').add_to(mapobj)
        
        #=======================Marker Elgharbia====================================

        folium.Marker(location=[30.828935887979828, 30.81468363315086],tooltip='KafrElZayat',popup='30.828935887979828, 30.81468363315086').add_to(mapobj)
        folium.Marker(location=[30.941234859668185, 30.819787152459256],tooltip='Basioun',popup='30.941234859668185, 30.819787152459256').add_to(mapobj)
        folium.Marker(location=[30.78236661466976, 31.003931835360497],tooltip='Tanta',popup='30.78236661466976, 31.003931835360497').add_to(mapobj)
        folium.Marker(location=[30.97124133198592, 30.952896608684792],tooltip='Qutur',popup='30.97124133198592, 30.952896608684792').add_to(mapobj)
        folium.Marker(location=[30.969841036674914, 31.166019730570685],tooltip='ElMahallaElKubra',popup='30.969841036674914, 31.166019730570685').add_to(mapobj)
        folium.Marker(location=[30.749281457375343, 31.129532111290036],tooltip='AsSantah',popup='30.749281457375343, 31.129532111290036').add_to(mapobj)
        folium.Marker(location=[30.96202482138702, 31.241725792395766],tooltip='Samannoud',popup='30.96202482138702, 31.241725792395766').add_to(mapobj)
        folium.Marker(location=[30.714483753839744, 31.240197668420624],tooltip='Zefta',popup='30.714483753839744, 31.240197668420624').add_to(mapobj)
        
        #=======================Marker Elkalubia=================================

        folium.Marker(location=[30.46954041758182, 31.18372798445176],tooltip='Banha',popup='30.46954041758182, 31.18372798445176').add_to(mapobj)
        folium.Marker(location=[30.180143566835696, 31.20638419614639],tooltip='Qalyub',popup='30.180143566835696, 31.20638419614639').add_to(mapobj)
        folium.Marker(location=[30.194609758641715, 31.13391214967144],tooltip='AlQanatirAlKhayriyyah',popup='30.194609758641715, 31.13391214967144').add_to(mapobj)
        folium.Marker(location=[30.124142365522676, 31.260465002556664],tooltip='ShubraAlKhaymah',popup='30.124142365522676, 31.260465002556664').add_to(mapobj)
        folium.Marker(location=[30.22039965655326, 31.368612270866304],tooltip='Elkhankah',popup='30.22039965655326, 31.368612270866304').add_to(mapobj)
        folium.Marker(location=[30.552839823187284, 31.255430468410704],tooltip='Kafrshokr',popup='30.552839823187284, 31.255430468410704').add_to(mapobj)
        folium.Marker(location=[30.31214792794175, 31.32292278281032],tooltip='ShibinElQanatir',popup='30.31214792794175, 31.32292278281032').add_to(mapobj)
        folium.Marker(location=[30.353756127836252, 31.2014138527108],tooltip='Toukh',popup='30.353756127836252, 31.2014138527108').add_to(mapobj)
        
        #========================================================================
        
        for item in path:
            if item == start:
                folium.Marker(location=Coordinates[item], popup=item, tooltip='Initial Stata', icon=folium.Icon(color='green')).add_to(mapobj)
            elif item == end:
                folium.Marker(location=Coordinates[item], popup=item, tooltip='Goal State', icon=folium.Icon(color='red')).add_to(mapobj)
            else:
                folium.Marker(location=Coordinates[item], popup=item, tooltip= item , icon=folium.Icon(color='black')).add_to(mapobj)

        for i in range(len(path)-1):
            coord= [Coordinates[path[i]][::-1], Coordinates[path[i+1]][::-1]]
            route = client.directions(coordinates=coord,profile='driving-car',format='geojson')
            folium.GeoJson(route, name='route').add_to(mapobj)
        #Saving MAP
        mapobj.save('map.html')

        #open file on WebBrowser
        filename = 'file:'+os.getcwd()+'/' + 'map.html'
        webbrowser.open_new_tab(filename)

    else:
        print('Sorry , Insufficient Informatio ')
#=========================CREATE GUI=========================================
pro = Tk()
pro.title('SEARCH ALGORITH')
pro.geometry('1100x500')
pro.config(background='#212121')

lbl1 = Label(pro , text='SEARCH ALGORITHM' , font=('Expanded Bold Oblique', 12, 'bold') ,bg='#FF3D00' , fg='#E0E0E0', height=2)
lbl1.pack(fill=X)
#====================Select start-============================================
lbl2 = Label(pro , text='From' ,font=('Times New Roman',12,'bold'), height=2 , bg='#212121' , fg='#FF3D00')
lbl2.place(x = 20 , y = 60)
Select_Start = StringVar()
Select_Start.set("Intial State")
comb1 = ttk.Combobox(pro , textvariable=Select_Start,values=('Tala','Alshohda','BerketAlseb3','Quesna','ShebinElkom','Minouf','Elbagoor','Ashmoon','Elsadat','KafrElZayat','Basioun','Tanta','Qutur','ElMahallaElKubra' ,'AsSantah','Samannoud','Zefta','Banha','Qalyub','AlQanatirAlKhayriyyah','ShubraAlKhaymah','Elkhankah','Kafrshokr','Toukh', 'ShibinElQanatir') , state='readonly' , font=10 ,background='#FF3D00',foreground='#212121')
comb1.place(x = 70, y =71 )

#======================Select end==============================================

lbl3 = Label(pro , text='To' ,font=('Times New Roman',12,'bold') , height=2 , bg='#212121' , fg='#FF3D00')
lbl3.place(x = 20 , y = 120)
Select_End = StringVar()
Select_End.set("Goal State")
comb2 = ttk.Combobox(pro , textvariable=Select_End ,values=('Tala','Alshohda','BerketAlseb3','Quesna','ShebinElkom','Minouf','Elbagoor','Ashmoon','Elsadat','KafrElZayat','Basioun','Tanta','Qutur','ElMahallaElKubra' ,'AsSantah','Samannoud','Zefta','Banha','Qalyub','AlQanatirAlKhayriyyah','ShubraAlKhaymah','Elkhankah','Kafrshokr','Toukh', 'ShibinElQanatir') , state='readonly' , font=10 ,background='#FF3D00',foreground='#212121')
comb2.place(x = 70, y =130 )

#=======================Select algorithm=======================================

lbl4 = Label(pro , text='Type' , font=('Times New Roman ',12,'bold') , height=2 , bg='#212121' , fg='#FF3D00')
lbl4.place(x = 20 , y = 180)
Select_Algorithm = StringVar()
Select_Algorithm.set('Algorithm')
comb3 = ttk.Combobox(pro , textvariable=Select_Algorithm,values=('BFS' , 'DFS' , 'AStar') , state='readonly', font=10 ,background='#FF3D00',foreground='#212121')
comb3.place(x = 70, y =189 )

#=======================Button for search======================================
bt1 = Button(pro , text='Search' , bg='#FF3D00', fg='#E0E0E0' , width=10 , height=2 ,command=partial(display_function,comb1,comb2,comb3))
bt1.place(x = 75 , y = 240)
bt2 = Button(pro , text='Exit' , bg='#FF3D00', fg='#E0E0E0' , width=10 , height=2 , command=pro.quit)
bt2.place(x = 190 , y = 240)
#======================Create map on GUI=======================================

fr1 = Frame(pro , width=710 , height=410 , bg='#424242')
fr1.place(x = 330 , y = 73)
map_widget = TkinterMapView(fr1 ,width=698 , height=400 )
map_widget.place(x = 5 , y = 5)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga" , max_zoom=10)

#=====================================Elmenofyia===============================

map_widget.set_position(30.683127111837056, 30.950034191578247 , marker=True)
map_widget.set_position(30.554928799816988, 31.012393143088957 , marker=True)
map_widget.set_position(30.45841991481536, 30.933867041463532, marker=True)
map_widget.set_position(30.627495984801378, 31.07244250380298, marker=True)
map_widget.set_position(30.43186671298956, 31.031983255977398, marker=True)
map_widget.set_position(30.300117313578117, 30.97564036423758, marker=True)
map_widget.set_position(30.56765698894867, 31.149568418149613, marker=True)
map_widget.set_position(30.362811748009076, 30.533153025293895, marker=True)
map_widget.set_position(30.59768043193886, 30.895758793318098, marker=True)

#=====================ElGarbia=================================================

map_widget.set_position(30.828935887979828, 30.81468363315086, marker=True)
map_widget.set_position(30.941234859668185, 30.819787152459256, marker=True)
map_widget.set_position(30.78236661466976, 31.003931835360497, marker=True)
map_widget.set_position(30.97124133198592, 30.952896608684792, marker=True)
map_widget.set_position(30.969841036674914, 31.166019730570685, marker=True)
map_widget.set_position(30.749281457375343, 31.129532111290036, marker=True)
map_widget.set_position(30.96202482138702, 31.241725792395766, marker=True)
map_widget.set_position(30.714483753839744, 31.240197668420624, marker=True)

#=====================El kalubia===============================================

map_widget.set_position(30.46954041758182, 31.18372798445176, marker=True)
map_widget.set_position(30.180143566835696, 31.20638419614639, marker=True)
map_widget.set_position(30.194609758641715, 31.13391214967144, marker=True)
map_widget.set_position(30.124142365522676, 31.260465002556664, marker=True)
map_widget.set_position(30.22039965655326, 31.368612270866304, marker=True)
map_widget.set_position(30.552839823187284, 31.255430468410704, marker=True)
map_widget.set_position(30.31214792794175, 31.32292278281032, marker=True)
map_widget.set_position(30.353756127836252, 31.2014138527108, marker=True)
map_widget.set_zoom(12)

pro.mainloop()

#========================FINISH================================================
#==============================================================================
#==============================================================================
