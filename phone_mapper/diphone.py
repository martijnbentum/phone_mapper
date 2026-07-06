'''Recoded phone set of the diphone_perception experiment.

Idiosyncratic to that dataset, not a general transcription standard:
the experiment labels phones with DISC symbols made filename-safe
(rewrite_dict) and recoded to two-letter codes (recode_dict).
https://github.com/martijnbentum/diphone_perception
'''
from .mapper import disc_to_ipa

name = 'diphone'

phonemes = 'I E A O } @ i a u y e | o K L M'
phonemes += ' p b t d k g N m n l r f v s z S Z j x h w _'
phonemes = phonemes.split()

rewrite_dict = {'|': 'eu', '_': 'J', '@': 'V', '}': 'U'}

recode_dict = {
    'I': 'ih', 'E': 'eh', 'A': 'ah', 'O': 'oh', 'U': 'uh', 'V': 'vh',
    'K': 'ei', 'L': 'ui', 'M': 'au', 'N': 'ng', 'S': 'sh', 'Z': 'zh',
    'G': 'gx', 'J': 'dj',
}

to_ipa_org = {disc: disc_to_ipa[disc] for disc in phonemes}
to_ipa_org['-'] = to_ipa_org['_']
to_ipa_rew = {rewrite_dict.get(k, k): v for k, v in to_ipa_org.items()}
to_ipa = {recode_dict.get(k, k): v for k, v in to_ipa_rew.items()}
to_ipa['gx'] = 'ɣ'
