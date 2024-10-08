import warnings
warnings.filterwarnings('ignore')
from ultralytics import RTDETR

if __name__ == '__main__':
    model = RTDETR('ultralytics/cfg/models/rt-detr/rtdetr-r18.yaml')
    model.load('D:\\workspace\\github\\RTDETR-main\\weights\\rtdetr-r18.pt') # loading pretrain weights
    model.train(data='dataset/data.yaml',
                cache=False,
                imgsz=640,
                epochs=100,
                batch=4,
                workers=4,
                
                # device='0',
                device='cpu', #本地调试使用cpu

                # resume='', # last.pt path
                project='runs/train',
                name='exp',
                )
