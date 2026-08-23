# Mini Git

CLI 기반으로 동작하는 미니 버전의 Git입니다. 실제 파일 내용은 추적하지 않고,
커밋 그래프(DAG), 브랜치, 로그, 최단 경로, 조상 탐색, 검색(역색인) 기능을
직접 구현했습니다.

## 실행 방법

```bash
python main.py
(python3 main.py)
```

Python 3.10 이상 환경에서 실행합니다. 외부 라이브러리 설치가 필요 없습니다
(표준 라이브러리만 사용).

## 폴더 구조

```
mini_git/
├── main.py         # 엔트리 포인트 (REPL 실행)
├── repository.py   # 저장소 상태(브랜치/HEAD/커밋) 및 명령 처리
├── commit.py        # Commit 클래스
├── sorting.py         # 병합 정렬(merge_sort) 직접 구현
└── README.md
```

## 지원 명령어

| 명령어 | 설명 |
|---|---|
| `init <user_name>` | 저장소 초기화, main 브랜치 생성, 사용자 설정 |
| `branch <branch_name>` | 현재 HEAD를 가리키는 새 브랜치 생성 |
| `switch <branch_name>` | HEAD를 지정한 브랜치로 이동 |
| `commit <message>` | 현재 HEAD를 부모로 하는 새 커밋 생성 |
| `log` | 부모가 자식보다 먼저 나오는 순서(위상 정렬)로 로그 출력 |
| `log --sort-by=date` | timestamp 기준으로 정렬해 로그 출력 |
| `log --sort-by=author` | 작성자 기준으로 정렬해 로그 출력 |
| `path <commit1> <commit2>` | 두 커밋 사이 최단 경로 출력 (없으면 `No path`) |
| `ancestors <commit_hash>` | 해당 커밋의 모든 조상 커밋 출력 |
| `search <keyword>` | 메시지에 키워드가 포함된 커밋 검색 |
| `search --author=<name>` | 특정 작성자의 커밋 검색 |
| `exit` / `quit` | 프로그램 종료 |

명령어는 대소문자를 구분하지 않습니다 (`INIT`, `init` 모두 허용).
공백이 포함된 인자(메시지 등)는 따옴표로 감싸서 입력합니다.
예: `commit "Add login feature"`

## 실행 예시

```
mini-git> init Alice
Initialized repository. Current user: Alice
mini-git> commit "Initial commit"
[main c1] Initial commit
mini-git> branch feature
Created branch: feature
mini-git> switch feature
Switched to branch: feature
mini-git> commit "Add login feature"
[feature c2] Add login feature
mini-git> switch main
Switched to branch: main
mini-git> commit "Add payment feature"
[main c3] Add payment feature
mini-git> log
commit c1 (Alice, 2024-01-15 09:00:00)
Initial commit
commit c2 (Alice, 2024-01-15 09:15:00)
Add login feature
commit c3 (Alice, 2024-01-15 09:30:00)
Add payment feature
mini-git> path c1 c3
Path: c1->c3
mini-git> search login
Found 1 commit(s):
- c2: Add login feature
mini-git> exit
Bye.
```

## 핵심 구현 설명

### 1. 커밋 그래프가 DAG인 이유
커밋은 항상 "이미 존재하는" 커밋만 부모로 가리킬 수 있습니다. 아직 만들어지지
않은 미래의 커밋을 부모로 지정하는 것은 불가능하므로, 화살표(부모 방향)는
항상 시간상 과거만 가리킵니다. 따라서 순환이 원천적으로 생길 수 없고,
커밋 그래프는 항상 DAG(방향성 비순환 그래프)가 됩니다.

### 2. LOG (위상 정렬)
"부모가 항상 자식보다 먼저 출력"되어야 하므로, 진입 차수(각 커밋이 가진
아직 처리되지 않은 부모의 수)를 계산하고, 진입 차수가 0인 커밋부터 큐에
넣어 순서대로 출력하는 방식(Kahn의 알고리즘)으로 구현했습니다. 하나를
출력할 때마다 그 자식들의 진입 차수를 1씩 줄이고, 0이 되는 순간 큐에
추가하는 것을 반복합니다.

### 3. ANCESTORS (조상 탐색)
스택을 이용한 DFS(깊이 우선 탐색)로 구현했습니다. 지정된 커밋의 부모들을
스택에 넣고, 하나씩 꺼내며 방문 처리한 뒤 그 부모의 부모들도 계속 스택에
추가하는 방식으로, 도달 가능한 모든 조상을 빠짐없이 찾습니다.

### 4. PATH (최단 경로)
커밋-부모 연결을 무방향 간선으로 간주하고, BFS(너비 우선 탐색)로 최단
거리를 구했습니다. 각 커밋을 방문할 때 "어디를 거쳐서 왔는지"(`came_from`)를
함께 기록해두고, 도착점에서 시작점까지 거꾸로 되짚어간 뒤 뒤집어서 최종
경로를 만듭니다.

### 5. 정렬 알고리즘 (병합 정렬 직접 구현)
`sorted()`, `list.sort()`를 사용하지 않고 병합 정렬을 직접 구현했습니다
(`sorting.py`). 리스트를 절반으로 계속 쪼개다가(재귀), 원소가 1개 이하가
되면 그 자체로 정렬된 것으로 보고, 이후 두 개의 정렬된 리스트를 맨 앞
원소끼리 비교하며 합칩니다.
- 시간복잡도: 평균/최악 모두 O(n log n) — 입력 상태와 무관하게 항상 일정
- 안정 정렬(Stable): 예. 두 값이 같을 때 `<=` 비교를 사용해 항상 원래
  앞쪽에 있던 원소를 먼저 꺼내므로, 동일한 값을 가진 원소들의 원래 순서가
  유지됩니다.
- 정렬 기준은 `key` 함수로 넘겨받아 유연하게 바꿀 수 있습니다
  (`lambda c: c.author`, `lambda c: c.timestamp`).

### 6. 역색인 (SEARCH)
커밋을 매번 순회하며 검색하면 커밋 수(N)에 비례해 시간이 걸리지만
(O(N)), 커밋이 생성되는 시점(COMMIT)에 미리 `keyword -> commit_hash 목록`,
`author -> commit_hash 목록` 두 종류의 딕셔너리를 만들어두면, 검색 시
딕셔너리 조회만으로 후보를 즉시 가져올 수 있습니다(평균 O(1)). 키워드는
커밋 메시지를 공백으로 분리(`split()`)한 뒤 소문자로 정규화해 저장합니다.

## 제약 사항 준수 내역

- `sorted()`, `list.sort()` 등 정렬 표준 API를 사용하지 않고, 병합 정렬을
  직접 구현해 모든 정렬에 사용했습니다.
- 그래프 전용 라이브러리를 사용하지 않고, `dict`/`set`/`list`와
  `collections.deque`(범용 큐)만으로 그래프 알고리즘을 구현했습니다.
- 파일 내용 추적, 네트워크 통신, 데이터 영속성(디스크 저장)은 구현하지
  않았습니다. 모든 상태는 프로그램 실행 중 메모리에서만 유지됩니다.
