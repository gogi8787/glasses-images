---
description: 새 쿠팡 상세이미지를 규칙에 맞게 검사하고 1장당 1커밋으로 올리기
argument-hint: <브랜드> <파일 경로 ...>
---

새 쿠팡 상세이미지를 올린다. 인자: $ARGUMENTS

1. 첫 번째 인자를 브랜드(예: moodframe, common)로, 나머지를 올릴 파일로 본다.
2. 각 파일을 `coupang/<브랜드>/` 로 옮기기 전에, 같은 이름이 이미 있으면 덮어쓰지 말고 멈춰서 물어본다
   (새 버전이면 `-v2` 를 붙이자고 제안).
3. `python3 scripts/check_images.py <파일들>` 로 검사한다. 규격(1000x1000 RGB JPG / 가로 780px PNG, 500KB 이하)에
   안 맞으면 고칠 방법을 먼저 제안하고 승인을 받은 뒤 고친다. 고친 뒤 다시 검사해서 통과할 때까지 반복한다.
4. 통과하면 이미지 1장당 커밋 1개, 메시지는 `쿠팡 상세이미지 <브랜드>/<파일명>` 으로 커밋한다.
5. 마지막에 각 이미지의 URL을 표로 정리해 준다:
   `https://raw.githubusercontent.com/gogi8787/glasses-images/main/coupang/<브랜드>/<파일명>`
