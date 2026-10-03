import json
import urllib.request
import urllib.error
import os

# Load user token from tenants/universe/.env
user_token = None
with open('tenants/universe/.env', 'r') as f:
    for line in f:
        if line.startswith('META_ACCESS_TOKEN='):
            user_token = line.split('=', 1)[1].strip()
            break
if not user_token:
    raise ValueError('META_ACCESS_TOKEN not found in tenants/universe/.env')

# Get page access token
page_id = '1036844829507460'
url = f'https://graph.facebook.com/v26.0/{page_id}?fields=access_token&access_token={user_token}'
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        page_token = data.get('access_token')
except Exception as e:
    print(f'Failed to get page token: {e}')
    exit(1)

if not page_token:
    print('No access token in response')
    exit(1)

# Base URL and fields
base_url = 'https://graph.facebook.com/v26.0/'
fields = 'id,from,created_time,is_published,permalink_url,shares,comments.summary(true),reactions.summary(true)'

# Post IDs in order: Wilfred (3) then Control (3)
post_ids = [
    '1036844829507460_122160935757072582',
    '1036844829507460_122161375299072582',
    '1036844829507460_122161649019072582',
    '1036844829507460_122160925809072582',
    '1036844829507460_122161373049072582',
    '1036844829507460_122161629063072582'
]

wilfred_data = []
control_data = []

# Ensure snapshots directory exists
os.makedirs('snapshots', exist_ok=True)

for i, post_id in enumerate(post_ids):
    url = f'{base_url}{post_id}?fields={fields}&access_token={page_token}'
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f'HTTP Error for {post_id}: {e.code} {e.reason}')
        # Stop on error as per no retry and we cannot proceed
        break
    except Exception as e:
        print(f'Error fetching {post_id}: {e}')
        break

    # Check from.id
    from_info = data.get('from', {})
    if from_info.get('id') != page_id:
        print(f'Post {post_id} has from.id {from_info.get("id")}, expected {page_id}. Stopping.')
        break

    # Save snapshot
    snapshot_path = f'snapshots/{post_id}.json'
    with open(snapshot_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Saved snapshot for {post_id}')

    # Assign to appropriate list
    if i < 3:
        wilfred_data.append(data)
    else:
        control_data.append(data)

# Descriptive comparison
print('\n=== Descriptive Comparison ===')
print(f'Wilfred posts collected: {len(wilfred_data)}')
print(f'Control posts collected: {len(control_data)}')

if wilfred_data and control_data:
    # Compare each field
    fields_to_compare = ['is_published', 'created_time', 'permalink_url']
    for field in fields_to_compare:
        print(f'\n{field}:')
        w_vals = [p.get(field) for p in wilfred_data]
        c_vals = [p.get(field) for p in control_data]
        print(f'  Wilfred: {w_vals}')
        print(f'  Control: {c_vals}')
    # For shares, comments, reactions
    for field in ['shares', 'comments', 'reactions']:
        print(f'\n{field}:')
        w_summary = []
        c_summary = []
        for p in wilfred_data:
            val = p.get(field)
            if isinstance(val, dict) and 'summary' in val:
                w_summary.append(val['summary'].get('total_count'))
            else:
                w_summary.append(None)
        for p in control_data:
            val = p.get(field)
            if isinstance(val, dict) and 'summary' in val:
                c_summary.append(val['summary'].get('total_count'))
            else:
                c_summary.append(None)
        print(f'  Wilfred summary totals: {w_summary}')
        print(f'  Control summary totals: {c_summary}')
else:
    print('Not enough data for comparison.')

