import clip
import torch
from PIL import Image

_device = "cuda" if torch.cuda.is_available() else "cpu"
_model, _preprocess = clip.load("ViT-B/32", device=_device)


class Embedder:
    def __init__(self):
        self.model = _model
        self.preprocess = _preprocess
        self.device = _device

    def embed(self, image: Image.Image) -> torch.Tensor:
        return self.model.encode_image(
            self.preprocess(image).unsqueeze(0).to(self.device)
        )


# with torch.no_grad():
#     image_features = model.encode_image(image)
#     text_features = model.encode_text(text)

#     logits_per_image, logits_per_text = model(image, text)
#     probs = logits_per_image.softmax(dim=-1).cpu().numpy()
#     print(image_features)

# print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]
