import os
import re
import numpy as np

from vao import *

def obj_parser(path):
    v = []
    vn = []
    faces = []
    total_faces_count = 0
    tri_faces_count = 0
    quad_faces_count = 0
    other_faces_count = 0
    vertices = []
    vertices_idx = 0
    vertices_dict = {}
    with open(os.path.join(path), "r") as f:
        for line in f:
            target = re.split(r"\s+",line.strip().rstrip('\n'))
            if(target[0]=='v'):
                v.append([float(i) for i in target[1:4]])
            elif(target[0]=='vn'):
                vn.append([float(i) for i in target[1:4]])
            elif(target[0]=='f'):
                if(len(target)==4):
                    tri_faces_count += 1
                    total_faces_count += 1
                elif(len(target)==5):
                    quad_faces_count += 1
                    total_faces_count += 1
                elif(len(target)>=6):
                    other_faces_count += 1
                    total_faces_count += 1
                else:
                    print("invalid obj file")
                    return
                # 1 and i and i+1 
                for i in range(2, len(target)-1):
                    args = []
                    args.append(target[1].split('/'))
                    args.append(target[i].split('/'))
                    args.append(target[i+1].split('/'))

                    face_normal = []
                    if(len(args[0])!=3 or len(args[1])!=3 or len(args[2])!=3):
                        a = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[1][0])-1])) 
                        b = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[2][0])-1])) 
                        c =  np.cross(a, b)
                        face_normal = c / np.linalg.norm(c)
                        vn.append(face_normal)

                    index = []
                    for arg in args:
                        a0 = int(arg[0])-1
                        a2 = 0
                        if len(arg)== 1 or len(arg) == 2:
                            a2 = len(vn)-1
                        else:
                            a2 = int(arg[2])-1

                        if (a0, a2) in vertices_dict:
                            index.append(vertices_dict[(a0, a2)])
                        else:
                            vertices.append(v[a0])
                            vertices.append(vn[a2])         
                            vertices_dict[(a0, a2)] = vertices_idx
                            index.append(vertices_idx)
                            vertices_idx += 1
                            
                    faces.append(index)

    vertices = np.array(vertices)
    faces = np.array(faces)

    VAO = vao_builder(vertices, faces)

    print('total number of faces: ', total_faces_count)
    print('number of faces with 3 vertices:', tri_faces_count)
    print('number of faces with 4 vertices:', quad_faces_count)
    print('number of faces with more than 4 vertices:', other_faces_count)
    return (VAO, len(faces))


def obj_multi_parser(path, delim):
    v = []
    vn = []
    faces = []
    tri_faces_count = 0
    quad_faces_count = 0
    other_faces_count = 0
    vertices = []
    vertices_idx = 0
    vertices_dict = {}
    object_name = ""
    results = []
    with open(os.path.join(path), "r") as f:
        for line in f:
            target = re.split(r"\s+",line.strip().rstrip('\n'))
            if(target[0]=='v'):
                v.append([float(i) for i in target[1:4]])
            elif(target[0]=='vn'):
                vn.append([float(i) for i in target[1:4]])
            elif(target[0]=='f'):
                if(len(target)==4):
                    tri_faces_count += 1
                elif(len(target)==5):
                    quad_faces_count += 1
                elif(len(target)>=6):
                    other_faces_count += 1
                else:
                    print("invalid obj file")
                    return
                # 1 and i and i+1 
                for i in range(2, len(target)-1):
                    args = []
                    args.append(target[1].split('/'))
                    args.append(target[i].split('/'))
                    args.append(target[i+1].split('/'))

                    face_normal = []
                    if(len(args[0])!=3 or len(args[1])!=3 or len(args[2])!=3):
                        a = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[1][0])-1])) 
                        b = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[2][0])-1])) 
                        c =  np.cross(a, b)
                        face_normal = c / np.linalg.norm(c)
                        vn.append(face_normal.tolist())

                    index = []
                    for arg in args:
                        a0 = int(arg[0])-1
                        a2 = 0
                        if len(arg)== 1 or len(arg) == 2:
                            a2 = len(vn)-1
                        else:
                            a2 = int(arg[2])-1

                        if (a0, a2) in vertices_dict:
                            index.append(vertices_dict[(a0, a2)])
                        else:
                            vertices.append(v[a0])
                            vertices.append(vn[a2])         
                            vertices_dict[(a0, a2)] = vertices_idx
                            index.append(vertices_idx)
                            vertices_idx += 1
                            
                    faces.append(index)

            elif(target[0]==delim):
                if(len(faces)==0):
                    object_name = target[1]
                    continue
                vao = vao_builder(np.array(vertices), np.array(faces)) 
                results.append((vao, len(faces), object_name))
                object_name = target[1]
                vertices = []
                faces = []
                vertices_dict = {}
                vertices_idx = 0

        vao = vao_builder(np.array(vertices), np.array(faces)) 
        results.append((vao, len(faces), object_name))
        vertices = []
        faces = []
        vertices_dict = {}
        vertices_idx = 0

    return results

# def obj_avgnorm_parser(path):
#     v = []
#     vn = []
#     vnavg = []
#     vnavg_num = []
#     vnset = []
#     
#     faces = []
#     tri_faces_count = 0
#     quad_faces_count = 0
#     other_faces_count = 0
#     with open(os.path.join(path), "r") as f:
#         for line in f:
#             target = re.split(r"\s+",line.strip().rstrip('\n'))
#             if(target[0]=='v'):
#                 v.append([float(i) for i in target[1:4]])
#                 vnavg.append([0,0,0])
#                 vnavg_num.append(0)
#                 vnset.append(set())
#             elif(target[0]=='vn'):
#                 vn.append([float(i) for i in target[1:4]])
#             elif(target[0]=='f'):
#                 if(len(target)==4):
#                     tri_faces_count += 1
#                 elif(len(target)==5):
#                     quad_faces_count += 1
#                 elif(len(target)>=6):
#                     other_faces_count += 1
#                 else:
#                     print("invalid obj file")
#                     return
#                 # 1 and i and i+1 
#                 for i in range(2, len(target)-1):
#                     args = []
#                     args.append(target[1].split('/'))
#                     args.append(target[i].split('/'))
#                     args.append(target[i+1].split('/'))
#
#                     face_normal = []
#                     if(len(args[0])!=3 or len(args[1])!=3 or len(args[2])!=3):
#                         a = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[1][0])-1])) 
#                         b = np.array(np.array(v[int(args[0][0])-1])-np.array(v[int(args[2][0])-1])) 
#                         c = np.cross(a, b)
#                         # face_normal = (c-np.min(c))/(np.max(c)-np.min(c))
#                         face_normal = c / np.linalg.norm(c)
#                         vn.append(face_normal.tolist())
#
#                     index = []
#                     for arg in args:
#                         if len(arg) == 1 or len(arg) == 2:
#                             a0 = int(arg[0])-1
#                             a2 = len(vn)-1
#                             index.append(a0)
#                             if not a2 in vnset[a0]:
#                                 vnavg[a0][0] += vn[a2][0]
#                                 vnavg[a0][1] += vn[a2][1]
#                                 vnavg[a0][2] += vn[a2][2]
#                                 vnavg_num[a0] += 1 
#                                 vnset[a0].add(a2)
#                         elif len(arg)==3:
#                             a0 = int(arg[0])-1 
#                             a2 = int(arg[2])-1
#                             index.append(a0) 
#                             if not a2 in vnset[a0]:
#                                 vnavg[a0][0] += vn[a2][0]
#                                 vnavg[a0][1] += vn[a2][1]
#                                 vnavg[a0][2] += vn[a2][2]
#                                 vnavg_num[a0] += 1 
#                                 vnset[a0].add(a2)
#                     faces.append(index)
#      
#     for i in range(len(vnavg)):
#         n = np.array(vnavg[i]) 
#         vnavg[i] = vnavg[i] / np.linalg.norm(n)
#
#     vertices = []
#     for i in range(len(v)):
#         vertices.append(v[i])
#         vertices.append(vnavg[i])
#     vertices = np.array(vertices)
#     faces = np.array(faces)
#     print(vertices)
#     print(faces)
#
#     VAO = vao_builder(vertices, faces)
#     return (VAO, len(faces))
