#! /bin/sh

test -d UD_Japanese-GSDLUW || git clone -b dev --depth=1 https://github.com/UniversalDependencies/UD_Japanese-GSDLUW
test -d UD_Japanese-PUDLUW || git clone -b dev --depth=1 https://github.com/UniversalDependencies/UD_Japanese-PUDLUW
test -d UD_Japanese-Modern || git clone --depth=1 https://github.com/UniversalDependencies/UD_Japanese-Modern

nawk '
BEGIN{
  rehead[0]=newhead[0]=0;
}
{
  if($1=="#")
    printf("%s\n",$0);
  else if(NF==10){
    if($1==1){
      n=id=1; 
      form[n]=$2;
      lemma[n]=$3;
      upos[n]=$4;
      match($10,/LUWPOS=[^|]+/)
      xpos[n]=substr($10,RSTART+7,RLENGTH-7);
      if(xpos[n]=="")
        xpos[n]=$5;
      head[id]=$7;
      deprel[id]=$8;
      rehead[id]=n;
    }
    else if($10~/LUWBILabel=I/){
      id=$1-0;
      form[n]=form[n] $2;
      lemma[n]=lemma[n] $3;
      upos[n]=upos[n]"+"$4;
      head[id]=$7;
      deprel[id]=$8;
      rehead[id]=n;
    }
    else{
      n++;
      id=$1-0;
      form[n]=$2;
      lemma[n]=$3;
      upos[n]=$4;
      match($10,/LUWPOS=[^|]+/)
      xpos[n]=substr($10,RSTART+7,RLENGTH-7);
      if(xpos[n]=="")
        xpos[n]=$5;
      head[id]=$7;
      deprel[id]=$8;
      rehead[id]=n;
    }
  }
  else if($0==""){
    for(i=id;i>0;i--){
      if(rehead[head[i]]!=rehead[i])
        newhead[rehead[i]]=i;
    }
    for(i=1;i<=n;i++)
      printf("%d\t%s\t%s\t%s\t%s\t_\t%d\t%s\t_\tSpaceAfter=No\n",i,form[i],lemma[i],upos[i],xpos[i],rehead[head[newhead[i]]],deprel[newhead[i]]);
    printf("\n");
  }
}' UD_Japanese-Modern/*.conllu |
( nawk '
{
  if($1=="#"||NF!=10)
    printf("%s\n",$0);
  else{
    if($4~/\+/){
      upos=$4;
      if(upos~/SCONJ/)
        upos="SCONJ";
      else if(upos~/CCONJ/)
        upos="CCONJ";
      else if(upos~/VERB(\+AUX)*$/)
        upos="VERB";
      else if(upos~/ADJ$/)
        upos="ADJ";
      else if(upos~/ADP/)
        upos="ADP";
      else if(upos~/PROPN/)
        upos="PROPN";
      else if(upos~/PRON/)
        upos="PRON";
      else if(upos~/NUM$/)
        upos="NUM";
      else if(upos=="NOUN+AUX")
        upos="ADV";
      else
        upos="NOUN";
      printf("%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s\n",$1,$2,$3,upos,$5,$6,$7,$8,$9,$10);
    }
    else
      printf("%s\n",$0);
  }
}'
cat UD_Japanese-GSDLUW/*-train.conllu UD_Japanese-PUDLUW/*.conllu
) > train.conllu

exit 0
