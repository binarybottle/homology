#!/usr/bin/python

# Author: Dmitriy Morozov <morozov@cs.duke.edu>
# (2004-2008) Department of Computer Science, Duke University

import pyx, string, sys, math

class PersistenceDiagram:
    def drawAxes(self,c,radius,spacing = 1, dimensions = None):
        if not dimensions:
            xmax = math.ceil(max(self.xmax,1) + radius + 1)
            xmin = math.floor(min(self.xmin,-1) - radius - 1)
            ymax = math.ceil(max(self.ymax,1) + radius + 1)
            ymin = math.floor(min(self.ymin,-1) - radius - 1)
        else:
            xmin,ymin,xmax,ymax = dimensions
        
        minmax = min([xmax, ymax])
        maxmin = max([xmin, ymin])
        for i in xrange(int(math.floor(xmin)),int(math.ceil(xmax)), spacing):
            c.stroke(pyx.path.line(i,ymin,i,ymax), [pyx.style.linestyle.dashed, pyx.color.gray(0.5)])
        for j in xrange(int(math.floor(ymin)),int(math.ceil(ymax)), spacing):
            c.stroke(pyx.path.line(xmin,j,xmax,j), [pyx.style.linestyle.dashed, pyx.color.gray(0.5)])
        c.stroke(pyx.path.line(xmin,0,xmax,0), [pyx.deco.earrow.normal])
        c.stroke(pyx.path.line(0,ymin,0,ymax), [pyx.deco.earrow.normal])
        c.stroke(pyx.path.line(maxmin,maxmin,minmax,minmax))


    def drawCanvas(self, c, points, color = 'red', filled = 1, radius = 0.15):
        for p in points:
            self.drawPoint(c,p,color,filled,radius)

    def drawPoint(self,c,p, color = 'red', filled = 1, radius = 0.15):
        if color == 'red':
            options = [pyx.color.rgb.red]
        elif color == 'blue':
            options = [pyx.color.rgb.blue]
        elif color == 'green':
            options = [pyx.color.rgb.green]
        else:
            options = []

        if filled:
            draw = c.fill
        else:
            draw = c.stroke

        xmax = max(self.xmax,1)
        xmin = min(self.xmin,-1)
        ymax = max(self.ymax,1)
        ymin = min(self.ymin,-1)

        x,y = p
        if abs(x) == float('inf') or abs(y) == float('inf'): radius = radius * 2
        if x == float('inf'): x = xmax + 1
        if x == float('-inf'): x = xmin - 1
        if y == float('inf'): y = ymax + 1
        if y == float('-inf'): y = ymin -1

        draw(pyx.path.circle(x,y,radius), options)

    def savePDF(self, filename, color = 'red', filled = 1, radius = 0.15, axes = 1, dimensions = None):
        for d in self.points.keys():
            c = pyx.canvas.canvas()
            self.drawAxes(c, radius, axes, dimensions)
            self.drawCanvas(c, self.points[d], color, filled, radius)
            c.writePDFfile(filename + str(d))
    
    def add(self, d, p, filter):
        x,y = p
        p = filter(x,y)
        if not p: return
        x,y = p

        if d not in self.points.keys():
            self.points[d] = []
        self.points[d] += [(x,y)]

        if abs(x) != float('inf'):
            self.xmax = max(x,self.xmax)
            self.xmin = min(x,self.xmin)
        if abs(y) != float('inf'):
            self.ymax = max(y,self.ymax)
            self.ymin = min(y,self.ymin)
    
    def load(self,filename, filter):
        self.xmax = self.ymax = 0
        self.xmin = self.ymin = 0
        f = file(filename, 'r')
        for line in f:
            if line.strip().startswith('#'): continue
            dim,xstr,ystr = string.split(line)
            self.add(dim, (float(xstr),float(ystr)), filter)
    
    def __init__(self, filename, filter = lambda x,y: (x,y)):
        self.points = {}
        self.load(filename, filter)


def noise_filter(epsilon):
    def noise(x,y):
        if y - x <= epsilon: return None
        return (x,y)

    return noise

def amplify_filter(x_mult, y_mult = None):
    if not y_mult: y_mult = x_mult

    def amplify(x,y):
        return (x_mult*x, y_mult*y)

    return amplify
