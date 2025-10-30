from rich.progress import Progress, BarColumn, TextColumn
import time

# 1. 설명, 막대, 퍼센트 열만 포함하여 Progress 객체를 생성합니다.
#    (TimeElapsedColumn, TimeRemainingColumn 등 시간 열을 제외합니다.)
custom_progress = Progress(
    TextColumn("[progress.description]{task.description}"),       # "Waiting..." 부분
    BarColumn(),                                                  # "━━━━━━━━..." 부분
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%")  # " 100%" 부분
)

# 2. Progress 객체를 컨텍스트 매니저로 사용합니다.
with custom_progress as progress:

    # 3. 'total' 값을 지정하여 작업을 추가합니다.
    task = progress.add_task("Waiting...", total=5)

    # 4. 루프를 돌면서 작업을 업데이트합니다.
    for step in range(5):
        time.sleep(1)
        progress.update(task, advance=1)

print("완료!")