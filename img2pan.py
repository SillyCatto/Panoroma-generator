#!/usr/bin/env python3

import cv2
import time
import threading

class AltairCam:
    """A wrapper around open-cv VideoCapture to include frame capturing capabilities."""

    def __init__(self, capture_to=None, capture_buffer=0.75):
        self._cam = cv2.VideoCapture(0)
        self._frame = None
        
        # capture variables
        self.capture_to = capture_to or 'cam_data'
        self.capture_buffer = capture_buffer  # in seconds

        self._frames = []
        self._should_run = False
        self._capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
    
    def _capture_frames(self):
        while self._should_run:
            self._frames.append(self._frame)
            print(f"Captured Frame: {len(self._frames)}")
            time.sleep(self.capture_buffer)
    
    def save_frames(self, destination=None, extension='png', flush=False):
        """Saves the captured frame to a destination.
        
        Arguments
        ---------
        destination : str
            By default saves the frames to `self.capture_to`. Otherwise, to the provided path
        extension : str
        flush : bool
            If true then clears all the captured frames after saving them. Otherwise, doesn't do anything.
            By default, this is `False`.
        """

        if self._frames:
            destination = destination or self.capture_to
            for index, frame in enumerate(self._frames):
                cv2.imwrite(f'{destination}/frame_{index}.{extension}', frame)
        
            if flush:
                self._frames = []
    
    def get_frames(self, flush=False):
        """Returns the captured frames.
        
        Arguments
        ---------
        flush : bool
            If true then clears all the captured frames after returning them. Otherwise, doesn't do anything.
            By default, this is `True`.
        """

        if flush:
            to_return = self._frames
            self._frames = []
            return to_return
        
        return self._frames
    
    def run_loop(self):
        """The main loop that reads the video input and based on the input keys - captures them.
        
        Usage
        -----
        When 'c' key is pressed,
            The cam starts saving the frames to memory every `self.capture_buffer` seconds.
        When 's' key is pressed,
            The cam stops saving the frames to memory and calls `self.save_frames(flush=True)`.
            This is useful for testing.
        When 'q' key is pressed,
            The cam stops saving the frames to memory and the cam itself is released. However,
            the frames are still stored and can be accessed using `save_frames` and `get_frames` methods.
        """

        while True:
            _, self._frame = self._cam.read()
            cv2.imshow('altair_cam', self._frame)
            # waitKey needs imshow window to operate
            key = cv2.waitKey(1)

            if key == ord('c'):
                print("[C]apturing the frames")
                self._should_run = True
                self._capture_thread.start()
            
            if key == ord('s'):
                print("[S]topping capture")
                self._should_run = False
                self._capture_thread.join()
                
                self.save_frames(flush=True)
            
            if key == ord('q'):
                print("[Q]uitting the camera")
                if self._capture_thread.is_alive():
                    # this logic doesn't call the save_frames method
                    # this allows us to do whatever we want with the frames after the event loop has ended
                    # this will be mostly useless while using this class as a part of another code, while
                    # using the 's' logic will mostly be useful for testing or generating captured frames
                    self._should_run = False
                    self._capture_thread.join()

                self._cam.release()
                cv2.destroyAllWindows()
                break


def panorama(images, stitch_mode):
    """Creates a panorama from a sequence of images.
    
    Arguments
    ---------
    images : Iterable[numpy.ndarray]
    stitch_mode : `cv2.Stitcher_PANORAMA` or `cv2.Stitcher_SCANS`
    """

    stitcher = cv2.Stitcher.create(stitch_mode)
    status, pano = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        raise RuntimeError(f"Stitching failed (status_code: {status})")
    
    return pano


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-ct', '--capture-to', help="save the generated frames to the provided path")
    parser.add_argument('-o', '--output-to', help="save the generated panaroma to the provided path")
    args = parser.parse_args()

    cam = AltairCam(capture_to=args.capture_to)
    cam.run_loop()

    if args.capture_to:
        cam.save_frames()
    
    frames = cam.get_frames(flush=True)
    pano = panorama(
        images=frames,
        stitch_mode=cv2.STITCHER_PANORAMA,
    )

    if args.output_to:
        cv2.imwrite(args.output_to, pano)
    else:
        cv2.imshow('output', pano)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
