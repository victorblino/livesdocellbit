def isNotFound(imageBytes):
    with open('404.jpg', 'rb') as notFound:
        if imageBytes.getbuffer() == notFound.read():
            return True
        return False
