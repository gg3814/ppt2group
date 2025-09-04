from pptx import Presentation

def extract_text(path:str):
    prs = Presentation(path)
    slides = []
    for i, slide in enumerate(prs.slides):
        buf = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                buf.append(shape.text)
        slides.append({"idx":i, "text":"\n".join(buf)})
    return slides
