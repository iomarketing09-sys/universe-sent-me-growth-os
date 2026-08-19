import json, statistics
from pathlib import Path

ROOT=Path('/home/ubuntu/universe-sent-me-growth-os')
RAW={
 'instagram':Path('/home/ubuntu/.mcp/tool-results/2026-08-19_02-50-33.317227361_windsor-ai_get_data_17ffd3d0.json'),
 'tiktok':Path('/home/ubuntu/.mcp/tool-results/2026-08-19_03-02-17.926722753_windsor-ai_get_data_b0820052.json'),
 'youtube':Path('/home/ubuntu/.mcp/tool-results/2026-08-19_03-01-49.788204265_windsor-ai_get_data_354eb33e.json'),
}
def load_rows(path):
 return json.loads(path.read_text())['structuredContent']['result']
def n(v):
 return None if v is None else float(v)
def choose(rows,key):
 best={}
 for r in rows:
  k=r.get(key)
  if not k: continue
  score=sum(v is not None for v in r.values())
  if k not in best or score>best[k][0]: best[k]=(score,r)
 return [x[1] for x in best.values()]
def tiktok_rows(rows):
 rows=choose([r for r in rows if r.get('video_id')],'video_id')
 out=[]
 for r in rows:
  out.append({'platform':'TikTok','account_id':r.get('account_id'),'account_name':r.get('account_name'),'content_id':r.get('video_id'),'published_at':r.get('video_create_datetime'),'content_type':'Video','caption':r.get('video_caption'),'duration_seconds':n(r.get('video_duration')),'views':n(r.get('video_views_count')),'reach':n(r.get('video_reach')),'likes':n(r.get('video_likes')),'comments':n(r.get('video_comments')),'shares':n(r.get('video_shares')),'saves_or_favorites':n(r.get('video_favorites')),'avg_watch_time_seconds':n(r.get('video_average_time_watched')),'total_watch_time_seconds':n(r.get('video_total_time_watched')),'completion_rate':n(r.get('video_full_watched_rate')),'followers_gained':n(r.get('video_new_followers')),'subscribers_gained':None,'subscribers_lost':None,'source':'Windsor.ai:tiktok_organic','retrieved_at':r.get('data_fetched_at'),'window_type':'lifetime_current_snapshot','comparability':'within_platform_primary'} )
 return out
def youtube_rows(rows):
 daily=[]
 for r in rows:
  if not r.get('video'): continue
  daily.append({'platform':'YouTube','account_id':r.get('account_id'),'account_name':r.get('account_name'),'content_id':r.get('video'),'published_at':None,'content_type':'Video_or_Short','title':r.get('video_title'),'date':r.get('date'),'views':n(r.get('views')),'likes':n(r.get('likes')),'comments':n(r.get('comments')),'shares':n(r.get('shares')),'avg_watch_time_seconds':n(r.get('average_view_duration')),'average_view_percentage':n(r.get('average_view_percentage')),'subscribers_gained':n(r.get('subscribers_gained')),'subscribers_lost':n(r.get('subscribers_lost')),'followers_gained':None,'lifetime_views_snapshot':n(r.get('video_view_count')),'source':'Windsor.ai:youtube','retrieved_at':r.get('data_fetched_at'),'window_type':'daily_observed_activity','comparability':'within_platform_primary'})
 snapshots={}
 for r in daily:
  k=r['content_id']
  if k not in snapshots or sum(v is not None for v in r.values())>sum(v is not None for v in snapshots[k].values()): snapshots[k]=r.copy()
 return daily,list(snapshots.values())
def instagram_rows(rows):
 out=[]
 for r in rows:
  typ='Reel' if r.get('media_type')=='REELS' else ('Carousel' if r.get('media_type')=='CAROUSEL_ALBUM' else 'Image')
  out.append({'platform':'Instagram','account_id':r.get('account_id'),'account_name':r.get('account_name'),'content_id':r.get('media_id'),'published_at':r.get('timestamp'),'content_type':typ,'caption':r.get('media_caption'),'views':n(r.get('media_views')),'reach':n(r.get('media_reach')),'likes':n(r.get('media_like_count')),'comments':n(r.get('media_comments_count')),'shares':n(r.get('media_shares')),'saves_or_favorites':n(r.get('media_saved')),'engagement':n(r.get('media_engagement')),'avg_watch_time_seconds':n(r.get('media_reel_avg_watch_time'))/1000 if r.get('media_reel_avg_watch_time') is not None else None,'total_watch_time_seconds':n(r.get('media_reel_total_watch_time'))/1000 if r.get('media_reel_total_watch_time') is not None else None,'source':'Windsor.ai:instagram','retrieved_at':r.get('data_fetched_at'),'window_type':'lifetime_current_snapshot','comparability':'within_platform_primary'})
 return out
def aggregate(rows,views_key='views'):
 def s(k): return sum((r.get(k) or 0) for r in rows)
 vals=[r.get('engagement') for r in rows if r.get('engagement') is not None]
 pct=[r.get('average_view_percentage') for r in rows if r.get('average_view_percentage') is not None]
 return {'content_count':len(rows),'views_total':s(views_key),'reach_total':s('reach'),'engagement_total':s('engagement'),'likes_total':s('likes'),'comments_total':s('comments'),'shares_total':s('shares'),'saves_or_favorites_total':s('saves_or_favorites'),'followers_gained_total':s('followers_gained'),'subscribers_gained_total':s('subscribers_gained'),'subscribers_lost_total':s('subscribers_lost'),'average_view_percentage_mean':sum(pct)/len(pct) if pct else None,'engagement_median':statistics.median(vals) if vals else None}
ig=instagram_rows(load_rows(RAW['instagram']))
tt=tiktok_rows(load_rows(RAW['tiktok']))
yt_daily,yt_snapshots=youtube_rows(load_rows(RAW['youtube']))
# derive comparable engagement where native engagement is absent
def add_eng(r):
 if r.get('engagement') is None:
  parts=[r.get(k) or 0 for k in ('likes','comments','shares','saves_or_favorites')]
  if any(x is not None for x in parts): r['engagement']=sum(parts)
for group in (ig,tt,yt_daily,yt_snapshots):
 for r in group: add_eng(r)
out={'cut':{'start':'2026-07-22','end':'2026-08-18'},'retrieved_at':'2026-08-19','sources':['Windsor.ai:instagram','Windsor.ai:tiktok_organic','Windsor.ai:youtube'],'normalization_rules':['One row per Instagram media_id and TikTok video_id after deduplication.','YouTube keeps daily_observed_activity separately from lifetime_current_snapshot.','No cross-platform totals are used as a performance verdict because metric definitions and windows differ.'],'platforms':{'Instagram':{'content_rows':ig,'aggregates':aggregate(ig)},'TikTok':{'content_rows':tt,'aggregates':aggregate(tt)},'YouTube':{'daily_rows':yt_daily,'daily_aggregates':aggregate(yt_daily),'lifetime_snapshots':yt_snapshots,'lifetime_snapshot_aggregates':aggregate(yt_snapshots,'lifetime_views_snapshot')}}}
path=ROOT/'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'
path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for p in ('Instagram','TikTok','YouTube'):
 d=out['platforms'][p]
 print(p,'content',len(d.get('content_rows',d.get('lifetime_snapshots',[]))),'daily',len(d.get('daily_rows',[])),'aggregates',d.get('aggregates',d.get('daily_aggregates')))
print('OUTPUT',path)
