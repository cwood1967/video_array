import cv2
import numpy as np


class Video:
    
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        self.nframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.shape = (self.nframes, self.height, self.width, 3)
        _ = self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.nframes//2) 
        self.current_frame = self.nframes//2
        self.dtype = np.uint8
        self.size = self.width*self.height*self.nframes*3
        self.ndim = 4
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
    
    
    def get_random_frame(self):
        r = np.random.randint(0, self.nframes)
        return self.__getitem__(r)
        
    def __getitem__(self, idx):
        print(idx)
        if isinstance(idx, tuple):
            idx = idx[0]
        if isinstance(idx, slice):
            res = self.getslice(idx)
            return res    
        else:    
            self.idx = int(idx)
            _ = self.cap.set(cv2.CAP_PROP_POS_FRAMES, float(idx)) 
            _, frame = self.cap.read()
            
            frame = frame[..., [2, 1, 0]] # BGR to RGB
            self.current_frame = frame
            return frame 
    
    def __len__(self):
        return self.nframes 

    def __array__(self, dtype=None):
        return self.current_frame 
    
    def getslice(self, idx):
        i0 = idx.start
        i1 = idx.stop
        step = idx.step
        if step is None:
            step = 1
            
        xlist = list()
        
        for i in range(i0, i1, step):
            _ = self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            _, frame = self.cap.read()
            frame = frame[..., [2, 1, 0]] # BGR to RGB
            xlist.append(frame)
            
        return np.stack(xlist)
            
            
