from tkinter import Y
import pandas as pd
from pathlib import Path
import os

# defaults
AUDIOSET_STRONG_TRAIN = 'strong_label/audioset_train_strong.tsv'
AUDIOSET_STRONG_EVAL = 'strong_label/audioset_eval_strong.tsv'
CLASS_NAMES = 'strong_label/class.csv'
MID_TO_DISPLAY_NAME = 'strong_label/mid_to_display_name.tsv'
DEFAULT_FS = 16000

DEFAULT_CSV_DATASET = '../data/unbalanced_train_segments.csv'
DEFAULT_DEST_DIR = '../output/'
DEFAULT_DEST_DIR = 'output/'


def get_class_names(class_names_path, class_mapping_path):
    class_names = pd.read_csv(class_names_path, header=None)
    class_mapping = pd.read_csv(class_mapping_path, sep='\t', header=None)
    
    cls_mapping = {}
    print(class_names)
    for idx, cls in class_names.iterrows():
        cls_name = cls.item()
        cls_mapping[cls_name] = class_mapping.loc[class_mapping[1]==cls_name, 0].item()
    
    print(cls_mapping)
    return cls_mapping


def parse_audioset_strong_label(audioset_path, class_names_path, class_mapping_path):
    cls_mapping = get_class_names(class_names_path, class_mapping_path)
    audioset = pd.read_csv(audioset_path, sep='\t')
    df_dict = {}
    for cls_name, cls_key in cls_mapping.items():
        cls_data = audioset.loc[audioset['label']==cls_key]
        # cls_name = cls_name.split(' ')[0]
        df_dict[cls_name] = cls_data

        # for index, row in cls_data.iterrows():
        #     print(row['segment_id'])
    return df_dict


def download(split):
    
    df_dict = parse_audioset_strong_label(split, CLASS_NAMES, MID_TO_DISPLAY_NAME)
    import shlex, subprocess
    max_len = 200
    for cls_name, cls_data in df_dict.items():
        dst_dir = Path(f'data/strong_label/{split.stem}/{cls_name}')
        dst_dir.mkdir(parents=True, exist_ok=True)
        for audio_idx, (index, row) in enumerate(cls_data.drop_duplicates(subset = "segment_id").iterrows()):
            if cls_name != 'Snoring':
                if audio_idx > max_len: 
                    break
            # if audio_idx > max_len: 
            #     break

            # command = (
            #     f'ffmpeg -i \'"$(youtube-dl -f {"bestaudio"} -g https://www.youtube.com/watch?v='
            #     f'{row["segment_id"]})"\' -ar {DEFAULT_FS} -- "{row["segment_id"]}.wav"'
            # )
            download_command = f'yt-dlp -x --audio-format mp3 -o "{dst_dir}/{row["segment_id"]}.mp3"\
                https://www.youtube.com/watch?v={row["segment_id"]}'
            # convert_command = f'ffmpeg -i --CHY2qO5zc_30000.mp3 -ar {DEFAULT_FS} -- "--CHY2qO5zc_30000.wav"'
            print(download_command)
            os.system(f'"{download_command}"')
            # os.system(convert_command)

# >>> import shlex, subprocess
# >>> command_line = input()
# /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
# >>> args = shlex.split(command_line)
# >>> print(args)
# ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
# >>> p = subprocess.Popen(args) # Success!

if __name__ == '__main__':
    split = Path(AUDIOSET_STRONG_TRAIN)
    # split = Path(AUDIOSET_STRONG_EVAL)
    download(split)