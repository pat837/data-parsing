import os
import pandas as pd
import youtube_dl
import ffmpeg


def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path


def trim_video(input_path, output_path, start_time, end_time):
    input_file = ffmpeg.input(input_path)
    output_file = input_file.trim(
        start=start_time, end=end_time).output(output_path)
    ffmpeg.run(output_file)


if __name__ == "__main__":
    # Step 1: Parse CSV file using pandas
    csv_file = "C:/Users/srinivas/Desktop/jio/urls.csv"
    df = pd.read_csv(csv_file)

    # import pdb;pdb.set_trace()

    clips = []
    for _, row in df.iterrows():
        # Step 2: Download video
        youtube_url = row['url']

        output_folder = 'C:/Users/srinivas/Desktop/jio/outputvideos'
        downloaded_path = download_video(youtube_url, output_folder)

        # Step 3: Trim video into multiple segments
        start_time = row['start']
        end_time = row['stop']

        trimmed_output = os.path.join(
            output_folder, f"{row['video_title']}_trimmed.mp4")
        trim_video(downloaded_path, trimmed_output, start_time, end_time)

        clips.append(trimmed_output)

    # Step 4: Club trimmed segments
    concat_list = '|'.join(clips)
    ffmpeg.input(f'concat:{concat_list}').output(
        'C:/Users/srinivas/Desktop/jio/pythomnoutputvideos', c='copy').run()
