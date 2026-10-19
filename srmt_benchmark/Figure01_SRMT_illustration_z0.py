from Import_CWD import *


############################################################
############################################################

imshow_args = {"cmap": None,
               "norm": None,
               "origin":"lower",
               }

cmap=matplotlib.cm.jet
imshow_args["cmap"]=cmap


#color_srmt = "cornflowerblue"
color_srmt = "royalblue"

color_box  = "gray"

color_edge = "gray"

############################################################


hfig    = plt.figure(figsize=(3.543, 4.36), dpi=figure_dpi)


margin  = [0.05,0.05,0.05,0.05,0.0,0.0]
barbox  = [0.05,0.01,0.6]
windows = [4,3]


args_box_edge = {
    "linewidth":0.3,
    "color":color_box,
    }

args_box_vertex = {
    "marker":"o",
    "color":"gray",
    "s":2,
    }


args_subcell_edge = {
    "linewidth":0.3,
    "color":color_box,
    }

args_subcell_edge_srmt = {
    "linewidth":0.5,
    "color":color_srmt,
    "zorder":20,
    }

args_tetrahedra_edge_srmt = {
    "linestyle":"-",
    "linewidth":0.5,
    "color":color_srmt
    }


fontsize_tmp = 8






##################################################
##################################################
rid,cid=0,0
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[0.0,0.5,0.0],[0.5,0.5,0.0]]
for i in range(4):
    func_box(haxe,points[i],0.5,args_box_edge)
    points[i][2]+=0.5
    func_box(haxe,points[i],0.5,args_box_edge)


points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[1.0,0.0,0.0]]
for i in range(3):
    for j in range(3):
        for k in range(3):
            haxe.scatter(i*0.5,j*0.5,k*0.5,**args_box_vertex)



# box - srmt
func_box(haxe,[0,0,0],0.5,args_subcell_edge_srmt)

# diagonals
points=[[0,0,0],[1.0,0,0],[0,1.0,0],[1.0,1.0,0]]

for i in range(4):
    for k in range(3):
        points[i][2]=k*0.5
        func_points_line(haxe,points[i],[0.5,0.5,k*0.5],args_box_edge)

for i in range(4):
    points[i][2]=0.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)
    
    points[i][2]=1.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s)c_{000}$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

#haxe.set_xlabel(r"$(%s%d)$"%(chr(ord("a")+rid),cid))

haxe.view_init(elev=10,azim=-25,roll=0)



##################################################

rid,cid=0,1
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)


args_tetrahedra_edge_srmt["linestyle"]="-"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)


args_tetrahedra_edge_srmt["linestyle"]="--"
# diagonals
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)




xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s1)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)


##################################################

rid,cid=0,2
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)


haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)



args_tetrahedra_edge_srmt["linestyle"]="-"

# edge
func_points_line(haxe,[0.0,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

# dianonals
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)


args_tetrahedra_edge_srmt["linestyle"]="--"

# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

# dianonals
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s2)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)






##################################################
##################################################
rid,cid=1,0
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[0.0,0.5,0.0],[0.5,0.5,0.0]]
for i in range(4):
    func_box(haxe,points[i],0.5,args_box_edge)
    points[i][2]+=0.5
    func_box(haxe,points[i],0.5,args_box_edge)


points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[1.0,0.0,0.0]]
for i in range(3):
    for j in range(3):
        for k in range(3):
            haxe.scatter(i*0.5,j*0.5,k*0.5,**args_box_vertex)



# box - srmt
func_box(haxe,[0.0,0.5,0],0.5,args_subcell_edge_srmt)

# diagonals
points=[[0.0,0.0,0.0],[1.0,0.0,0.0],[0.0,1.0,0.0],[1.0,1.0,0.0]]

for i in range(4):
    for k in range(3):
        points[i][2]=k*0.5
        func_points_line(haxe,points[i],[0.5,0.5,k*0.5],args_box_edge)

for i in range(4):
    points[i][2]=0.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)
    
    points[i][2]=1.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s)c_{010}$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

#haxe.set_xlabel(r"$(%s%d)$"%(chr(ord("a")+rid),cid))

haxe.view_init(elev=10,azim=-25,roll=0)



##################################################

rid,cid=1,1
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)


args_tetrahedra_edge_srmt["linestyle"]="-"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)


# diagonals
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)


args_tetrahedra_edge_srmt["linestyle"]="--"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s1)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)


##################################################

rid,cid=1,2
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)


haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)



args_tetrahedra_edge_srmt["linestyle"]="-"

# edge
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.5,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.5,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)



args_tetrahedra_edge_srmt["linestyle"]="--"
# edge
func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)





xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s2)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)





##################################################
##################################################
rid,cid=2,0
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
points=[[0,0,0],[0.5,0,0],[0,0.5,0],[0.5,0.5,0]]
for i in range(4):
    func_box(haxe,points[i],0.5,args_box_edge)
    points[i][2]+=0.5
    func_box(haxe,points[i],0.5,args_box_edge)


points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[1.0,0.0,0.0]]
for i in range(3):
    for j in range(3):
        for k in range(3):
            haxe.scatter(i*0.5,j*0.5,k*0.5,**args_box_vertex)



# box - srmt
func_box(haxe,[0.5,0.5,0],0.5,args_subcell_edge_srmt)

# diagonals
points=[[0,0,0],[1.0,0,0],[0,1.0,0],[1.0,1.0,0]]

for i in range(4):
    for k in range(3):
        points[i][2]=k*0.5
        func_points_line(haxe,points[i],[0.5,0.5,k*0.5],args_box_edge)

for i in range(4):
    points[i][2]=0.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)
    
    points[i][2]=1.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s)c_{110}$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

#haxe.set_xlabel(r"$(%s%d)$"%(chr(ord("a")+rid),cid))

haxe.view_init(elev=10,azim=-25,roll=0)



##################################################

rid,cid=2,1
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)


args_tetrahedra_edge_srmt["linestyle"]="-"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)


# diagonals
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.5],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)



args_tetrahedra_edge_srmt["linestyle"]="--"
# edge

# diagonals
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)




xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s1)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)


##################################################

rid,cid=2,2
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)


haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)



args_tetrahedra_edge_srmt["linestyle"]="-"

# edge
func_points_line(haxe,[0.0,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

# dianonals
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)


args_tetrahedra_edge_srmt["linestyle"]="--"

# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

# dianonals
func_points_line(haxe,[0.5,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.5],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)


xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s2)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)





##################################################
##################################################
rid,cid=3,0
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
points=[[0,0,0],[0.5,0,0],[0,0.5,0],[0.5,0.5,0]]
for i in range(4):
    func_box(haxe,points[i],0.5,args_box_edge)
    points[i][2]+=0.5
    func_box(haxe,points[i],0.5,args_box_edge)


points=[[0.0,0.0,0.0],[0.5,0.0,0.0],[1.0,0.0,0.0]]
for i in range(3):
    for j in range(3):
        for k in range(3):
            haxe.scatter(i*0.5,j*0.5,k*0.5,**args_box_vertex)



# box - srmt
func_box(haxe,[0.5,0.0,0],0.5,args_subcell_edge_srmt)


# diagonals
points=[[0,0,0],[1.0,0,0],[0,1.0,0],[1.0,1.0,0]]

for i in range(4):
    for k in range(3):
        points[i][2]=k*0.5
        func_points_line(haxe,points[i],[0.5,0.5,k*0.5],args_box_edge)

for i in range(4):
    points[i][2]=0.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)
    
    points[i][2]=1.0
    func_points_line(haxe,points[i],[0.5,0.5,0.5],args_box_edge)



xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s)c_{100}$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

#haxe.set_xlabel(r"$(%s%d)$"%(chr(ord("a")+rid),cid))

haxe.view_init(elev=10,azim=-25,roll=0)



##################################################

rid,cid=3,1
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)
haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)


args_tetrahedra_edge_srmt["linestyle"]="-"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.5,0.0,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)


# diagonals
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.0,0.5],args_tetrahedra_edge_srmt)


args_tetrahedra_edge_srmt["linestyle"]="--"
# edge
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.0,0.0,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)




xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s1)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)


##################################################

rid,cid=3,2
axes_pos=fig_axes_position(index=[rid,cid],size=[1,1],windows=windows,margin=margin)


haxe=hfig.add_axes(axes_pos,projection="3d")


# box
func_box(haxe,[0,0,0],0.5,args_subcell_edge)


args_tetrahedra_edge_srmt["linestyle"]="-"

# edge
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.0,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

func_points_line(haxe,[0.0,0.5,0.5],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.5,0.0,0.5],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.5,0.5,0.5],args_tetrahedra_edge_srmt)



args_tetrahedra_edge_srmt["linestyle"]="--"
# edge
func_points_line(haxe,[0.0,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.0,0.5,0.0],[0.5,0.5,0.0],args_tetrahedra_edge_srmt)

# diagonals
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.0],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.0,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)
func_points_line(haxe,[0.5,0.5,0.0],[0.0,0.5,0.5],args_tetrahedra_edge_srmt)






xlim=haxe.get_xlim()
ylim=haxe.get_ylim()
zlim=haxe.get_zlim()
haxe.text(xlim[0]+0.2*(xlim[1]-xlim[0]),ylim[0]+0.3*(ylim[1]-ylim[0]),zlim[0]-0.55*(zlim[1]-zlim[0]),r"$(%s2)$"%(chr(ord("a")+rid)),fontsize=fontsize_tmp)


#haxe.set_xlabel(r"$X$")
#haxe.set_ylabel(r"$Y$")
#haxe.set_zlabel(r"$Z$")
haxe.set_axis_off()

haxe.view_init(elev=10,azim=-25,roll=0)





##################################################

fig_path = path_fig
fig_name = os.path.splitext(os.path.basename(__file__))[0]

fig_save(plt,figpath=fig_path,figname=fig_name,extension=fig_fmts)
