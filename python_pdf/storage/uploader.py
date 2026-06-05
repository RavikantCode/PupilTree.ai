import os
import shutil
from dotenv import load_dotenv
load_dotenv()


class LocalUploader:
    def upload(self, local_path: str, name: str) -> str:
        return local_path

class CloudinaryUploader:
    def __init__(self):
        import cloudinary
        import cloudinary.uploader
        self._uploader = cloudinary
        uploader
        cloudinary.config(
            cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
            api_key=os.environ["CLOUDINARY_API_KEY"],
            api_secret=os.environ["CLOUDINARY_API_SECRET"],
        )

    def upload(self, local_path: str, name: str) -> str:
        result = self._uploader.upload(
            local_path,
            public_id=name,
            folder="pupiltree_exam",
            resource_type="image",
        )
        return result["secure_url"]

def get_uploader():
    if os.environ.get("USE_CLOUDINARY"):
        return CloudinaryUploader()
    return LocalUploader()