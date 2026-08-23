from collections import deque
from commit import Commit
from sorting import merge_sort
from datetime import datetime

class Repository:
    """Mini Git 저장소 하나의 상태(브랜치, HEAD, 커밋 그래프 등)를 관리한다."""

    def __init__(self):
        """현재 HEAD가 가리키는 커밋을 가리키는 새 브랜치를 생성한다."""
        self.commits = {}
        self.branches = {} # branch_name -> HEAD commit_hash (없으면 None)
        self.current_branch = None
        self.user = None    # hash -> Commit  (해시맵 기반 빠른 조회, O(1) 평균)
        self.keyword_index = {}
        self.author_index = {}


    def init(self, user_name):
        """저장소를 초기화하고 main 브랜치와 HEAD, 현재 사용자(author)를 설정한다."""
        self.branches = {"main": None}
        self.current_branch = "main"
        self.user = user_name

    def commit(self, message):
        """현재 HEAD가 가리키는 커밋을 가리키는 새 브랜치를 생성한다."""
        head = self.branches[self.current_branch]

        if head is None:
            parents = []
        else :
            parents = [head]
        
        commit_hash = "c" + str(len(self.commits)+1)

        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        new_commit = Commit(commit_hash, message, self.user, formatted, parents)

        self.commits[commit_hash] = new_commit
        self.branches[self.current_branch] = commit_hash

        self.update_index(new_commit)

        return commit_hash

    def update_index(self, commit):
        tokens = commit.message.split()
        for word in tokens:
            keyword = word.lower()
            self.keyword_index.setdefault(keyword, []).append(commit.hash)

        self.author_index.setdefault(commit.author, []).append(commit.hash)


    def branch(self, branch_name):
        """현재 HEAD가 가리키는 커밋을 가리키는 새 브랜치를 생성한다."""
        current_head = self.branches[self.current_branch]
        self.branches[branch_name] = current_head

    def switch(self, branch_name):
        """HEAD를 지정된 브랜치로 전환한다."""
        if branch_name not in self.branches:
            raise Exception(f"Unknown branch: {branch_name}")
        self.current_branch = branch_name


    def log(self, sort_by=None):
        """커밋 로그를 반환한다. sort_by가 None이면 위상정렬, "author"이면 작성자 기준 정렬, "date"이면 날짜 기준 정렬"""

        if sort_by is None:        
            children = {h: [] for h in self.commits}
            in_degree = {h: 0 for h in self.commits}

            for c in self.commits.values():
                for p in c.parents:
                    children[p].append(c.hash)
                    in_degree[c.hash] += 1

            queue = deque()
            for h in in_degree:
                if in_degree[h] == 0:
                    queue.append(h)

            result = []

            while queue:
                current = queue.popleft()
                result.append(current)

                for child in children[current]:
                    in_degree[child] -= 1

                    if in_degree[child] == 0:
                        queue.append(child)
            return result

        elif sort_by == "author":
            commit_list = list(self.commits.values())
            return merge_sort(commit_list, lambda c: c.author)

        elif sort_by == "date":
            commit_list = list(self.commits.values())
            return merge_sort(commit_list, lambda c: c.timestamp)


    def ancestors(self, commit_hash):
        """지정된 커밋에서 도달 가능한 모든 조상 커밋을 출력한다."""
        stack = list(self.commits[commit_hash].parents)
        visited = set()

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            for p in self.commits[current].parents:
                stack.append(p)
            
        return visited

    def path(self, start, end):
        """두 커밋 사이의 최단 경로(무방향 간선 기준)를 반환한다."""
        adjacency = {h: set() for h in self.commits}
        for c in self.commits.values():
            for p in c.parents:
                adjacency[c.hash].add(p)
                adjacency[p].add(c.hash)

        if start == end:
            return [start]

        queue =deque()
        queue.append(start)
        visited = {start} # start는 이미 방문한 걸로 시작
        came_from = {}

        while queue:
            current = queue.popleft()

            if current == end:
                break   # 목표 도착! 반복 멈춤

            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        if end not in visited:
            return None

        path = [end]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        
        return path


    def search_keyword(self, keyword):
        """역색인을 이용해 키워드가 포함된 커밋 메시지를 가진 커밋들을 찾는다."""
        hashes = self.keyword_index.get(keyword.lower(), [])
        return hashes

    def search_author(self,author):
        """역색인을 이용해 지정된 작성자가 작성한 커밋들을 찾는다."""
        hashes = self.author_index.get(author, [])
        return hashes