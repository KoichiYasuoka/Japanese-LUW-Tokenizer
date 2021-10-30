#! /bin/sh
test -d aozorabunko || git clone --depth=1 https://github.com/aozorabunko/aozorabunko
( cd aozorabunko && find gaiji -name '*.png' ) | sort |
LANG=C awk '
BEGIN{
  printf("/<!DOCTYPE[^<]*$/d\n");
  printf("/^[^>]*dtd.>/d\n");
  printf("/<div[^>]*bibliographical_information.>/,$d\n");
}
{
  h=substr($1,length($1)-8,2)
  l=substr($1,length($1)-5,2)
  if($1~/1-[0-9][0-9]\/1-[0-9][0-9]-[0-9][0-9]\.png$/)
    printf("s?<img [^>]*%s[^>]*>?%c%c?g\n",$1,h+160,l+160);
  else if($1~/2-[0-9][0-9]\/2-[0-9][0-9]-[0-9][0-9]\.png$/){
    if(h!=94||l-87<0)
      printf("s?<img [^>]*%s[^>]*>?%c%c%c?g\n",$1,143,h+160,l+160);
  }
}
END{
  printf("s?<img [^>]*>?[UNK]?g\n");
  printf("s?<r[tp]>[^<]*</r[tp]>??g\n");
  printf("s/<[^>]*>//g\n");
  printf("s/%c%c[%c%c%c%c%c%c%c%c]*/&%c/g\n",161,163,161,203,161,205,161,215,161,217,13);
}' | iconv -f EUC-JISX0213 -t UTF-8 > aozora.sed

egrep -l 'encoding="Shift_JIS"|charset=Shift_JIS' aozorabunko/cards/*/files/*_*.html |
( while read F
  do tr '\015' '\012' < $F | iconv -f CP932 -t UTF-8 | sed -f aozora.sed
  done
) | tr '\015' '\012' | egrep -v '^[[:blank:]]*$' > aozora.txt
exit 0
