#!/usr/bin/env python3
"""Daily narrative digest: GSHQ project status + AI research briefing."""

import urllib.request
import json
import os
import re
import base64
from datetime import datetime, timedelta, timezone

TOKEN = os.environ.get('GITHUB_BOT_TOKEN', '') or os.environ.get('GITHUB_TOKEN', '')
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github+json',
}
HF_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'HermesAgent/1.0',
}

OWNER = 'jameslbarnes'
REPO_NAME = 'generalsemanticshq'
ETHEREA_REPO_NAME = 'etherea-ai'
GH_API = 'https://api.github.com'
HF_API = 'https://huggingface.co/api'


def _gh_url(*parts):
    return GH_API + '/' + '/'.join(str(p) for p in parts)


def api_get(url, headers=None):
    h = headers or HEADERS
    req = urllib.request.Request(url, headers=h)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except Exception:
        return None


def api_put(url, data, headers=None):
    h = headers or HEADERS
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers=h, method='PUT')
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except Exception:
        return None


# --- Deduplication ---

def load_previous_findings():
    """Load URLs/names from previous research logs to avoid repeats."""
    seen = set()
    tree_url = _gh_url('repos', OWNER, REPO_NAME, 'git', 'trees', 'main') + '?recursive=1'
    tree = api_get(tree_url)
    if not tree:
        return seen
    for t in tree.get('tree', []):
        if t['path'].startswith('research') and t['path'].endswith('.md') and 'README' not in t['path']:
            blob = api_get(t['url'])
            if blob and blob.get('content'):
                text = base64.b64decode(blob['content']).decode('utf-8')
                urls = re.findall(r'https?://[^\s\)]+', text)
                seen.update(urls)
                repos = re.findall(r'github\.com/([^\s\)/]+/[^\s\)/]+)', text)
                seen.update(repos)
                hf_ids = re.findall(r'huggingface\.co/([^\s\)/]+/[^\s\)/]+)', text)
                seen.update(hf_ids)
    return seen


# --- Project data ---

def get_recent_commits(owner, repo, since):
    since_str = since.strftime('%Y-%m-%dT%H:%M:%SZ')
    url = _gh_url('repos', owner, repo, 'commits') + f'?since={since_str}&per_page=10'
    commits = api_get(url)
    if not commits:
        return []
    return [{'message': c['commit']['message'].split('\n')[0], 'author': c['commit']['author']['name']} for c in commits]


def get_open_issues(owner, repo):
    url = _gh_url('repos', owner, repo, 'issues') + '?state=open&per_page=30'
    issues = api_get(url)
    if not issues:
        return []
    return [i for i in issues if not i.get('pull_request')]


def get_recently_closed(owner, repo, since):
    since_str = since.strftime('%Y-%m-%dT%H:%M:%SZ')
    url = _gh_url('repos', owner, repo, 'issues') + f'?state=closed&sort=updated&direction=desc&since={since_str}&per_page=10'
    issues = api_get(url)
    if not issues:
        return []
    return [i for i in issues if not i.get('pull_request')]


def find_reminders_due(issues, today_str):
    reminders = []
    for i in issues:
        body = (i.get('body') or '')
        for line in body.split('\n'):
            if 'reminder:' in line.lower() and today_str in line:
                reminders.append({
                    'number': i['number'],
                    'title': i['title'],
                    'reminder': line.strip(),
                })
    return reminders


def find_due_dates(issues):
    due_soon = []
    for i in issues:
        body = (i.get('body') or '').lower()
        for line in body.split('\n'):
            if 'due' in line:
                date_match = re.search(r'(\w+ \d+,? \d{4}|\d{4}-\d{2}-\d{2})', line, re.IGNORECASE)
                if date_match:
                    due_soon.append({
                        'number': i['number'],
                        'title': i['title'],
                        'due_line': line.strip(),
                    })
                break
    return due_soon


# --- AI Research ---
def get_new_github_repos_today():
    """Repos created in the last 24h with significant stars, spam-filtered."""
    yesterday = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%Y-%m-%d')
    # Two searches: broad AI + specific world-model/video/robotics
    q1 = f'created:>{yesterday}+stars:>20+(AI+OR+model+OR+video+OR+diffusion+OR+LLM+OR+agent+OR+transformer)'
    q2 = f'created:>{yesterday}+stars:>5+(robot+OR+embodied+OR+world+model+OR+video+prediction+OR+diffusion+transformer+OR+autoregressive+video)'
    data1 = api_get(_gh_url('search', 'repositories') + f'?q={q1}&sort=stars&order=desc&per_page=15')
    data2 = api_get(_gh_url('search', 'repositories') + f'?q={q2}&sort=stars&order=desc&per_page=10')
    # Merge and deduplicate
    seen_names = set()
    all_items = []
    for source in [data1, data2]:
        if source:
            for r in source.get('items', []):
                if r['full_name'] not in seen_names:
                    seen_names.add(r['full_name'])
                    all_items.append(r)
    all_items.sort(key=lambda x: x['stargazers_count'], reverse=True)
    # Filter out spam
    results = []
    for r in all_items:
        desc = r.get('description') or ''
        owner_name = r.get('owner', {}).get('login', '')
        if len(desc) < 20:
            continue
        if owner_name.isdigit():
            continue
        if desc.lower().count('ai') > 0 and len(desc) < 30 and r['stargazers_count'] < 50:
            continue
        results.append(r)
        if len(results) >= 10:
            break
    return results


def get_hf_daily_papers():
    data = api_get(HF_API + '/daily_papers?limit=50', headers=HF_HEADERS)
    if not data:
        return []
    keywords = ['video', 'world model', 'autoregressive', 'diffusion', 'generation',
                'vision', 'multimodal', 'embodied', 'robot', 'foundation model',
                'image', 'speech', 'tts', 'voice']
    results = []
    for p in data:
        paper = p.get('paper', {})
        title = paper.get('title', '').lower()
        if any(kw in title for kw in keywords):
            arxiv_id = paper.get('id', '')
            results.append({
                'title': paper.get('title', ''),
                'published': paper.get('publishedAt', '')[:10],
                'upvotes': p.get('numUpvotes', 0),
                'url': f'https://arxiv.org/abs/{arxiv_id}',
            })
    return results[:10]


def get_hf_trending_models():
    data = api_get(HF_API + '/trending', headers=HF_HEADERS)
    if not data:
        return []
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    yesterday = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%Y-%m-%d')
    results = []
    trending = data if isinstance(data, list) else data.get('recentlyTrending', [])
    for item in trending:
        repo_data = item.get('repoData', {}) if isinstance(item, dict) else {}
        modified = repo_data.get('lastModified', '')
        if today in modified or yesterday in modified:
            model_id = repo_data.get('id', '')
            results.append({
                'id': model_id,
                'likes': repo_data.get('likes', 0),
                'pipeline': repo_data.get('pipeline_tag', ''),
                'modified': modified[:10],
                'repo_type': item.get('repoType', 'model'),
                'url': f'https://huggingface.co/{model_id}',
            })
    return results[:10]


# --- Research log ---

def build_research_log(date_str, ai_items):
    lines = [f'# Research Log \u2014 {date_str}', '']
    if not ai_items:
        lines.append('No new findings today.')
        return '\n'.join(lines)
    for item in ai_items:
        lines.append(f"## {item['name']}")
        lines.append(f"- **Type:** {item.get('type', 'unknown')}")
        lines.append(f"- **What:** {item.get('description', '')}")
        if item.get('released'):
            lines.append(f"- **Released:** {item['released']}")
        if item.get('stars'):
            lines.append(f"- **Stars:** {item['stars']}")
        if item.get('likes'):
            lines.append(f"- **HF Likes:** {item['likes']}")
        if item.get('url'):
            lines.append(f"- **URL:** {item['url']}")
        if item.get('tags'):
            lines.append(f"- **Tags:** {', '.join(item['tags'])}")
        lines.append('')
    return '\n'.join(lines)


def push_research_log(date_str, content):
    file_path = f'research/{date_str}.md'
    encoded = base64.b64encode(content.encode()).decode()

    # Check if file exists via tree
    tree_url = _gh_url('repos', OWNER, REPO_NAME, 'git', 'trees', 'main') + '?recursive=1'
    tree = api_get(tree_url)
    existing_sha = None
    if tree:
        for t in tree.get('tree', []):
            if t['path'] == file_path:
                existing_sha = t['sha']
                break

    data = {
        'message': f'research: add findings for {date_str}',
        'content': encoded,
    }
    if existing_sha:
        data['sha'] = existing_sha

    put_url = _gh_url('repos', OWNER, REPO_NAME, 'contents', file_path)
    api_put(put_url, data)


# --- Narrative builder ---

def build_narrative_digest():
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=24)
    today_str = now.strftime('%Y-%m-%d')
    day_name = now.strftime('%A, %B %d')

    previous = load_previous_findings()

    # Project data
    gshq_commits = get_recent_commits(OWNER, REPO_NAME, since)
    etherea_commits = get_recent_commits(OWNER, ETHEREA_REPO_NAME, since)
    open_issues = get_open_issues(OWNER, REPO_NAME)
    closed_issues = get_recently_closed(OWNER, REPO_NAME, since)
    reminders = find_reminders_due(open_issues, today_str)
    due_dates = find_due_dates(open_issues)

    # AI research
    new_repos = get_new_github_repos_today()
    hf_papers = get_hf_daily_papers()
    hf_trending = get_hf_trending_models()

    # Deduplicate
    fresh_repos = [r for r in new_repos if r['full_name'] not in previous and r['html_url'] not in previous]
    fresh_papers = [p for p in hf_papers if p['url'] not in previous]
    fresh_trending = [t for t in hf_trending if t['id'] not in previous]

    # Build AI items for research log (all findings) and narrative (top 3)
    ai_items = []
    ai_narrative = []

    for r in fresh_repos[:5]:
        item = {
            'name': r['full_name'],
            'type': 'GitHub repo',
            'description': r.get('description', '') or '',
            'released': r['created_at'][:10],
            'stars': r['stargazers_count'],
            'url': r['html_url'],
            'tags': r.get('topics', []),
        }
        ai_items.append(item)
        if len(ai_narrative) < 3:
            ai_narrative.append(item)

    for p in fresh_papers[:5]:
        item = {
            'name': p['title'],
            'type': 'arxiv paper',
            'description': p['title'],
            'released': p['published'],
            'url': p['url'],
            'tags': ['paper'],
        }
        ai_items.append(item)
        if len(ai_narrative) < 3:
            ai_narrative.append(item)

    for t in fresh_trending[:5]:
        item = {
            'name': t['id'],
            'type': f"HuggingFace {t['repo_type']}",
            'description': f"{t['pipeline']} model" if t['pipeline'] else 'trending on HuggingFace',
            'likes': t['likes'],
            'url': t['url'],
            'tags': [t['pipeline']] if t['pipeline'] else [],
        }
        ai_items.append(item)
        if len(ai_narrative) < 3:
            ai_narrative.append(item)

    # Push research log
    if ai_items:
        log_content = build_research_log(today_str, ai_items)
        push_research_log(today_str, log_content)

    # --- Build narrative ---
    parts = []
    parts.append(day_name)
    parts.append('')

    # Opening: what happened overnight
    if gshq_commits or etherea_commits:
        commit_msgs = [c['message'] for c in gshq_commits[:3]]
        if commit_msgs:
            summary = ', '.join(commit_msgs)
            if len(gshq_commits) > 3:
                summary += f', and {len(gshq_commits) - 3} more'
            parts.append(f'In the repo overnight: {summary}.')
        if etherea_commits:
            eth_msgs = [c['message'] for c in etherea_commits[:3]]
            parts.append(f'On Etherea-AI: {", ".join(eth_msgs)}.')
        else:
            parts.append('Nothing new on Etherea-AI.')
    else:
        parts.append('Quiet night \u2014 no new commits on either repo.')

    if closed_issues:
        titles = [f'#{i["number"]} ({i["title"]})' for i in closed_issues[:3]]
        parts.append(f'Closed: {", ".join(titles)}.')
    else:
        parts[-1] += ' No issues were closed and no PRs opened.'

    parts.append('')

    # Today's action items
    today_actions = []
    for r in reminders:
        detail = r['reminder'].split('\u2014')[-1].strip() if '\u2014' in r['reminder'] else r['reminder']
        today_actions.append(f'#{r["number"]} ({r["title"]}) \u2014 {detail}')
    for d in due_dates:
        today_actions.append(f'#{d["number"]} ({d["title"]}) \u2014 {d["due_line"]}')

    if today_actions:
        action_text = '. '.join(today_actions[:3])
        parts.append(f'{action_text}. {"These need" if len(today_actions) > 1 else "This needs"} attention today.')
    else:
        parts.append('Nothing time-sensitive for today.')

    parts.append('')

    # Simmering
    action_numbers = set()
    for r in reminders:
        action_numbers.add(r['number'])
    for d in due_dates:
        action_numbers.add(d['number'])
    simmering = [i for i in open_issues if i['number'] not in action_numbers]
    if simmering:
        simmer_list = ', '.join([f'{i["title"]} (#{i["number"]})' for i in simmering[:7]])
        parts.append(f'Simmering: {simmer_list}.')

    parts.append('')

    # AI briefing (max 3, narrative)
    if ai_narrative:
        bits = []
        for item in ai_narrative[:3]:
            name = item['name']
            desc = item.get('description', '')
            url = item.get('url', '')
            stars = item.get('stars')
            likes = item.get('likes')
            metric = f' ({stars} stars)' if stars else (f' ({likes} likes)' if likes else '')
            bits.append(f'{name}{metric} \u2014 {desc}. {url}')
        parts.append('AI briefing: ' + ' '.join(bits))
    else:
        parts.append('AI briefing: Nothing notable surfaced today that we haven\'t already tracked.')

    return '\n'.join(parts)


if __name__ == '__main__':
    print(build_narrative_digest())
