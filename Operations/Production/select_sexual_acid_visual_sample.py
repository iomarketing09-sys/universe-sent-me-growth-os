import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
df=pd.read_csv(root/'Operations/Research/2026-08-19_Candidatos_Humor_Sexual_Acido.csv')
acid=df[df.candidate_type.eq('acid')].sort_values(['shares','interactions'],ascending=False).head(8)
sexual=df[df.candidate_type.isin(['sexual','mixed'])].sort_values(['shares','interactions'],ascending=False).head(8)
out=pd.concat([acid,sexual]).drop_duplicates('meta_id')
out['sample_group']=out.candidate_type.map({'acid':'acid','sexual':'sexual','mixed':'mixed'})
path=root/'Operations/Research/2026-08-19_Muestra_Visual_Humor_Sexual_Acido.csv'; out.to_csv(path,index=False)
print(out[['meta_id','candidate_type','caption','interactions','comments','shares']].to_string(index=False))
