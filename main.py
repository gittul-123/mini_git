"""Mini Git CLI 프로그램의 엔트리 포인트. REPL로 명령을 반복 입력받아 실행한다."""
import shlex
from repository import Repository

repo = Repository()

while True:
    line = input("mini-git> ")

    if not line.strip():
        continue

    try:
        parts = shlex.split(line)
        command = parts[0].lower()

        if command in ("exit", "quit"):
            print("Bye.")
            break

        if command == "init":
            if len(parts) != 2:
                raise Exception("Invalid args")
            user_name = parts[1]
            repo.init(user_name)
            print("Initialized repository. Current user:", user_name)

        elif command == "commit":
            if len(parts) != 2:
                raise Exception("Invalid args")
            message = parts[1]
            commit_hash = repo.commit(message)
            print(f"[{repo.current_branch} {commit_hash}] {message}")

        elif command == "branch":
            if len(parts) != 2:
                raise Exception("Invalid args")
            branch_name = parts[1]
            repo.branch(branch_name)
            print(f"Created branch: {branch_name}")

        elif command == "switch":
            if len(parts) != 2:
                raise Exception("Invalid args")
            branch_name = parts[1]
            repo.switch(branch_name)
            print(f"Switched to branch: {branch_name}")

        elif command == "log":
            if len(parts) == 1: # 옵션 없음, 기본 위상정렬
                result = repo.log()
                for h in result:
                    c = repo.commits[h]
                    print(f"commit {c.hash} ({c.author}, {c.timestamp})")
                    print(c.message)

            elif len(parts) == 2 and parts[1].startswith("--sort-by="):
                option = parts[1]
                sort_by = option[len("--sort-by="):]
                if sort_by not in ("date", "author"):
                    raise Exception("Invalid args")
                result = repo.log(sort_by=sort_by)
                for c in result:
                    print(f"commit {c.hash} ({c.author}, {c.timestamp})")
                    print(c.message)
            
            else:
                raise Exception("Invalid args")

        elif command == "path":
            if len(parts) != 3:
                raise Exception("Invalid args")
            start = parts[1]
            end = parts[2]
            result = repo.path(start, end)
            if result is None:
                print("No path")
            else:
                print("Path:", "->".join(result))

        elif command == "ancestors":
            if len(parts) != 2:
                raise Exception("Invalid args")
            commit_hash = parts[1]
            result = repo.ancestors(commit_hash)
            if not result:
                print("No ancestors.")
            else:
                print("Ancestors:", ", ".join(result))

        elif command == "search":
            if len(parts) != 2:
                raise Exception("Invalid args")
            arg = parts[1]
            if arg.startswith("--author="):
                author = arg[len("--author="):]
                hashes = repo.search_author(author)
            else:
                keyword = arg
                hashes = repo.search_keyword(keyword)

            if not hashes:
                print("Found 0 commits.")
            else:
                print(f"Found {len(hashes)} commit(s):")
                for h in hashes:
                    c = repo.commits[h]
                    print(f"- {h}: {c.message}")

        else:
            raise Exception(f"Unknown command: {command}")

    except Exception as e:
        print(str(e))