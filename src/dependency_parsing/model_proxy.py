import os
from statistics import mode
import gdown
import zipfile


class ModelProxy:
    file_id = {
        "FR_GSD-ID_CSUI": "1tg3qNum3Q97-ogBJbXeSqwEdV38kN1hu",
        "IT_ISDT-ID_CSUI": "1K4-mwq9CwHjoIHfGksUUVghP35oyUB8b",
        "SL_SSJ-ID_CSUI": "1jzIJMUWbuueMOWHklQthQAzHVKw4tacT",
        "EN_GUM-ID_CSUI": "1PmzgzT4F5_gBUtMPE8ZEJNGJOTjkc9tj",
        "FR_GSD-ID_GSD": "1bpJsiPwRI09PwA8FdH1L7n1BPw4WbLGw",
        "IT_ISDT-ID_GSD": "1n8VE-LiKkdsUvyNvREK0IEVoNIZ0mn5b",
        "SL_SSJ-ID_GSD": "1IoAYZdKkKCHR4-azXQsg2gQrAX-vtPuR",
        "EN_GUM-ID_GSD": "1JXwgsMwkhfRtvNx9q6hGH-izyA8f-mph",
    }

    def download_model(model_name):
        if model_name not in ModelProxy.file_id:
            print(model_name)
            raise NotImplementedError

        url = "https://drive.google.com/uc?id={}".format(ModelProxy.file_id[model_name])
        output_dir = os.path.join(os.getcwd(), "src", "dependency_parsing", ".pretrained_model")
        output_file = os.path.join(output_dir, "{}.zip".format(model_name))
        gdown.download(url, output_file, quiet=True)

        with zipfile.ZipFile(output_file, "r") as zip_ref:
            zip_ref.extractall(output_dir)
