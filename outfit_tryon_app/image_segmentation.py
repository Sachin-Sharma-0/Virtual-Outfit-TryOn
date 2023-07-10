import cv2
import numpy as np
from mrcnn import utils, model as modellib
from mrcnn.config import Config
import coco

# Load the configuration
config = coco.CocoConfig()

# Create the Mask R-CNN model
model = modellib.MaskRCNN(mode="inference", config=config, model_dir="logs")

# Load the pre-trained weights
model.load_weights("mask_rcnn_coco.h5", by_name=True)

def segment_image(image_path):

    # Load and preprocess the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform image segmentation
    segmented_image = model.segment(image)

    return segmented_image


# Load the pre-trained Mask R-CNN model
model = modellib.MaskRCNN(mode="inference", config=config, model_dir="logs")
model.load_weights("mask_rcnn_coco.h5", by_name=True)

# Load and preprocess the user's photo
user_photo = cv2.imread("user_photo.jpg")
user_photo = cv2.cvtColor(user_photo, cv2.COLOR_BGR2RGB)

# Run the segmentation on the user's photo
results = model.detect([user_photo], verbose=1)
r = results[0]

# Extract the masked region (body) from the user's photo
mask = r['masks'][:, :, 0]
segmented_image = cv2.bitwise_and(user_photo, user_photo, mask=mask.astype(np.uint8))

# Display the segmented image
cv2.imshow("Segmented Image", segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
