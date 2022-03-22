# git 명령어 정리
- `git init`
- `git status`
- `git commit`
- `git push`
- `git branch -D <삭제할 브런치명>` : branch 삭제
- `git reflog` : 삭제 이력까지 모두 확인 가능한 참조 목록
- `git checkout` : 특정 branch 로 이동
- `git checkout -b  <삭제한 브런치명> <커밋 해시값>` : branch 복구
- `git merge <branch 명>` : 해당 branch 와 merge
- `git remote` : 원격 저장소 이름 목록 확인
- `git remote add <새로운_원격저장소_이름> <fork한 git 주소>` : 새로운 원격 저장소 추가
- `git fetch <새로운 원격 저장소 이름>` : 로컬저장소에는 없지만 원격 저장소에 있는 데이터 가져오기
- `git commit —amend` : 기존 commit 한 정보에 추가 커밋을 하지않고 기존 커밋을 수정하는 경우 사용
- `git restore` : 변경 내역 (unstaged 한 내용) 삭제(commit 상태로 복구)
- `git stash` : 저장하기
- `git stash save [description]` : 설명 추가하면서 저장하기
- `git stash list` :  stash 리스트 보여주기
- `git stash apply` : 가장 최근 stash 가져와 적용
- `git stash apply —index` : staged 된 상태까지 적용하고 싶은 경우
- `git stash drop` : 가장 최근 stash 내용 삭제
- `git stash drop stash@{숫자}` .   해당하는 친구 삭제
- `git stash pop` apply + drop 을 합친 키워드 -> 가장 최근 stash 사용 및 삭제
- `git stash clear` 전체 삭제
- `git reset [mode]`	
  - 브랜치에 여러 버전을 올린 후, 이전 커밋으로 되돌릴 때 사용  
                        돌아간 커밋 내역 이후의 커밋 히스토리들을 초기화  
						[hard] : 지정한 커밋 이력 이후 변경사항 다 삭제  
						[mixed] : 로컬에 unstaged 상태로 유지하고 커밋은 리셋  
						[soft] : 지정한 커밋 이력 이후 변경 사항은 로컬에 staged 상태로  유지 후 커밋은 리셋  
						reset 이후에는 강제 push -f 를 해야 함  
- `git revert` : 지정한 커밋의 내용으로 새로운 커밋 생성(히스토리 보존) 