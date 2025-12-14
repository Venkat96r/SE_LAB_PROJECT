import cv2
import numpy as np
from scipy import ndimage
import math


class ImageQualityAnalyzer:
    """
    Full Image Quality Assessment Class
    Includes:
    - Multi-method blur detection
    - Text-specific blur
    - High-frequency analysis
    - Edge sharpness
    - Multiscale blur
    - Contrast & clarity analysis
    - Skew detection
    """

    def check(self, image_path: str) -> dict:
        """
        Main entry point for quality analysis.
        """
        img = cv2.imread(image_path)
        if img is None:
            return {
                "score": 0,
                "suggestions": ["Invalid image file. Please upload a valid image."]
            }

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        score = 100
        suggestions = []

        # ----------------------------
        # 1. Resolution Check
        # ----------------------------
        if w < 500 or h < 500:
            score -= 15
            suggestions.append("Low resolution image. Please upload a higher resolution image.")

        # ----------------------------
        # 2. Blur Metrics
        # ----------------------------
        blur_scores = self.compute_blur_metrics(gray)
        overall_blur = self.combine_blur_metrics(blur_scores, gray.shape)

        if overall_blur < 0.15:
            score -= 55
            suggestions.append("Image is severely blurred. Please recapture clearly.")
        elif overall_blur < 0.3:
            score -= 40
            suggestions.append("Image is very blurry. Improve focus when capturing.")
        elif overall_blur < 0.5:
            score -= 30
            suggestions.append("Image is moderately blurry.")
        elif overall_blur < 0.7:
            score -= 20
            suggestions.append("Image is slightly blurry.")

        # ----------------------------
        # 3. Contrast Assessment
        # ----------------------------
        contrast = gray.std()
        local_contrast = self.analyze_local_contrast(gray)

        if contrast < 40 or local_contrast < 20:
            score -= 15
            suggestions.append("Low contrast. Improve lighting conditions.")

        # ----------------------------
        # 4. Text Clarity
        # ----------------------------
        clarity_score = self.assess_text_clarity(gray)
        if clarity_score < 0.5:
            score -= 25
            suggestions.append("Text clarity is poor. Ensure focus and good lighting.")

        # ----------------------------
        # 5. Skew Detection
        # ----------------------------
        skew_angle = self.detect_skew_angle(gray)
        if abs(skew_angle) > 10:
            score -= 15
            suggestions.append(f"Document skewed by {abs(skew_angle):.1f}° — please align properly.")

        # Final adjustments
        score = max(0, min(100, score))
        if not suggestions:
            suggestions.append("Good quality image ✅")

        return {
            "score": score,
            "suggestions": suggestions,
            "blur_details": {
                "overall_blur_score": overall_blur,
                "individual_scores": blur_scores,
                "text_clarity": clarity_score,
                "skew_angle": skew_angle
            }
        }

    # ==========================================================
    #                 Blur Detection Helpers
    # ==========================================================

    def compute_blur_metrics(self, gray):
        """Compute all blur metrics used for quality scoring."""
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

        gradient_mag = np.sqrt(sobel_x**2 + sobel_y**2)

        return {
            "laplacian": cv2.Laplacian(gray, cv2.CV_64F).var(),
            "sobel": np.var(sobel_x) + np.var(sobel_y),
            "gradient_mean": np.mean(gradient_mag),
            "gradient_std": np.std(gradient_mag),
            "high_freq": self.calculate_high_frequency(gray),
            "text_blur": self.detect_text_blur(gray),
            "edge_sharpness": self.analyze_edge_sharpness(gray),
            "multiscale": self.detect_multiscale_blur(gray)
        }

    def calculate_high_frequency(self, gray):
        """FFT-based high frequency measurement."""
        f_transform = np.fft.fftshift(np.fft.fft2(gray))
        magnitude = np.log(np.abs(f_transform) + 1)

        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2

        high_freq_mask = np.ones_like(magnitude)
        r = min(rows, cols) // 6
        y, x = np.ogrid[:rows, :cols]
        mask_area = (x - ccol) ** 2 + (y - crow) ** 2 <= r * r
        high_freq_mask[mask_area] = 0

        return np.mean(magnitude * high_freq_mask)

    # Text region blur detection
    def detect_text_blur(self, gray):
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(adaptive, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        scores = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 50 < w * h < 5000:
                region = gray[y:y+h, x:x+w]
                if region.size > 0:
                    lap_var = cv2.Laplacian(region, cv2.CV_64F).var()
                    sobel_var = np.var(cv2.Sobel(region, cv2.CV_64F, 1, 0)) + \
                                np.var(cv2.Sobel(region, cv2.CV_64F, 0, 1))
                    scores.append((lap_var + sobel_var * 0.5) / 1.5)

        if scores:
            return min(np.mean(scores) / 300, 1.0)
        return 0.0

    # Multiscale blur detection
    def detect_multiscale_blur(self, gray):
        original_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        scales = [1, 2, 3]
        ratios = []

        for scale in scales:
            blurred = cv2.GaussianBlur(gray, (scale*2+1, scale*2+1), scale)
            blurred_var = cv2.Laplacian(blurred, cv2.CV_64F).var()
            if blurred_var > 0:
                ratios.append(original_var / blurred_var)

        if ratios:
            return min(np.mean(ratios) / 5.0, 1.0)
        return 0.0

    # Edge sharpness
    def analyze_edge_sharpness(self, gray):
        edges = cv2.Canny(gray, 50, 150)
        if np.sum(edges) == 0:
            return 0.0

        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        grad = np.sqrt(sobel_x**2 + sobel_y**2)

        edge_gradients = grad[edges > 0]
        if len(edge_gradients) == 0:
            return 0.0

        combined = (np.mean(edge_gradients) * 0.7) + (np.max(edge_gradients) * 0.3)
        return min(combined / 80, 1.0)

    # Combine metrics into final blur score
    def combine_blur_metrics(self, blur, shape):
        normalized = {
            "laplacian": min(blur["laplacian"] / 400, 1.0),
            "sobel": min(blur["sobel"] / 800, 1.0),
            "gradient_mean": min(blur["gradient_mean"] / 40, 1.0),
            "gradient_std": min(blur["gradient_std"] / 25, 1.0),
            "high_freq": min(blur["high_freq"] / 8, 1.0),
            "text_blur": blur["text_blur"],
            "edge_sharpness": blur["edge_sharpness"],
            "multiscale": blur["multiscale"]
        }

        weights = {
            "laplacian": 0.12,
            "sobel": 0.12,
            "gradient_mean": 0.10,
            "gradient_std": 0.10,
            "high_freq": 0.08,
            "text_blur": 0.25,
            "edge_sharpness": 0.15,
            "multiscale": 0.08
        }

        return sum(normalized[k] * weights[k] for k in normalized)

    # Local contrast
    def analyze_local_contrast(self, gray):
        kernel = np.ones((9, 9), np.float32) / 81
        float_img = gray.astype(np.float32)

        local_mean = cv2.filter2D(float_img, -1, kernel)
        local_var = cv2.filter2D(float_img**2, -1, kernel) - local_mean**2
        std = np.sqrt(np.maximum(local_var, 0))
        return np.mean(std)

    # Text clarity
    def assess_text_clarity(self, gray):
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel)

        clean_ratio = np.sum(opening == 255) / np.sum(adaptive == 255) \
                       if np.sum(adaptive == 255) else 0

        edges = cv2.Canny(gray, 30, 100)
        edge_density = np.sum(edges > 0) / edges.size

        projection = np.sum(adaptive == 0, axis=1)
        lines = len([1 for i in range(1, len(projection))
                     if projection[i] > 0 and projection[i-1] == 0])
        normalized_lines = min(lines / (gray.shape[0] / 50), 1.0)

        return (clean_ratio * 0.3) + (min(edge_density * 8, 1.0) * 0.4) + (normalized_lines * 0.3)

    # Skew detection
    def detect_skew_angle(self, gray):
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                                minLineLength=50, maxLineGap=10)
        if lines is None:
            return 0.0

        angles = []
        for line in lines:
            x1,y1,x2,y2 = line[0]
            length = np.hypot(x2-x1, y2-y1)
            if length > 30:
                angle = math.degrees(math.atan2(y2-y1, x2-x1))
                angle = angle - 180 if angle > 90 else angle
                angle = angle + 180 if angle < -90 else angle
                angles.append(angle)

        if not angles:
            return 0.0

        angles = np.array(angles)
        angles = angles[np.abs(angles) < 45]

        if len(angles) == 0:
            return 0.0

        weights = 1 / (1 + np.abs(angles))
        return np.average(angles, weights=weights)
