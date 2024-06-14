import time
import mne
from mne_lsl.stream import StreamLSL as Stream
from ssvep_model import fbcca_realtime


class StreamSSVEP(Stream):
    def __init__(self, host_id = 'openbcigui', used_eeg = "obci_eeg1", win_size = 2):
        self.host_id = host_id
        self.used_eeg = used_eeg
        super().__init__(name=self.used_eeg,stype = 'EEG',source_id = self.host_id,  bufsize=5)# 5 seconds of buffer 
        print('starting lsl streaming...')
        self.connect(acquisition_delay=0.001)
        self.sfreq = 125
        self.win_size = win_size

    def get_classification(self, list_freqs, num_harms=3, num_fbs=5):
        data = self.get_data(self.win_size)[0]
        #rt_epoch = mne.EpochsArray([data], self.info, verbose=False)
        #rt_epoch.apply_function(lambda x: x * 1e-6)
        ssvep_pred = fbcca_realtime(data, list_freqs, self.sfreq, num_harms, num_fbs)
        if ssvep_pred:
            print(f"SSVEP classification result: { list_freqs[ssvep_pred]} hz")
        else:
            print("SSVEP classification result: Threshold not reached")
        return ssvep_pred