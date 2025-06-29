import os
import random
import shutil

def organize_test_files():
    source_dir_typo = '01'
    source_dir_correct = '02'
    dest_dirs = ['for_test_a', 'for_test_b']

    # Get unique base filenames (e.g., '01.html', '02.html', ...)
    base_filenames = [f for f in os.listdir(source_dir_typo) if f.endswith('.html')]
    random.shuffle(base_filenames)

    # We need 10 files for each directory, 5 with typos, 5 without.
    # Total 20 unique titles needed.
    if len(base_filenames) < 20:
        print("Not enough unique files to perform the operation.")
        return

    # Select 20 unique titles
    selected_titles = base_filenames[:20]

    # Assign 10 titles to be with typos, 10 to be correct
    typo_titles = set(random.sample(selected_titles, 10))
    correct_titles = set(selected_titles) - typo_titles

    # Assign files to directories
    test_a_titles = random.sample(list(selected_titles), 10)
    test_b_titles = list(set(selected_titles) - set(test_a_titles))

    report = {d: [] for d in dest_dirs}

    def copy_files(titles, dest_dir):
        for title in titles:
            if title in typo_titles:
                shutil.copy(os.path.join(source_dir_typo, title), dest_dir)
                report[dest_dir].append({'name': title, 'typo': True})
            else:
                shutil.copy(os.path.join(source_dir_correct, title), dest_dir)
                report[dest_dir].append({'name': title, 'typo': False})

    copy_files(test_a_titles, 'for_test_a')
    copy_files(test_b_titles, 'for_test_b')

    # Generate the report string
    report_str = "## テストディレクトリ\n"
    for dest_dir, files in report.items():
        report_str += f"### {dest_dir}\n"
        report_str += "| ファイル名 | 誤字の有無 |\n"
        report_str += "|------------|------------|\n"
        # Sort files by name for a clean report
        sorted_files = sorted(files, key=lambda x: x['name'])
        for file_info in sorted_files:
            status = "あり" if file_info['typo'] else "なし"
            report_str += f"| {file_info['name']}    | {status}       |\n"
        report_str += "\n"

    # Read readme and append the report
    with open('readme.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Remove old report if it exists
    if "## テストディレクトリ" in readme_content:
        readme_content = readme_content.split("## テストディレクトリ")[0]

    with open('readme.md', 'w', encoding='utf-8') as f:
        f.write(readme_content + report_str)

if __name__ == "__main__":
    organize_test_files()