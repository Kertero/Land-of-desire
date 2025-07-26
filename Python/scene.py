from uplogic import ULLoop


class SceneLoop(ULLoop):

    def start(self):
        """This code runs once on scene start."""
        pass

    def update(self):
        """This code runs when a frame is rendered (default up to 60x/second)."""
        pass

    def stop(self):
        """This code runs when the game is stopped."""
        pass


SceneLoop()