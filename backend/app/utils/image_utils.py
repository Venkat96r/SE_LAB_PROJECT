def safe_float_conversion(v):
    try:
        return float(v)
    except:
        return 0.0

def process_bounding_box(box):
    # If box is a list of four points: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # Convert to min/max format for bounding box
    if isinstance(box, list) and all(isinstance(pt, (list, tuple)) and len(pt) == 2 for pt in box):
        xs = [float(pt[0]) for pt in box]
        ys = [float(pt[1]) for pt in box]
        return {
            "x1": min(xs),
            "y1": min(ys),
            "x2": max(xs),
            "y2": max(ys),
        }
    # If box is a flat list or tuple of 4 values
    if isinstance(box, (list, tuple)) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box):
        x1, y1, x2, y2 = map(float, box)
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    # Otherwise, fallback (invalid format)
    return {"x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0}

def get_confidence_level(c):
    if c >= 0.9: return "high"
    if c >= 0.7: return "medium"
    if c >= 0.5: return "low"
    return "very_low"

def deskew_image(image):
    return image