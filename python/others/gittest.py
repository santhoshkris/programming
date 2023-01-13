"""Git testing."""

from git import Repo
# import os

# repo = Repo('~/test-repo')
# # print(repo.branches)
# branch_name = input("Enter the branch name..: ")
# print(branch_name)
# repo.git.checkout('-b', branch_name)
# # os.system('echo "HELLO..." >> ~/test-repo/README.md')
# repo.git.add('--all')
# repo.git.commit('-m', 'commit message from py script')
# repo.git.push('--set-upstream', 'origin', branch_name)
# origin = repo.remote(name='origin')
# origin.push()

# repo = Repo.clone_from('git@github.com:seekasia/myjs.git', '.')


def git_test():
    repo = Repo('~/dotfiles')
    print(repo.branches)
