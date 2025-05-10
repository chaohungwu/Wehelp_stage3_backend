import os
from dotenv import load_dotenv
import boto3
from datetime import datetime


AWS_S3_access_key = os.getenv("AWS_S3_access_key")
AWS_S3_secret_access_key = os.getenv("AWS_S3_secret_access_key")
AWS_S3_bucket_name = os.getenv("AWS_S3_bucket_name")
region_name = os.getenv("region_name")



s3 = boto3.client('s3')
s3_client = boto3.client(
                    "s3",
                    aws_access_key_id = AWS_S3_access_key,
                    aws_secret_access_key = AWS_S3_secret_access_key,
                    region_name = region_name,
                    )



class s3_function:
    def __init__(self):
        pass

    async def UploadImgToS3(self, img_file):
        currentDateAndTime = datetime.now()

        file_bytes = await img_file.read()
        file_name = img_file.filename
        
        # 上傳本地檔案到 S3
        bucket_name = AWS_S3_bucket_name

        s3_key = "messageboard_img/{}_{}_{}_{}_{}_{}_{}".format(currentDateAndTime.year,
                                                                currentDateAndTime.month,
                                                                currentDateAndTime.day,
                                                                currentDateAndTime.hour,
                                                                currentDateAndTime.minute,
                                                                currentDateAndTime.second,
                                                                file_name)

        s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_bytes,
                # ACL="public-read",
                ContentType=img_file.content_type 
        )

        image_url = f"https://d2uqyos5dxmh9l.cloudfront.net/{s3_key}"


        return {"img_path":image_url,"message":"ok"}