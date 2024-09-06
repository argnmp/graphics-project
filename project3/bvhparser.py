import os
import re
import sys
import numpy as np

from vao import *
from shader import *
from draw import *
from objparser import *


    
def consumeline(f):
    line = []
    line = f.readline()
    if not line:
        return (line, -1)  
    line = re.split(r"\s+", line.strip().rstrip('\n'))
    while(len(line)==0):
        line = f.readline()
        line = re.split(r"\s+", line.strip().rstrip('\n'))
        if not line:
            return (line, -1)  
        
    return (line, 0)

def parse_df(cursor, line):
    df = int(line[1])
    dftype_map = []
    for i in range(2, len(line)):
        target = line[i].lower()
        if(target == "xposition"):
            dftype_map.append(1)        
        elif(target == "yposition"):
            dftype_map.append(2)        
        elif(target == "zposition"):
            dftype_map.append(3)        
        elif(target == "xrotation"):
            dftype_map.append(4)        
        elif(target == "yrotation"):
            dftype_map.append(5)        
        elif(target == "zrotation"):
            dftype_map.append(6)        
        cursor.configure_df(df, dftype_map)

class Of:
    def __init__(self, parent, part):
        self.parent = parent
        self.part = part
        self.offset = -1
    def set_offset(self, offset):
        self.offset = offset

def get_y_offset(f):
    parent = None
    cursor = None
    cur_depth = 0

    cur_y_offset = 0
    max_y_offset = -sys.maxsize
    min_y_offset = sys.maxsize
    
    while True:
        (line, flag) = consumeline(f)
        if(flag == -1): break

        if line[0] == 'HIERARCHY':
            continue
                
        elif line[0] == 'MOTION':
            f.seek(0)
            break

        if(flag == -1): break

        if(line[0]=="JOINT" or line[0]=="ROOT" or line[0]=="End"):
            # change parent and set cursor
            parent = cursor
            cursor = Of(parent, line[0])  

        elif(line[0]=="{"):
            # increase depth
            cur_depth += 1

            # configure offset
            (line, flag) = consumeline(f)
            cursor.set_offset(float(line[2]))

            if(cursor.part != "End"):
                # configure channels
                (line, flag) = consumeline(f)

            cur_y_offset += cursor.offset
            max_y_offset = max(max_y_offset, cur_y_offset)
            min_y_offset = min(min_y_offset, cur_y_offset)

        elif(line[0]=="}"):
            cur_y_offset -= cursor.offset
            cur_depth -= 1                

            if(cur_depth == 0):
                f.seek(0)
                break

            # restore parent
            cursor = parent
            parent = cursor.parent
        else:
            break
    
    f.seek(0)
    return (max_y_offset, min_y_offset)


def bvh_parser(path):
    cube_vertices = [
        [-1 ,  1 ,  1] , [-0.577 ,  0.577,  0.577],
        [ 1 ,  1 ,  1] , [ 0.816 ,  0.408,  0.408],
        [ 1 , -1 ,  1] , [ 0.408 , -0.408,  0.816],
        [-1 , -1 ,  1] , [-0.408 , -0.816,  0.408],
        [-1 ,  1 , -1] , [-0.408 ,  0.408, -0.816],
        [ 1 ,  1 , -1] , [ 0.408 ,  0.816, -0.408],
        [ 1 , -1 , -1] , [ 0.577 , -0.577, -0.577],
        [-1 , -1 , -1] , [-0.816 , -0.408, -0.408],
    ] 

    cube_indices = [
        [0,2,1],
        [0,3,2],
        [4,5,6],
        [4,6,7],
        [0,1,5],
        [0,5,4],
        [3,6,2],
        [3,7,6],
        [1,2,6],
        [1,6,5],
        [0,7,3],
        [0,4,7],
    ]
    
    # cube_vao = obj_parser("/Users/tyler/workspace/cse4020/project/project3/Project2-sample-objs/cube-tri.obj")
    (cube_vao, cube_fn) = prepare_vao_cube()
    shader_phong = load_shaders(g_vertex_phong_shader_src, g_fragment_phong_shader_src)



    root = None 

    parent = None
    cursor = None
    cur_depth = 0

    

    frames = 0
    frame_time = 0
    joint_count = 0
    joint_names = []
    
    
    parsing_seq = 0 
    
    with open(os.path.join(path), "r") as f:
        (max_y, min_y) = get_y_offset(f)
        if(max_y - min_y > 2):
            globalvar.g_bvh_offset_multiplier = 1.4 / (max_y - min_y)

        f.seek(0)
        while True:
            (line, flag) = consumeline(f)
            if(flag == -1): break

            if line[0] == 'HIERARCHY':
                parsing_seq = 0
                continue
                
            elif line[0] == 'MOTION':
                (line, flag) = consumeline(f)                 
                frames = int(line[1])
                (line, flag) = consumeline(f)                 
                frame_time = float(line[2])
                
                parsing_seq = 1
                continue

            if parsing_seq == 0:
                # HIERARCHY parsing mode
                if(flag == -1): break

                if(line[0]=="JOINT" or line[0]=="ROOT" or line[0]=="End"):
                    # change parent and set cursor
                    parent = cursor
                    cursor = CNode(parent, line[0], line[1])  
                    if line[0] != "End":
                        joint_count += 1
                        joint_names.append(line[1])

                    if(line[0]=="ROOT"):
                        root = cursor   

                elif(line[0]=="{"):
                     # increase depth
                     cur_depth += 1

                     # configure offset
                     (line, flag) = consumeline(f)
                     cursor.set_offset((float(line[1])*globalvar.g_bvh_offset_multiplier, float(line[2])*globalvar.g_bvh_offset_multiplier, float(line[3])*globalvar.g_bvh_offset_multiplier))
                     cursor.set_offset_transform(glm.translate(cursor.offset))
                     

                     if(cursor.part != "End"):
                        # configure channels
                        (line, flag) = consumeline(f)
                        parse_df(cursor, line)

                     if(cursor.part != "ROOT"):
                        # create line vao
                        face_idx = len(cursor.parent.vertices) / 2
                        cursor.parent.vertices.append([0,0,0]) 
                        cursor.parent.vertices.append([1,1,1]) 
                        cursor.parent.vertices.append(list(cursor.offset)) 
                        cursor.parent.vertices.append([1,1,1]) 
                        cursor.parent.faces.append([face_idx, face_idx+1]) 

                        # add link information
                        link = CNode(None, "link", "link")
                        link.parent = cursor.parent
                        link.vertices = cube_vertices
                        link.faces = cube_indices
                        link.configure_vao(cube_vao, 0, cube_fn)
                        link.configure_shader(shader_phong, True)
                        link.set_color_properties([10, 10, 10], [1,1,1], [0.4, 0.55, 1], 10, True)

                        mat = glm.mat4()
                        mat = glm.lookAt(cursor.offset, (0,0,0), (0,1,0))*glm.translate(glm.vec3(cursor.offset))
                        if(glm.any(glm.isnan(mat[0]))):
                            mat = glm.lookAt(cursor.offset, (0,0,0), (0,0,1))*glm.translate(glm.vec3(cursor.offset))
                             
                        dist = glm.distance((0,0,0), cursor.offset)/2
                        link.set_static_transform(glm.inverse(mat)*glm.scale((0.015, 0.015, dist))*glm.translate((0,0,1)))
                        
                        cursor.parent.link_nodes.append(link)

                elif(line[0]=="}"):
                    cur_depth -= 1                
                    if(cur_depth == 0): continue;
                    # restore parent
                    cursor = parent
                    parent = cursor.parent

                else:
                    print("wrong input!")
                 
            elif parsing_seq == 1:
                # MOTION parsing mode
                cur_idx = 0
                st = [root]
                while(len(st)!=0):
                    elem = st.pop() 
                    if(elem.is_df_configured): 
                        elem.append_df_params([float(line[i]) for i in range(cur_idx, cur_idx + elem.df)])
                        cur_idx += elem.df
                    for i in reversed(elem.children):
                        st.append(i)
            
    root.recursive_vao_update()
    root.set_color_properties([10, 10, 10], [1,1,1], [0.5, 0.8, 1], 10, True)

    return (root, frames, frame_time, joint_count, joint_names)
            
            
            
