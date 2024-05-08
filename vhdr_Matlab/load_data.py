import os
import itertools
import numpy as np
import mne
from scipy.io import loadmat

# raw 데이터 경로 및 subject, session 정보
dire = '/Matlab'
save_dir = '/artifact_remove'
subjects = ['sub1']
sessions = ['day1','day2']

# 채널 위치 정보 불러오기
chanlocs_path = '/chanlocs.mat'
chanlocs_data = loadmat(chanlocs_path)
chanlocs = chanlocs_data['chanlocs'][0]
channels = []

# 전체 채널 위치 정보를 확인하고 Montage에 추가
for i in range(127):
  label = chanlocs[i][0][0] # label
  x = chanlocs[i][4][0][0] # x
  y = chanlocs[i][5][0][0] # y
  z = chanlocs[i][6][0][0] # z
  channels.append([label, x, y, z])
  
# 각 조건에 따른 이벤트 ID 및 레이블
stim_all = [list(itertools.chain([1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16])),
            list(itertools.chain(['a','b','c','d'], ['e','f','g','h'], ['i','j','k','l'], ['m','n','o','p']))]

ival = [-1.5, 0]  # 초 단위

# load data
for sub in subjects:
  for sess in sessions:
    final_save_dir = os.path.join(save_dir, 'proc_mat', sub, sess)
    os.makedirs(final_save_dir, exist_ok=True)
    print(f'start: {sub} {sess}')
    file_dir = os.path.join(dire, sub, sess)
    files = sorted([f for f in os.listdir(file_dir) if f.endswith('.vhdr')])
    print(*files, sep='\n')

    # 파일 처리 및 경고 메시지
    if len(files) != 2:
        print('Please check the number of files')
        continue
    
    # MNE 라이브러리를 사용하여 EEG 데이터 읽기
    raw = mne.io.read_raw_brainvision(os.path.join(file_dir, files[0]), preload=True)
    event_id = {label: num for label, num in zip(stim_all[1], stim_all[0])}
    events, _ = mne.events_from_annotations(raw)
    
    # 채널 선택
    picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False)
    raw.pick(picks[:127])
    
    # 채널 몽타주 설정
    montage_ch_pos = {ch[0]: (ch[1], ch[2], ch[3]) for ch in channels}
    montage = mne.channels.make_dig_montage(ch_pos=montage_ch_pos)
    raw.set_montage(montage)
    
    # 필터링
    raw.filter(30, 125)
    raw.notch_filter(np.array([60, 120]))

    # 재참조
    raw.set_eeg_reference('average')

    # 채널 선택 후의 새로운 picks 배열 업데이트
    picks_updated = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False)

    # 이벤트 ID에 따라 에포킹
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=ival[0], tmax=ival[1], picks=picks_updated, preload=True)

    # 각 조건에 따른 에포킹 데이터 추출 및 저장
    for label, num in zip(stim_all[1], stim_all[0]):
      epo = epochs[label]
      X = epo.get_data(copy=True)
      y = epo.events[:, 2]  # 이벤트 ID
      # 데이터 저장
      np.savez(os.path.join(final_save_dir, f'data_{label}.npz'), X=X, y=y)