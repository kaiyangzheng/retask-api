from ..models import CustomUser 
from collections import deque

class UserGraph:
    def __init__(self, user_id):
        self.user = CustomUser.objects.get(id=user_id)
    
    def generate_graph(self):
        users = CustomUser.objects.all()
        graph = {}
        for user in users:
            graph[str(user)] = []
            for friend in user.friends.all():
                graph[str(user)].append(str(friend))
        return graph

    # basic breadth first search
    def search(self, name):
        search_queue = deque()
        search_queue += self.user.friends.all()
        searched = [self.user]
        while search_queue:
            user = search_queue.popleft()
            if not user in searched:
                if user.username == name:
                    return user, searched
                else:
                    search_queue += user.friends.all()
                    searched.append(user)
        return None

    # breadth first search that persists the search path
    # uses a queue of paths
    def bfs(self, name):
        # create graph
        graph = self.generate_graph()
        # queue of users to search
        queue = []
        searched = []
        # add first path with only root user
        queue.append([self.user])
        while queue:
            # get first path in queue
            path = queue.pop(0)
            # get last user in path
            user = path[-1]
            if user not in searched:
                # if the last user is the name we are looking for, return the path
                if user.username == name:
                    depth = len(path) - 1
                    return user, depth, path
                # add new paths to the queue - each new path is a copy of the old path + 1 of the user's friends
                # so if the old path is [a, b, c], the new paths are [a, b, c, d], [a, b, c, e], [a, b, c, f]
                for friend in graph[str(user)]:
                    new_path = list(path)
                    new_path.append(CustomUser.objects.get(username=friend))
                    queue.append(new_path)
                searched.append(user)
        return None

    # breadth first search that persists the search path
    # uses a parent dictionary and backtracking to find the path
    def bfs_backtracking(self, name):

        def backtrace(parent, start, end):
            # add first path to path array with only root user
            path = [end]
            # keeps appending parents to the path until the root user is reached
            while path[-1] != start:
                path.append(parent[path[-1]])
            # reverses to get right
            path.reverse()
            for i, node in enumerate(path):
                user = CustomUser.objects.get(username=node)
                path[i] = user
            return path

        # base search is the same as basic bfs without persisting the search path
        # however, we keep track of each node's parent using the parent dictionary
        graph = self.generate_graph()
        parent = {}
        queue = []
        # add first user to queue
        queue.append(str(self.user))
        while queue: 
            # pop first user from queue
            node = queue.pop(0)
            user = CustomUser.objects.get(username=node)
            # if the user is the name we are looking for, return the path
            if user.username == name:
                path = backtrace(parent, str(self.user), node)
                depth = len(path) - 1
                return user, depth, path
            # itereate through friends of user
            for friend in graph[str(node)]:
                # add friend to queue if not already in queue to be searched
                if friend not in queue: 
                    # set the current user to be the parent of the friend
                    parent[str(friend)] = node 
                    queue.append(friend)


    # bfs that returns all the users within a certain depth
    def bfs_depth(self, depth):
        graph = self.generate_graph()
        queue = []
        searched = []
        queue.append([self.user])
        while queue: 
            path = queue.pop(0)
            user = path[-1]
            if user not in searched:
                for friend in graph[str(user)]:
                    new_path = list(path)
                    new_path.append(CustomUser.objects.get(username=friend))
                    queue.append(new_path)
                searched.append(user)
                if len(path) - 1 == depth: 
                    return searched 
        return None

    # TODO: implement bfs that returns x closest users with a certain property


                



