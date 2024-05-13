from pylsl import StreamInlet, resolve_stream

# EEG 스트림을 찾습니다
eeg_streams = resolve_stream('type', 'EEG')

# 첫 번째 스트림으로 StreamInlet을 생성합니다
eeg_inlet = StreamInlet(eeg_streams[0])

# 스트림 정보를 가져옵니다
info = eeg_inlet.info()

# StreamInfo 객체에서 채널 정보를 읽습니다
channels = info.desc().child("channels").child("channel")
channel_names = []

while not channels.empty():
    # 각 채널의 이름을 리스트에 추가합니다
    channel_names.append(channels.child_value("label"))
    channels = channels.next_sibling()

print("Channel names:", channel_names)
print("Channel count:", len(channel_names))

# 샘플을 가져옵니다
sample, timestamp = eeg_inlet.pull_sample()

# 채널 이름과 샘플 값을 결합합니다
channel_data = dict(zip(channel_names, sample))
print(channel_data)
print("Timestamp:", timestamp)
print("Channel Data:")
for channel, value in channel_data.items():
    print(f"{channel}: {value}")