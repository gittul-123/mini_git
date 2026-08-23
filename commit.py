class Commit:
    def __init__(self, commit_hash, message, author, timestamp, parents):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = parents



