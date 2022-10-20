    self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or None if not
        found
        """
        objects = self.__session.query(classes[cls])
        for obj in objects:
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.
        If no name is passed, returns the count of all objects in storage.
        """
        nobjects = 0
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                nobjects += len(self.__session.query(classes[clss]).all())
        return nobjects
