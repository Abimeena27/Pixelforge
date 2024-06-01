import boto3
from PIL import Image
from io import BytesIO

def resize_image(event, context):
  # Get the S3 bucket and key from the event
  s3_record = event['Records'][0]['s3']
  bucket = s3_record['bucket']['name']
  key = s3_record['object']['key']

  # Download the image from S3
  s3_client = boto3.client('s3')
  response = s3_client.get_object(Bucket=bucket, Key=key)
  image_data = response['Body'].read()

  # Resize the image using Pillow
  image = Image.open(BytesIO(image_data))
  # Replace with desired resize method (thumbnail, resize, etc.)
  resized_image = image.resize((500, 500), Image.ANTIALIAS)  # Resize to 500x500 with antialiasing

  # Create a BytesIO object to store the resized image
  resized_data = BytesIO()
  resized_image.save(resized_data, format=image.format)
  resized_data.seek(0)

  # Upload the resized image to S3 with a different key (optional)
  resized_key = f"resized_{key}"  # Add a prefix to resized image
  s3_client.put_object(Bucket=bucket, Key=resized_key, Body=resized_data)

  # (Optional) Delete the original image (if resized stored in same bucket)
  # s3_client.delete_object(Bucket=bucket, Key=key)

  return {
      'message': f"Image {key} resized and uploaded as {resized_key}"
  }
