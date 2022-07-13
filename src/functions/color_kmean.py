try:
    import unzip_requirements
except ImportError:
    pass

import boto3, os, json
from src.lib.wrapper import functionWrapper
from botocore.config import Config
import numpy as np
import scipy.cluster
from PIL import Image
import cv2


KMEANED_IMAGE_BUCKET = os.getenv("KMEANED_IMAGE_BUCKET", "")
REGION_NAME = os.getenv("REGION_NAME", "")
USER_TABLE = os.getenv('USER_TABLE', '')


#s3から画像をダウンロードする
def get_s3_image(
    name: str,
    bucket_name: str,
    region_name: str = 'ap-northeast-1',
    ) -> bytes:
    session = boto3.session.Session(region_name=region_name)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    res = bucket.Object(name).get()
    check_return(res, "GetS3Object")
    return res.get('Body').read()


# DynamoDBに新しく要素を追加
def put_item(
        item: dict,
        table_name: str
) -> None:
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    table = dynamodb.Table(table_name)
    res = table.put_item(Item=item)


# DynamoDBからデータを取得
def get_item(
    user_id: str,
    table_name: str
) -> Dict:
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    table = dynamodb.Table(table_name)
    res = table.get_item(
        Key={'id': user_id}
    )
    # check_return(res, "getDynamoItem")

    # return res['Item']
    return res


# 画像からk平均法を用いてよく使われている色を5色抽出する
def kmean(img, cluster_count):
    img = Image.open(img_path)
    img_small = img.resize((100, 100))
    color_arr = np.array(img_small)
    w_size, h_size, n_color = color_arr.shape
    color_arr = color_arr.reshape(w_size * h_size, n_color)
    color_arr = color_arr.astype(np.float)
    codebook, distortion = scipy.cluster.vq.kmeans(color_arr, cluster_count)

    colors = []
    RGBs = []
    for col in codebook:# 色数ループ
        RGB = []# RGB値が十進数で3つ入る
        for primary_color in col.astype(int):# RGBループ
            RGB.append(primary_color.item())# .item()は、[numpy.int64]型から[int]型へ変換してる
        color = "#{:x}{:x}{:x}".format(RGB[0], RGB[1], RGB[2])# RGBを16進数(#000000)の文字列で表示
        print(color)
        print(RGB)
        colors.append(color)
        RGBs.append(RGB)

    return colors, RGBs


@functionWrapper
def main(event, context):
    print(event)
    cluster_count = 5

    if 'Records' in event.keys():
        download_key = event['Records'][0]['s3']['object']['key']
        print('id :', id)

        # 解析前画像をs3からダウンロード
        img_str = get_s3_image(download_key, FACE_IMAGE_BUCKET, REGION_NAME)
        img = cv2.imdecode(
            np.asarray(bytearray(face_img_str)), cv2.IMREAD_COLOR)

        colors, RGBs = kmean(img, cluster_count)

        body = {
            "color0":colors[0],
            "color1":colors[1],
            "color2":colors[2],
            "color3":colors[3],
            "color4":colors[4]
        }
    else:
        raise BaseException
    return body
