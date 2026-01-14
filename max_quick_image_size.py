from __future__ import annotations


def _to_multiple_of(value: int, multiple: int) -> int:
    if multiple <= 0:
        return int(value)
    value = int(value)
    remainder = value % multiple
    if remainder == 0:
        return value
    # Round to nearest multiple (ties go up)
    down = value - remainder
    up = down + multiple
    return up if (value - down) >= (up - value) else down


class MaxQuickImageSize:
    @classmethod
    def INPUT_TYPES(cls):
        # Note: ComfyUI INT widgets support `step` so the up/down arrows move by 32.
        # Users can still type any number, so we also snap to multiples of 32 at runtime.
        return {
            "required": {
                "width": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 16384, "step": 1, "forceInput": True},
                ),
                "height": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 16384, "step": 1, "forceInput": True},
                ),
                "square_size": ("INT", {"default": 1024, "min": 0, "max": 16384, "step": 32}),
                "landscape_width": ("INT", {"default": 1280, "min": 0, "max": 16384, "step": 32}),
                "landscape_height": ("INT", {"default": 720, "min": 0, "max": 16384, "step": 32}),
                "portrait_width": ("INT", {"default": 720, "min": 0, "max": 16384, "step": 32}),
                "portrait_height": ("INT", {"default": 1280, "min": 0, "max": 16384, "step": 32}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("new_width", "new_height")
    FUNCTION = "pick_size"
    CATEGORY = "MaxTools"

    def pick_size(
        self,
        width: int,
        height: int,
        square_size: int,
        landscape_width: int,
        landscape_height: int,
        portrait_width: int,
        portrait_height: int,
    ):
        # Snap presets to multiples of 32 as requested
        square_size = _to_multiple_of(square_size, 32)
        landscape_width = _to_multiple_of(landscape_width, 32)
        landscape_height = _to_multiple_of(landscape_height, 32)
        portrait_width = _to_multiple_of(portrait_width, 32)
        portrait_height = _to_multiple_of(portrait_height, 32)

        width = int(width)
        height = int(height)

        if width <= 0 or height <= 0:
            # Degenerate input: default to square preset.
            return (square_size, square_size)

        aspect = width / float(height)

        # “Square or very close to 1”: keep it simple with a small tolerance.
        # You can tweak this value later if desired.
        square_tol = 0.05
        if abs(aspect - 1.0) <= square_tol:
            return (square_size, square_size)

        if aspect > 1.0:
            return (landscape_width, landscape_height)

        return (portrait_width, portrait_height)


NODE_CLASS_MAPPINGS = {
    "MaxQuickImageSize": MaxQuickImageSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaxQuickImageSize": "Max Quick Image Size",
}
