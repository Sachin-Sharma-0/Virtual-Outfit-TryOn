from flask import Flask, render_template, request
import os
from image_segmentation import segment_image
from pose_estimation import estimate_pose
from image_warping import warp_image
from image_composition import compose_image

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    # Handle image upload and processing logic here
    user_images = request.files.getlist('user_images[]')
    outfit_image = request.files['outfit_image']
    
    # Save the uploaded images to the appropriate location
    for i, user_image in enumerate(user_images, start=1):
        user_image.save(f"user_image_{i}.jpg")
    
    outfit_image.save("outfit_image.jpg")
    
    return 'Images uploaded successfully'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tryon', methods=['POST'])
def tryon():
    # Get the user's photos and outfit image from the form
    user_photos = request.files.getlist('user_photos')
    outfit_image = request.files['outfit_image']

    # Create a directory to store the user's uploaded photos
    os.makedirs('uploads', exist_ok=True)

    # Save the user's photos and outfit image
    user_photo_paths = []
    for i, photo in enumerate(user_photos):
        photo_path = f'uploads/user_photo_{i}.jpg'
        photo.save(photo_path)
        user_photo_paths.append(photo_path)

    outfit_image_path = 'uploads/outfit_image.jpg'
    outfit_image.save(outfit_image_path)

    # Perform image segmentation on the user's photos
    segmented_photos = []
    for photo_path in user_photo_paths:
        segmented_photo = segment_image(photo_path)
        segmented_photos.append(segmented_photo)

    # Estimate the pose of the user in the segmented photos
    pose_keypoints = []
    for segmented_photo in segmented_photos:
        pose_keypoint = estimate_pose(segmented_photo)
        pose_keypoints.append(pose_keypoint)

    # Warp the outfit image to match the user's pose
    warped_outfit = warp_image(outfit_image_path, pose_keypoints)

    # Compose the warped outfit with the segmented photos
    final_images = []
    for segmented_photo, pose_keypoint in zip(segmented_photos, pose_keypoints):
        final_image = compose_image(segmented_photo, warped_outfit, pose_keypoint)
        final_images.append(final_image)

    # Render the result page with the final images
    return render_template('result.html', final_images=final_images)

if __name__ == '__main__':
    app.run(debug=True)
