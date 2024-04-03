import datetime
import os

import dotenv
import pytz
import requests
import requests_cache

dotenv.load_dotenv()
requests_cache.install_cache('github_cache', expire_after=3600 * 24)

TOKEN = os.environ.get('PERSONAL_ACCESS_TOKEN', 'no token')
HEADERS = {'Authorization': f'token {TOKEN}'}


def get_repos() -> list[str]:
    """Get a list of repos for the authenticated user."""
    url = 'https://api.github.com/user/repos'
    params = {'per_page': 100}
    repos = []

    while url:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        # print(r.from_cache)
        data = r.json()
        repos.extend([repo['full_name'] for repo in data])  # username/repo

        url = None
        if 'next' in r.links:
            url = r.links['next']['url']

    return repos


def get_commit_hour(dt: str, tz: str = 'Europe/Moscow') -> int:
    utc_time = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')
    tz_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(tz))
    return tz_time.hour


def get_repo_commits(full_repo_name: str) -> list[int]:
    """Get a list of commits from a specific repo with a Moscow time."""
    url = f'https://api.github.com/repos/{full_repo_name}/commits'
    params = {'per_page': 100}
    commit_hours = []

    while url:
        try:
            r = requests.get(url, headers=HEADERS, params=params)
            r.raise_for_status()
        except requests.HTTPError:
            return []
        data = r.json()

        for commit in data:
            # message = commit['commit']['message']
            commit_dt = commit['commit']['committer']['date']
            hour = get_commit_hour(commit_dt)
            commit_hours.append(hour)

        url = None
        if 'next' in r.links:
            url = r.links['next']['url']

    return commit_hours


def show_total_commit_pct() -> None:
    """Output percentage of commits for each hour."""
    repos = get_repos()
    hour_counts = {hour: 0 for hour in range(24)}

    for repo in repos:
        commit_hours = get_repo_commits(repo)
        if commit_hours:
            for hour in commit_hours:
                hour_counts[hour] += 1

    total_commits = sum(hour_counts.values())

    for hour, count in hour_counts.items():
        percentage = (count / total_commits) * 100 if total_commits > 0 else 0
        print(f"Hour {hour:02d}: {percentage:.2f}%")


if __name__ == '__main__':
    show_total_commit_pct()
