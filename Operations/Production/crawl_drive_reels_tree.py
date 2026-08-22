import json
import subprocess
from collections import deque
from pathlib import Path

ROOT_FOLDER = '1kWkZSbWvMGe0fwXu93UTh1iK6aVfE70a'


def list_children(folder_id):
    params = json.dumps({
        'q': f"'{folder_id}' in parents and trashed = false",
        'pageSize': 1000,
        'orderBy': 'name',
        'fields': 'files(id,name,mimeType,parents,createdTime,modifiedTime,size,videoMediaMetadata,imageMediaMetadata,webViewLink),nextPageToken',
    })
    result = subprocess.run(['gws', 'drive', 'files', 'list', '--params', params, '--format', 'json'], check=True, capture_output=True, text=True)
    return json.loads(result.stdout).get('files', [])

queue = deque([ROOT_FOLDER])
visited = set()
all_files = []
errors = []
while queue:
    folder = queue.popleft()
    if folder in visited:
        continue
    visited.add(folder)
    try:
        children = list_children(folder)
    except Exception as exc:
        errors.append({'folder_id': folder, 'error': str(exc)})
        continue
    all_files.extend(children)
    for f in children:
        if f.get('mimeType') == 'application/vnd.google-apps.folder':
            queue.append(f['id'])

out = {
    'root_folder_id': ROOT_FOLDER,
    'folders_visited': sorted(visited),
    'files': all_files,
    'errors': errors,
}
Path('/home/ubuntu/drive_reels_tree.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'folders_visited': len(visited), 'files': len(all_files), 'errors': len(errors), 'output': '/home/ubuntu/drive_reels_tree.json'}, ensure_ascii=False))
