class Stereo:
    '''
    A class for extracting the 3d location of objects using their 2d locations in images.
    '''
    def __init__(self, b:int, f:int, disparity_shift = 0):
        '''
        Args:
            b (int): the distance between the center of the cameras in any unit
            f (float): focal point of the cameras
            disparity_shift (int): shift in the disparity caused by camera calibraion. must be derived from the setup. default is 0.
        '''
        self.b = b
        self.f = f
        self.disparity_shift = disparity_shift
    
    def locate(self, p1:tuple, p2:tuple)->tuple:
        self.disparity = abs(p1[0] - p2[0] + self.disparity_shift) # d = X1 - X2 + Ds
        self.z = (self.b * self.f) / self.disparity # Z = f * B / d
        self.x = p1[0] * self.z / self.f # X = X1 * Z / f
        self.y = (p1[1] + p2[1]) * self.z / self.f
        return (self.x, self.y, self.z)