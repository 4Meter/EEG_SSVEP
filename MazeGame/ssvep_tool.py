import time
import mne
from mne_lsl.stream import StreamLSL as Stream
from ssvep_model import fbcca_realtime


class StreamSSVEP(Stream):
    def __init__(self, host_id = 'openbcigui', used_eeg = "obci_eeg1", cls_interval = 0.5, win_size = 2):
        self.host_id = host_id
        self.used_eeg = used_eeg
        self = Stream(name=self.used_eeg,stype = 'EEG',source_id = self.host_id,  bufsize=5)  # 5 seconds of buffer
        print('starting lsl streaming...')
        self.connect(acquisition_delay=0.001)
        self.set_montage("standard_1020")
        self.sfreq = 125
        self.cls_interval = cls_interval
        self.win_size = win_size

    def get_classification(self, list_freqs, num_harms=3, num_fbs=5):
        data = self.get_data(self.win_size)[0]
        rt_epoch = mne.EpochsArray([data], self.info)
        rt_epoch.apply_function(lambda x: x * 1e-6)
        ssvep_pred = fbcca_realtime(rt_epoch.get_data(copy = True)[0], list_freqs, self.sfreq, num_harms, num_fbs)
        print(f"SSVEP classification result: {list_freqs[ssvep_pred]} hz")