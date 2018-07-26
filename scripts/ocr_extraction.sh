home=$(pwd)
echo $home
for folder in $@
    do
        vol=${folder%-*}
        echo $vol
        cd $home/$folder
        for f in $(ls)
            do
                tesseract "$f" "../../../ts_output/$vol/$f" -l lat+eng
            done
    done



