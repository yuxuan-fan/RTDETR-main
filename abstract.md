# 基于[ultralytics](https://github.com/ultralytics/ultralytics)的RT-DETR

    ------- From 哔哩哔哩 魔鬼面具UP -------
    本项目使用的ultralytics版本为8.0.201,在ultralytics/__init__.py中的__version__有标识.

    其中为了尽量对齐与官方PaddlePaddle-(RT-DETR)中的训练策略,主要对源码作了以下修改:
    1. 在ultralytics/engine/trainer.py中的optimizer_step函数中的torch.nn.utils.clip_grad_norm_中的参数max_norm修改为0.1
    2. 在ultralytics/engine/trainer.py中的_setup_train函数中将self.args.nbs等于self.batch_size,这样做的目的是让模型不需要积累梯度再进行更新参数
    3. ultralytics/cfg/default.yaml配置文件的更改<详细请看使用教程视频>
    
    注意:
    1. 如对以上修改觉得不对的地方,需要提供具体不对的地方和对应官方paddlepaddle或者pytorch版本实现的地方私聊我
    2. 以上修改只是为了<尽量>对齐官方PaddlePaddle的设置,不代表完全对齐,因为官方的设置不代表一定在其他数据集精度高,所以这里只修改了最影响精度部分的设置
    3. 本项目使用方法跟官方一致,具体可参考(https://docs.ultralytics.com/models/rtdetr/)
    4. 此项目只用于训练RT-DETR和DETR头的结构(YOLOV5-DETR,YOLOV8-DETR),如需要训练原版yolov5,v8模型请移步到官方代码中使用.

    我的实验环境:
    python: 3.8.16
    torch: 1.13.1+cu117
    torchvision: 0.14.1+cu117
    timm: 0.9.8
    mmcv: 2.1.0
    mmengine: 0.9.0

# RT-DETR环境配置

    1. 执行pip uninstall ultralytics把安装在环境里面的ultralytics库卸载干净.<这里需要注意,如果你也在使用yolov8,最好使用anaconda创建一个虚拟环境供本代码使用,避免环境冲突导致一些奇怪的问题>
    2. 卸载完成后同样再执行一次,如果出现WARNING: Skipping ultralytics as it is not installed.证明已经卸载干净.
    3. 如果需要使用官方的CLI运行方式,需要把ultralytics库安装一下,执行命令:<python setup.py develop>,当然安装后对本代码进行修改依然有效.(develop作用解释具体可看: https://blog.csdn.net/qq_16568205/article/details/110433714)  注意:不需要使用官方的CLI运行方式,可以选择跳过这步
    4. 额外需要的包安装命令:
        pip install timm==0.9.8 thop efficientnet_pytorch==0.7.1 einops grad-cam==1.4.8 dill==0.3.6 albumentations==1.3.1 pytorch_wavelets==1.3.0 tidecv PyWavelets -i https://pypi.tuna.tsinghua.edu.cn/simple
        以下主要是使用dyhead必定需要安装的包,如果安装不成功dyhead没办法正常使用!
        pip install -U openmim
        mim install mmengine
        mim install "mmcv>=2.0.0"
    5. 运行时候如果还缺什么包就请自行安装即可.

    AutoDL环境推荐教程:https://www.bilibili.com/video/BV1tT4y1b75q/

    需要编译才能运行的一些模块:
        1. mamba(百度云视频-20240219更新说明)
        2. dcnv3(百度云视频-20231119更新说明)
        3. dcnv4(百度云视频-20240120更新说明)
        4. smpconv(百度云视频-20240608更新说明)
        5. mamba-yolo(百度云视频-20240622更新说明)
    
    本目录下的test_env.py文件为了验证一些需要编译的或者难安装的(mmcv)是否成功的代码.详细请看以下这期视频:https://pan.baidu.com/s/1sWwvN4UC3blBRVe1twrJAg?pwd=bru5

# RT-DETR预训练权重下载

    请看weights/weight_download.txt已提供好百度云链接.

# 自带的一些文件说明
1. train.py
    训练模型的脚本
2. main_profile.py
    输出模型和模型每一层的参数,计算量的脚本(rtdetr-l和rtdetr-x因为thop库的问题,没办法正常输出每一层的参数和计算量和时间)
3. val.py
    使用训练好的模型计算指标的脚本
4. detect.py
    推理的脚本
5. track.py
    跟踪推理的脚本
6. heatmap.py
    生成热力图的脚本
7. get_FPS.py
    计算模型储存大小、模型推理时间、FPS的脚本
8. get_COCO_metrice.py
    计算COCO指标的脚本
9. plot_result.py
    绘制曲线对比图的脚本
10. get_model_erf.py
    绘制模型的有效感受野.[视频链接](https://www.bilibili.com/video/BV1Gx4y1v7ZZ/)
11. export.py
    导出模型脚本

# RT-DETR基准模型

1. ultralytics/cfg/models/rt-detr/rtdetr-r18.yaml(有预训练权重COCO+Objects365,来自RTDETR-Pytorch版本的移植)

    rtdetr-r18 summary: 421 layers, 20184464 parameters, 20184464 gradients, 58.6 GFLOPs
2. ultralytics/cfg/models/rt-detr/rtdetr-r34.yaml(有预训练权重COCO,来自RTDETR-Pytorch版本的移植)

    rtdetr-r34 summary: 525 layers, 31441668 parameters, 31441668 gradients, 90.6 GFLOPs
3. ultralytics/cfg/models/rt-detr/rtdetr-r50-m.yaml(有预训练权重COCO,来自RTDETR-Pytorch版本的移植)

    rtdetr-r50-m summary: 637 layers, 36647020 parameters, 36647020 gradients, 98.3 GFLOPs
4. ultralytics/cfg/models/rt-detr/rtdetr-r50.yaml(有预训练权重COCO+Objects365,来自RTDETR-Pytorch版本的移植)

    rtdetr-r50 summary: 629 layers, 42944620 parameters, 42944620 gradients, 134.8 GFLOPs
5. ultralytics/cfg/models/rt-detr/rtdetr-r101.yaml

    rtdetr-r101 summary: 867 layers, 76661740 parameters, 76661740 gradients, 257.7 GFLOPs
6. ultralytics/cfg/models/rt-detr/rtdetr-l.yaml(有预训练权重)

    rtdetr-l summary: 673 layers, 32970732 parameters, 32970732 gradients, 108.3 GFLOPs
7. ultralytics/cfg/models/rt-detr/rtdetr-x.yaml(有预训练权重)

    rtdetr-x summary: 867 layers, 67468108 parameters, 67468108 gradients, 232.7 GFLOPs
# RT-DETR改进方案

#### 目前整合的一些注意力机制 还需要别的注意力机制可从[github](https://github.com/z1069614715/objectdetection_script/tree/master/cv-attention)拉取对应的代码到ultralytics/nn/extra_modules/attention.py即可. 视频教程可看项目视频中的(如何在yaml配置文件中添加注意力层)
EMA, SimAM, SpatialGroupEnhance, BiLevelRoutingAttention, BiLevelRoutingAttention_nchw, TripletAttention, CoordAtt, CBAM, BAMBlock, EfficientAttention(CloFormer中的注意力), LSKBlock, SEAttention, CPCA, deformable_LKA, EffectiveSEModule, LSKA, SegNext_Attention, DAttention(Vision Transformer with Deformable Attention CVPR2022), FocusedLinearAttention(ICCV2023), MLCA, ELA, CAA, EfficientAdditiveAttnetion, AFGCAttention(Neural Networks ECCV2024)

### 以RT-DETR-R18为基准模型的改进方案
1. ultralytics/cfg/models/rt-detr/rt-detr-timm.yaml

    使用[timm](https://github.com/huggingface/pytorch-image-models)库系列的主干替换rtdetr的backbone.(基本支持现有CNN模型)timm的内容可看[这期视频](https://www.bilibili.com/video/BV1Mx4y1A7jy/)
2. ultralytics/cfg/models/rt-detr/rt-detr-fasternet.yaml

    使用[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)替换rtdetr的backbone.
3. ultralytics/cfg/models/rt-detr/rt-detr-EfficientViT.yaml

    使用[EfficientViT CVPR2023](https://github.com/microsoft/Cream/tree/main/EfficientViT)替换rtdetr的backbone.
4. ultralytics/cfg/models/rt-detr/rtdetr-convnextv2.yaml

    使用[ConvNextV2 2023](https://github.com/facebookresearch/ConvNeXt-V2)替换rtdetr的backbone.
5. ultralytics/cfg/models/rt-detr/rtdetr-EfficientFormerv2.yaml

    使用[EfficientFormerv2 2022](https://github.com/snap-research/EfficientFormer)替换rtdetr的backbone.
6. ultralytics/cfg/models/rt-detr/rtdetr-repvit.yaml

    使用[RepViT ICCV2023](https://github.com/THU-MIG/RepViT)替换rtdetr的backbone.
7. ultralytics/cfg/models/rt-detr/rtdetr-CSwomTramsformer.yaml

    使用[CSwinTramsformer CVPR2022](https://github.com/microsoft/CSWin-Transformer)替换rtdetr的backbone.
8. ultralytics/cfg/models/rt-detr/rtdetr-VanillaNet.yaml

    使用[VanillaNet 2023](https://github.com/huawei-noah/VanillaNet)替换rtdetr的backbone.
9. ultralytics/cfg/models/rt-detr/rtdetr-SwinTransformer.yaml

    使用[SwinTransformer ICCV2021](https://github.com/microsoft/Swin-Transformer)替换rtdetr的backbone.
10. ultralytics/cfg/models/rt-detr/rtdetr-lsknet.yaml

    使用[LSKNet ICCV2023](https://github.com/zcablii/LSKNet)替换rtdetr的backbone.

11. ultralytics/cfg/models/rt-detr/rtdetr-CascadedGroupAttention.yaml

    使用[EfficientViT CVPR2023](https://github.com/microsoft/Cream/tree/main/EfficientViT)中的CascadedGroupAttention改进rtdetr中的AIFI.(详细请看百度云视频-rtdetr-CascadedGroupAttention说明)

12. ultralytics/cfg/models/rt-detr/rtdetr-DWRC3.yaml

    使用[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)模块构建DWRC3改进rtdetr.
    百度云视频：20231109更新说明

13. ultralytics/cfg/models/rt-detr/rtdetr-AIFI-LPE.yaml

    使用LearnedPositionalEncoding改进AIFI中的位置编码生成.(详细介绍请看百度云视频-20231119更新说明)

14. ultralytics/cfg/models/rt-detr/rtdetr-Ortho.yaml

    使用[OrthoNets](https://github.com/hady1011/OrthoNets/tree/main)中的正交通道注意力改进resnet18-backbone中的BasicBlock.(详细介绍请看百度云视频-20231119更新说明)

15. ultralytics/cfg/models/rt-detr/rtdetr-DCNV2.yaml

    使用可变形卷积DCNV2改进resnet18-backbone中的BasicBlock.
    百度云视频：20231119更新说明

16. ultralytics/cfg/models/rt-detr/rtdetr-DCNV3.yaml

    使用可变形卷积[DCNV3 CVPR2023](https://github.com/OpenGVLab/InternImage)改进resnet18-backbone中的BasicBlock.(安装教程请看百度云视频-20231119更新说明)

17. ultralytics/cfg/models/rt-detr/rtdetr-DCNV2-Dynamic.yaml

    使用自研可变形卷积DCNV2-Dynamic改进resnet18-backbone中的BasicBlock.(详细介绍请看百度云视频-MPCA与DCNV2_Dynamic的说明)

18. ultralytics/cfg/models/rt-detr/rtdetr-iRMB.yaml

    使用[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB改进resnet18-backbone中的BasicBlock.(详细介绍请看百度云视频-20231119更新说明)

19. ultralytics/cfg/models/rt-detr/rtdetr-iRMB-Cascaded.yaml

    使用[EfficientViT CVPR2023](https://github.com/microsoft/Cream/tree/main/EfficientViT)中的CascadedGroupAttention对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet18-backbone中的BasicBlock.(详细介绍请看百度云视频-20231119更新说明)

20. ultralytics/cfg/models/rt-detr/rtdetr-attention.yaml

    添加注意力模块到resnet18-backbone中的BasicBlock中.(手把手教程请看百度云视频-手把手添加注意力教程)

21. ultralytics/cfg/models/rt-detr/rtdetr-p2.yaml

    添加小目标检测头P2到TransformerDecoderHead中.
    百度云视频：20231126更新说明

22. ultralytics/cfg/models/rt-detr/rtdetr-DySnake.yaml

    添加[DySnakeConv](https://github.com/YaoleiQi/DSCNet)到resnet18-backbone中的BasicBlock中.
    百度云视频：20231126更新说明

23. ultralytics/cfg/models/rt-detr/rtdetr-PConv.yaml

    使用[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的PConv改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

24. ultralytics/cfg/models/rt-detr/rtdetr-PConv-Rep.yaml

    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的PConv进行二次创新后改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

25. ultralytics/cfg/models/rt-detr/rtdetr-Faster.yaml

    使用[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

26. ultralytics/cfg/models/rt-detr/rtdetr-Faster-Rep.yaml

    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

27. ultralytics/cfg/models/rt-detr/rtdetr-Faster-EMA.yaml

    使用[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

28. ultralytics/cfg/models/rt-detr/rtdetr-Faster-Rep-EMA.yaml
    
    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv和[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet18-backbone中的BasicBlock.
    百度云视频：20231126更新说明

29. ultralytics/cfg/models/rt-detr/rtdetr-AKConv.yaml

    使用[AKConv 2023](https://github.com/CV-ZhangXin/AKConv)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231202更新说明

30. ultralytics/cfg/models/rt-detr/rtdetr-RFAConv.yaml

    使用[RFAConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231202更新说明

31. ultralytics/cfg/models/rt-detr/rtdetr-RFCAConv.yaml

    使用[RFCAConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231202更新说明

32. ultralytics/cfg/models/rt-detr/rtdetr-RFCBAMConv.yaml

    使用[RFCBAMConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231202更新说明

33. ultralytics/cfg/models/rt-detr/rt-detr-unireplknet.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)替换rtdetr的backbone.
    百度云视频：20231202更新说明

34. ultralytics/cfg/models/rt-detr/rtdetr-AIFI-DAttention.yaml

    使用[Vision Transformer with Deformable Attention CVPR2022](https://github.com/LeapLabTHU/DAT)中的DAttention改进AIFI.
    百度云视频：20231202更新说明

35. ultralytics/cfg/models/rt-detr/rtdetr-Conv3XC.yaml

    使用[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC改进resnet18-backbone中的BasicBlock.
    百度云视频：20231210更新说明

36. ultralytics/cfg/models/rt-detr/rtdetr-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock改进resnet18-backbone中的BasicBlock.
    百度云视频：20231210更新说明

37. ultralytics/cfg/models/rt-detr/rtdetr-DWRC3-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)进行二次创新改进rtdetr.
    百度云视频：20231210更新说明

38. ultralytics/cfg/models/rt-detr/rtdetr-Conv3XCC3.yaml

    使用[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC改进RepC3.
    百度云视频：20231214更新说明

39. ultralytics/cfg/models/rt-detr/rtdetr-DRBC3.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock改进RepC3.
    百度云视频：20231214更新说明

40. ultralytics/cfg/models/rt-detr/rtdetr-DBBC3.yaml

    使用[DiverseBranchBlock CVPR2021](https://github.com/DingXiaoH/DiverseBranchBlock)改进RepC3.
    百度云视频：20231214更新说明

41. ultralytics/cfg/models/rt-detr/rtdetr-DBB.yaml

    使用[DiverseBranchBlock CVPR2021](https://github.com/DingXiaoH/DiverseBranchBlock)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231214更新说明

42. ultralytics/cfg/models/rt-detr/rtdetr-DualConv.yaml

    使用[DualConv](https://github.com/ChipsGuardian/DualConv)改进resnet18-backbone中的BasicBlock.
    百度云视频：20231214更新说明

43. ultralytics/cfg/models/rt-detr/rtdetr-ASF.yaml

    使用[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion来改进rtdetr.
    百度云视频：20231223更新说明

44. ultralytics/cfg/models/rt-detr/rtdetr-ASF-P2.yaml

    在ultralytics/cfg/models/rt-detr/rtdetr-ASF.yaml的基础上进行二次创新，引入P2检测层并对网络结构进行优化.
    百度云视频：20231223更新说明

45. ultralytics/cfg/models/rt-detr/rtdetr-slimneck.yaml

    使用[SlimNeck](https://github.com/AlanLi1997/slim-neck-by-gsconv)中的VoVGSCSP\VoVGSCSPC和GSConv改进rtdetr中的CCFM.
    百度云视频：20231223更新说明

46. ultralytics/cfg/models/rt-detr/rtdetr-slimneck-ASF.yaml

    使用[SlimNeck](https://github.com/AlanLi1997/slim-neck-by-gsconv)中的VoVGSCSP\VoVGSCSPC和GSConv和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion改进rtdetr中的CCFM.
    百度云视频：20231223更新说明

47. ultralytics/cfg/models/rt-detr/rtdetr-TransNeXt.yaml

    使用[TransNeXt](https://github.com/DaiShiResearch/TransNeXt)改进yolov8的backbone.
    百度云视频：20240106更新说明

48. ultralytics/cfg/models/rt-detr/rtdetr-AggregatedAtt.yaml

    使用[TransNeXt](https://github.com/DaiShiResearch/TransNeXt)中的聚合感知注意力改进resnet18中的BasicBlock.(百度云视频-20240106更新说明)

49. ultralytics/cfg/models/rt-detr/rtdetr-SDI.yaml

    使用[U-NetV2](https://github.com/yaoppeng/U-Net_v2)中的 Semantics and Detail Infusion Module对CCFM中的feature fusion进行改进.
    百度云视频：20240106更新说明

50. ultralytics/cfg/models/rt-detr/rtdetr-goldyolo.yaml

    利用华为2023最新GOLD-YOLO中的Gatherand-Distribute进行改进特征融合模块.
    百度云视频：20240113更新说明

51. ultralytics/cfg/models/rt-detr/rtdetr-goldyolo-asf.yaml

    利用华为2023最新GOLD-YOLO中的Gatherand-Distribute和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion进行改进特征融合模块.
    百度云视频：20240113更新说明

52. ultralytics/cfg/models/rt-detr/rtdetr-DCNV4.yaml

    使用[DCNV4](https://github.com/OpenGVLab/DCNv4)改进resnet18中的BasicBlock.
    百度云视频：20240120更新说明

53. ultralytics/cfg/models/rt-detr/rtdetr-AIFI-HiLo.yaml

    使用[LITv2](https://github.com/ziplab/LITv2)中具有提取高低频信息的高效注意力对AIFI进行二次改进.
    百度云视频：20240120更新说明

54. ultralytics/cfg/models/rt-detr/rtdetr-HSFPN.yaml

    使用[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN改进RTDETR中的CCFM.
    百度云视频：20240120更新说明

55. ultralytics/cfg/models/rt-detr/rtdetr-HSPAN.yaml

    对[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN进行二次创新后得到HSPAN改进RTDETR中的CCFM.
    百度云视频：20240120更新说明

56. ultralytics/cfg/models/rt-detr/rtdetr-DySample.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进CCFM中的上采样.
    百度云视频：20240128更新说明

57. ultralytics/cfg/models/rt-detr/rtdetr-CARAFE.yaml

    使用[ICCV2019 CARAFE](https://arxiv.org/abs/1905.02188)改进CCFM中的上采样.
    百度云视频：20240128更新说明

58. ultralytics/cfg/models/rt-detr/rtdetr-HWD.yaml

    使用[Haar wavelet downsampling](https://www.sciencedirect.com/science/article/abs/pii/S0031320323005174)改进CCFM的下采样.
    百度云视频：20240128更新说明

59. ultralytics/cfg/models/rt-detr/rtdetr-ASF-Dynamic.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion的上采样模块得到Dynamic Sample Attentional Scale Sequence Fusion改进CCFM.
    百度云视频：20240128更新说明

60. ultralytics/cfg/models/rt-detr/rtdetr-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)改进resnet18中的BasicBlock.
    百度云视频：20240206更新说明

61. ultralytics/cfg/models/rt-detr/rtdetr-iRMB-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet18-backbone中的BasicBlock.
    百度云视频：20240206更新说明

62. ultralytics/cfg/models/rt-detr/rtdetr-iRMB-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet18-backbone中的BasicBlock.
    百度云视频：20240206更新说明

63. ultralytics/cfg/models/rt-detr/rtdetr-VSS.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)改进resnet18-backbone中的BasicBlock.
    百度云视频：20240219更新说明

64. ultralytics/cfg/models/rt-detr/rtdetr-RepNCSPELAN.yaml

    使用[YOLOV9](https://github.com/WongKinYiu/yolov9)中的RepNCSPELAN和ADown进行改进RTDETR-R18.
    百度云视频：20240225更新说明

65. ultralytics/cfg/models/rt-detr/rtdetr-DBBNCSPELAN.yaml

    在rtdetr-RepNCSPELAN.yaml使用[Diverse Branch Block CVPR2021](https://arxiv.org/abs/2103.13425)进行二次创新.(详细介绍请看百度云视频-20240225更新说明)

66. ultralytics/cfg/models/rt-detr/rtdetr-OREPANCSPELAN.yaml

    在rtdetr-RepNCSPELAN.yaml使用[Online Convolutional Re-parameterization (CVPR2022)](https://github.com/JUGGHM/OREPA_CVPR2022/tree/main)进行二次创新.(详细介绍请看百度云视频-20240225更新说明)

67. ultralytics/cfg/models/rt-detr/rtdetr-DRBNCSPELAN.yaml

    在rtdetr-RepNCSPELAN.yaml使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock进行二次创新.(详细介绍请看百度云视频-20240225更新说明)

68. ultralytics/cfg/models/rt-detr/rtdetr-Conv3XCNCSPELAN.yaml

    在rtdetr-RepNCSPELAN.yaml使用[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC进行二次创新.(详细介绍请看百度云视频-20240225更新说明)

69. ultralytics/cfg/models/rt-detr/rtdetr-bifpn.yaml

    添加BIFPN到rtdetr-r18中.  
    其中BIFPN中有三个可选参数：
    1. Fusion  
        其中BIFPN中的Fusion模块支持五种: weight, adaptive, concat, bifpn(default), SDI  
        其中weight, adaptive, concat出自[paper链接-Figure 3](https://openreview.net/pdf?id=q2ZaVU6bEsT), SDI出自[U-NetV2](https://github.com/yaoppeng/U-Net_v2)
    2. node_mode  
        block模块选择,具体可看对应百度云视频-20240302更新公告.
    3. head_channel  
        BIFPN中的通道数,默认设置为256.

70. ultralytics/cfg/models/rt-detr/rtdetr-ContextGuided.yaml

    使用[CGNet](https://github.com/wutianyiRosun/CGNet/tree/master)中的Light-weight Context Guided和Light-weight Context Guided DownSample改进rtdetr-r18.
    百度云视频：20240302更新说明

71. ultralytics/cfg/models/rt-detr/rtdetr-ContextGuidedDown.yaml

    使用[CGNet](https://github.com/wutianyiRosun/CGNet/tree/master)中的Light-weight Context Guided DownSample改进rtdetr-r18.
    百度云视频：20240302更新说明

72. ultralytics/cfg/models/rt-detr/rtdetr-PACAPN.yaml

    自研结构, Parallel Atrous Convolution Attention Pyramid Network, PAC-APN
    1. 并行(上/下)采样分支可为网络提供多条特征提取途径，丰富特征表达的多样性、再结合gate机制对采样后的特征进行特征选择，强化更有意义的特征，抑制冗余或不相关的特征，提升特征表达的有效性。
    2. PAC模块通过使用具有不同膨胀率的并行空洞卷积，能够有效地提取不同尺度的特征。这使得网络能够捕捉数据中局部和上下文信息，提高其表示复杂模式的能力。
    百度云视频：20240307更新说明

73. ultralytics/cfg/models/rt-detr/rtdetr-DGCST.yaml

    使用[Lightweight Object Detection](https://arxiv.org/abs/2403.01736)中的Dynamic Group Convolution Shuffle Transformer改进rtdetr-r18.
    百度云视频：20240307更新说明

74. ultralytics/cfg/models/rt-detr/rtdetr-DGCST2.yaml

    使用[Lightweight Object Detection](https://arxiv.org/abs/2403.01736)中的Dynamic Group Convolution Shuffle Transformer与Dynamic Group Convolution Shuffle Module进行结合改进rtdetr-r18.
    百度云视频：20240307更新说明

75. ultralytics/cfg/models/rt-detr/rtdetr-rmt.yaml

    使用[CVPR2024 RMT](https://arxiv.org/abs/2309.11523)改进rtdetr的主干.
    百度云视频：20240321更新说明

76. ultralytics/cfg/models/rt-detr/rtdetr-RetBlockC3.yaml

    使用[CVPR2024 RMT](https://arxiv.org/abs/2309.11523)中的RetBlock改进RepC3.
    百度云视频：20240321更新说明

77. ultralytics/cfg/models/rt-detr/rtdetr-ELA-HSFPN.yaml

    使用[Efficient Local Attention](https://arxiv.org/abs/2403.01123)改进HSFPN.
    百度云视频：20240321更新说明

78. ultralytics/cfg/models/rt-detr/rtdetr-CA-HSFPN.yaml

    使用[Coordinate Attention CVPR2021](https://github.com/houqb/CoordAttention)改进HSFPN.
    百度云视频：20240321更新说明

79. ultralytics/cfg/models/rt-detr/rtdetr-pkinet.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)改进backbone.(需要安装mmcv和mmengine)
    百度云视频：20240404更新说明

80. ultralytics/cfg/models/rt-detr/rtdetr-RepNCSPELAN-CAA.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的CAA模块改进RepNCSPELAN.
    百度云视频：20240404更新说明

81. ultralytics/cfg/models/rt-detr/rtdetr-CAA-HSFPN.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的CAA模块HSFPN.
    百度云视频：20240404更新说明

82. ultralytics/cfg/models/rt-detr/rtdetr-C2f-PKI.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的PKIModule和CAA模块和C2f改进backbone.
    百度云视频：20240404更新说明

83. ultralytics/cfg/models/rt-detr/rtdetr-fadc.yaml

    使用[CVPR2024 Frequency-Adaptive Dilated Convolution](https://github.com/Linwei-Chen/FADC)改进resnet18-basicblock.(需要安装mmcv)
    百度云视频：20240404更新说明

84. ultralytics/cfg/models/rt-detr/rtdetr-FDPN.yaml

    自研特征聚焦扩散金字塔网络(Focusing Diffusion Pyramid Network)
    1. 通过定制的特征聚焦模块与特征扩散机制，能让每个尺度的特征都具有详细的上下文信息，更有利于后续目标的检测与分类。
    2. 定制的特征聚焦模块可以接受三个尺度的输入，其内部包含一个Inception-Style的模块，其利用一组并行深度卷积来捕获丰富的跨多个尺度的信息。
    3. 通过扩散机制使具有丰富的上下文信息的特征进行扩散到各个检测尺度.
    百度云视频：20240412更新说明

85. ultralytics/cfg/models/rt-detr/rtdetr-FDPN-DASI.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Dimension-Aware Selective Integration Module对自研的Focusing Diffusion Pyramid Network再次创新.
    百度云视频：20240412更新说明

86. ultralytics/cfg/models/rt-detr/rtdetr-C2f-PPA.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Parallelized Patch-Aware Attention Module改进C2f.
    百度云视频：20240412更新说明

87. ultralytics/cfg/models/rt-detr/rtdetr-CSFCN.yaml

    使用[Context and Spatial Feature Calibration for Real-Time Semantic Segmentation](https://github.com/kaigelee/CSFCN/tree/main)中的Context and Spatial Feature Calibration模块改进rtdetr-neck.
    百度云视频：20240427更新说明

88. ultralytics/cfg/models/rt-detr/rtdetr-SRFD.yaml

    使用[A Robust Feature Downsampling Module for Remote Sensing Visual Tasks](https://ieeexplore.ieee.org/document/10142024)改进rtdetr的下采样.
    百度云视频：20240427更新说明

89. ultralytics/cfg/models/rt-detr/rtdetr-mobilenetv4.yaml

    使用[MobileNetV4](https://github.com/jaiwei98/MobileNetV4-pytorch/tree/main)改进rtdetr-backbone.
    百度云视频：20240427更新说明

90. ultralytics/cfg/models/rt-detr/rtdetr-CGAFusion.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的content-guided attention fusion改进rtdetr-neck.
    百度云视频：20240502更新说明

91. ultralytics/cfg/models/rt-detr/rtdetr-CAFMFusion.yaml

    利用具有[HCANet](https://github.com/summitgao/HCANet)中的CAFM，其具有获取全局和局部信息的注意力机制进行二次改进content-guided attention fusion.
    百度云视频：20240502更新说明
 
92. ultralytics/cfg/models/rt-detr/rtdetr-RGCSPELAN.yaml

    自研RepGhostCSPELAN.
    1. 参考GhostNet中的思想(主流CNN计算的中间特征映射存在广泛的冗余)，采用廉价的操作生成一部分冗余特征图，以此来降低计算量和参数量。
    2. 舍弃yolov5与yolov8中常用的BottleNeck，为了弥补舍弃残差块所带来的性能损失，在梯度流通分支上使用RepConv，以此来增强特征提取和梯度流通的能力，并且RepConv可以在推理的时候进行融合，一举两得。
    3. 可以通过缩放因子控制RGCSPELAN的大小，使其可以兼顾小模型和大模型。
    百度云视频：20240502更新说明

93. ultralytics/cfg/models/rt-detr/rtdetr-starnet.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)改进yolov8-backbone.
    百度云视频：20240518更新说明

94. ultralytics/cfg/models/rt-detr/rtdetr-faster-CGLU.yaml

    使用[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU对CVPR2023中的FasterNet进行二次创新.
    百度云视频：20240518更新说明

95. ultralytics/cfg/models/rt-detr/rtdetr-SDFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的superficial detail fusion module改进rtdetr-neck.
    百度云视频：20240518更新说明

96. ultralytics/cfg/models/rt-detr/rtdetr-PSFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的profound semantic fusion module改进rtdetr-neck.
    百度云视频：20240518更新说明

97. ultralytics/cfg/models/rt-detr/rtdetr-Star.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock改进resnet18-basicblock.
    百度云视频：20240518更新说明

98. ultralytics/cfg/models/rt-detr/rtdetr-KAN.yaml

    使用[Pytorch-Conv-KAN](https://github.com/IvanDrokin/torch-conv-kan)的KAN卷积算子改进resnet18-basicblock.
    目前支持:
    1. FastKANConv2DLayer
    2. KANConv2DLayer
    3. KALNConv2DLayer
    4. KACNConv2DLayer
    5. KAGNConv2DLayer
    百度云视频：20240525更新说明

99. ultralytics/cfg/models/rt-detr/rtdetr-KANC3.yaml

    使用[Pytorch-Conv-KAN](https://github.com/IvanDrokin/torch-conv-kan)的KAN卷积算子改进RepC3.
    目前支持:
    1. FastKANConv2DLayer
    2. KANConv2DLayer
    3. KALNConv2DLayer
    4. KACNConv2DLayer
    5. KAGNConv2DLayer
    百度云视频：20240525更新说明

100. ultralytics/cfg/models/rt-detr/rtdetr-ContextGuideFPN.yaml

    Context Guide Fusion Module（CGFM）是一个创新的特征融合模块，旨在改进YOLOv8中的特征金字塔网络（FPN）。该模块的设计考虑了多尺度特征融合过程中上下文信息的引导和自适应调整。
    1. 上下文信息的有效融合：通过SE注意力机制，模块能够在特征融合过程中捕捉并利用重要的上下文信息，从而增强特征表示的有效性，并有效引导模型学习检测目标的信息，从而提高模型的检测精度。
    2. 特征增强：通过权重化的特征重组操作，模块能够增强重要特征，同时抑制不重要特征，提升特征图的判别能力。
    3. 简单高效：模块结构相对简单，不会引入过多的计算开销，适合在实时目标检测任务中应用。
    这期视频讲解在B站:https://www.bilibili.com/video/BV1Vx4y1n7hZ/

101. ultralytics/cfg/models/rt-detr/rtdetr-DEConv.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的detail-enhanced convolution改进resnet18-basicblock.
    关于DEConv在运行的时候重参数化后比重参数化前的计算量还要大的问题:是因为重参数化前thop库其计算不准的问题,看重参数化后的参数即可.
    百度云视频：20240608更新说明

102. ultralytics/cfg/models/rt-detr/rtdetr-C2f-SMPCGLU.yaml

    Self-moving Point Convolutional GLU模型改进C2f.
    SMP来源于[CVPR2023-SMPConv](https://github.com/sangnekim/SMPConv),Convolutional GLU来源于[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt).
    1. 普通的卷积在面对数据中的多样性和复杂性时，可能无法捕捉到有效的特征，因此我们采用了SMPConv，其具备最新的自适应点移动机制，从而更好地捕捉局部特征，提高特征提取的灵活性和准确性。
    2. 在SMPConv后添加CGLU，Convolutional GLU 结合了卷积和门控机制，能够选择性地通过信息通道，提高了特征提取的有效性和灵活性。
    3. 这种类似Transformer的encoder结构，利用DEConv进行特征提取，CGLU可以进一步的非线性变换和加强特征提取，提升模型的表达能力。
    百度云视频：20240608更新说明

103. ultralytics/cfg/models/rt-detr/rtdetr-C2f-vHeat.yaml

    使用[vHeat](https://github.com/MzeroMiko/vHeat/tree/main)中的HeatBlock改进C2f.
    百度云视频：20240618更新说明

104. ultralytics/cfg/models/rt-detr/rtdetr-WaveletPool.yaml

    使用[Wavelet Pooling](https://openreview.net/forum?id=rkhlb8lCZ)改进RTDETR的上采样和下采样。
    百度云视频：20240618更新说明

105. Re-CalibrationFPN

    为了加强浅层和深层特征的相互交互能力，推出重校准特征金字塔网络(Re-CalibrationFPN).
    P2345：ultralytics/cfg/models/v8/yolov8-ReCalibrationFPN-P2345.yaml(带有小目标检测头的ReCalibrationFPN)
    P345：ultralytics/cfg/models/v8/yolov8-ReCalibrationFPN-P345.yaml
    P3456：ultralytics/cfg/models/v8/yolov8-ReCalibrationFPN-P3456.yaml(带有大目标检测头的ReCalibrationFPN)
    1. 浅层语义较少，但细节丰富，有更明显的边界和减少失真。此外，深层蕴藏着丰富的物质语义信息。因此，直接融合低级具有高级特性的特性可能导致冗余和不一致。为了解决这个问题，我们提出了[SBA](https://github.com/Barrett-python/DuAT)模块，它有选择地聚合边界信息和语义信息来描绘更细粒度的物体轮廓和重新校准物体的位置。
    2. 相比传统的FPN结构，[SBA](https://github.com/Barrett-python/DuAT)模块引入了高分辨率和低分辨率特征之间的双向融合机制，使得特征之间的信息传递更加充分，进一步提升了多尺度特征融合的效果。
    3. [SBA](https://github.com/Barrett-python/DuAT)模块通过自适应的注意力机制，根据特征图的不同分辨率和内容，自适应地调整特征的权重，从而更好地捕捉目标的多尺度特征。
    百度云视频：20240618更新说明

106. RTDETR-Mamba

    集成[Mamba-YOLO](https://github.com/HZAI-ZJNU/Mamba-YOLO),并把head改为RTDETR-Head.(需要编译，请看百度云视频-20240622更新说明)
    ultralytics/cfg/models/rt-detr/rtdetr-mamba-T.yaml
    ultralytics/cfg/models/rt-detr/rtdetr-mamba-B.yaml
    ultralytics/cfg/models/rt-detr/rtdetr-mamba-L.yaml

107. ultralytics/cfg/models/rt-detr/rtdetr-GLSA.yaml

    使用[GLSA](https://github.com/Barrett-python/DuAT)模块改进rtdetr的neck.
    百度云视频：20240622更新说明

108. ultralytics/cfg/models/rt-detr/rtdetr-bifpn-GLSA.yaml

    使用[GLSA](https://github.com/Barrett-python/DuAT)模块对bifpn进行二次创新.
    百度云视频：20240622更新说明

109. ultralytics/cfg/models/rt-detr/rtdetr-SOEP.yaml

    小目标在正常的P3、P4、P5检测层上略显吃力，比较传统的做法是加上P2检测层来提升小目标的检测能力，但是同时也会带来一系列的问题，例如加上P2检测层后计算量过大、后处理更加耗时等问题，日益激发需要开发新的针对小目标有效的特征金字塔，我们基于原本的CCFF上进行改进，提出SmallObjectEnhancePyramid，相对于传统的添加P2检测层，我们使用P2特征层经过SPDConv得到富含小目标信息的特征给到P3进行融合，然后使用CSP思想和基于[AAAI2024的OmniKernel](https://ojs.aaai.org/index.php/AAAI/article/view/27907)进行改进得到CSP-OmniKernel进行特征整合，OmniKernel模块由三个分支组成，即三个分支，即全局分支、大分支和局部分支、以有效地学习从全局到局部的特征表征，最终从而提高小目标的检测性能。
    百度云视频：20240703更新说明

110. ultralytics/cfg/models/rt-detr/rtdetr-CTrans.yaml

    使用[[AAAI2022] UCTransNet](https://github.com/McGregorWwww/UCTransNet/tree/main)中的ChannelTransformer改进rtdetr-neck.
    百度云视频：20240703更新说明

111. ultralytics/cfg/models/rt-detr/rtdetr-p6-CTrans.yaml

    使用[[AAAI2022] UCTransNet](https://github.com/McGregorWwww/UCTransNet/tree/main)中的ChannelTransformer改进rtdetr-neck.(带有p6版本)
    百度云视频：20240703更新说明

112. ultralytics/cfg/models/rt-detr/rtdetr-AIFI-EfficientAdditive.yaml

    使用[ICCV2023 SwiftFormer](https://github.com/Amshaker/SwiftFormer/tree/main)中的EfficientAdditiveAttention改进AIFI.
    百度云视频：20240703更新说明

113. ultralytics/cfg/models/rt-detr/rtdetr-WTConv.yaml

    使用[ECCV2024 Wavelet Convolutions for Large Receptive Fields](https://github.com/BGU-CS-VIL/WTConv)中的WTConv改进BasicBlock.
    百度云视频：20240715更新说明

114. ultralytics/cfg/models/rt-detr/rtdetr-CGRFPN.yaml

    Context-Guided Spatial Feature Reconstruction Feature Pyramid Network.
    1. 借鉴[ECCV2024-CGRSeg](https://github.com/nizhenliang/CGRSeg)中的Rectangular Self-Calibration Module经过精心设计,用于空间特征重建和金字塔上下文提取,它在水平和垂直方向上捕获全局上下文，并获得轴向全局上下文来显式地建模矩形关键区域.
    2. PyramidContextExtraction Module使用金字塔上下文提取模块（PyramidContextExtraction），有效整合不同层级的特征信息，提升模型的上下文感知能力。
    3. FuseBlockMulti 和 DynamicInterpolationFusion 这些模块用于多尺度特征的融合，通过动态插值和多特征融合，进一步提高了模型的多尺度特征表示能力和提升模型对复杂背景下目标的识别能力。
    百度云视频：20240715更新说明

115. ultralytics/cfg/models/rt-detr/rtdetr-C2f-FMB.yaml

    使用[ECCV2024 SMFANet](https://github.com/Zheng-MJ/SMFANet/tree/main)的Feature Modulation block改进C2f.
    项目视频百度云链接:20240725版本更新说明

116. ultralytics/cfg/models/rt-detr/rtdetr-C2f-gConv.yaml

    使用[Rethinking Performance Gains in Image Dehazing Networks](https://arxiv.org/abs/2209.11448)的gConvblock改进C2f.
    项目视频百度云链接:20240725版本更新说明

117. ultralytics/cfg/models/rt-detr/rtdetr-gConvC3.yaml

    使用[Rethinking Performance Gains in Image Dehazing Networks](https://arxiv.org/abs/2209.11448)的gConvblock改进RepC3.
    项目视频百度云链接:20240725版本更新说明

118. ultralytics/cfg/models/rt-detr/rtdetr-LDConv.yaml

    使用[LDConv](https://github.com/CV-ZhangXin/LDConv/tree/main)改进下采样.
    项目视频百度云链接:20240802版本更新说明

119. ultralytics/cfg/models/rt-detr/rtdetr-MAFPN.yaml

    使用[MAF-YOLO](https://arxiv.org/pdf/2407.04381)的MAFPN改进Neck.
    项目视频百度云链接:20240802版本更新说明

120. ultralytics/cfg/models/rt-detr/rtdetr-BIMAFPN.yaml

    利用BIFPN的思想对[MAF-YOLO](https://arxiv.org/pdf/2407.04381)的MAFPN进行二次改进得到BIMAFPN.
    项目视频百度云链接:20240802版本更新说明

121. ultralytics/cfg/models/rt-detr/rtdetr-WDBB.yaml

    使用[YOLO-MIF](https://github.com/wandahangFY/YOLO-MIF)中的WDBB改进BasicBlock.
    项目视频百度云链接:20240815版本更新说明

122. ultralytics/cfg/models/rt-detr/rtdetr-DeepDBB.yaml

    使用[YOLO-MIF](https://github.com/wandahangFY/YOLO-MIF)中的DeepDBB改进BasicBlock.
    项目视频百度云链接:20240815版本更新说明

123. ultralytics/cfg/models/rt-detr/rtdetr-AIFIRepBN.yaml

    使用[ICML-2024 SLAB](https://github.com/xinghaochen/SLAB)中的RepBN改进AIFI.
    项目视频百度云链接:20240815版本更新说明

124. ultralytics/cfg/models/rt-detr/rtdetr-C2f-AddutuveBlock.yaml

    使用[CAS-ViT](https://github.com/Tianfang-Zhang/CAS-ViT)中的AdditiveBlock和CSP思想改进backbone.
    项目视频百度云链接:20240825版本更新说明

125. ultralytics/cfg/models/rt-detr/rtdetr-C2f-AddutuveBlock-CGLU.yaml

    使用[CAS-ViT](https://github.com/Tianfang-Zhang/CAS-ViT)中的AdditiveBlock和[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU和CSP思想改进backbone.
    项目视频百度云链接:20240825版本更新说明

126. ultralytics/cfg/models/rt-detr/rtdetr-AdditiveTokenMixer.yaml

    使用[CAS-ViT](https://github.com/Tianfang-Zhang/CAS-ViT)中的AdditiveBlock改进AIFI.
    项目视频百度云链接:20240825版本更新说明

127. ultralytics/cfg/models/rt-detr/rtdetr-EMBSFPN.yaml

    基于BIFPN、[MAF-YOLO](https://arxiv.org/pdf/2407.04381)、[CVPR2024 EMCAD](https://github.com/SLDGroup/EMCAD)提出全新的Efficient Multi-Branch&Scale FPN.
    Efficient Multi-Branch&Scale FPN拥有<轻量化>、<多尺度特征加权融合>、<多尺度高效卷积模块>、<高效上采样模块>、<全局异构核选择机制>。
    1. 具有多尺度高效卷积模块和全局异构核选择机制，Trident网络的研究表明，具有较大感受野的网络更适合检测较大的物体，反之，较小尺度的目标则从较小的感受野中受益，因此我们在FPN阶段，对于不同尺度的特征层选择不同的多尺度卷积核以适应并逐步获得多尺度感知场信息。
    2. 借鉴BIFPN中的多尺度特征加权融合，能把Concat换成Add来减少参数量和计算量的情况下，还能通过不同尺度特征的重要性进行自适用选择加权融合。
    3. 高效上采样模块来源于CVPR2024-EMCAD中的EUCB，能够在保证一定效果的同时保持高效性。
    项目视频百度云链接:20240825版本更新说明

128. ultralytics/cfg/models/rt-detr/rtdetr-C2f-MSMHSA-CGLU.yaml

    使用[CMTFNet](https://github.com/DrWuHonglin/CMTFNet/tree/main)中的M2SA和[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU改进c2f.
    项目视频百度云链接:20240902版本更新说明

129. ultralytics/cfg/models/rt-detr/rtdetr-CSP-PMSFA.yaml

    自研模块:CSP-Partial Multi-Scale Feature Aggregation.
    1. 部分多尺度特征提取：参考CVPR2020-GhostNet、CVPR2024-FasterNet的思想，采用高效的PartialConv，该模块能够从输入中提取多种尺度的特征信息，但它并不是在所有通道上进行这种操作，而是部分（Partial）地进行，从而提高了计算效率。
    2. 增强的特征融合: 最后的 1x1 卷积层通过将不同尺度的特征融合在一起，同时使用残差连接将输入特征与处理后的特征相加，有效保留了原始信息并引入了新的多尺度信息，从而提高模型的表达能力。
    项目视频百度云链接:20240902版本更新说明

130. ultralytics/cfg/models/rt-detr/rtdetr-AIFI-MSMHSA.yaml

    使用[CMTFNet](https://github.com/DrWuHonglin/CMTFNet/tree/main)中的M2SA改进AIFI.
    项目视频百度云链接:20240902版本更新说明

### 以RT-DETR-R50为基准模型的改进方案

1. ultralytics/cfg/models/rt-detr/rtdetr-r50-Ortho.yaml

    使用[OrthoNets](https://github.com/hady1011/OrthoNets/tree/main)中的正交通道注意力改进resnet50-backbone中的BottleNeck.(详细介绍请看百度云视频-20231119更新说明)

2. ultralytics/cfg/models/rt-detr/rtdetr-r50-DCNV2.yaml

    使用可变形卷积DCNV2改进resnet50-backbone中的BottleNeck.

3. ultralytics/cfg/models/rt-detr/rtdetr-r50-DCNV3.yaml

    使用可变形卷积[DCNV3 CVPR2023](https://github.com/OpenGVLab/InternImage)改进resnet50-backbone中的BottleNeck.(安装教程请看百度云视频-20231119更新说明)

4. ultralytics/cfg/models/rt-detr/rtdetr-r50-DCNV2-Dynamic.yaml

    使用自研可变形卷积DCNV2-Dynamic改进resnet50-backbone中的BottleNeck.(详细介绍请看百度云视频-MPCA与DCNV2_Dynamic的说明)

5. ultralytics/cfg/models/rt-detr/rtdetr-r50-iRMB.yaml

    使用[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB改进resnet50-backbone中的BottleNeck.(详细介绍请看百度云视频-20231119更新说明)

6. ultralytics/cfg/models/rt-detr/rtdetr-r50-iRMB-Cascaded.yaml

    使用[EfficientViT CVPR2023](https://github.com/microsoft/Cream/tree/main/EfficientViT)中的CascadedGroupAttention对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet50-backbone中的BottleNeck.(详细介绍请看百度云视频-20231119更新说明)

7. ultralytics/cfg/models/rt-detr/rtdetr-r50-attention.yaml

    添加注意力模块到resnet50-backbone中的BottleNeck.(手把手教程请看百度云视频-手把手添加注意力教程)

8. ultralytics/cfg/models/rt-detr/rtdetr-r50-DySnake.yaml

    添加[DySnakeConv](https://github.com/YaoleiQi/DSCNet)到resnet50-backbone中的BottleNeck中.

9. ultralytics/cfg/models/rt-detr/rtdetr-r50-PConv.yaml

    使用[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的PConv改进resnet50-backbone中的BottleNeck.

10. ultralytics/cfg/models/rt-detr/rtdetr-r50-PConv-Rep.yaml

    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的PConv进行二次创新后改进resnet50-backbone中的BottleNeck.

11. ultralytics/cfg/models/rt-detr/rtdetr-r50-Faster.yaml

    使用[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block改进resnet50-backbone中的BottleNeck.

12. ultralytics/cfg/models/rt-detr/rtdetr-r50-Faster-Rep.yaml

    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet50-backbone中的BottleNeck.

13. ultralytics/cfg/models/rt-detr/rtdetr-r50-Faster-EMA.yaml

    使用[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet50-backbone中的BottleNeck.

14. ultralytics/cfg/models/rt-detr/rtdetr-r50-Faster-Rep-EMA.yaml
    
    使用[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv和[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)对[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block进行二次创新后改进resnet50-backbone中的BottleNeck.

15. ultralytics/cfg/models/rt-detr/rtdetr-r50-AKConv.yaml

    使用[AKConv 2023](https://github.com/CV-ZhangXin/AKConv)改进resnet50-backbone中的BottleNeck.

16. ultralytics/cfg/models/rt-detr/rtdetr-r50-RFAConv.yaml

    使用[RFAConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet50-backbone中的BottleNeck.

17. ultralytics/cfg/models/rt-detr/rtdetr-r50-RFCAConv.yaml

    使用[RFCAConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet50-backbone中的BottleNeck.

18. ultralytics/cfg/models/rt-detr/rtdetr-r50-RFCBAMConv.yaml

    使用[RFCBAMConv 2023](https://github.com/Liuchen1997/RFAConv)改进resnet50-backbone中的BottleNeck.

19. ultralytics/cfg/models/rt-detr/rtdetr-r50-Conv3XC.yaml

    使用[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC改进resnet50-backbone中的BottleNeck.

20. ultralytics/cfg/models/rt-detr/rtdetr-r50-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock改进resnet50-backbone中的BottleNeck.

21. ultralytics/cfg/models/rt-detr/rtdetr-r50-DBB.yaml

    使用[DiverseBranchBlock CVPR2021](https://github.com/DingXiaoH/DiverseBranchBlock)改进resnet50-backbone中的BottleNeck.

22. ultralytics/cfg/models/rt-detr/rtdetr-r50-DualConv.yaml

    使用[DualConv](https://github.com/ChipsGuardian/DualConv)改进resnet50-backbone中的BottleNeck.

23. ultralytics/cfg/models/rt-detr/rtdetr-r50-ASF.yaml

    使用[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion来改进rtdetr.

24. ultralytics/cfg/models/rt-detr/rtdetr-r50-AggregatedAtt.yaml

    使用[TransNeXt](https://github.com/DaiShiResearch/TransNeXt)中的聚合感知注意力改进resnet50中的BottleNeck.(百度云视频-20240106更新说明)

25. ultralytics/cfg/models/rt-detr/rtdetr-r50-DCNV4.yaml

    使用[DCNV4](https://github.com/OpenGVLab/DCNv4)改进resnet50中的BottleNeck.

26. ultralytics/cfg/models/rt-detr/rtdetr-r50-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)改进resnet50中的BottleNeck.

27. ultralytics/cfg/models/rt-detr/rtdetr-r50-iRMB-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet50中的BottleNeck

28. ultralytics/cfg/models/rt-detr/rtdetr-r50-iRMB-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进resnet50中的BottleNeck.

29. ultralytics/cfg/models/rt-detr/rtdetr-r50-VSS.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)改进resnet50中的BottleNeck.

30. ultralytics/cfg/models/rt-detr/rtdetr-r50-RepNCSPELAN.yaml

    使用[YOLOV9](https://github.com/WongKinYiu/yolov9)中的RepNCSPELAN和ADown进行改进RTDETR-R50.

31. ultralytics/cfg/models/rt-detr/rtdetr-r50-bifpn.yaml

    添加BIFPN到rtdetr-r50中.  
    其中BIFPN中有三个可选参数：
    1. Fusion  
        其中BIFPN中的Fusion模块支持五种: weight, adaptive, concat, bifpn(default), SDI  
        其中weight, adaptive, concat出自[paper链接-Figure 3](https://openreview.net/pdf?id=q2ZaVU6bEsT), SDI出自[U-NetV2](https://github.com/yaoppeng/U-Net_v2)
    2. node_mode  
        block模块选择,具体可看对应百度云视频-20240302更新公告.
    3. head_channel  
        BIFPN中的通道数,默认设置为256.

32. ultralytics/cfg/models/rt-detr/rtdetr-r50-ContextGuided.yaml

    使用[CGNet](https://github.com/wutianyiRosun/CGNet/tree/master)中的Light-weight Context Guided和Light-weight Context Guided DownSample改进rtdetr-r50.

33. ultralytics/cfg/models/rt-detr/rtdetr-r50-PACAPN.yaml

    自研结构, Parallel Atrous Convolution Attention Pyramid Network, PAC-APN

34. ultralytics/cfg/models/rt-detr/rtdetr-r50-DGCST.yaml

    使用[Lightweight Object Detection](https://arxiv.org/abs/2403.01736)中的Dynamic Group Convolution Shuffle Transformer改进rtdetr-r50.

35. ultralytics/cfg/models/rt-detr/rtdetr-r50-RetBlockC3.yaml

    使用[CVPR2024 RMT](https://arxiv.org/abs/2309.11523)中的RetBlock改进RepC3.

36. ultralytics/cfg/models/rt-detr/rtdetr-r50-fadc.yaml

    使用[CVPR2024 Frequency-Adaptive Dilated Convolution](https://github.com/Linwei-Chen/FADC)改进resnet50中的BottleNeck.

37. ultralytics/cfg/models/rt-detr/rtdetr-r50-SRFD.yaml

    使用[A Robust Feature Downsampling Module for Remote Sensing Visual Tasks](https://ieeexplore.ieee.org/document/10142024)改进rtdetr的下采样.

38. ultralytics/cfg/models/rt-detr/rtdetr-r50-faster-CGLU.yaml

    使用[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU对CVPR2023中的FasterNet进行二次创新.

39. ultralytics/cfg/models/rt-detr/rtdetr-r50-Star.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock改进resnet50-bottleblock.

40. ultralytics/cfg/models/rt-detr/rtdetr-r50-KAN.yaml

    使用[Pytorch-Conv-KAN](https://github.com/IvanDrokin/torch-conv-kan)的KAN卷积算子改进resnet50-bottleblock.
    目前支持:
    1. FastKANConv2DLayer
    2. KANConv2DLayer
    3. KALNConv2DLayer
    4. KACNConv2DLayer
    5. KAGNConv2DLayer

41. ultralytics/cfg/models/rt-detr/rtdetr-r50-DEConv.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的detail-enhanced convolution改进resnet50-bottleblock.
    关于DEConv在运行的时候重参数化后比重参数化前的计算量还要大的问题:是因为重参数化前thop库其计算不准的问题,看重参数化后的参数即可.

42. ultralytics/cfg/models/rt-detr/rtdetr-r50-WTConv.yaml

    使用[ECCV2024 Wavelet Convolutions for Large Receptive Fields](https://github.com/BGU-CS-VIL/WTConv)中的WTConv改进resnet50-bottleblock.

43. ultralytics/cfg/models/rt-detr/rtdetr-r50-WDBB.yaml

    使用[YOLO-MIF](https://github.com/wandahangFY/YOLO-MIF)中的WDBB改进BottleNeck.

44. ultralytics/cfg/models/rt-detr/rtdetr-r50-DeepDBB.yaml

    使用[YOLO-MIF](https://github.com/wandahangFY/YOLO-MIF)中的DeepDBB改进BottleNeck.

### 以RT-DETR-L为基准模型的改进方案
1. ultralytics/cfg/models/rt-detr/rtdetr-l-GhostHGNetV2.yaml

    使用GhostConv改进HGNetV2.(详细介绍请看百度云视频-20231109更新说明)

2. ultralytics/cfg/models/rt-detr/rtdetr-l-RepHGNetV2.yaml

    使用RepConv改进HGNetV2.(详细介绍请看百度云视频-20231109更新说明)

3. ultralytics/cfg/models/rt-detr/rtdetr-l-attention.yaml

    添加注意力模块到HGBlock中.(手把手教程请看百度云视频-手把手添加注意力教程)

### 以Yolov8为基准模型的改进方案
1. ultralytics/cfg/models/yolo-detr/yolov8-detr.yaml

    使用RT-DETR中的TransformerDecoderHead改进yolov8.

2. ultralytics/cfg/models/yolo-detr/yolov8-detr-DWR.yaml

    使用RT-DETR中的TransformerDecoderHead和[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)模块改进yolov8.

3. ultralytics/cfg/models/yolo-detr/yolov8-detr-fasternet.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)改进yolov8.(支持替换其他主干,请看百度云视频-替换主干示例教程)

4. ultralytics/cfg/models/yolo-detr/yolov8-detr-AIFI-LPE.yaml

    使用RT-DETR中的TransformerDecoderHead和LearnedPositionalEncoding改进yolov8.(详细介绍请看百度云视频-20231119更新说明)

5. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DCNV2.yaml

    使用RT-DETR中的TransformerDecoderHead和可变形卷积DCNV2改进yolov8.

6. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DCNV3.yaml

    使用RT-DETR中的TransformerDecoderHead和可变形卷积[DCNV3 CVPR2023](https://github.com/OpenGVLab/InternImage)改进yolov8.(安装教程请看百度云视频-20231119更新说明)

7. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DCNV2-Dynamic.yaml

    使用RT-DETR中的TransformerDecoderHead和自研可变形卷积DCNV2-Dynamic改进yolov8.(详细介绍请看百度云视频-MPCA与DCNV2_Dynamic的说明)

8. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Ortho.yaml

    使用RT-DETR中的TransformerDecoderHead和[OrthoNets](https://github.com/hady1011/OrthoNets/tree/main)中的正交通道注意力改进yolov8.(详细介绍请看百度云视频-20231119更新说明)

9. ultralytics/cfg/models/yolo-detr/yolov8-detr-attention.yaml

    添加注意力到基于RTDETR-Head中的yolov8中.(手把手教程请看百度云视频-手把手添加注意力教程)

10. ultralytics/cfg/models/yolo-detr/yolov8-detr-p2.yaml

    添加小目标检测头P2到TransformerDecoderHead中.

11. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DySnake.yaml

    [DySnakeConv](https://github.com/YaoleiQi/DSCNet)与C2f融合.  

12. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Faster.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block改进yolov8.

13. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Faster-Rep.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv二次创新后的Faster-Block-Rep改进yolov8.

14. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Faster-EMA.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)二次创新后的Faster-Block-EMA的Faster-Block-EMA改进yolov8.

15. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Faster-Rep-EMA.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv、[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)二次创新后的Faster-Block改进yolov8.

16. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-AKConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[AKConv 2023](https://github.com/CV-ZhangXin/AKConv)改进yolov8.

17. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFAConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov8.

18. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFCAConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov8.

19. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFCBAMConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov8.

20. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Conv3XC.yaml

    使用RT-DETR中的TransformerDecoderHead和[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC改进yolov8.

21. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-SPAB.yaml

    使用RT-DETR中的TransformerDecoderHead和[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的SPAB改进yolov8.

22. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DRB.yaml

    使用RT-DETR中的TransformerDecoderHead和[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock改进yolov8.

23. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-UniRepLKNetBlock.yaml

    使用RT-DETR中的TransformerDecoderHead和[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的UniRepLKNetBlock改进yolov8.

24. ultralytics/cfg/models/yolo-detr/yolov8-detr-DWR-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)进行二次创新改进yolov8.

25. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DBB.yaml

    使用RT-DETR中的TransformerDecoderHead和[DiverseBranchBlock CVPR2021](https://github.com/DingXiaoH/DiverseBranchBlock)改进yolov8.

26. ultralytics/cfg/models/yolo-detr/yolov8-detr-CSP-EDLAN.yaml

    使用RT-DETR中的TransformerDecoderHead和[DualConv](https://github.com/ChipsGuardian/DualConv)打造CSP Efficient Dual Layer Aggregation Networks改进yolov8.

27. ultralytics/cfg/models/yolo-detr/yolov8-detr-ASF.yaml

    使用RT-DETR中的TransformerDecoderHead和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion改进yolov8.

28. ultralytics/cfg/models/yolo-detr/yolov8-detr-ASF-P2.yaml

    在ultralytics/cfg/models/yolo-detr/yolov8-detr-ASF.yaml的基础上进行二次创新，引入P2检测层并对网络结构进行优化.

29. ultralytics/cfg/models/yolo-detr/yolov8-detr-slimneck.yaml

    使用RT-DETR中的TransformerDecoderHead和[SlimNeck](https://github.com/AlanLi1997/slim-neck-by-gsconv)中VoVGSCSP\VoVGSCSPC和GSConv改进yolov8的neck.

30. ultralytics/cfg/models/yolo-detr/yolov8-detr-slimneck-asf.yaml

    在ultralytics/cfg/models/yolo-detr/yolov8-detr-slimneck.yaml使用[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion进行二次创新.

31. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-AggregatedAtt.yaml

    使用RT-DETR中的TransformerDecoderHead和[TransNeXt](https://github.com/DaiShiResearch/TransNeXt)中的聚合感知注意力改进C2f.(百度云视频-20240106更新说明)

32. ultralytics/cfg/models/yolo-detr/yolov8-detr-SDI.yaml

    使用RT-DETR中的TransformerDecoderHead和[U-NetV2](https://github.com/yaoppeng/U-Net_v2)中的 Semantics and Detail Infusion Module对yolov8中的feature fusion进行改进.

33. ultralytics/cfg/models/yolo-detr/yolov8-detr-goldyolo.yaml

    利用RT-DETR中的TransformerDecoderHead和华为2023最新GOLD-YOLO中的Gatherand-Distribute进行改进特征融合模块.

34. ultralytics/cfg/models/yolo-detr/yolov8-detr-goldyolo-asf.yaml

    利用RT-DETR中的TransformerDecoderHead和华为2023最新GOLD-YOLO中的Gatherand-Distribute和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion进行改进特征融合模块.

35. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DCNV4.yaml

    使用[DCNV4](https://github.com/OpenGVLab/DCNv4)改进C2f.

36. ultralytics/cfg/models/yolo-detr/yolov8-detr-HSFPN.yaml

    利用RT-DETR中的TransformerDecoderHead和使用[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN改进YOLOV8中的PAN.

37. ultralytics/cfg/models/yolo-detr/yolov8-detr-HSPAN.yaml

    利用RT-DETR中的TransformerDecoderHead和对[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN进行二次创新后得到HSPAN改进YOLOV8中的PAN.

38. ultralytics/cfg/models/yolo-detr/yolov8-detr-Dysample.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进yolov8-detr neck中的上采样.

39. ultralytics/cfg/models/yolo-detr/yolov8-detr-CARAFE.yaml

    使用[ICCV2019 CARAFE](https://arxiv.org/abs/1905.02188)改进yolov8-detr neck中的上采样.

40. ultralytics/cfg/models/yolo-detr/yolov8-detr-HWD.yaml

    使用[Haar wavelet downsampling](https://www.sciencedirect.com/science/article/abs/pii/S0031320323005174)改进yolov8-detr neck的下采样.

41. ultralytics/cfg/models/yolo-detr/yolov8-detr-ASF-Dynamic.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion的上采样模块得到Dynamic Sample Attentional Scale Sequence Fusion改进yolov8-detr中的neck.

42. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)改进yolov8-detr中的C2f.

43. ultralytics/cfg/models/yolo-detr/yolov8-detr-iRMB-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进yolov8-detr中的C2f.

44. ultralytics/cfg/models/yolo-detr/yolov8-detr-iRMB-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进yolov8-detr中的C2f.

45. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-VSS.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)对C2f中的BottleNeck进行改进,使其能更有效地捕获图像中的复杂细节和更广泛的语义上下文.

46. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-LVMB.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)与Cross Stage Partial进行结合,使其能更有效地捕获图像中的复杂细节和更广泛的语义上下文.

47. ultralytics/cfg/models/yolo-detr/yolov8-detr-RepNCSPELAN.yaml

    使用[YOLOV9](https://github.com/WongKinYiu/yolov9)中的RepNCSPELAN进行改进yolov8-detr.

48. ultralytics/cfg/models/yolo-detr/yolov8-detr-bifpn.yaml

    添加BIFPN到yolov8中.  
    其中BIFPN中有三个可选参数：
    1. Fusion  
        其中BIFPN中的Fusion模块支持五种: weight, adaptive, concat, bifpn(default), SDI  
        其中weight, adaptive, concat出自[paper链接-Figure 3](https://openreview.net/pdf?id=q2ZaVU6bEsT), SDI出自[U-NetV2](https://github.com/yaoppeng/U-Net_v2)
    2. node_mode  
        block模块选择,具体可看对应百度云视频-20240302更新公告.
    3. head_channel  
        BIFPN中的通道数,默认设置为256.

49. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-ContextGuided.yaml

    使用[CGNet](https://github.com/wutianyiRosun/CGNet/tree/master)中的Light-weight Context Guided和Light-weight Context Guided DownSample改进yolov8-detr.

50. ultralytics/cfg/models/yolo-detr/yolov8-detr-PACAPN.yaml

    自研结构, Parallel Atrous Convolution Attention Pyramid Network, PAC-APN

51. ultralytics/cfg/models/yolo-detr/yolov8-detr-DGCST.yaml

    使用[Lightweight Object Detection](https://arxiv.org/abs/2403.01736)中的Dynamic Group Convolution Shuffle Transformer改进yolov8-detr.

52. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-RetBlock.yaml

    使用[CVPR2024 RMT](https://arxiv.org/abs/2309.11523)中的RetBlock改进C2f.

53. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-PKI.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的PKIModule和CAA模块改进C2f.

54. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-fadc.yaml

    使用[CVPR2024 Frequency-Adaptive Dilated Convolution](https://github.com/Linwei-Chen/FADC)改进C2f.

55. ultralytics/cfg/models/yolo-detr/yolov8-detr-FDPN.yaml

    自研特征聚焦扩散金字塔网络(Focusing Diffusion Pyramid Network)
    1. 通过定制的特征聚焦模块与特征扩散机制，能让每个尺度的特征都具有详细的上下文信息，更有利于后续目标的检测与分类。
    2. 定制的特征聚焦模块可以接受三个尺度的输入，其内部包含一个Inception-Style的模块，其利用一组并行深度卷积来捕获丰富的跨多个尺度的信息。
    3. 通过扩散机制使具有丰富的上下文信息的特征进行扩散到各个检测尺度.

56. ultralytics/cfg/models/yolo-detr/yolov8-detr-FDPN-DASI.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Dimension-Aware Selective Integration Module对自研的Focusing Diffusion Pyramid Network再次创新.

57. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-PPA.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Parallelized Patch-Aware Attention Module改进C2f.

58. ultralytics/cfg/models/yolo-detr/yolov8-detr-SRFD.yaml

    使用[A Robust Feature Downsampling Module for Remote Sensing Visual Tasks](https://ieeexplore.ieee.org/document/10142024)改进yolov8的下采样.

59. ultralytics/cfg/models/yolo-detr/yolov8-detr-CSFCN.yaml

    使用[Context and Spatial Feature Calibration for Real-Time Semantic Segmentation](https://github.com/kaigelee/CSFCN/tree/main)中的Context and Spatial Feature Calibration模块改进yolov8.

60. ultralytics/cfg/models/yolo-detr/yolov8-detr-CGAFusion.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的content-guided attention fusion改进yolov8-neck.

61. ultralytics/cfg/models/yolo-detr/yolov8-detr-CAFMFusion.yaml

    利用具有[HCANet](https://github.com/summitgao/HCANet)中的CAFM，其具有获取全局和局部信息的注意力机制进行二次改进content-guided attention fusion.
 
62. ultralytics/cfg/models/yolo-detr/yolov8-detr-RGCSPELAN.yaml

    自研RepGhostCSPELAN.
    1. 参考GhostNet中的思想(主流CNN计算的中间特征映射存在广泛的冗余)，采用廉价的操作生成一部分冗余特征图，以此来降低计算量和参数量。
    2. 舍弃yolov5与yolov8中常用的BottleNeck，为了弥补舍弃残差块所带来的性能损失，在梯度流通分支上使用RepConv，以此来增强特征提取和梯度流通的能力，并且RepConv可以在推理的时候进行融合，一举两得。
    3. 可以通过缩放因子控制RGCSPELAN的大小，使其可以兼顾小模型和大模型。

63. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Faster-CGLU.yaml

    使用[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU对CVPR2023中的FasterNet进行二次创新.

64. ultralytics/cfg/models/yolo-detr/yolov8-detr-SDFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的superficial detail fusion module改进yolov8-neck.

65. ultralytics/cfg/models/yolo-detr/yolov8-detr-PSFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的profound semantic fusion module改进yolov8-neck.

66. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Star.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock改进C2f.

67. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-Star-CAA.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock和[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的CAA改进C2f.

68. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-KAN.yaml

    使用[Pytorch-Conv-KAN](https://github.com/IvanDrokin/torch-conv-kan)的KAN卷积算子改进C2f.
    目前支持:
    1. FastKANConv2DLayer
    2. KANConv2DLayer
    3. KALNConv2DLayer
    4. KACNConv2DLayer
    5. KAGNConv2DLayer

69. ultralytics/cfg/models/yolo-detr/yolov8-detr-ContextGuideFPN.yaml

    Context Guide Fusion Module（CGFM）是一个创新的特征融合模块，旨在改进YOLOv8中的特征金字塔网络（FPN）。该模块的设计考虑了多尺度特征融合过程中上下文信息的引导和自适应调整。
    1. 上下文信息的有效融合：通过SE注意力机制，模块能够在特征融合过程中捕捉并利用重要的上下文信息，从而增强特征表示的有效性，并有效引导模型学习检测目标的信息，从而提高模型的检测精度。
    2. 特征增强：通过权重化的特征重组操作，模块能够增强重要特征，同时抑制不重要特征，提升特征图的判别能力。
    3. 简单高效：模块结构相对简单，不会引入过多的计算开销，适合在实时目标检测任务中应用。
    这期视频讲解在B站:https://www.bilibili.com/video/BV1Vx4y1n7hZ/

70. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-DEConv.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的detail-enhanced convolution改进C2f.
    关于DEConv在运行的时候重参数化后比重参数化前的计算量还要大的问题:是因为重参数化前thop库其计算不准的问题,看重参数化后的参数即可.

71. ultralytics/cfg/models/yolo-detr/yolov8-detr-C2f-SMPCGLU.yaml

    Self-moving Point Convolutional GLU模型改进C2f.
    SMP来源于[CVPR2023-SMPConv](https://github.com/sangnekim/SMPConv),Convolutional GLU来源于[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt).
    1. 普通的卷积在面对数据中的多样性和复杂性时，可能无法捕捉到有效的特征，因此我们采用了SMPConv，其具备最新的自适应点移动机制，从而更好地捕捉局部特征，提高特征提取的灵活性和准确性。
    2. 在SMPConv后添加CGLU，Convolutional GLU 结合了卷积和门控机制，能够选择性地通过信息通道，提高了特征提取的有效性和灵活性。
    3. 这种类似Transformer的encoder结构，利用DEConv进行特征提取，CGLU可以进一步的非线性变换和加强特征提取，提升模型的表达能力。

### 以Yolov5为基准模型的改进方案
1. ultralytics/cfg/models/yolo-detr/yolov5-detr.yaml

    使用RT-DETR中的TransformerDecoderHead改进yolov5.

2. ultralytics/cfg/models/yolo-detr/yolov5-detr-DWR.yaml

    使用RT-DETR中的TransformerDecoderHead和[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)模块改进yolov5.

3. ultralytics/cfg/models/yolo-detr/yolov5-detr-fasternet.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)改进yolov5.(支持替换其他主干,请看百度云视频-替换主干示例教程)

4. ultralytics/cfg/models/yolo-detr/yolov5-detr-AIFI-LPE.yaml

    使用RT-DETR中的TransformerDecoderHead和LearnedPositionalEncoding改进yolov5.(详细介绍请看百度云视频-20231119更新说明)

5. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DCNV2.yaml

    使用RT-DETR中的TransformerDecoderHead和可变形卷积DCNV2改进yolov5.

6. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DCNV3.yaml

    使用RT-DETR中的TransformerDecoderHead和可变形卷积[DCNV3 CVPR2023](https://github.com/OpenGVLab/InternImage)改进yolov5.(安装教程请看百度云视频-20231119更新说明)

7. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DCNV2-Dynamic.yaml

    使用RT-DETR中的TransformerDecoderHead和自研可变形卷积DCNV2-Dynamic改进yolov5.(详细介绍请看百度云视频-MPCA与DCNV2_Dynamic的说明)

8. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Ortho.yaml(详细介绍请看百度云视频-20231119更新说明)

    使用RT-DETR中的TransformerDecoderHead和[OrthoNets](https://github.com/hady1011/OrthoNets/tree/main)中的正交通道注意力改进yolov5.

9. ultralytics/cfg/models/yolo-detr/yolov5-detr-attention.yaml

    添加注意力到基于RTDETR-Head中的yolov5中.(手把手教程请看百度云视频-手把手添加注意力教程)

10. ultralytics/cfg/models/yolo-detr/yolov5-detr-p2.yaml

    添加小目标检测头P2到TransformerDecoderHead中.

11. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DySnake.yaml

    [DySnakeConv](https://github.com/YaoleiQi/DSCNet)与C3融合.  

12. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Faster.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中的Faster-Block改进yolov5.

13. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Faster-Rep.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv二次创新后的Faster-Block-Rep改进yolov5.

14. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Faster-EMA.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)二次创新后的Faster-Block-EMA的Faster-Block-EMA改进yolov5.

15. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Faster-Rep-EMA.yaml

    使用RT-DETR中的TransformerDecoderHead和[FasterNet CVPR2023](https://github.com/JierunChen/FasterNet)中与[RepVGG CVPR2021](https://github.com/DingXiaoH/RepVGG)中的RepConv、[EMA ICASSP2023](https://arxiv.org/abs/2305.13563v1)二次创新后的Faster-Block改进yolov5.

16. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-AKConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[AKConv 2023](https://github.com/CV-ZhangXin/AKConv)改进yolov5.

17. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFAConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov5.

18. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFCAConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov5.

19. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-RFAConv.yaml

    使用RT-DETR中的TransformerDecoderHead和[RFCBAMConv 2023](https://github.com/Liuchen1997/RFAConv)改进yolov5.

20. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Conv3XC.yaml

    使用RT-DETR中的TransformerDecoderHead和[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的Conv3XC改进yolov5.

21. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-SPAB.yaml

    使用RT-DETR中的TransformerDecoderHead和[Swift Parameter-free Attention Network](https://github.com/hongyuanyu/SPAN/tree/main)中的SPAB改进yolov5.

22. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DRB.yaml

    使用RT-DETR中的TransformerDecoderHead和[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock改进改进yolov5.

23. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-UniRepLKNetBlock.yaml

    使用RT-DETR中的TransformerDecoderHead和[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的UniRepLKNetBlock改进改进yolov5.

24. ultralytics/cfg/models/yolo-detr/yolov5-detr-DWR-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[DWRSeg](https://arxiv.org/abs/2212.01173)中的Dilation-wise Residual(DWR)进行二次创新改进yolov5.

25. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DBB.yaml

    使用RT-DETR中的TransformerDecoderHead和[DiverseBranchBlock CVPR2021](https://github.com/DingXiaoH/DiverseBranchBlock)改进yolov5.

26. ultralytics/cfg/models/yolo-detr/yolov5-detr-CSP-EDLAN.yaml

    使用RT-DETR中的TransformerDecoderHead和[DualConv](https://github.com/ChipsGuardian/DualConv)打造CSP Efficient Dual Layer Aggregation Networks改进yolov5.

27. ultralytics/cfg/models/yolo-detr/yolov5-detr-ASF.yaml

    使用RT-DETR中的TransformerDecoderHead和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion改进yolov5.

28. ultralytics/cfg/models/yolo-detr/yolov5-detr-ASF-P2.yaml

    在ultralytics/cfg/models/yolo-detr/yolov5-detr-ASF.yaml的基础上进行二次创新，引入P2检测层并对网络结构进行优化.

29. ultralytics/cfg/models/yolo-detr/yolov5-detr-slimneck.yaml

    使用RT-DETR中的TransformerDecoderHead和[SlimNeck](https://github.com/AlanLi1997/slim-neck-by-gsconv)中VoVGSCSP\VoVGSCSPC和GSConv改进yolov5的neck.

30. ultralytics/cfg/models/yolo-detr/yolov5-detr-slimneck-asf.yaml

    在ultralytics/cfg/models/yolo-detr/yolov5-detr-slimneck.yaml使用[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion进行二次创新.

31. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-AggregatedAtt.yaml

    使用RT-DETR中的TransformerDecoderHead和[TransNeXt](https://github.com/DaiShiResearch/TransNeXt)中的聚合感知注意力改进C3.(百度云视频-20240106更新说明)

32. ultralytics/cfg/models/yolo-detr/yolov5-detr-SDI.yaml

    使用RT-DETR中的TransformerDecoderHead和[U-NetV2](https://github.com/yaoppeng/U-Net_v2)中的 Semantics and Detail Infusion Module对yolov5中的feature fusion进行改进.

33. ultralytics/cfg/models/yolo-detr/yolov5-detr-goldyolo.yaml

    利用RT-DETR中的TransformerDecoderHead和华为2023最新GOLD-YOLO中的Gatherand-Distribute进行改进特征融合模块.

34. ultralytics/cfg/models/yolo-detr/yolov5-detr-goldyolo-asf.yaml

    利用RT-DETR中的TransformerDecoderHead和华为2023最新GOLD-YOLO中的Gatherand-Distribute和[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion进行改进特征融合模块.

35. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DCNV4.yaml

    使用[DCNV4](https://github.com/OpenGVLab/DCNv4)改进C3.

36. ultralytics/cfg/models/yolo-detr/yolov5-detr-HSFPN.yaml

    利用RT-DETR中的TransformerDecoderHead和使用[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN改进YOLOV5中的PAN.

37. ultralytics/cfg/models/yolo-detr/yolov5-detr-HSPAN.yaml

    利用RT-DETR中的TransformerDecoderHead和对[MFDS-DETR](https://github.com/JustlfC03/MFDS-DETR)中的HS-FPN进行二次创新后得到HSPAN改进YOLOV5中的PAN.

38. ultralytics/cfg/models/yolo-detr/yolov8-detr-Dysample.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进yolov8-detr neck中的上采样.

39. ultralytics/cfg/models/yolo-detr/yolov8-detr-CARAFE.yaml

    使用[ICCV2019 CARAFE](https://arxiv.org/abs/1905.02188)改进yolov8-detr neck中的上采样.

40. ultralytics/cfg/models/yolo-detr/yolov8-detr-HWD.yaml

    使用[Haar wavelet downsampling](https://www.sciencedirect.com/science/article/abs/pii/S0031320323005174)改进yolov8-detr neck的下采样.

41. ultralytics/cfg/models/yolo-detr/yolov5-detr-ASF-Dynamic.yaml

    使用[ICCV2023 DySample](https://arxiv.org/abs/2308.15085)改进[ASF-YOLO](https://github.com/mkang315/ASF-YOLO)中的Attentional Scale Sequence Fusion的上采样模块得到Dynamic Sample Attentional Scale Sequence Fusion改进yolov5-detr中的neck.

42. ultralytics/cfg/models/yolo-detr/yolov5-detr-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)改进yolov5-detr中的C3.

43. ultralytics/cfg/models/yolo-detr/yolov5-detr-iRMB-DRB.yaml

    使用[UniRepLKNet](https://github.com/AILab-CVC/UniRepLKNet/tree/main)中的DilatedReparamBlock对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进yolov5-detr中的C2f.

44. ultralytics/cfg/models/yolo-detr/yolov5-detr-iRMB-SWC.yaml

    使用[shift-wise conv](https://arxiv.org/abs/2401.12736)对[EMO ICCV2023](https://github.com/zhangzjn/EMO)中的iRMB进行二次创新来改进yolov5-detr中的C2f.

45. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-VSS.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)对C3中的BottleNeck进行改进,使其能更有效地捕获图像中的复杂细节和更广泛的语义上下文.

46. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-LVMB.yaml

    使用最新的Mamba架构[Mamba-UNet中的VSS](https://github.com/ziyangwang007/Mamba-UNet)与Cross Stage Partial进行结合,使其能更有效地捕获图像中的复杂细节和更广泛的语义上下文.

47. ultralytics/cfg/models/yolo-detr/yolov5-detr-RepNCSPELAN.yaml

    使用[YOLOV9](https://github.com/WongKinYiu/yolov9)中的RepNCSPELAN进行改进yolov5-detr.

48. ultralytics/cfg/models/yolo-detr/yolov5-detr-bifpn.yaml

    添加BIFPN到yolov8中.  
    其中BIFPN中有三个可选参数：
    1. Fusion  
        其中BIFPN中的Fusion模块支持五种: weight, adaptive, concat, bifpn(default), SDI  
        其中weight, adaptive, concat出自[paper链接-Figure 3](https://openreview.net/pdf?id=q2ZaVU6bEsT), SDI出自[U-NetV2](https://github.com/yaoppeng/U-Net_v2)
    2. node_mode  
        block模块选择,具体可看对应百度云视频-20240302更新公告.
    3. head_channel  
        BIFPN中的通道数,默认设置为256.

49. ultralytics/cfg/models/yolo-detr/yolov5-detr-C2f-ContextGuided.yaml

    使用[CGNet](https://github.com/wutianyiRosun/CGNet/tree/master)中的Light-weight Context Guided和Light-weight Context Guided DownSample改进yolov5-detr.

50. ultralytics/cfg/models/yolo-detr/yolov5-detr-PACAPN.yaml

    自研结构, Parallel Atrous Convolution Attention Pyramid Network, PAC-APN

51. ultralytics/cfg/models/yolo-detr/yolov5-detr-DGCST.yaml

    使用[Lightweight Object Detection](https://arxiv.org/abs/2403.01736)中的Dynamic Group Convolution Shuffle Transformer改进yolov5-detr.

52. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-RetBlock.yaml

    使用[CVPR2024 RMT](https://arxiv.org/abs/2309.11523)中的RetBlock改进C3.

53. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-PKI.yaml

    使用[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的PKIModule和CAA模块改进C3.

54. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-fadc.yaml

    使用[CVPR2024 Frequency-Adaptive Dilated Convolution](https://github.com/Linwei-Chen/FADC)改进C3.

55. ultralytics/cfg/models/yolo-detr/yolov5-detr-FDPN.yaml

    自研特征聚焦扩散金字塔网络(Focusing Diffusion Pyramid Network)
    1. 通过定制的特征聚焦模块与特征扩散机制，能让每个尺度的特征都具有详细的上下文信息，更有利于后续目标的检测与分类。
    2. 定制的特征聚焦模块可以接受三个尺度的输入，其内部包含一个Inception-Style的模块，其利用一组并行深度卷积来捕获丰富的跨多个尺度的信息。
    3. 通过扩散机制使具有丰富的上下文信息的特征进行扩散到各个检测尺度.

56. ultralytics/cfg/models/yolo-detr/yolov5-detr-FDPN-DASI.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Dimension-Aware Selective Integration Module对自研的Focusing Diffusion Pyramid Network再次创新.

57. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-PPA.yaml

    使用[HCFNet](https://github.com/zhengshuchen/HCFNet)中的Parallelized Patch-Aware Attention Module改进C3.

58. ultralytics/cfg/models/yolo-detr/yolov5-detr-SRFD.yaml

    使用[A Robust Feature Downsampling Module for Remote Sensing Visual Tasks](https://ieeexplore.ieee.org/document/10142024)改进yolov5的下采样.

59. ultralytics/cfg/models/yolo-detr/yolov5-detr-CSFCN.yaml

    使用[Context and Spatial Feature Calibration for Real-Time Semantic Segmentation](https://github.com/kaigelee/CSFCN/tree/main)中的Context and Spatial Feature Calibration模块改进yolov5.

60. ultralytics/cfg/models/yolo-detr/yolov5-detr-CGAFusion.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的content-guided attention fusion改进yolov5-neck.

61. ultralytics/cfg/models/yolo-detr/yolov5-detr-CAFMFusion.yaml

    利用具有[HCANet](https://github.com/summitgao/HCANet)中的CAFM，其具有获取全局和局部信息的注意力机制进行二次改进content-guided attention fusion.
 
62. ultralytics/cfg/models/yolo-detr/yolov5-detr-RGCSPELAN.yaml

    自研RepGhostCSPELAN.
    1. 参考GhostNet中的思想(主流CNN计算的中间特征映射存在广泛的冗余)，采用廉价的操作生成一部分冗余特征图，以此来降低计算量和参数量。
    2. 舍弃yolov5与yolov8中常用的BottleNeck，为了弥补舍弃残差块所带来的性能损失，在梯度流通分支上使用RepConv，以此来增强特征提取和梯度流通的能力，并且RepConv可以在推理的时候进行融合，一举两得。
    3. 可以通过缩放因子控制RGCSPELAN的大小，使其可以兼顾小模型和大模型。

63. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Faster-CGLU.yaml

    使用[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt)中的Convolutional GLU对CVPR2023中的FasterNet进行二次创新.

64. ultralytics/cfg/models/yolo-detr/yolov5-detr-SDFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的superficial detail fusion module改进yolov5-neck.

65. ultralytics/cfg/models/yolo-detr/yolov5-detr-PSFM.yaml

    使用[PSFusion](https://github.com/Linfeng-Tang/PSFusion)中的profound semantic fusion module改进yolov5-neck.

66. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Star.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock改进C3.

67. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-Star-CAA.yaml

    使用[StarNet CVPR2024](https://github.com/ma-xu/Rewrite-the-Stars/tree/main)中的StarBlock和[CVPR2024 PKINet](https://github.com/PKINet/PKINet)中的CAA改进C3.

68. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-KAN.yaml

    使用[Pytorch-Conv-KAN](https://github.com/IvanDrokin/torch-conv-kan)的KAN卷积算子改进C3.
    目前支持:
    1. FastKANConv2DLayer
    2. KANConv2DLayer
    3. KALNConv2DLayer
    4. KACNConv2DLayer
    5. KAGNConv2DLayer

69. ultralytics/cfg/models/yolo-detr/yolov5-detr-ContextGuideFPN.yaml

    Context Guide Fusion Module（CGFM）是一个创新的特征融合模块，旨在改进YOLOv8中的特征金字塔网络（FPN）。该模块的设计考虑了多尺度特征融合过程中上下文信息的引导和自适应调整。
    1. 上下文信息的有效融合：通过SE注意力机制，模块能够在特征融合过程中捕捉并利用重要的上下文信息，从而增强特征表示的有效性，并有效引导模型学习检测目标的信息，从而提高模型的检测精度。
    2. 特征增强：通过权重化的特征重组操作，模块能够增强重要特征，同时抑制不重要特征，提升特征图的判别能力。
    3. 简单高效：模块结构相对简单，不会引入过多的计算开销，适合在实时目标检测任务中应用。
    这期视频讲解在B站:https://www.bilibili.com/video/BV1Vx4y1n7hZ/

70. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-DEConv.yaml

    使用[DEA-Net](https://github.com/cecret3350/DEA-Net)中的detail-enhanced convolution改进C3.
    关于DEConv在运行的时候重参数化后比重参数化前的计算量还要大的问题:是因为重参数化前thop库其计算不准的问题,看重参数化后的参数即可.

71. ultralytics/cfg/models/yolo-detr/yolov5-detr-C3-SMPCGLU.yaml

    Self-moving Point Convolutional GLU模型改进C3.
    SMP来源于[CVPR2023-SMPConv](https://github.com/sangnekim/SMPConv),Convolutional GLU来源于[TransNeXt CVPR2024](https://github.com/DaiShiResearch/TransNeXt).
    1. 普通的卷积在面对数据中的多样性和复杂性时，可能无法捕捉到有效的特征，因此我们采用了SMPConv，其具备最新的自适应点移动机制，从而更好地捕捉局部特征，提高特征提取的灵活性和准确性。
    2. 在SMPConv后添加CGLU，Convolutional GLU 结合了卷积和门控机制，能够选择性地通过信息通道，提高了特征提取的有效性和灵活性。
    3. 这种类似Transformer的encoder结构，利用DEConv进行特征提取，CGLU可以进一步的非线性变换和加强特征提取，提升模型的表达能力。

### IoU系列

更换教程可看
1. IoU,GIoU,DIoU,CIoU,EIoU,SIoU(百度云视频-20231125更新说明)
2. MPDIoU[论文链接](https://arxiv.org/pdf/2307.07662.pdf)(百度云视频-20231125更新说明)
3. Inner-IoU,Inner-GIoU,Inner-DIoU,Inner-CIoU,Inner-EIoU,Inner-SIoU[论文链接](https://arxiv.org/abs/2311.02877)(百度云视频-20231125更新说明)
4. Inner-MPDIoU(利用Inner-Iou与MPDIou进行二次创新)(百度云视频-20231125更新说明)
5. Normalized Gaussian Wasserstein Distance.[论文链接](https://arxiv.org/abs/2110.13389)(百度云视频-20231125更新说明)
6. Shape-IoU,Inner-Shape-IoU[论文链接](https://arxiv.org/abs/2110.13389)(百度云视频-20240106更新说明)
7. SlideLoss,EMASlideLoss[创新思路](https://www.bilibili.com/video/BV1W14y1i79U/?vd_source=c8452371e7ca510979593165c8d7ac27).[Yolo-Face V2](https://github.com/Krasjet-Yu/YOLO-FaceV2/blob/master/utils/loss.py)(百度云视频-20240113更新说明)
8. Wise-IoU(v1,v2,v3)系列(IoU,WIoU,EIoU,GIoU,DIoU,CIoU,SIoU,MPDIoU,ShapeIoU)(百度云视频-20240113更新说明)
9. Inner-Wise-IoU(v1,v2,v3)系列(IoU,WIoU,EIoU,GIoU,DIoU,CIoU,SIoU,MPDIoU,ShapeIoU)(百度云视频-20240113更新说明)
10. Focaler-IoU,Focaler-GIoU,Focaler-DIoU,Focaler-CIoU,Focaler-EIoU,Focaler-SIoU,Focaler-Shape-IoU,Focaler-MPDIoU[论文链接](https://arxiv.org/abs/2401.10525)(百度云视频-20240128更新说明)
11. Focaler-Wise-IoU(v1,v2,v3)(IoU,WIoU,EIoU,GIoU,DIoU,CIoU,SIoU,MPDIoU,ShapeIoU)[论文链接](https://arxiv.org/abs/2401.10525)(百度云视频-20240128更新说明)
12. Powerful-IoU,Powerful-IoUV2,Inner-Powerful-IoU,Inner-Powerful-IoUV2,Focaler-Powerful-IoU,Focaler-Powerful-IoUV2,Wise-Powerful-IoU(v1,v2,v3),Wise-Powerful-IoUV2(v1,v2,v3)[论文链接](https://www.sciencedirect.com/science/article/abs/pii/S0893608023006640)(百度云视频-20240219更新说明)
13. SlideVarifocalLoss,EMASlideVarifocalLoss[创新思路](https://www.bilibili.com/video/BV1W14y1i79U/?vd_source=c8452371e7ca510979593165c8d7ac27).[Yolo-Face V2](https://github.com/Krasjet-Yu/YOLO-FaceV2/blob/master/utils/loss.py)(百度云视频-20240302更新说明)

# 怎么像yolov5那样输出每一层的参数,计算量？
参考main_profile.py,选择自己的配置文件路径即可

# 如何替换主干？
可以看项目视频-替换主干示例教程.

# 如何绘制曲线对比图?
在plot_result.py中的names指定runs/train中的训练结果名字name即可.  
比如目前runs/train中有exp,exp1,exp2这三个文件夹,plot_result.py中names中的值为:['exp', 'exp1', 'exp2'],运行后会自动保存为metrice_curve.png和loss_curve.png在当前运行的目录下.
各种不同类型的模型曲线对比图和精度对比图也可以看这期视频：https://www.bilibili.com/video/BV1yf421X7t5/

# 如何计算COCO指标?
可以看项目视频-计算COCO指标教程.  
python dataset/yolo2coco.py --image_path dataset/images/test --label_path dataset/labels/test  
python get_COCO_metrice.py --pred_json runs/val/exp/predictions.json --anno_json data.json  
新旧版的差异就在于 predictions.json的生成方式,新版就是在val.py中把save_json设置为True即可

# 常见错误和解决方案(如果是跑自带的一些配置文件报错可以先看看第十大点对应的配置文件是否有提示需要修改内容)
1. RuntimeError: xxxxxxxxxxx does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True)'.....

    解决方案：在ultralytics/utils/torch_utils.py中init_seeds函数中把torch.use_deterministic_algorithms里面的True改为False

2. ModuleNotFoundError：No module named xxx

    解决方案：缺少对应的包，先把YOLOV8环境配置的安装命令进行安装一下，如果还是缺少显示缺少包，安装对应的包即可(xxx就是对应的包).

3. OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.  

    解决方案：https://zhuanlan.zhihu.com/p/599835290

<a id="a"></a>

4. 多卡训练问题.[参考链接](https://docs.ultralytics.com/yolov5/tutorials/multi_gpu_training/#multi-gpu-dataparallel-mode-not-recommended:~:text=just%201%20GPU.-,Multi%2DGPU%20DistributedDataParallel%20Mode%20(%E2%9C%85%20recommended),-You%20will%20have)

    python -m torch.distributed.run --nproc_per_node 2 train.py

5. 指定显卡训练.

    1. 使用device参数进行指定.  
    2. 参考链接:https://blog.csdn.net/m0_55097528/article/details/130323125, 简单来说就是用这个来代替device参数.  

6. ValueError: Expected more than 1 value per channel when training, got input size torch.Size...

    如果是在训练情况下的验证阶段出现的话,大概率就是最后一个验证的batch为1,这种情况只需要把验证集多一张或者少一张即可,或者变更batch参数.

7. AttributeError: Can't pickle local object 'EMASlideLoss.__init__.<locals>.<lambda>'

    可以在ultralytics/utils/loss.py中添加import dill as pickle,然后装一下dill这个包.  
    pip install dill -i https://pypi.tuna.tsinghua.edu.cn/simple

8. RuntimeError: Dataset 'xxxxx' error ❌

    将data.yaml中的路径都改为绝对路径.

9. AttributeError: Can't pickle local object 'EMASlideLoss.__init__.<locals>.<lambda>'

    可以在ultralytics/utils/loss.py中添加import dill as pickle,然后装一下dill这个包.  
    pip install dill -i https://pypi.tuna.tsinghua.edu.cn/simple

10. RuntimeError: Dataset 'xxxxx' error ❌

    将data.yaml中的路径都改为绝对路径.

11. WARNING  NMS time limit 2.100s exceeded

    在ultralytics/utils/ops.py中non_max_suppression函数里面找到这个语句：
        time_limit = 2.0 + max_time_img * bs  # seconds to quit after
    前面的2.0自己改大点即可，大到不会出现这个NMS time limit即可.

12. OSError: [WinError 1455] 页面文件太小，无法完成操作。

    此问题常见于windows训练.一般情况下有两种解决方案:
    1. 把workers设置小点直接不会报错.最小为0
    2. 扩大虚拟内存(可百度).

# 常见疑问
1. Fuse指的是什么？

    Fuse是指模型的一些模块进行融合,最常见的就是conv和bn层进行融合,在训练的时候模型是存在conv和bn的,但在推理的过程中,模型在初始化的时候会进行模型fuse,把其中的conv和bn进行融合,通过一些数学转换把bn层融合到conv里面,还有一些例如DBB,RepVGG等等模块支持融合的,这些在fuse阶段都会进行融合,融合后可以一般都可以得到比融合前更快的推理速度,而且基本不影响精度.

2. FPS如何计算？

    1. 在运行val.py后最后会出来Speed: 0.1ms preprocess, 5.4ms inference, 0.0ms loss, 0.4ms postprocess per image这行输出,这行输出就代表了每张图的前处理,推理,loss,后处理的时间,当然在val.py过程中是不需要计算loss的,所以为0,FPS最严谨来说就是1000(1s)/(preprocess+inference+postprocess),没那么严谨的话就是只除以inference的时间,还有一个问题就是batchsize应该设置为多少,其实这行输出就已经是每张图的时间了,但是batchsize还是会对这个时间有所影响,主要是关于并行处理的问题,GPU中可以一次处理多个batch的数据,也可以只处理一个数据,但是处理多batch的数据比处理一个数据的时候整体速度要快,举个例子,比如我有1000张图,我分别设置batchsize为32和batchsize为1,整体运行的时间百分之99都是batchsize为32的快,因此这就导致不同batch输出的时间不同,至于该设置多少来计算FPS,貌似众说纷纭,所以这里我也不好给意见.  
    附上yolov5作者对于FPS和Batch的一个实验链接: https://github.com/ultralytics/yolov5/discussions/6649
    2. 项目中的get_FPS.py是只算推理时间.
    3. batch问题,比如你设置为16,那所有对比的模型都在同一个batch来计算即可.
    4. 小模型尽量要大bs(16,32)测.

3. 训练的时候出现两次结构打印是什么情况?

    第一次打印的和第二次打印的主要不同地方就是类别数,第一次打印的是yaml配置文件中的nc参数的类别数的结构,第二次打印的是你实际数据集类别数的结构,其差异就在类别数,实际使用的是第二次打印的结构.

4. 怎么找到对应模块的说明视频?

    1. 视频都在本项目下的项目视频百度云链接.txt,然后可以看这里的[更新公告](https://blog.csdn.net/qq_37706472/article/details/136178142)来确定哪些改进点是哪一期更新的,然后可以直接找到对应的视频链接下载看即可.
    2. 20231010之前的日期都以模块命名.
    3. 不一定所有的模块都有视频说明,看模块的复杂度.

5. 保存的模型存储大小问题.

    在训练图中看保存的模型大小是会比训练结束后的偏大,因为其会保存一些过程中的一些其他信息,但这些不会影响原本模型的参数量和计算量,等训练结束后,其会自己读取清除额外的信息.

6. 怎么指定使用哪一种大小的模型呢？

    假设我选择的配置文件是yolov8.yaml,我想选择m大小的模型,则train.py中的指定为ultralytics/cfg/models/v8/yolov8m.yaml即可,同理,如果我想指定s大小的模型,则指定为ultralytics/cfg/models/v8/yolov8s.yaml即可,如果直接设置为ultralytics/cfg/models/v8/yolov8.yaml,则默认使用n大小模型,又或者我需要使用ultralytics/cfg/models/v8/yolov8-bifpn.yaml,我需要设定为s模型,则应该为ultralytics/cfg/models/v8/yolov8s-bifpn.yaml.(V5同理)

7. 热力图使用脚本相关问题.

    1. 需要安装grad-cam==1.4.8
    2. 使用示例：https://www.bilibili.com/video/BV1fU421o7jH/  如果更换了主干还需看：https://www.bilibili.com/video/BV1F6421V77v/
    3. 进度条不满是正常现象,只要进度条不是0,都可以进行出图.

8. 怎么判断模型收敛了？模型会不会过拟合？

    1. 主要看训练结束后的result.png中的精度曲线,精度曲线没有上升的趋势就可以了.
    2. 很多场景的数据下在曲线上都会呈现像过拟合的趋势,但是代码中已经会自动保存best.pt,用best.pt可以避免训练后期过拟合导致的精度下降等等影响,简单来说就是只需要用best.pt即可,不需要理会过拟合的问题.

9. 曲线震荡问题.

    这类问题都不好解决,如果基础模型就震荡很厉害,基本都是跟数据集有关系,如果改进后的模型后出现,基本都是改进模型不合适的问题.

10. 绘制结构图问题.

    可看以下这两个视频:
    1. https://www.bilibili.com/video/BV1X94y1K76Z/
    2. https://www.bilibili.com/video/BV1WA4m1V7nQ/

11. mmcv安装问题.

    可以看官方文档：https://mmcv.readthedocs.io/en/latest/get_started/installation.html#install-with-pip
 
12. 预训练权重相关问题.

    可以看这个视频：https://www.bilibili.com/video/BV1Q1421Q7Zw/
    不载入预训练权重的话，只需要在train.py中的model.load注释即可！

13. 绘制结构图教程.

    1. [什么？你说你不会画模型结构图？行吧，那你进来看看吧，手把手教你画YAML结构图！](https://www.bilibili.com/video/BV1X94y1K76Z/)
    2. [什么？你说你更换主干后看不懂配置文件也不懂画结构图？那你快点进来看看了！](https://www.bilibili.com/video/BV1WA4m1V7nQ/)
    3. [从简到难手把手教你画Pytorch模块内的结构图！](https://www.bilibili.com/video/BV1dC411p7H7/)

14. 配置文件整合问题.

    1. [YOLOV8-不会把多个改进整合到一个yaml配置文件里面？那来看看这个吧！从简到难手把手带你整合三个yaml](https://www.bilibili.com/video/BV15H4y1Y7a2/)

15. 训练结果可重现的问题.

    1. torch版本需要大于等于1.13.1才会开启确定性训练算法.
    2. 训练中不能开启cache参数.
    3. 满足以上条件外,还要看模型中是否有不支持确定性训练算法的操作,pytorch官网也标注,即使开启确定性训练算法也不是百分百能保证训练结果的可重现性.

16. 参数详解.

    1. [训练参数官方文档地址](https://docs.ultralytics.com/modes/train/#resuming-interrupted-trainings:~:text=a%20training%20run.-,Train%20Settings,-The%20training%20settings)
    2. [验证参数官方文档地址](https://docs.ultralytics.com/modes/val/#usage-examples:~:text=of%20each%20category-,Arguments%20for%20YOLO%20Model%20Validation,-When%20validating%20YOLO)
    3. [推理参数官方文档地址](https://docs.ultralytics.com/modes/predict/#inference-sources:~:text=of%20Results%20objects-,Inference%20Arguments,-model.predict())
    4. [导出参数官方文档地址](https://docs.ultralytics.com/modes/export/#usage-examples)

17. Freezing layer 'model.22.dfl.conv.weight'

    这个是正常的，这一层就是不需要训练。

18. 为什么程序开始的时候会下载yolov8n.pt.

    这个是用于AMP混合精度训练测试用的，不是预训练权重，如果下载慢，可以自行下载后放到运行目录下，它检测到有这个文件就不会下载。

19. 为什么训练过程中显存不断在变化？有时大有时小？

    因为yolov8中的标签分配策略的问题，正常现象。

20. 如何关闭早停？

    train.py中设置patience为0.

21. 设置了epochs为300，但是发现还没有收敛，可以在300次的基础上再训练100次吗？

    不行，训练了300次后再训练100次跟一次性训练400次的结果很大概率不一样，因为它们的学习率匹配不上。

22. 我的验证集精度0.6，但是测试集精度只有0.5，这是什么问题？

    没问题，一般是由于测试集与验证集差异较大导致，如果是私有数据集可以考虑重新合并随机划分，如果是公开数据集就不用管，例如visdrone2019，验证集也跟测试集相差10个点。

23. 预测的时候在同一个目标上出现了两个框，怎么解决？

    在detect.py中设置agnostic_nms=True，原始的nms是基于每个类里面进行的，设置agnostic_nms=True就是所有目标下进行，不会细分类别，可以解决这个问题。

24. 能不能不要分测试集？

    除非是公开数据集没有测试集，否则不建议，如果到时候审稿人问到为什么你没有测试集，你没有一个合理的理由可以回复，最坏的结果是实验重做。

25. 如何可视化中间层的特征图？

    运行detect.py中并设置visualize=True.

26. 为什么yolov8-p2.yaml比yolov8.yaml参数量要小，但是计算量变大?

    正常现象,可看[github-issue链接](https://github.com/ultralytics/ultralytics/issues/7502).

27. 像项目自带的v3、v5配置文件能直接用来做模型的对比实验吗？

    不可以，因为里面用的都是v8的anchorfree的头，不是原版的模型。

28. 计算量、参数量以哪个脚本输出的为准？

    以val.py输出的结果为准，val.py输出的是重参数化后的结果，论文中以这个结果为准.

# 一些非常推荐小白看的视频链接
1. [YOLOV8模型详细讲解(包含该如何改进YOLOV8)(刚入门小白，需要改进YOLOV8的同学必看！)](https://www.bilibili.com/video/BV1Ms421u7VH/)
2. [提升多少才能发paper？轻量化需要看什么指标？需要轻量化到什么程度才能发paper？这期给大家一一解答！](https://www.bilibili.com/video/BV1QZ421M7gu/)
3. [深度学习实验部分常见疑问解答！(小白刚入门必看！少走弯路！少自我内耗！)](https://www.bilibili.com/video/BV1Bz421B7pC/)
    ```
    1. 如何衡量自己的所做的工作量够不够？
    2. 为什么别人的论文说这个模块对xxx有作用，但是我自己用的时候还掉点了？
    3. 提升是和什么模型相比呢 比如和yolov8这种基础模型比还是和别人提出的目前最好的模型比
    4. 对比不同的模型的时候，输入尺寸，学习率，学习次数这些是否需要一致？
    ```
4. [深度学习实验部分常见疑问解答二！(小白刚入门必看！少走弯路！少自我内耗！)](https://www.bilibili.com/video/BV1ZM4m1m785/)
    ```
    1. 为什么我用yolov8自带的coco8、coco128训练出来的效果很差？
    2. 我的数据集很大，机器跑得慢，我是否可以用数据集的百分之10的数据去测试这个改进点是否有效？有效再跑整个数据集？
    ```
5. [深度学习实验部分常见疑问解答三！(怎么判断模型是否收敛？模型过拟合怎么办？)](https://www.bilibili.com/video/BV11S421d76P/)
6. [YOLO系列模型训练结果详细解答！(训练过程的一些疑问，该放哪个文件运行出来的结果、参数量计算量在哪里看..等等问题)](https://www.bilibili.com/video/BV11b421J7Vx/)