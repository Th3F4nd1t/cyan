# all the various io methods are here

# a gui rgb pixel screen that takes in a width and height and can be drawn to with rgb values at locations with an optional buffer, clear, and update method
class Screen:
    def __init__(self, width, height, useBuffer=False, allowedRGBValues=[[-1], [-1], [-1]]):
        """
        width: int, the width of the screen
        height: int, the height of the screen
        useBuffer: bool, whether the screen should be buffered
        allowedRGBValues: list, [<all values: bool>, <step: float>, [rmin, rmax], [gmin, gmax], [bmin, bmax]], the allowed rgb values for the screen
        """
        self.width = width
        self.height = height
        self.updateBufferOnDraw = not useBuffer
        self.allowUpdate = useBuffer
        self.allowClear = useBuffer
        self.buffer = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
        self.screen = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
        self.allowedRGBValues = allowedRGBValues
        self.clear(overwrite=True)
        self.update(overwrite=True)

    def draw(self, x, y, r, g, b):
        """
        x: int, the x location to draw the pixel
        y: int, the y location to draw the pixel
        r: int, the red value of the pixel
        g: int, the green value of the pixel
        b: int, the blue value of the pixel
        """
        if self.allowedRGBValues[0][0]:
            if r < self.allowedRGBValues[2][0] or r > self.allowedRGBValues[2][1]:
                return
            if g < self.allowedRGBValues[3][0] or g > self.allowedRGBValues[3][1]:
                return
            if b < self.allowedRGBValues[4][0] or b > self.allowedRGBValues[4][1]:
                return
        if self.allowUpdate:
            self.screen[y][x] = [r, g, b]
        if self.updateBufferOnDraw:
            self.buffer[y][x] = [r, g, b]
