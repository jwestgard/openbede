while read f
    do 
        if [[ $f == $1* ]]
        then
            keep=${f#$1}
            new=$2$keep
            echo "mv" "$f" "$new"
        fi
    done
