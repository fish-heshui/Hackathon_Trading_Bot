import{_ as Q}from"./DraggableContainer.vue_vue_type_script_setup_true_lang-BeWeePSk.js";import{_ as j}from"./ExchangeSelect.vue_vue_type_script_setup_true_lang-BhtgCjO-.js";import{Z as ee,aa as ne,af as te,c as l,a as s,k as y,N as D,a1 as se,x as g,z as w,H as ae,e as n,d as J,cc as re,l as b,F as E,m as U,b as i,f as a,g as H,h as c,B as oe,j as ie,r as v,u as le,R as de,S as ue,i as C,v as me,W as ce,a2 as pe,Y as N,V as A,c6 as ge,X as O,t as fe}from"./index-D1nGKoiE.js";import{u as _e,_ as ve,a as be}from"./pairlistConfig-Dfuwnjnw.js";import{s as xe}from"./index-CEpCyxkv.js";import{_ as he}from"./TimeRangeSelect.vue_vue_type_script_setup_true_lang-DkXyeAfZ.js";import{_ as ke}from"./check-DEKslqbd.js";import"./plus-box-outline-DggSO52U.js";var ye=`
    .p-progressbar {
        display: block;
        position: relative;
        overflow: hidden;
        height: dt('progressbar.height');
        background: dt('progressbar.background');
        border-radius: dt('progressbar.border.radius');
    }

    .p-progressbar-value {
        margin: 0;
        background: dt('progressbar.value.background');
    }

    .p-progressbar-label {
        color: dt('progressbar.label.color');
        font-size: dt('progressbar.label.font.size');
        font-weight: dt('progressbar.label.font.weight');
    }

    .p-progressbar-determinate .p-progressbar-value {
        height: 100%;
        width: 0%;
        position: absolute;
        display: none;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        transition: width 1s ease-in-out;
    }

    .p-progressbar-determinate .p-progressbar-label {
        display: inline-flex;
    }

    .p-progressbar-indeterminate .p-progressbar-value::before {
        content: '';
        position: absolute;
        background: inherit;
        inset-block-start: 0;
        inset-inline-start: 0;
        inset-block-end: 0;
        will-change: inset-inline-start, inset-inline-end;
        animation: p-progressbar-indeterminate-anim 2.1s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite;
    }

    .p-progressbar-indeterminate .p-progressbar-value::after {
        content: '';
        position: absolute;
        background: inherit;
        inset-block-start: 0;
        inset-inline-start: 0;
        inset-block-end: 0;
        will-change: inset-inline-start, inset-inline-end;
        animation: p-progressbar-indeterminate-anim-short 2.1s cubic-bezier(0.165, 0.84, 0.44, 1) infinite;
        animation-delay: 1.15s;
    }

    @keyframes p-progressbar-indeterminate-anim {
        0% {
            inset-inline-start: -35%;
            inset-inline-end: 100%;
        }
        60% {
            inset-inline-start: 100%;
            inset-inline-end: -90%;
        }
        100% {
            inset-inline-start: 100%;
            inset-inline-end: -90%;
        }
    }
    @-webkit-keyframes p-progressbar-indeterminate-anim {
        0% {
            inset-inline-start: -35%;
            inset-inline-end: 100%;
        }
        60% {
            inset-inline-start: 100%;
            inset-inline-end: -90%;
        }
        100% {
            inset-inline-start: 100%;
            inset-inline-end: -90%;
        }
    }

    @keyframes p-progressbar-indeterminate-anim-short {
        0% {
            inset-inline-start: -200%;
            inset-inline-end: 100%;
        }
        60% {
            inset-inline-start: 107%;
            inset-inline-end: -8%;
        }
        100% {
            inset-inline-start: 107%;
            inset-inline-end: -8%;
        }
    }
    @-webkit-keyframes p-progressbar-indeterminate-anim-short {
        0% {
            inset-inline-start: -200%;
            inset-inline-end: 100%;
        }
        60% {
            inset-inline-start: 107%;
            inset-inline-end: -8%;
        }
        100% {
            inset-inline-start: 107%;
            inset-inline-end: -8%;
        }
    }
`,we={root:function(u){var f=u.instance;return["p-progressbar p-component",{"p-progressbar-determinate":f.determinate,"p-progressbar-indeterminate":f.indeterminate}]},value:"p-progressbar-value",label:"p-progressbar-label"},Se=ee.extend({name:"progressbar",style:ye,classes:we}),Ve={name:"BaseProgressBar",extends:ne,props:{value:{type:Number,default:null},mode:{type:String,default:"determinate"},showValue:{type:Boolean,default:!0}},style:Se,provide:function(){return{$pcProgressBar:this,$parentInstance:this}}},R={name:"ProgressBar",extends:Ve,inheritAttrs:!1,computed:{progressStyle:function(){return{width:this.value+"%",display:"flex"}},indeterminate:function(){return this.mode==="indeterminate"},determinate:function(){return this.mode==="determinate"},dataP:function(){return te({determinate:this.determinate,indeterminate:this.indeterminate})}}},$e=["aria-valuenow","data-p"],Te=["data-p"],De=["data-p"],Ce=["data-p"];function Pe(t,u,f,_,x,o){return s(),l("div",D({role:"progressbar",class:t.cx("root"),"aria-valuemin":"0","aria-valuenow":t.value,"aria-valuemax":"100","data-p":o.dataP},t.ptmi("root")),[o.determinate?(s(),l("div",D({key:0,class:t.cx("value"),style:o.progressStyle,"data-p":o.dataP},t.ptm("value")),[t.value!=null&&t.value!==0&&t.showValue?(s(),l("div",D({key:0,class:t.cx("label"),"data-p":o.dataP},t.ptm("label")),[se(t.$slots,"default",{},function(){return[g(w(t.value+"%"),1)]})],16,De)):y("",!0)],16,Te)):o.indeterminate?(s(),l("div",D({key:1,class:t.cx("value"),"data-p":o.dataP},t.ptm("value")),null,16,Ce)):y("",!0)],16,$e)}R.render=Pe;const Be={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"};function Ee(t,u){return s(),l("svg",Be,[...u[0]||(u[0]=[n("path",{fill:"currentColor",d:"M8 17v-2h8v2zm8-7l-4 4l-4-4h2.5V7h3v3zM5 3h14a2 2 0 0 1 2 2v14c0 1.11-.89 2-2 2H5a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2m0 2v14h14V5z"},null,-1)])])}const Ue=ae({name:"mdi-download-box-outline",render:Ee}),ze={class:"flex flex-row items-end gap-1"},Me={class:"ms-2 w-full grow space-y-1"},Ne=["title"],Ae={key:1},Oe={class:"flex justify-between"},Je={key:1},He={key:2,class:"w-25"},Re={key:3,class:"flex flex-col md:flex-row w-full grow gap-2"},Fe=J({__name:"BackgroundJobTracking",setup(t){const{runningJobs:u,clearJobs:f}=re();return(_,x)=>{const o=Ue,P=ke,p=R,h=oe,k=H;return s(),l("div",ze,[n("ul",Me,[(s(!0),l(E,null,U(a(u),(d,V)=>(s(),l("li",{key:V,class:"border p-1 pb-2 rounded-sm dark:border-surface-700 border-surface-300 flex gap-2 items-center",title:V},[d.taskStatus?.job_category==="download_data"?(s(),b(o,{key:0})):(s(),l("span",Ae,w(d.taskStatus?.job_category),1)),n("div",Oe,[d.taskStatus?.status==="success"?(s(),b(P,{key:0,class:"text-success",title:""})):(s(),l("span",Je,w(d.taskStatus?.status),1)),d.taskStatus?.progress?(s(),l("span",He,w(d.taskStatus?.progress),1)):y("",!0)]),d.taskStatus?.progress?(s(),b(p,{key:2,class:"w-full grow",value:d.taskStatus?.progress/100*100,"show-progress":"",max:100,striped:""},null,8,["value"])):y("",!0),d.taskStatus?.progress_tasks?(s(),l("div",Re,[(s(!0),l(E,null,U(Object.entries(d.taskStatus?.progress_tasks),([B,S])=>(s(),l("div",{key:B,class:"w-full"},[g(w(S.description)+" ",1),i(p,{class:"w-full grow",value:Math.round(S.progress/S.total*100*100)/100,"show-progress":"",pt:{value:{class:d.taskStatus.status==="success"?"bg-emerald-500":"bg-amber-500"}},striped:""},null,8,["value","pt"])]))),128))])):y("",!0)],8,Ne))),128))]),Object.keys(a(u)).length>0?(s(),b(k,{key:0,severity:"secondary",class:"ms-auto",onClick:a(f)},{icon:c(()=>[i(h)]),_:1},8,["onClick"])):y("",!0)])}}}),Le=v([{description:"All USDT Pairs",pairs:[".*/USDT"]},{description:"All USDT Futures Pairs",pairs:[".*/USDT:USDT"]}]);function Ie(){return{pairTemplates:ie(()=>Le.value.map((t,u)=>({...t,idx:u})))}}const qe={class:"px-1 mx-auto w-full max-w-4xl lg:max-w-7xl"},We={class:"flex mb-3 gap-3 flex-col"},Xe={class:"flex flex-col gap-3"},Ye={class:"flex flex-col lg:flex-row gap-3"},Ze={class:"flex-fill"},Ge={class:"flex flex-col gap-2"},Ke={class:"flex gap-2"},Qe={class:"flex flex-col gap-1"},je={class:"flex flex-col gap-1"},en={class:"flex-fill px-3"},nn={class:"flex flex-col gap-2"},tn={class:"px-3 border dark:border-surface-700 border-surface-300 p-2 rounded-sm"},sn={class:"flex flex-col gap-2"},an={class:"flex justify-between items-center"},rn={key:0},on={key:1,class:"flex items-center gap-2"},ln={class:"mb-2 border dark:border-surface-700 border-surface-300 rounded-sm p-2 text-start"},dn={class:"mb-2 border dark:border-surface-700 border-surface-300 rounded-md p-2 text-start"},un={class:"mb-2 border dark:border-surface-700 border-surface-300 rounded-md p-2 text-start"},mn={class:"px-3"},cn=J({__name:"DownloadDataMain",setup(t){const u=le(),f=_e(),_=v(["BTC/USDT","ETH/USDT",""]),x=v(["5m","1h"]),o=v({useCustomTimerange:!1,timerange:"",days:30}),{pairTemplates:P}=Ie(),p=v({customExchange:!1,selectedExchange:{exchange:"binance",trade_mode:{margin_mode:ue.NONE,trading_mode:de.SPOT}}}),h=v(!1),k=v(!1),d=v(!1);function V(m){_.value.push(...m)}function B(m){_.value=[...m]}async function S(){const m={pairs:_.value.filter(e=>e!==""),timeframes:x.value.filter(e=>e!=="")};o.value.useCustomTimerange&&o.value.timerange?m.timerange=o.value.timerange:m.days=o.value.days,d.value&&(m.erase=h.value,m.download_trades=k.value,p.value.customExchange&&(m.exchange=p.value.selectedExchange.exchange,m.trading_mode=p.value.selectedExchange.trade_mode.trading_mode,m.margin_mode=p.value.selectedExchange.trade_mode.margin_mode)),await u.activeBot.startDataDownload(m)}return(m,e)=>{const F=Fe,z=ve,$=H,L=me,T=ce,I=he,q=xe,W=pe,X=be,Y=ge,Z=j,G=Q;return s(),l("div",qe,[i(F,{class:"mb-4"}),i(G,{header:"Downloading Data",class:"mx-1 p-4"},{default:c(()=>[n("div",We,[n("div",Xe,[n("div",Ye,[n("div",Ze,[n("div",Ge,[e[12]||(e[12]=n("div",{class:"flex justify-between"},[n("h4",{class:"text-start font-bold text-lg"},"Select Pairs"),n("h5",{class:"text-start font-bold text-lg"},"Pairs from template")],-1)),n("div",Ke,[i(z,{modelValue:a(_),"onUpdate:modelValue":e[0]||(e[0]=r=>C(_)?_.value=r:null),placeholder:"Pair",size:"small",class:"flex-grow-1"},null,8,["modelValue"]),n("div",Qe,[n("div",je,[(s(!0),l(E,null,U(a(P),r=>(s(),b($,{key:r.idx,severity:"secondary",title:r.pairs.reduce((M,K)=>`${M}${K}
`,""),onClick:M=>V(r.pairs)},{default:c(()=>[g(w(r.description),1)]),_:2},1032,["title","onClick"]))),128))]),i(L),i($,{disabled:a(f).whitelist.length===0,title:"Add all pairs from Pairlist Config - requires the pairlist config to have ran first.",severity:"secondary",onClick:e[1]||(e[1]=r=>B(a(f).whitelist))},{default:c(()=>[...e[11]||(e[11]=[g(" Use Pairs from Pairlist Config ",-1)])]),_:1},8,["disabled"])])])])]),n("div",en,[n("div",nn,[e[13]||(e[13]=n("h4",{class:"text-start font-bold text-lg"},"Select timeframes",-1)),i(z,{modelValue:a(x),"onUpdate:modelValue":e[2]||(e[2]=r=>C(x)?x.value=r:null),placeholder:"Timeframe"},null,8,["modelValue"])])])]),n("div",tn,[n("div",sn,[n("div",an,[e[15]||(e[15]=n("h4",{class:"text-start mb-0 font-bold text-lg"},"Time Selection",-1)),i(T,{modelValue:a(o).useCustomTimerange,"onUpdate:modelValue":e[3]||(e[3]=r=>a(o).useCustomTimerange=r),class:"mb-0",switch:""},{default:c(()=>[...e[14]||(e[14]=[g(" Use custom timerange ",-1)])]),_:1},8,["modelValue"])]),a(o).useCustomTimerange?(s(),l("div",rn,[i(I,{modelValue:a(o).timerange,"onUpdate:modelValue":e[4]||(e[4]=r=>a(o).timerange=r)},null,8,["modelValue"])])):(s(),l("div",on,[e[16]||(e[16]=n("label",null,"Days to download:",-1)),i(q,{modelValue:a(o).days,"onUpdate:modelValue":e[5]||(e[5]=r=>a(o).days=r),type:"number","aria-label":"Days to download",min:1,step:1,size:"small"},null,8,["modelValue"])]))])]),n("div",ln,[i($,{class:"mb-2",severity:"secondary",onClick:e[6]||(e[6]=r=>d.value=!a(d))},{default:c(()=>[e[17]||(e[17]=g(" Advanced Options ",-1)),a(d)?(s(),b(X,{key:1})):(s(),b(W,{key:0}))]),_:1}),i(N,null,{default:c(()=>[A(n("div",null,[i(Y,{severity:"info",class:"mb-2 py-2"},{default:c(()=>[...e[18]||(e[18]=[g(" Advanced options (Erase data, Download trades, and Custom Exchange settings) will only be applied when this section is expanded. ",-1)])]),_:1}),n("div",dn,[i(T,{modelValue:a(h),"onUpdate:modelValue":e[7]||(e[7]=r=>C(h)?h.value=r:null),class:"mb-2"},{default:c(()=>[...e[19]||(e[19]=[g("Erase existing data",-1)])]),_:1},8,["modelValue"]),i(T,{modelValue:a(k),"onUpdate:modelValue":e[8]||(e[8]=r=>C(k)?k.value=r:null),class:"mb-2"},{default:c(()=>[...e[20]||(e[20]=[g(" Download Trades instead of OHLCV data ",-1)])]),_:1},8,["modelValue"])]),n("div",un,[i(T,{modelValue:a(p).customExchange,"onUpdate:modelValue":e[9]||(e[9]=r=>a(p).customExchange=r),class:"mb-2"},{default:c(()=>[...e[21]||(e[21]=[g(" Custom Exchange ",-1)])]),_:1},8,["modelValue"]),i(N,{name:"fade"},{default:c(()=>[A(i(Z,{modelValue:a(p).selectedExchange,"onUpdate:modelValue":e[10]||(e[10]=r=>a(p).selectedExchange=r)},null,8,["modelValue"]),[[O,a(p).customExchange]])]),_:1})])],512),[[O,a(d)]])]),_:1})]),n("div",mn,[i($,{severity:"primary",onClick:S},{default:c(()=>[...e[22]||(e[22]=[g("Start Download",-1)])]),_:1})])])])]),_:1})])}}}),pn={};function gn(t,u){const f=cn;return s(),b(f,{class:"pt-4"})}const wn=fe(pn,[["render",gn]]);export{wn as default};
//# sourceMappingURL=DownloadDataView-QcKYwWXp.js.map
