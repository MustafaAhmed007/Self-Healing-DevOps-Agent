'use client';

import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [health, setHealth] = useState(null);
  const [repo, setRepo] = useState('');
  const [issue, setIssue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { fetch(`${API}/health`).then(r => r.json()).then(setHealth).catch(() => setHealth({status:'offline'})); }, []);

  async function startRepair(e) {
    e.preventDefault(); setLoading(true); setResult(null);
    try {
      const r = await fetch(`${API}/v1/repairs`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({repository:repo, issue_number:Number(issue), publish:false}) });
      setResult(await r.json());
    } catch (err) { setResult({error:String(err)}); } finally { setLoading(false); }
  }

  return <main style={{maxWidth:960,margin:'40px auto',padding:24,fontFamily:'system-ui'}}>
    <h1>Self-Healing DevOps Agent</h1>
    <p>Evidence-driven repair control plane.</p>
    <p>Status: <b>{health?.status || 'checking'}</b> · sandbox: {health?.sandbox || '—'}</p>
    <form onSubmit={startRepair} style={{display:'grid',gap:12,maxWidth:600}}>
      <input required placeholder="OWNER/REPOSITORY" value={repo} onChange={e=>setRepo(e.target.value)} style={{padding:12}} />
      <input required type="number" min="1" placeholder="Issue number" value={issue} onChange={e=>setIssue(e.target.value)} style={{padding:12}} />
      <button disabled={loading} style={{padding:12}}>{loading ? 'Running repair…' : 'Start bounded repair'}</button>
    </form>
    {result && <pre style={{marginTop:24,padding:16,overflow:'auto',background:'#f4f4f4'}}>{JSON.stringify(result,null,2)}</pre>}
  </main>;
}
