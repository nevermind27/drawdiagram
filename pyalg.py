from pyflowchart import Flowchart
from pyflowchart import *
import ast
from pycparser import c_parser,c_ast
#import pygraphviz as pgv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import matplotlib.path
from matplotlib.lines import Line2D

def make_flowchart(code,field,name):
    fc = Flowchart.from_code(code, field=field, inner=True, simplify=False, conds_align=True)
    output_html('output.html', 'py'+name, fc.flowchart())
    return (fc.flowchart())
def analyze_code(code_ast,last_node,direction):
    flag=0
    n=0
    for node in ast.iter_child_nodes(code_ast):
        if isinstance(node, ast.If):
            if node.parent==code_ast:
                cond = ConditionNode(ast.unparse(node.test))
                last_node.connect(cond)
                last_node=cond
                last_node = (analyze_code(node, cond, 'yes'))
                new_node=OperationNode('')
                last_node.connect(new_node,'bottom')
            flag=1
        elif isinstance(node, ast.For):
            flag = 1

            if node.parent == code_ast:
                # Create a node to check the loop condition
                loop_cond = OperationNode(ast.unparse(node.iter))
                last_node.connect(loop_cond, direction)

                # Create a ConditionNode for the loop condition
                #cond = ConditionNode(ast.unparse(node.target), loop_cond)
                last_node = cond
                #loop_cond.connect(cond, 'no')

                # Connect the loop condition to the loop body
                last_node = analyze_code(node, loop_cond, 'yes')
                last_node.connect(loop_cond)

        elif isinstance(node, ast.While):
            flag = 1

            if node.parent == code_ast:
                # Create a node to check the loop condition
                loop_cond = OperationNode(ast.unparse(node.test))
                last_node.connect(loop_cond, direction)

                # Create a ConditionNode for the loop condition
                cond = ConditionNode(ast.unparse(node.test), loop_cond)
                last_node = cond
                loop_cond.connect(cond, 'no')

                # Connect the loop condition to the loop body
                last_node = analyze_code(node, cond, 'yes')
                last_node.connect(cond)

        elif isinstance(node, ast.Assign) or isinstance(node, ast.AugAssign):
                flag=1
                if node.parent==code_ast: #and last_node.node_type==ConditionNode:
                    op = OperationNode(ast.unparse(node))
                    print('FORMAT OF NODE',ast.dump(node))
                    if n==0 and direction!='' :
                        last_node.connect(op,'yes')
                        n+=2 #придумать что-то другое вместо n, тк плохо для вложенности в иф
                    elif direction!='' and n!=0:
                        last_node.connect(op,'no')
                        n=0
                        last_node = op
                    else:
                        last_node.connect(op)
                        last_node=op
                if flag:
                    return last_node
def analyzecpp(code,name):
    parser = c_parser.CParser()
    ast = parser.parse(code)
    st = StartNode('trps')
    last_node = analyze_code(ast, st, '')
    end = EndNode('')
    end.connect(last_node)
    fc = Flowchart(st)
    output_html('output.html', 'cpp'+name, fc.flowchart())
def analyze_code_obj(code):
    fig, ax = plt.subplots()

    # Display the image
    im = Image.open('im.jpg')
    ax.imshow(im)
    analyze_object_code(code,classes,relations)
    draw_object(classes, relations, ax)
    plt.show()
    code_ast = ast.parse(code)

x0=250
y0=200
wide=120
length=80
def create_uml_diagram():
    ...
def draw(name, relation,cl):
    ...
class Class:
    def __init__(self,name):
        self.name=name
        #self.x=x
        #self.y=y
class Relation:
    def __init__(self,class1,class2,type):
        self.class1=class1 #который наследует, содержится в другом
        self.class2=class2 #который наследуется, cодержит что-то
        self.type=type
classes=[]
relations=[]

#print(ast.dump(code_ast.body[2].body[0])) # наследование проверять через bases empty?

def analyze_object_code(code_ast,classes,relations):
    code_ast= ast.parse(code_ast)
    for node in ast.iter_child_nodes(code_ast):
        print(ast.dump(node))
        if isinstance(node, ast.ClassDef):
            cl=Class(node.name)
            classes.append(cl)
            if node.bases:
                for base in node.bases:
                    relation=Relation(node.name,base,'inheritance')
                    relations.append(relation)
            print(ast.dump(node.body[0]))
            if isinstance(node.body[0],ast.FunctionDef) :
                if node.body[0].name == '__init__':
                    for func in ast.iter_child_nodes(node.body[0]):
                        count=0
                        for fun in ast.iter_child_nodes(func):
                            count+=1

                            if count%2==0:
                                f=ast.unparse(fun)
                                f=f[:-2]
                                if f in [o.name for o in classes]:

                                    relation= Relation(node.name,f,'composition')
                                    relations.append(relation)
    for node in ast.iter_child_nodes(code_ast):
        if isinstance(node, ast.ClassDef):
            if node.bases:
                for base in node.bases:
                    relation=Relation(node.name,base,'inheritance')
                    relations.append(relation)
        if isinstance(node.body[0], ast.FunctionDef) and node.body[0].name == '__init__':
            for func in ast.iter_child_nodes(node.body[0]):
                count = 0
                for fun in ast.iter_child_nodes(func):
                    count += 1

                    if count % 2 == 0:
                        f = ast.unparse(fun)
                        f = f[:-2]
                        if f in [o.name for o in classes]:
                            relation = Relation(node.name, f, 'composition')
                            relations.append(relation)

def draw_rect(x0,y0,name,ax):
    rect = patches.Rectangle((x0, y0), 120, 80, linewidth=1, edgecolor='black', facecolor='none')
    line = Line2D([x0, x0+120], [y0+20, y0+20], color="k")
    text = ax.text(x0+8,y0+13,name, wrap=True)

    ax._add_text(text)
    ax.set_xticks([])
    ax.set_yticks([])
    # Add the patch to the Axes
    ax.add_line(line)
    ax.add_patch(rect)

coords = [[250,200],[420,200],[20,200],[250,300],[250,200]]
def arrow(x,y,direction,ax):
    y+=40
    if direction=='right':
        line= Line2D([x-12,x ], [y,y-7], color="k")
        ax.add_line(line)
        line=Line2D([x-12,x ],[y,y+7] , color="k")
        ax.add_line(line)
    if direction=='left':
        line = Line2D([x, x+12], [ y,y-7], color="k")
        ax.add_line(line)
        line = Line2D([x, x+12],[y, y + 7] , color="k")
        ax.add_line(line)
def romb(x,y,direction,ax):
    shape = patches.Rectangle((x, y-3),
                      width=7,
                      height=7,
                      angle=45,
                      color="Black")
    ax.add_patch(shape)
def draw_object(classes, relations,ax):
    count=0
    for cl in classes:
        draw_rect(coords[count][0],coords[count][1],cl.name,ax)
        count+=1
    for r in relations:
        if type(r.class2)!=str:
            r.class2=ast.unparse(r.class2)
        if r.class1 in [o.name for o in classes] and r.class2 in [o.name for o in classes]:
            print('zashli')
            x1,y1=coords[[o.name for o in classes].index(r.class1)]
            x2,y2=coords[[o.name for o in classes].index(r.class2)]
            direction=''
            if x1!=x2 and y1==y2:
                if x2>x1:
                    x1=x1+120
                    line = Line2D([x1, x2], [y1 + 40, y1 + 40], color="k")
                    direction='right'
                if x1>x2:
                    x2+=120
                    line = Line2D([x2, x1], [y1+40, y1+40], color="k")
                    direction = 'left'
                ax.add_line(line)
            if x1==x2 and y1!=y2:
                if y2>y1:
                    y1=y1+120
                    direction = 'up'
                if y1>x2:
                    y2=y2+120
                    direction='down'
                line=Line2D([x1, x1], [y1, y2], color="k")
                ax.add_line(line)
            if x1!=x2 and y1!=y2:
                if y2>y1:
                    y1=y1+120
                if y1>y2:
                    y2=y2+120
                if x2>x1:
                    x1=x1+120
                if x1>x2:
                    x2+=120
                line = Line2D([x1, x2], [y1, y1], color="k")
                ax.add_line(line)
                line = Line2D([x1, x2], [y1, y1], color="k")
                ax.add_line(line)
                print(r.type)
            if r.type == 'inheritance':
                arrow(x2, y2, direction, ax)
            if r.type == 'composition':
                romb(x1, y1 + 40, direction, ax)
