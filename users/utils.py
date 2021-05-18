from users.models import Flight
import matplotlib.pyplot as plt 
import base64
from io import BytesIO

import numpy as np

def get_graph():
    
    buffer = BytesIO()
    plt.savefig(buffer , format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph



def get_plot(x,y,b):
    x = np.array(x)
    y = np.array(y)
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.scatter(x, y, color = "m",marker = "o", s = 30)
    y_pred = b[0] + b[1]*x
    plt.plot(x, y_pred, color = "r")
    plt.title('Comparision')
    plt.tight_layout()
    graph = get_graph()
    return graph


def estimate_coef(x, y):
    x = np.array(x)
    y = np.array(y)
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
    
    return (b_0, b_1)


def get_plot1(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.scatter(x,y)
    plt.title('Comparision')
    plt.tight_layout()
    graph = get_graph()
    return graph


class Graph:
    
    def init(self, vertices):
        self.V = vertices   
        self.graph = []     

    
    def add_edge(self, s, d, w):
        self.graph.append([s, d, w])

    
    def print_solution(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

    def bellman_ford(self, src):

        
        dist = [float("Inf")] * self.V
        
        dist[src] = 0

        
        for _ in range(self.V - 1):
            for s, d, w in self.graph:
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w

        
        for s, d, w in self.graph:
            if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                print("Graph contains negative weight cycle")
                return

        
        self.print_solution(dist)


flight = Flight.objects.all()

flight = list(flight)



g = []
s = []
d = []
for i in flight:
    g.append(i.fareEconomy)

for i in flight:
    g.append(i.sourceLocation)


for i in flight:
    g.append(i.destinationLocation)

