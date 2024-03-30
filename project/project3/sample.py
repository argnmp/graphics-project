from shader import *
from keyinput import *
from vao import *
from draw import *
from objparser import *
import globalvar

# time variant transformation should be defined in root object for child nodes

def load_earth(parent, earth_vaos, windowing_transformation):
    shader_phong = load_shaders(g_vertex_phong_shader_src, g_fragment_phong_shader_src)
    obj_earth = Node(parent, None, 0, 0, shader_phong, True)
    obj_earth.set_static_transform(windowing_transformation)
    obj_earth.set_origin_transform(glm.inverse(windowing_transformation))
    sat = None
    for (index,(vao, fn, object_name)) in enumerate(earth_vaos):
        temp = Node(obj_earth, vao, 0, fn, shader_phong, True)
        if object_name.startswith("White"):
            temp.set_color_properties([10, 10, 10], [1,1,1], [0.95,0.95,0.95], 10, True)
        elif object_name.startswith("Blue"):
            temp.set_color_properties([10, 10, 10],  [1,1,1], [0.1,0.502,1],10, True)
        elif object_name.startswith("Green"):
            temp.set_color_properties([10, 10, 10], [1,1,1], [0.235,0.702,0.443], 50, True)
        elif object_name.startswith("Brown"):
            temp.set_color_properties([10, 10, 10],  [1,1,1],[0.5,0.25,0], 50, True)
        elif object_name.startswith("Lava"):
            temp.set_color_properties([10, 10, 10], [1,1,1], [1,0,0], 5, True)
        elif object_name.startswith("Material"):
            sat = temp
            sat.set_color_properties([100, 100, 100], [1,1,1], [0.965, 0.935, 0.835], 100, True)
            sat.set_origin_transform(glm.translate((-1.15, -3.3, -5.5)))
    def f1():
        sat.set_org_local_transform(glm.rotate(globalvar.g_time*5, (0,1,0)))
    obj_earth.set_refresh_function(f1)


    return (obj_earth)


def load_tucano(parent, tucano_vaos, windowing_transformation):
    shader_phong = load_shaders(g_vertex_phong_shader_src, g_fragment_phong_shader_src)
    obj_tucano = Node(parent, None, 0, 0, shader_phong, True)
    obj_tucano.set_static_transform(windowing_transformation)
    obj_tucano.set_origin_transform(glm.inverse(windowing_transformation))
    obj_tucano_prop = None
    obj_tucano_flapL = None
    obj_tucano_flapR = None
    obj_tucano_eleronL = None
    obj_tucano_eleronR = None
    for (index,(vao, fn, object_name)) in enumerate(tucano_vaos):
        if(index==1):
            obj_tucano_prop = Node(obj_tucano, vao, 0, fn, shader_phong, True)
            obj_tucano_prop.set_origin_transform(glm.translate((0, -1.6, 0)))

        elif(index==11):
            obj_tucano_flapL = Node(obj_tucano, vao, 0, fn, shader_phong, True)
            obj_tucano_flapL.set_origin_transform(glm.rotate(np.radians(5), (0, 1, 0))*glm.rotate(np.radians(-5), (0,0,1))*glm.translate((-0.55, -1.1, -0.4)))

        elif(index==12):
            obj_tucano_flapR = Node(obj_tucano, vao, 0, fn, shader_phong, True)
            obj_tucano_flapR.set_origin_transform(glm.rotate(np.radians(-5), (0, 1, 0))*glm.rotate(np.radians(5), (0,0,1))*glm.translate((0.55, -1.1, -0.4)))

        elif(index==13):
            obj_tucano_eleronL = Node(obj_tucano, vao, 0, fn, shader_phong, True)
            obj_tucano_eleronL.set_origin_transform(glm.rotate(np.radians(9), (0, 1, 0))*glm.rotate(np.radians(-7), (0,0,1))*glm.translate((-3, -1.3, -0.6)))
        elif(index==14):
            obj_tucano_eleronR = Node(obj_tucano, vao, 0, fn, shader_phong, True)
            obj_tucano_eleronR.set_origin_transform(glm.rotate(np.radians(-9), (0, 1, 0))*glm.rotate(np.radians(7), (0,0,1))*glm.translate((3, -1.3, -0.6)))

        else:
            Node(obj_tucano, vao, 0, fn, shader_phong, True)

    def f():
        obj_tucano_prop.set_org_local_transform(glm.rotate(globalvar.g_time*10,(0,0,1)))
        obj_tucano_flapL.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time), (1, 0, 0)))
        obj_tucano_flapR.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time), (1, 0, 0)))
        obj_tucano_eleronL.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time)*0.5, (1, 0, 0)))
        obj_tucano_eleronR.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time)*0.5, (1, 0, 0)))
    obj_tucano.set_refresh_function(f)


    return (obj_tucano, obj_tucano_prop, obj_tucano_flapL, obj_tucano_flapR, obj_tucano_eleronL, obj_tucano_eleronR)

def load_drone(parent, drone_vaos, windowing_transformation):
    shader_phong = load_shaders(g_vertex_phong_shader_src, g_fragment_phong_shader_src)
    obj_drone = Node(parent, None, 0, 0, shader_phong, True)
    obj_drone.set_static_transform(windowing_transformation)
    obj_drone.set_origin_transform(glm.inverse(windowing_transformation))
     
    for (index,(vao, fn, object_name)) in enumerate(drone_vaos):
        temp = Node(obj_drone, vao, 0, fn, shader_phong, True)
        temp.set_static_transform(glm.translate((0,-0.25,0)))
        if index==2:
            temp.set_origin_transform(glm.translate((-0.1,0,0.075)))
        elif index==30:
            temp.set_origin_transform(glm.translate((0.1,0,0.075)))
        elif index==12:
            temp.set_origin_transform(glm.translate((0.101,0,-0.145)))
        elif index==29:
            temp.set_origin_transform(glm.translate((-0.101,0,-0.145)))

    def f():
        for i in [2, 30, 12, 29]:
            obj_drone.children[i].set_org_local_transform(glm.rotate(globalvar.g_time*20, (0,1,0)))
        
    obj_drone.set_refresh_function(f)
        
    return obj_drone
    
def load_balloon(parent, balloon_vaos, windowing_transformation):
    shader_phong = load_shaders(g_vertex_phong_shader_src, g_fragment_phong_shader_src)
    obj_balloon = Node(parent, None, 0, 0, shader_phong, True)
    obj_balloon.set_static_transform(windowing_transformation)
    obj_balloon.set_origin_transform(glm.inverse(windowing_transformation))
     
    for (index,(vao, fn, object_name)) in enumerate(balloon_vaos):
        temp = Node(obj_balloon, vao, 0, fn, shader_phong, True)
        temp.set_color_properties([10, 10, 10], [1,1,1], [1, 0.3, 0.3], 50, True)

    return obj_balloon

class Scene:
    timer = 0
    def __init__(self, obj_base):
        #scene
        earth_vaos = obj_multi_parser(os.path.join(".","obj","earth.obj"), 'o')
        tucano_vaos = obj_multi_parser(os.path.join(".","obj","tucano.obj"), 'g')
        drone_vaos = obj_multi_parser(os.path.join(".","obj","drone.obj"), 'o')
        balloon_vaos = obj_multi_parser(os.path.join(".","obj","balloon.obj"), 'o') 

        (obj_earth) = load_earth(obj_base, earth_vaos, glm.scale((0.2, 0.2, 0.2)))
        self.obj_earth = obj_earth

        (obj_tucano1,obj_tucano1_prop,obj_tucano1_flapL,obj_tucano1_flapR, obj_tucano1_eleronL, obj_tucano1_eleronR) = load_tucano(obj_earth, tucano_vaos, glm.scale((0.3,0.3,0.3)))
        obj_tucano1.set_color_properties([10, 10, 10], [1,1,1], [0.7,0.7,1], 10, True)
        obj_tucano1_prop.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
        obj_tucano1_flapL.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
        obj_tucano1_flapR.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
        obj_tucano1_eleronL.set_color_properties([10,10,10], [1,1,1], [0.4, 0.4, 1], 10, True)
        obj_tucano1_eleronR.set_color_properties([10,10,10], [1,1,1], [0.4, 0.4, 1], 10, True)
        self.obj_tucano1 = obj_tucano1

        (obj_drone1) = load_drone(obj_tucano1, drone_vaos, glm.translate((4,0,-5))*glm.scale((10,10,10)))
        (obj_drone2) = load_drone(obj_tucano1, drone_vaos, glm.translate((-4,0,-5))*glm.scale((10,10,10)))
        obj_drone1.set_color_properties([10, 10, 10], [1,1,1], [0.4, 0.4, 1], 10, True)
        obj_drone2.set_color_properties([10, 10, 10], [1,1,1], [0.4, 0.4, 0.9], 10, True)
        self.obj_drone1 = obj_drone1
        self.obj_drone2 = obj_drone2

        (obj_tucano2,obj_tucano2_prop,obj_tucano2_flapL,obj_tucano2_flapR, obj_tucano2_eleronL, obj_tucano2_eleronR) = load_tucano(obj_earth, tucano_vaos, glm.scale((0.3,0.3,-0.3)))
        obj_tucano2.set_color_properties([10, 10, 10], [1,1,1], [1,0.7,0.7], 10, True)
        obj_tucano2_prop.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
        obj_tucano2_flapL.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
        obj_tucano2_flapR.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
        obj_tucano2_eleronL.set_color_properties([10,10,10], [1,1,1], [1, 0.4, 0.4], 10, True)
        obj_tucano2_eleronR.set_color_properties([10,10,10], [1,1,1], [1, 0.4, 0.4], 10, True)
        self.obj_tucano2 = obj_tucano2

        (obj_balloon) = load_balloon(obj_tucano2, balloon_vaos, glm.translate((0,2,-5))*glm.rotate(np.radians(90), (1,0,0))*glm.scale((10,-10,10)))
        self.obj_balloon = obj_balloon

        (obj_drone3) = load_drone(obj_tucano2, drone_vaos, glm.translate((0,3,0))*glm.scale((10,10,10)))
        obj_drone3.set_color_properties([10, 10, 10], [1,1,1], [1, 0.4, 0.6], 50, True)
        self.obj_drone3 = obj_drone3
    
    def render(self, VP):
        timer_multiplier = 1/((np.sin(globalvar.g_time)*10 + 11))
        self.timer += (0.02)*timer_multiplier
        self.obj_earth.set_local_transform(glm.rotate(globalvar.g_time*0.3, (0,1,0)))

        self.obj_tucano1.set_local_transform(glm.rotate(-(self.timer), (0, 1, 0))*glm.translate((8, 0, 0))*glm.rotate(np.sin(globalvar.g_time),(0,0,1)))
        self.obj_drone1.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time*3), ((0,0,1))))
        self.obj_drone2.set_org_local_transform(glm.rotate(-np.sin(globalvar.g_time*3), ((0,0,1))))
        self.obj_tucano2.set_local_transform(glm.rotate(np.radians(60), (0,1,0))*glm.rotate(-(globalvar.g_time*0.5), (1,0,0))*glm.translate((0, 6, 0)))
        self.obj_balloon.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time*10)*0.1, (1,0,0))*glm.rotate(globalvar.g_time*5, (0,1,0)))
        self.obj_drone3.set_org_local_transform(glm.translate((0,0,np.sin(globalvar.g_time)*0.3))*glm.rotate(np.sin(globalvar.g_time*1.3)*0.3, (1,0,0)))

        self.obj_earth.recursive_draw(GL_TRIANGLES, VP)
        self.obj_tucano1.recursive_draw(GL_TRIANGLES, VP)
        self.obj_tucano2.recursive_draw(GL_TRIANGLES, VP)
        self.obj_drone1.recursive_draw(GL_TRIANGLES, VP)
        self.obj_drone2.recursive_draw(GL_TRIANGLES, VP)
        self.obj_balloon.recursive_draw(GL_TRIANGLES, VP)
        self.obj_drone3.recursive_draw(GL_TRIANGLES, VP)





