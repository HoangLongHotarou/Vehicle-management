from facenet_pytorch import MTCNN, InceptionResnetV1, fixed_image_standardization, training
import torch
from torchvision import datasets, transforms
from core.config import settings
import numpy as np
import os
import cv2
from PIL import Image
import hnswlib
# import tqdm


class FaceRecognition():
    def __init__(self, gpu=False):
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() and gpu else 'cpu')
        self.mtcnn = MTCNN(
            thresholds=[0.7, 0.7, 0.8], keep_all=True, device=self.device)
        self.mtcnn_one_box = MTCNN(
            thresholds=[0.7, 0.7, 0.8], keep_all=False, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        self.max_elements = settings.MAX_ELEMENTS
        self.p = None
        self.trans_data_augmentation = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(
                brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        self.trans_default = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    def trans_for_train(self, img):
        return self.trans_data_augmentation(img).unsqueeze(0)

    def trans_for_recognition(self, img):
        return self.trans_default(img).unsqueeze(0)

    def train(self, url):
        vicap = cv2.VideoCapture(url)
        success = True
        count = 0
        embs = []
        while success:
            success, image = vicap.read()
            count += 1
            if image is None:
                continue
            image = image[:, :, ::-1]
            if count % 5 == 0:
                count = 0
                boxes, _ = self.mtcnn.detect(image)
                if boxes is None:
                    continue
                box = boxes[0]
                bbox = list(map(int, box.tolist()))
                if min(bbox) < 0:
                    continue
                # bbox = [x1,y1,x2,y2]
                image = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                im_pil = Image.fromarray(image)
                face = self.trans_for_train(im_pil)
                with torch.no_grad():
                    emb = self.resnet(face)
                    emb = emb.detach()
                    if emb == []:
                        continue
                    embs.append(emb.numpy()[0].tolist())
        vicap.release()
        return embs

    def continue_train(self, embs, hash_username):
        p = hnswlib.Index(space='l2', dim=512)
        len_embs = len(embs)
        try:
            p.load_index(
                'data_file/embedding.bin',
                max_elements=self.max_elements
            )
        except:
            p.init_index(
                ef_construction=200,
                M=16,
                max_elements=self.max_elements
            )
        p.add_items(embs, [f'{hash_username}{i:02}' for i in range(len_embs)])
        p.save_index('data_file/embedding.bin')

    def delete_face(self, hash_username, len_embs):
        p = hnswlib.Index(space='l2', dim=512)
        p.load_index(
            'data_file/embedding.bin',
            max_elements=self.max_elements,
            allow_replace_deleted=True
        )
        for i in range(len_embs):
            p.mark_deleted(int(f'{hash_username}{i:02}'))
        p.save_index('data_file/embedding.bin')

    def predict(self, image):
        results = []
        image = cv2.resize(image, (360, 360))
        self.p = hnswlib.Index(space='l2', dim=512)
        self.p.load_index(
            'data_file/embedding.bin',
            max_elements=self.max_elements
        )
        if image is None:
            return results
        img = image
        img = img[:, :, ::-1]
        boxes, _ = self.mtcnn.detect(img)
        if boxes is not None:
            for box in boxes:
                bbox = list(map(int, box.tolist()))
                img_region = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                im_pil = Image.fromarray(img_region)
                face = self.trans_for_recognition(im_pil)
                emb = self.resnet(face).detach()
                labels, distances = self.p.knn_query(emb, k=1)
                distance = distances[0][0]
                if distance < 0.55:
                    # print(distance)
                    int2str = str(labels[0][0])
                    hash_username = int2str[:8]
                    results.append(
                        {
                            'hash_username': hash_username,
                            'distance': float(distance),
                            'coordinate': bbox
                        }
                    )
        return results

    def predict_one_user(self, image):
        results = []
        self.p = hnswlib.Index(space='l2', dim=512)
        self.p.load_index(
            'data_file/embedding.bin',
            max_elements=self.max_elements
        )
        if image is None:
            return results
        img = image
        img = img[:, :, ::-1]
        boxes, _ = self.mtcnn_one_box.detect(img)
        if boxes is not None:
            box = boxes[0]
            bbox = list(map(int, box.tolist()))
            img_region = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            im_pil = Image.fromarray(img_region)
            face = self.trans_for_recognition(im_pil)
            emb = self.resnet(face).detach()
            labels, distances = self.p.knn_query(emb, k=1)
            distance = distances[0][0]
            if distance < 0.55:
                # print(distance)
                int2str = str(labels[0][0])
                hash_username = int2str[:8]
                results.append(
                    {
                        'hash_username': hash_username,
                        'distance': float(distance),
                        'coordinate': bbox
                    }
                )
        return results
