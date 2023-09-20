class DisplayProcessor:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.window_width = 0
        self.window_height = 0
        self.count = 0
        self.points = []
        
    def set_window_width(self, window_width):
        self.window_width = window_width
    
    def get_window_width(self):
        return self.window_width
    
    def set_window_height(self, window_height):
        self.window_height = window_height
    
    def get_window_height(self):
        return self.window_height
    
    def make_circle_points(self, n = 3 ,m = 4):
        vertical_step_size = int(self.window_height/n)
        horizantal_step_size = int(self.window_width/m)
        for i in range (0,self.window_height,horizantal_step_size):
            for j in range (0,self.window_width,vertical_step_size):
                self.points.append((j,i))
              
    def get_possition(self):
        point = self.points[self.count]
        self.count = self.count + 1
        return point[0], point[1]

