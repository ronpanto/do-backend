class GenericStorage(object):
    """
    The interface for package indexing storage.
    The goal is for this class to be simple. specific logic is in the BusinessLogic class
    """
    def add_entry(self, package, deps):
        """

        :param package: package name
        :param deps: list of strings representing the dependencies
        :return: Nothing. Just performs the action
        """
        raise NotImplementedError()

    def remove_entry(self, package):
        """

        :param package: the package name
        :return: Nothing, just performs the actions
        """
        raise NotImplementedError()

    def get_entry(self, package):
        """

        :param package: package name
        :return: the list of dependencies for that package
        """
        raise NotImplementedError()

    def check_many_exist(self, packages):
        """

        :param packages: collection of package names
        :return: True if they are all indexed, False otherwise
        """
        raise NotImplementedError()

    def check_dependents(self, package):
        """

        :param package: package name
        :return: True if the package has any other packages depending on it. False otherwise
        """
        raise NotImplementedError()
