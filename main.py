import shlex
from repository import Repository

repo = Repository()

while True:
    line = input("mini-git> ")

    try:
        parts = shlex.split(line)
        command = parts[0].lower()

        if command in ("exit", "quit"):
            print("Bye.")
            break

        if command == "init":
            user_name = parts[1]
            repo.init(user_name)
            print("Initialized repository. Current user:", user_name)

        elif command == "commit":
            message = parts[1]
            commit_hash = repo.commit(message)
            print(f"[{repo.current_branch} {commit_hash}] {message}")

        elif command == "branch":
            branch_name = parts[1]
            repo.branch(branch_name)
            print(f"Created branch: {branch_name}")

        elif command == "switch":
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

            else :
                # 옵션이 있음, 예: --sort=author, --sort=timestamp
                option = parts[1]
                sort_by = option[len("--sort-by="):]
                result = repo.log(sort_by=sort_by)
                for c in result:
                    print(f"commit {c.hash} ({c.author}, {c.timestamp})")
                    print(c.message)

        elif command == "path":
            start = parts[1]
            end = parts[2]
            result = repo.path(start, end)
            if result is None:
                print("No path")
            else:
                print("Path:", "->".join(result))

        elif command == "ancestors":
            commit_hash = parts[1]
            result = repo.ancestors(commit_hash)
            if not result:
                print("No ancestors.")
            else:
                print("Ancestors:", ", ".join(result))

        elif command == "search":
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

    except Exception as e:
        print(str(e))