import numpy as np
import cv2
# ============================================================================
path = "C:\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\[Original]RB5 S132 LsUN DAPI+Olig2+CC1 L1 Image ID 38.tif"
img = cv2.imread(path)
h, w = img.shape[0:2]
neww = 800
newh = int(neww*(h/w))
img = cv2.resize(img, (neww, newh))
shape = img.shape
CANVAS_SIZE = (shape[0],shape[1])

FINAL_LINE_COLOR = (255, 255, 255)
WORKING_LINE_COLOR = (127, 127, 127)
ROINumber = 2
# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name, img):
        self.window_name = window_name # Name for our window
        self.img = img
        self.done = False # Flag signalling we're done with one polygon
        self.doneAll = False # Flag signalling we're done with all polygons
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon
        self.polygons = {} # Dictionary of all polygons


    def on_mouse(self, event, x, y, buttons, user_param):
        # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)

        if self.done: # Nothing more to do
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            self.current = (x, y)

        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we're done
            print("Completing polygon with %d points." % len(self.points))
            self.done = True


    def run(self):
        # Let's create our working window and set a mouse callback to handle events
        cv2.namedWindow(self.window_name, flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.window_name, np.zeros(CANVAS_SIZE, np.uint8))
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)
        i = 0
        for i in range(ROINumber):
            self.done = False
            if i == 0:
                Polycanvas = np.copy(img, subok= True)
            while(not self.done):
                # This is our drawing loop, we just continuously draw new images
                # and show them in the named window
                canvas = np.copy(Polycanvas, subok= True)
                if (len(self.points) > 0):
                    # Draw all the current polygon segments
                    cv2.polylines(canvas, np.array([self.points]), False, FINAL_LINE_COLOR, 1)
                    # And  also show what the current segment would look like
                    cv2.line(canvas, self.points[-1], self.current, WORKING_LINE_COLOR)
                # Update the window
                cv2.imshow(self.window_name, canvas)
                # And wait 50ms before next iteration (this will pump window messages meanwhile)
                if cv2.waitKey(50) == 27: # ESC hit
                    self.done = True

            # User finised entering the polygon points, so let's make the final drawing
            print(i)

            # of a filled polygon
            if (len(self.points) > 0):
                cv2.fillPoly(Polycanvas, np.array([self.points]), FINAL_LINE_COLOR)
            # And show it
            cv2.imshow(self.window_name, Polycanvas)

            self.polygons[i] = self.points
            self.points = []

            # Waiting for the user to press any key
            i = i+1

            print(self.polygons)

        cv2.waitKey()
        cv2.destroyWindow(self.window_name)
        Polycanvas = cv2.resize(Polycanvas, CANVAS_SIZE)
        return Polycanvas


# ============================================================================

if __name__ == "__main__":
    pd = PolygonDrawer("Polygon", img)
    image = pd.run()
    #rezie image back to original size
    cv2.imwrite("polygon.png", image)
