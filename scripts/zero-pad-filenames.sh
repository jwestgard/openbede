while read f
    do 
        pre=${f%-*}
        ext=${f#*.}
        ser=${f#$pre-}
        ser=${ser%.$ext}
        pad=000$ser
        pad=${pad:(-3)}
        mv "$f" "$pre-$pad.$ext"
    done
