import warnings

import clip
import torch
from PIL import Image


class Embedder:
    def __init__(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "model"):
            self.model = None
            self.preprocess = None
            torch.cuda.empty_cache()

    def embed_image(self, image: Image.Image) -> torch.Tensor:
        with torch.no_grad():
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            return self.model.encode_image(image_input)

    def embed_text(self, text: str) -> torch.Tensor:
        with torch.no_grad():
            text_input = clip.tokenize(text).to(self.device)
            return self.model.encode_text(text_input)


# with torch.no_grad():
#     image_features = model.encode_image(image)
#     text_features = model.encode_text(text)

#     logits_per_image, logits_per_text = model(image, text)
#     probs = logits_per_image.softmax(dim=-1).cpu().numpy()
#     print(image_features)

# print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]
