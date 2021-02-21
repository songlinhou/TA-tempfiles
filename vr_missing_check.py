# tool created by Ray
import argparse
import pandas as pd
import os
from os.path import basename

missing_names = []


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--video_path",
                        help="The path to the video response folder",
                        required=True)
    parser.add_argument("-g",
                        "--grading_path",
                        default="grading.xlsx",
                        help="The path of the grading excel file")

    parser.add_argument("-f",
                        "--formated_output",
                        default="formated_csv",
                        help="The path of the generated csv file")

    args = parser.parse_args()
    return args


def match_names(df, video_folder):
    global missing_names
    missing_names = []
    account_names_in_df = df['User Name']
    names_with_videos = os.listdir(video_folder)
    names_with_videos = [
        basename(fname).split(".")[0] for fname in names_with_videos
    ]
    for name_in_df in account_names_in_df:
        if name_in_df not in names_with_videos:
            missing_names.append(name_in_df)
    return missing_names


def auto_no_submission_score(name):
    global missing_names
    try:
        if name.strip() in missing_names:
            return "0"
    except:
        pass
    return ""


def auto_no_submission_comment(name):
    global missing_names
    try:
        if name.strip() in missing_names:
            return "No submission"
    except:
        pass
    return ""


def generate_csv(df, output_name):
    global video_folder
    output_file_name = f'{output_name}.csv'
    new_df = pd.DataFrame()
    new_df['Student Name'] = df['Student Name']
    new_df['User Name'] = df['User Name']
    new_df['no_submissions_score'] = df['User Name'].apply(
        auto_no_submission_score)
    new_df['no_submissions_comment'] = df['User Name'].apply(
        auto_no_submission_comment)
    new_df.to_csv(output_file_name, index=False)
    print(f"CSV saved at {output_file_name}")


def run():
    global missing_names
    args = parse_args()
    df = pd.read_excel(args.grading_path)
    video_folder = args.video_path
    missing_names = match_names(df, args.video_path)
    num = len(missing_names)
    print("-" * 30)
    print(f"{num} people didn't submit video responses")
    print("-" * 30)
    index = range(1, num + 1)
    [print(f'[{idx}]\t{name}') for idx, name in zip(index, missing_names)]
    print("-" * 30)
    output_name = args.formated_output
    generate_csv(df, output_name)


if __name__ == '__main__':
    run()
