import cv2
import torch
from argparse import ArgumentParser
from torchvision.models import alexnet, densenet121, efficientnet_b0, mobilenet_v3_small, resnet50, squeezenet1_1, vgg11, \
    AlexNet_Weights, DenseNet121_Weights, EfficientNet_B0_Weights, MobileNet_V3_Small_Weights, ResNet50_Weights, SqueezeNet1_1_Weights, VGG11_Weights

models = {"AlexNet": (alexnet, AlexNet_Weights), "DenseNet-121": (densenet121, DenseNet121_Weights), "EfficientNet-b0": (efficientnet_b0, EfficientNet_B0_Weights), "Mobilenet-v3": (mobilenet_v3_small, MobileNet_V3_Small_Weights), "ResNet-50": (resnet50, ResNet50_Weights), "SqueezeNet-v1.1": (squeezenet1_1, SqueezeNet1_1_Weights), "VGG-11": (vgg11, VGG11_Weights)}

if __name__ == "__main__":
    # get image filename
    parser = ArgumentParser()
    parser.add_argument("IMAGE", help="image to classify")
    args = parser.parse_args()
    filename = args.IMAGE
    
    # load image as a tensor
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    image = torch.tensor(image).permute((2, 0, 1))

    print(f"{'Name':<20}{'Class':<20}Score")
    for name, (model, weights) in models.items():
        # load model in evaluation mode
        model = model(weights=weights.DEFAULT)
        model.eval()

        # preprocess image
        preprocess = weights.DEFAULT.transforms()
        preprocess.resize_size = 224
        preprocess.crop_size = 224
        batch = preprocess(image).unsqueeze(0)

        # get target class and score
        prediction = model(batch).squeeze(0).softmax(0)
        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        category_name = weights.DEFAULT.meta["categories"][class_id]

        # print results
        print(f"{name:<20}{category_name:<20}{100 * score:.1f}%")
