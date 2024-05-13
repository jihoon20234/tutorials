from psychopy import visual, core, event
import glob

# 이미지 파일 경로를 불러옵니다.
image_files = sorted(glob.glob('topomap_*.png'))

# PsychoPy 화면 설정
win = visual.Window([2560, 1440], fullscr=True, color=(0, 0, 0), colorSpace='rgb', waitBlanking=False, checkTiming=False)
win.mouseVisible = False  # 마우스 커서 숨기기

for stmuli in image_files:
  print("img: ", stmuli)
  img_file = visual.ImageStim(win, image=stmuli,pos=(0, 0))
  img_file.draw()
  win.flip()
  core.wait(0.1)  # 1초 동안 기다립니다.

core.wait(3)