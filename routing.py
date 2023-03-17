#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : routing.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
#   FUNCTIONS :
#       PacketRouting.PacketRouting()
#       PacketRouting.edges_between_nodes()
#       PacketRouting.closest_nodes_to_endpoints()
#       PacketRouting.draw()
#       PacketRouting.dijskra_algorithm()
# 
#   NOTES :
#       - ...
# 
#   AUTHOR(S) : Noah Arcand Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
#
#   CHANGES :
#       - ...
# 
#   VERSION     DATE        WHO             DETAILS
#   0.0.1a      2022.11.26  Noah            Creation of project.
#   0.0.2a      2023.01.09  Noah            Basic simulation of LEO satellite constellation.
#   0.0.2b      2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
#   0.0.2c      2023.01.21  Noah/Ranul      Added distortion to LEO satellite orbit to better represent Mercator Projection.
#   0.1.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
#   0.1.1a      2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
#

from math import dist
import pygame

from constants import *


class PacketRouting:
    def __init__(self, LEO_node_positions, MEO_node_positions, endpoint_positions):
        self.LEO_node_positions = LEO_node_positions
        self.LEO_MAX_REACHABILITY = 100

        self.MEO_node_positions = MEO_node_positions
        self.MEO_MAX_REACHABILITY = 250

        self.endpoint_positions = endpoint_positions
    

    def edges_between_LEO_nodes(self):
        self.LEO_edges = {}
        # Loop through all nodes
        for i in range(len(self.LEO_node_positions)):
            for j in range(len(self.LEO_node_positions)):
                if self.LEO_node_positions[i] != self.LEO_node_positions[j]:
                    distance_between_nodes = dist(self.LEO_node_positions[i], self.LEO_node_positions[j])
                    if distance_between_nodes <= self.LEO_MAX_REACHABILITY:
                        if (self.LEO_node_positions[j], self.LEO_node_positions[i]) not in self.LEO_edges:
                            self.LEO_edges[(self.LEO_node_positions[i], self.LEO_node_positions[j])] = distance_between_nodes
        # Return node edge dict
        return self.LEO_edges


    def edges_between_MEO_nodes(self):
        self.MEO_edges = {}
        # Loop through all nodes
        for i in range(len(self.MEO_node_positions)):
            for j in range(len(self.MEO_node_positions)):
                if self.MEO_node_positions[i] != self.MEO_node_positions[j]:
                    distance_between_nodes = dist(self.MEO_node_positions[i], self.MEO_node_positions[j])
                    if distance_between_nodes <= self.MEO_MAX_REACHABILITY:
                        if (self.MEO_node_positions[j], self.MEO_node_positions[i]) not in self.MEO_edges:
                            self.MEO_edges[(self.MEO_node_positions[i], self.MEO_node_positions[j])] = distance_between_nodes
        # Return node edge dict
        return self.MEO_edges


    def closest_LEO_nodes_to_endpoints(self):
        self.LEO_endpoints_link = [] # Initialize coordinate pair list
        for endpoint in self.endpoint_positions:    # Find nearest node for each endpoint
            min_dist = float("inf") # Create initial float variable with infinity value
            
            for node in self.LEO_node_positions:    # Loop through each node to find nearest to endpoint
                distance_to_endpoint = dist(endpoint, node) # Get distance between node and endpoint
                
                if distance_to_endpoint < min_dist: # If distance is smaller than current nearest node,
                    min_dist = distance_to_endpoint # Set it as the new nearest node
                    endpoint_node = node    # Save node position
            
            self.LEO_endpoints_link.append((endpoint_node, endpoint))    # Add node and endpoint positions to list
        # Return nearest nodes for each endpoints
        return self.LEO_endpoints_link
    

    def closest_MEO_nodes_to_endpoints(self):
        self.MEO_endpoints_link = [] # Initialize coordinate pair list
        for endpoint in self.endpoint_positions:    # Find nearest node for each endpoint
            min_dist = float("inf") # Create initial float variable with infinity value
            
            for node in self.MEO_node_positions:    # Loop through each node to find nearest to endpoint
                distance_to_endpoint = dist(endpoint, node) # Get distance between node and endpoint
                
                if distance_to_endpoint < min_dist: # If distance is smaller than current nearest node,
                    min_dist = distance_to_endpoint # Set it as the new nearest node
                    endpoint_node = node    # Save node position
            
            self.MEO_endpoints_link.append((endpoint_node, endpoint))    # Add node and endpoint positions to list
        # Return nearest nodes for each endpoints
        return self.MEO_endpoints_link


    def draw(self, screen, colour, points):
        pygame.draw.lines(screen, colour, False, points, 3)


    def LEO_dijskra_algorithm(self):
        # Add source node and destionation node
        self.closest_LEO_nodes_to_endpoints()
        src_node = self.LEO_endpoints_link[0][0]
        dst_node = self.LEO_endpoints_link[-1][0]
    
        # Create an adjancency graph for the edges of each node
        self.edges_between_LEO_nodes()
        adjancent_nodes = {v: {} for v in self.LEO_node_positions}
        for (u, v), w_uv in self.LEO_edges.items():
            adjancent_nodes[u][v] = w_uv
            adjancent_nodes[v][u] = w_uv

        node_path = []          # Initialize path
        shortest_distance = {}  # Temporary shortest distance node to node
        parent_node = {}        # Keep track of previous nodes traversed

        # Initialize all nodes with shortest distance of infinity, except for the source node, which is 0
        for node in adjancent_nodes:
            shortest_distance[node] = float("inf")
        shortest_distance[src_node] = 0
        
        # Go through each adjacent node, one by one
        while adjancent_nodes:
            minimum_distance_node = None
            for node in adjancent_nodes:
                if minimum_distance_node is None:
                    minimum_distance_node = node
                elif shortest_distance[node] < shortest_distance[minimum_distance_node]:
                    minimum_distance_node = node

            for child_node, distance in adjancent_nodes[minimum_distance_node].items():
                if distance + shortest_distance[minimum_distance_node] < shortest_distance[child_node]:
                    shortest_distance[child_node] = distance + shortest_distance[minimum_distance_node]
                    parent_node[child_node] = minimum_distance_node
            adjancent_nodes.pop(minimum_distance_node)
        
        current_node = dst_node

        while current_node != src_node:
            try:
                node_path.insert(0, current_node)
                current_node = parent_node[current_node]
            except KeyError:
                print("path is not reachable")
                break
        
        node_path.insert(0, src_node)

        #return shortest_distance[dst_node]  # Return shortest distance value
        return node_path    # Return node path of shortest distance
    

    def MEO_dijskra_algorithm(self):
        # Add source node and destionation node
        self.closest_MEO_nodes_to_endpoints()
        src_node = self.MEO_endpoints_link[0][0]
        dst_node = self.MEO_endpoints_link[-1][0]
    
        # Create an adjancency graph for the edges of each node
        self.edges_between_MEO_nodes()
        adjancent_nodes = {v: {} for v in self.MEO_node_positions}
        for (u, v), w_uv in self.MEO_edges.items():
            adjancent_nodes[u][v] = w_uv
            adjancent_nodes[v][u] = w_uv

        node_path = []          # Initialize path
        shortest_distance = {}  # Temporary shortest distance node to node
        parent_node = {}        # Keep track of previous nodes traversed

        # Initialize all nodes with shortest distance of infinity, except for the source node, which is 0
        for node in adjancent_nodes:
            shortest_distance[node] = float("inf")
        shortest_distance[src_node] = 0
        
        # Go through each adjacent node, one by one
        while adjancent_nodes:
            minimum_distance_node = None
            for node in adjancent_nodes:
                if minimum_distance_node is None:
                    minimum_distance_node = node
                elif shortest_distance[node] < shortest_distance[minimum_distance_node]:
                    minimum_distance_node = node

            for child_node, distance in adjancent_nodes[minimum_distance_node].items():
                if distance + shortest_distance[minimum_distance_node] < shortest_distance[child_node]:
                    shortest_distance[child_node] = distance + shortest_distance[minimum_distance_node]
                    parent_node[child_node] = minimum_distance_node
            adjancent_nodes.pop(minimum_distance_node)
        
        current_node = dst_node

        while current_node != src_node:
            try:
                node_path.insert(0, current_node)
                current_node = parent_node[current_node]
            except KeyError:
                print("path is not reachable")
                break
        
        node_path.insert(0, src_node)

        #return shortest_distance[dst_node]  # Return shortest distance value
        return node_path    # Return node path of shortest distance