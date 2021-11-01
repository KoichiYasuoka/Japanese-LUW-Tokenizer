#! /usr/bin/python3 -i
aug=lambda x:x.replace("侠","俠").replace("倶","俱").replace("洗","冼").replace("剥","剝").replace("即","卽").replace("呑","吞").replace("呉","吳").replace("填","塡").replace("巣","巢").replace("徴","徵").replace("徳","德").replace("掲","揭").replace("撃","擊").replace("教","敎").replace("晩","晚").replace("横","橫").replace("歩","步").replace("歴","歷").replace("毎","每").replace("冷","泠").replace("渉","涉").replace("涙","淚").replace("清","淸").replace("渇","渴").replace("温","溫").replace("状","狀").replace("産","產").replace("痩","瘦").replace("禰","祢").replace("箪","簞").replace("緑","綠").replace("緒","緖").replace("縁","緣").replace("繋","繫").replace("莱","萊").replace("薫","薰").replace("虚","虛").replace("蝉","蟬").replace("説","說").replace("躯","軀").replace("郎","郞").replace("醤","醬").replace("録","錄").replace("錬","鍊").replace("間","閒").replace("頬","頰").replace("顛","顚").replace("鴎","鷗").replace("麺","麵").replace("黄","黃").replace("黒","黑").replace("叱","𠮟")

with open("aug.txt","w",encoding="utf-8") as w:
  for d in ["udja.txt","aozora.txt"]:
    with open(d,"r",encoding="utf-8") as f:
      for r in f:
        s=r.strip()
        if s!="":
          t=aug(s)
          if t!=s:
            print(t,file=w)

with open("aug.luw.txt","w",encoding="utf-8") as w:
  for d in ["udja.luw.txt","aozora.luw.txt"]:
    with open(d,"r",encoding="utf-8") as f:
      for r in f:
        s=r.strip()
        if s!="":
          t=aug(s)
          if t!=s:
            print(t,file=w)

