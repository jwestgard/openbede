s=1
while read f
    do 
        pre=${f%%.*}
        ext=${f#*.}
        pad=000$s
        pad=${pad:(-3)}
        mv "$f" "$pre-s$pad.$ext"
        ((s++))
    done
