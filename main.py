import os
from time import time, sleep, perf_counter, perf_counter_ns
from concurrent.futures import ProcessPoolExecutor
import git
from pathlib import Path
from github import Github

TOKEN = os.environ.get("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")
TOKEN2 = os.environ.get("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")
g = Github(TOKEN)
INSTALL_DIR = Path.cwd() / 'repos'
#executor = ProcessPoolExecutor()


def search_repos():
    repos = []
    for i, repo in enumerate(g.search_repositories("language:rust", sort="stars")):
        if i >= 250:
            break
        repos.append(str(repo.clone_url))
    return repos


def record_repos_paths_to_file():
    repos_list = search_repos()
    with open("reposPaths.txt", 'w') as file:
        for i in repos_list:
            file.write(i + '\n')
            print(i)
    return repos_list


def clone(git_url, repo_dir):
    print('Cloning into %s' % repo_dir)
    git.Repo.clone_from(git_url, repo_dir)


def search_rust_files(directory):
    rs_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".rs"):
                rs_files.append(os.path.join(root, file))
    return rs_files


def file_count_funcs(file):
    count = 0
    with open(file, 'r', encoding="utf-8", errors="ignore") as f:
        for line in f:
            if 'fn ' in line:
                count += 1
    return count


def main():
    list_repos = []
    ###list_repos.append("https://github.com/Schniz/fnm.git")
    list_repos = search_repos()
    with open("log.txt", 'w') as log:
        # with open("reposPaths.txt", 'r') as path:
        #   list_repos.append(path.read())
        global_count = 0
        for i, repo in enumerate(list_repos):
            current_repo_funcs = 0
            try:
                clone(repo, INSTALL_DIR / str(i))
                rs_files = search_rust_files(INSTALL_DIR / str(i))
                for file in rs_files:
                    count_funcs = file_count_funcs(file)
                    current_repo_funcs += count_funcs
                    path_to_file = file.split('\\')
                    file_name = path_to_file[len(path_to_file) - 1]
                    log.write(
                        str(i) + '; ' + str(repo) + '; ' + str(file_name) + '; ' + str(
                            count_funcs) + '\n')
                log.write('Repository funcs: ' + str(current_repo_funcs) + '\n')
                global_count += current_repo_funcs
                log.write('Global count funcs: ' + str(global_count) + '\n')
            except git.GitError:
                print('some error\n')
                continue
        log.write('Global count funcs: ' + str(global_count) + '\n')


if __name__ == "__main__":
    t1 = perf_counter()
    main()
    t2 = perf_counter()
    print(t2 - t1)
