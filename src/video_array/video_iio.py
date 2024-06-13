
import imageio.v3 as iio
import numpy as np


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.vo = iio.imopen(filename, 'r', plugin='pyav')

        self.fps = self.vo.metadata()['fps']
        self.shape = self.vo.properties().shape
        self.width = self.shape[2]
        self.height = self.shape[1]
        self.nframes = self.shape[0]
        self.total_seconds = self.nframes/self.fps
        if self.nframes < 1:
            self.nframes, self.total_seconds = self.calc_duration()
            self.shape = (self.nframes, self.height, self.width, 3)

        self.current_frame = self.nframes//2
        self.dtype = np.uint8
        self.size = self.width*self.height*self.nframes*3
        self.ndim = 4
        self.fps = self.vo.metadata()['fps']
    
    
    def calc_duration(self):
        duration = self.vo.metadata()['DURATION']
        if ':' in duration:
            sh, sm,  ss = duration.split(":")
            h = 3600*float(sh)
            m = 60*float(sm)
            s = float(ss)
            _total_seconds = h + m + s
            nframes = int(self.fps*_total_seconds)
            ## this might miss some frames at the end, but will be consistent
            total_seconds = nframes/self.fps
        else:
            h = 0
            m = 0
            total_seconds = float(duration)
            nframes = int()
        return nframes, total_seconds
     
    def get_random_frame(self):
        r = np.random.randint(0, self.nframes)
        return self.__getitem__(r)
        
    def __getitem__(self, idx):
        #print(idx)
        if isinstance(idx, tuple):
            idx = idx[0]
        if isinstance(idx, slice):
            res = self.getslice(idx)
            return res    
        else:    
            self.idx = int(idx)
            frame = self.vo.read(index=idx)
            
            #frame = frame[..., [2, 1, 0]] # BGR to RGB
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
            frame = self.vo.read(index=i)
            # frame = frame[..., [2, 1, 0]] # BGR to RGB
            xlist.append(frame)
            
        return np.stack(xlist)
    
    def close(self):
        self.vo.close()
