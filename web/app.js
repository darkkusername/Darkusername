const state={};
const $=s=>document.querySelector(s);
async function api(path,options={}){
  const r=await fetch(path,{...options,headers:{"Content-Type":"application/json",...(options.headers||{})}});
  const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Request failed"); return data;
}
async function load(){
  const [dash,status,health]=await Promise.all([api("/api/v1/dashboard"),api("/api/v1/agent/status"),api("/health")]);
  $("#health").textContent=health.status.toUpperCase();
  $("#market").textContent=dash.market;
  $("#language").textContent=dash.language;
  $("#agents").textContent=status.agents.length;
}
async function run(){
  const task=$("#task").value.trim(); if(!task)return;
  $("#result").textContent="Running pipeline…";
  try{
    const data=await api("/api/v1/pipeline/run",{method:"POST",body:JSON.stringify({task})});
    $("#result").textContent=JSON.stringify(data,null,2);
  }catch(e){$("#result").textContent=e.message}
}
$("#run").addEventListener("click",run); load().catch(e=>$("#result").textContent=e.message);
