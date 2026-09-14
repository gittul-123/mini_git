class Commit:
    """Git 커밋 하나를 표현하는 클래스. hash, message, author, timestamp,
    parents(부모 커밋 hash 목록)를 필드로 가진다."""
    def __init__(self, commit_hash, message, author, timestamp, parents):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = parents