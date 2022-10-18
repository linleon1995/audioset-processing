from pathlib import Path

import pandas as pd


def get_audioset_num_class(data_path: str, class_name: str, data_indices_path: str) -> int:
    """To check the file number of interesting class.

    Args:
        data_path (str): AudioSet data table path.
        class_name (str): Intersting class name in AudioSet.
        data_indices_path (str): Mapping between class name and url key.

    Returns:
        int: The count of file of interesting class.
    """
    df = pd.read_csv(data_path, sep='\t')
    class_df = pd.read_csv(data_indices_path, sep='\t', header=None)

    class_key = class_df.loc[class_df[1]==class_name][0].values[0]
    df_with_class = df.loc[df['label']==class_key]
    num_class = len(pd.unique(df_with_class['segment_id']))
    return num_class


def get_download_rate(
    data_path: str, class_name: str, data_indices_path: str, download_dir: str, suffix: str = 'wav'):
    """To get download rate of AudioSet

    Args:
        data_path (str): AudioSet data table path.
        class_name (str): Intersting class name in AudioSet.
        data_indices_path (str): Mapping between class name and url key.
        download_dir (str): The local data saving directory.
        suffix (str, optional): Interesting data format. Defaults to 'wav'.
    """
    download_dir = Path(download_dir)
    num_download = len(list(download_dir.rglob(f'*.{suffix}')))
    num_class = get_audioset_num_class(data_path, class_name, data_indices_path)
    print(f'{class_name} {num_download}/{num_class} ({num_download/num_class*100:.2f} %)')


def main():
    classes = [
        'Snoring', 
        'Car passing by', 
        'White noise, pink noise', 
        'Alarm clock', 
        'Wind noise (microphone)'
    ]
    for c in classes:
        data_path = 'strong_label/audioset_train_strong.tsv'
        dirname = c.split(' ')[0]
        download_dir = f'data/strong/audioset_train_strong/{dirname}'
        get_download_rate(data_path, c, 'strong_label/mid_to_display_name.tsv', download_dir)


if __name__ == '__main__':
    main()
